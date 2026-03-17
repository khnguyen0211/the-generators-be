"""Health check routes."""

from flask import current_app
from flask_restx import Resource
from server.swagger import ns_health
from server.models import api_response, health_data
from helpers.response_helper import ResponseHelper


@ns_health.route("")
class HealthResource(Resource):
    """Health check resource."""

    @ns_health.doc("health_check")
    @ns_health.response(200, "Service is healthy", api_response)
    @ns_health.response(503, "Service is degraded")
    def get(self):
        """Check health status of all services."""
        from services.redis_queue_service import RedisQueueService
        
        config = current_app.config["config_service"]
        queue_service = current_app.config["queue_service"]
        worker_service = current_app.config["worker_service"]
        
        health_data = {
            "status": "healthy",
            "environment": config.environment,
            "services": {
                "api": "up",
                "queue": "unknown",
                "worker": "unknown",
            }
        }
        
        # Check queue type
        if isinstance(queue_service, RedisQueueService):
            try:
                queue_service._redis.ping()
                health_data["services"]["queue"] = "up (redis)"
            except Exception:
                health_data["services"]["queue"] = "down (redis)"
                health_data["status"] = "degraded"
        else:
            health_data["services"]["queue"] = "up (memory)"
        
        # Check worker
        if worker_service._running:
            health_data["services"]["worker"] = "up"
        else:
            health_data["services"]["worker"] = "down"
            health_data["status"] = "degraded"
        
        status_code = 200 if health_data["status"] == "healthy" else 503
        return ResponseHelper.success(data=health_data, status_code=status_code)
