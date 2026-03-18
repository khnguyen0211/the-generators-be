"""Image to Video API routes."""

from flask import request, current_app
from flask_restx import Resource
from server.swagger import ns_image_to_video
from server.models import api_response, image_to_video_generate_request, generate_response_data, models_response_data
from helpers.response_helper import ResponseHelper
from .validator import ImageToVideoValidator
from .service import ImageToVideoService

JOB_TYPE = "image_to_video"


def _get_handler(config):
    """Create handler function for queue worker."""
    service = ImageToVideoService(config)
    return service.generate


@ns_image_to_video.route("/generate")
class GenerateResource(Resource):
    """Image to video generation resource."""

    @ns_image_to_video.doc("generate_image_to_video")
    @ns_image_to_video.expect(image_to_video_generate_request)
    @ns_image_to_video.response(202, "Job submitted", api_response)
    @ns_image_to_video.response(400, "Validation error")
    def post(self):
        """Submit image-to-video generation job."""
        data = request.get_json() or {}

        is_valid, errors = ImageToVideoValidator.validate_generate_request(data)
        if not is_valid:
            return ResponseHelper.error(message="Validation failed", errors=errors)

        config = current_app.config["config_service"]
        queue_service = current_app.config["queue_service"]

        if queue_service.get_handler(JOB_TYPE) is None:
            queue_service.register_handler(JOB_TYPE, _get_handler(config))

        if "provider" not in data:
            data["provider"] = config.image_to_video_default

        job = queue_service.enqueue(JOB_TYPE, data)

        return ResponseHelper.success(
            data={"job_id": job.id, "status": job.status.value},
            message="Job submitted",
            status_code=202,
        )


@ns_image_to_video.route("/models")
class ModelsResource(Resource):
    """Available models resource."""

    @ns_image_to_video.doc("list_image_to_video_models")
    @ns_image_to_video.response(200, "Success", api_response)
    def get(self):
        """List available image-to-video providers."""
        config = current_app.config["config_service"]
        service = ImageToVideoService(config)
        models = service.get_available_models()
        return ResponseHelper.success(data=models)
