"""In-Memory Queue Service implementation."""

import logging
import threading
from datetime import datetime
from typing import Any, Callable, Dict, Optional

from .base_queue_service import BaseQueueService, Job, JobStatus

logger = logging.getLogger("the_generators")


class MemoryQueueService(BaseQueueService):
    """In-memory queue service. Thread-safe. Data lost on restart."""

    def __init__(self):
        self._jobs: Dict[str, Job] = {}
        self._queue: list = []
        self._handlers: Dict[str, Callable] = {}
        self._lock = threading.Lock()
        self._event = threading.Event()

    def enqueue(self, job_type: str, payload: Dict[str, Any]) -> Job:
        """Add job to queue."""
        job = Job(
            id=self.generate_job_id(),
            job_type=job_type,
            payload=payload,
        )
        with self._lock:
            self._jobs[job.id] = job
            self._queue.append(job.id)
        self._event.set()  # Wake up worker
        logger.info(f"[QUEUE] Job created: {job.id} | type={job_type} | queue_size={len(self._queue)}")
        return job

    def get_job(self, job_id: str) -> Optional[Job]:
        """Get job by ID."""
        return self._jobs.get(job_id)

    def get_next_pending(self) -> Optional[Job]:
        """Get next pending job. Blocks until job available."""
        while True:
            with self._lock:
                while self._queue:
                    job_id = self._queue.pop(0)
                    job = self._jobs.get(job_id)
                    if job and job.status == JobStatus.PENDING:
                        return job
            
            self._event.clear()
            self._event.wait(timeout=1.0)  # Wait for signal or timeout

    def update_status(self, job_id: str, status: JobStatus,
                      result: dict = None, error: str = None) -> None:
        """Update job status."""
        job = self._jobs.get(job_id)
        if job:
            old_status = job.status.value
            job.status = status
            job.updated_at = datetime.now()
            if result:
                job.result = result
            if error:
                job.error = error
            logger.info(f"[QUEUE] Job status updated: {job_id} | {old_status} -> {status.value}")

    def register_handler(self, job_type: str, handler: Callable) -> None:
        """Register handler for job type."""
        self._handlers[job_type] = handler

    def get_handler(self, job_type: str) -> Optional[Callable]:
        """Get handler for job type."""
        return self._handlers.get(job_type)
