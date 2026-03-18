"""Text to Speech API routes."""

from flask import request, current_app
from flask_restx import Resource
from server.swagger import ns_text_to_speech
from server.models import api_response, tts_generate_request, generate_response_data, models_response_data
from helpers.response_helper import ResponseHelper
from .validator import TextToSpeechValidator
from .service import TextToSpeechService

JOB_TYPE = "text_to_speech"


def _get_handler(config):
    """Create handler function for queue worker."""
    service = TextToSpeechService(config)
    return service.generate


@ns_text_to_speech.route("/generate")
class GenerateResource(Resource):
    """Text to speech generation resource."""

    @ns_text_to_speech.doc("generate_speech")
    @ns_text_to_speech.expect(tts_generate_request)
    @ns_text_to_speech.response(202, "Job submitted", api_response)
    @ns_text_to_speech.response(400, "Validation error")
    def post(self):
        """Submit text-to-speech generation job."""
        data = request.get_json() or {}

        is_valid, errors = TextToSpeechValidator.validate_generate_request(data)
        if not is_valid:
            return ResponseHelper.error(message="Validation failed", errors=errors)

        config = current_app.config["config_service"]
        queue_service = current_app.config["queue_service"]

        if queue_service.get_handler(JOB_TYPE) is None:
            queue_service.register_handler(JOB_TYPE, _get_handler(config))

        if "provider" not in data:
            data["provider"] = config.text_to_speech_default

        job = queue_service.enqueue(JOB_TYPE, data)

        return ResponseHelper.success(
            data={"job_id": job.id, "status": job.status.value},
            message="Job submitted",
            status_code=202,
        )


@ns_text_to_speech.route("/models")
class ModelsResource(Resource):
    """Available models resource."""

    @ns_text_to_speech.doc("list_speech_models")
    @ns_text_to_speech.response(200, "Success", api_response)
    def get(self):
        """List available text-to-speech providers."""
        config = current_app.config["config_service"]
        service = TextToSpeechService(config)
        models = service.get_available_models()
        return ResponseHelper.success(data=models)
