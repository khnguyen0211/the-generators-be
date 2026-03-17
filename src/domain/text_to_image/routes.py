"""Text to Image API routes."""

from flask import request, current_app
from flask_restx import Resource
from server.swagger import ns_text_to_image
from server.models import api_response, generate_request, generate_response_data, models_response_data
from helpers.response_helper import ResponseHelper
from .validator import TextToImageValidator
from .service import TextToImageService

JOB_TYPE = "text_to_image"


def _get_handler(config):
    """Create handler function for queue worker."""
    service = TextToImageService(config)
    return service.generate


@ns_text_to_image.route("/generate")
class GenerateResource(Resource):
    """Text to image generation resource."""

    @ns_text_to_image.doc("generate_image")
    @ns_text_to_image.expect(generate_request)
    @ns_text_to_image.response(202, "Job submitted", api_response)
    @ns_text_to_image.response(400, "Validation error")
    def post(self):
        """Submit text-to-image generation job."""
        data = request.get_json() or {}

        is_valid, errors = TextToImageValidator.validate_generate_request(data)
        if not is_valid:
            return ResponseHelper.error(message="Validation failed", errors=errors)

        config = current_app.config["config_service"]
        queue_service = current_app.config["queue_service"]

        # Register handler if not already registered
        if queue_service.get_handler(JOB_TYPE) is None:
            queue_service.register_handler(JOB_TYPE, _get_handler(config))

        # Set default provider if not specified
        if "provider" not in data:
            data["provider"] = config.text_to_image_default

        job = queue_service.enqueue(JOB_TYPE, data)

        return ResponseHelper.success(
            data={"job_id": job.id, "status": job.status.value},
            message="Job submitted",
            status_code=202,
        )


@ns_text_to_image.route("/models")
class ModelsResource(Resource):
    """Available models resource."""

    @ns_text_to_image.doc("get_models")
    @ns_text_to_image.response(200, "Success", api_response)
    def get(self):
        """Get available text-to-image models."""
        config = current_app.config["config_service"]
        service = TextToImageService(config)
        return ResponseHelper.success(data=service.get_available_models())
