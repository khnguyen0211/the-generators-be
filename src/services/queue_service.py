"""QueueService - Generic in-memory job queue."""

import uuid
import threading
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, Optional
from dataclasses import dataclass, field


class JobStatus(Enum):
    """Job status enum."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Job:
    """Job data model."""
    id: str
    job_type: str
    payload: Dict[str, Any]
    status: JobStatus = JobStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "job_id": self.id,
            "job_type": self.job_type,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class QueueService:
    """In-memory queue service. Thread-safe."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._jobs: Dict[str, Job] = {}
                    cls._instance._queue: list = []
                    cls._instance._handlers: Dict[str, Callable] = {}
                    cls._instance._queue_lock = threading.Lock()
        return cls._instance

    def register_handler(self, job_type: str, handler: Callable) -> None:
        """Register a handler function for a job type."""
        self._handlers[job_type] = handler

    def enqueue(self, job_type: str, payload: Dict[str, Any]) -> Job:
        """Add job to queue. Returns job with ID."""
        job = Job(
            id=str(uuid.uuid4()),
            job_type=job_type,
            payload=payload,
        )
        with self._queue_lock:
            self._jobs[job.id] = job
            self._queue.append(job.id)
        return job

    def get_job(self, job_id: str) -> Optional[Job]:
        """Get job by ID."""
        return self._jobs.get(job_id)

    def get_next_pending(self) -> Optional[Job]:
        """Get next pending job from queue."""
        with self._queue_lock:
            while self._queue:
                job_id = self._queue.pop(0)
                job = self._jobs.get(job_id)
                if job and job.status == JobStatus.PENDING:
                    return job
        return None

    def update_status(self, job_id: str, status: JobStatus, 
                      result: dict = None, error: str = None) -> None:
        """Update job status."""
        job = self._jobs.get(job_id)
        if job:
            job.status = status
            job.updated_at = datetime.now()
            if result:
                job.result = result
            if error:
                job.error = error

    def get_handler(self, job_type: str) -> Optional[Callable]:
        """Get handler for job type."""
        return self._handlers.get(job_type)
