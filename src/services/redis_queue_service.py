"""Redis Queue Service implementation."""

import json
import logging
from datetime import datetime
from typing import Any, Callable, Dict, Optional

import redis

from .base_queue_service import BaseQueueService, Job, JobStatus

logger = logging.getLogger("the_generators")


class RedisQueueService(BaseQueueService):
    """Redis-backed queue service. Persistent. Supports multiple workers."""

    QUEUE_KEY = "jobs:queue"
    JOB_PREFIX = "jobs:data:"

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        self._redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self._handlers: Dict[str, Callable] = {}

    def enqueue(self, job_type: str, payload: Dict[str, Any]) -> Job:
        """Add job to queue."""
        job = Job(
            id=self.generate_job_id(),
            job_type=job_type,
            payload=payload,
        )
        
        # Save job data
        self._save_job(job)
        logger.debug(f"[REDIS] SET {self.JOB_PREFIX}{job.id} (expires in 24h)")
        
        # Push to queue
        self._redis.rpush(self.QUEUE_KEY, job.id)
        logger.debug(f"[REDIS] RPUSH {self.QUEUE_KEY} {job.id}")
        
        queue_size = self._redis.llen(self.QUEUE_KEY)
        logger.info(f"[QUEUE] Job created: {job.id} | type={job_type} | queue_size={queue_size}")
        
        return job

    def get_job(self, job_id: str) -> Optional[Job]:
        """Get job by ID."""
        key = f"{self.JOB_PREFIX}{job_id}"
        data = self._redis.get(key)
        logger.debug(f"[REDIS] GET {key} | found={data is not None}")
        if data:
            return self._deserialize_job(data)
        return None

    def get_next_pending(self) -> Optional[Job]:
        """Get next pending job. Blocks until job available."""
        # BLPOP blocks until item available (timeout 1 second)
        result = self._redis.blpop(self.QUEUE_KEY, timeout=1)
        
        if result:
            _, job_id = result
            logger.debug(f"[REDIS] BLPOP returned job_id={job_id}")
            job = self.get_job(job_id)
            if job and job.status == JobStatus.PENDING:
                return job
        
        return None

    def update_status(self, job_id: str, status: JobStatus,
                      result: dict = None, error: str = None) -> None:
        """Update job status."""
        job = self.get_job(job_id)
        if job:
            old_status = job.status.value
            job.status = status
            job.updated_at = datetime.now()
            if result:
                job.result = result
            if error:
                job.error = error
            self._save_job(job)
            logger.info(f"[QUEUE] Job status updated: {job_id} | {old_status} -> {status.value}")

    def register_handler(self, job_type: str, handler: Callable) -> None:
        """Register handler for job type."""
        self._handlers[job_type] = handler

    def get_handler(self, job_type: str) -> Optional[Callable]:
        """Get handler for job type."""
        return self._handlers.get(job_type)

    def _save_job(self, job: Job) -> None:
        """Save job to Redis."""
        data = json.dumps({
            "id": job.id,
            "job_type": job.job_type,
            "payload": job.payload,
            "status": job.status.value,
            "result": job.result,
            "error": job.error,
            "created_at": job.created_at.isoformat(),
            "updated_at": job.updated_at.isoformat(),
        })
        # Expire after 24 hours
        self._redis.setex(f"{self.JOB_PREFIX}{job.id}", 86400, data)

    def _deserialize_job(self, data: str) -> Job:
        """Deserialize job from JSON."""
        d = json.loads(data)
        return Job(
            id=d["id"],
            job_type=d["job_type"],
            payload=d["payload"],
            status=JobStatus(d["status"]),
            result=d["result"],
            error=d["error"],
            created_at=datetime.fromisoformat(d["created_at"]),
            updated_at=datetime.fromisoformat(d["updated_at"]),
        )

    @staticmethod
    def check_connection(host: str, port: int, db: int = 0) -> bool:
        """Check if Redis is available."""
        try:
            r = redis.Redis(host=host, port=port, db=db)
            r.ping()
            return True
        except (redis.ConnectionError, redis.TimeoutError):
            return False
