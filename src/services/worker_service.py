"""WorkerService - Background worker for processing jobs."""

import threading
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.queue_service import QueueService
    from services.logger_service import LoggerService


class WorkerService:
    """Background worker that processes jobs from queue."""

    def __init__(self, queue_service: "QueueService", logger: "LoggerService"):
        self._queue = queue_service
        self._logger = logger
        self._running = False
        self._thread: threading.Thread = None

    def start(self) -> None:
        """Start worker in background thread."""
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._thread.start()
        self._logger.info("Worker service started")

    def stop(self) -> None:
        """Stop worker."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        self._logger.info("Worker service stopped")

    def _worker_loop(self) -> None:
        """Main worker loop."""
        from services.queue_service import JobStatus

        while self._running:
            try:
                job = self._queue.get_next_pending()
                if job is None:
                    time.sleep(0.5)
                    continue

                self._logger.info(f"Processing job {job.id} ({job.job_type})")
                self._queue.update_status(job.id, JobStatus.PROCESSING)

                handler = self._queue.get_handler(job.job_type)
                if handler is None:
                    self._queue.update_status(
                        job.id, JobStatus.FAILED, 
                        error=f"No handler for job type: {job.job_type}"
                    )
                    continue

                result = handler(job.payload)
                self._queue.update_status(job.id, JobStatus.COMPLETED, result=result)
                self._logger.info(f"Job {job.id} completed")

            except Exception as e:
                if job:
                    self._queue.update_status(job.id, JobStatus.FAILED, error=str(e))
                    self._logger.error(f"Job {job.id} failed: {str(e)}")
