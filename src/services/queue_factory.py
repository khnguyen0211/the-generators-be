"""Queue Factory - Creates appropriate queue service based on availability."""

from typing import TYPE_CHECKING

from .base_queue_service import BaseQueueService
from .memory_queue_service import MemoryQueueService
from .redis_queue_service import RedisQueueService

if TYPE_CHECKING:
    from .logger_service import LoggerService


class QueueFactory:
    """Factory to create queue service with fallback strategy."""

    @staticmethod
    def create(config, logger: "LoggerService" = None) -> BaseQueueService:
        """Create queue service. Uses Redis if available, else in-memory.
        
        Args:
            config: ConfigService instance
            logger: Optional logger for status messages
            
        Returns:
            BaseQueueService implementation
        """
        redis_host = config.get("REDIS_HOST", "localhost")
        redis_port = int(config.get("REDIS_PORT", "6379"))
        redis_db = int(config.get("REDIS_DB", "0"))

        # Try Redis first
        if RedisQueueService.check_connection(redis_host, redis_port, redis_db):
            if logger:
                logger.info(f"Using Redis queue at {redis_host}:{redis_port}")
            return RedisQueueService(host=redis_host, port=redis_port, db=redis_db)
        
        # Fallback to in-memory
        if logger:
            logger.warning("Redis unavailable, using in-memory queue (data will be lost on restart)")
        return MemoryQueueService()
