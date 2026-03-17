"""Base Queue Service - Abstract interface for queue implementations."""

import uuid
from abc import ABC, abstractmethod
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


class BaseQueueService(ABC):
    """Abstract base class for queue services."""

    @abstractmethod
    def enqueue(self, job_type: str, payload: Dict[str, Any]) -> Job:
        """Add job to queue."""
        pass

    @abstractmethod
    def get_job(self, job_id: str) -> Optional[Job]:
        """Get job by ID."""
        pass

    @abstractmethod
    def get_next_pending(self) -> Optional[Job]:
        """Get next pending job from queue."""
        pass

    @abstractmethod
    def update_status(self, job_id: str, status: JobStatus,
                      result: dict = None, error: str = None) -> None:
        """Update job status."""
        pass

    @abstractmethod
    def register_handler(self, job_type: str, handler: Callable) -> None:
        """Register a handler for job type."""
        pass

    @abstractmethod
    def get_handler(self, job_type: str) -> Optional[Callable]:
        """Get handler for job type."""
        pass

    @staticmethod
    def generate_job_id() -> str:
        """Generate unique job ID."""
        return str(uuid.uuid4())
