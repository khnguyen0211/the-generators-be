"""Flask app entry point."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flask import Flask, send_from_directory, redirect
from flask_cors import CORS

from services.config_service import ConfigService
from services.logger_service import LoggerService
from services.queue_factory import QueueFactory
from services.worker_service import WorkerService
from helpers.response_helper import ResponseHelper


def create_app() -> Flask:
    """Factory function to create Flask app."""
    app = Flask(__name__)

    # Initialize services
    config = ConfigService()
    config.load()

    logger = LoggerService(config)
    logger.setup()

    # Create queue service (Redis if available, else in-memory)
    queue_service = QueueFactory.create(config, logger)
    worker_service = WorkerService(queue_service, logger)

    CORS(app)

    # Store services in app config
    app.config["config_service"] = config
    app.config["logger_service"] = logger
    app.config["queue_service"] = queue_service
    app.config["worker_service"] = worker_service

    # Initialize Swagger API
    from server.swagger import api, ns_jobs, ns_text_to_image, ns_text_to_video, ns_text_to_speech, ns_health
    api.init_app(app)

    # Import route resources to register them
    from server.job_routes import JobResource
    from server.health_routes import HealthResource
    from domain.text_to_image.routes import GenerateResource, ModelsResource
    from domain.text_to_video.routes import GenerateResource as VideoGenerateResource, ModelsResource as VideoModelsResource
    from domain.text_to_speech.routes import GenerateResource as SpeechGenerateResource, ModelsResource as SpeechModelsResource

    # Register job handlers at startup
    from domain.text_to_image.service import TextToImageService
    from domain.text_to_video.service import TextToVideoService
    from domain.text_to_speech.service import TextToSpeechService
    queue_service.register_handler("text_to_image", TextToImageService(config).generate)
    queue_service.register_handler("text_to_video", TextToVideoService(config).generate)
    queue_service.register_handler("text_to_speech", TextToSpeechService(config).generate)

    logger.info(f"App started in '{config.environment}' environment")

    # Error handlers
    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.error(f"Unhandled exception: {str(e)}")
        return ResponseHelper.error(
            message="Internal server error",
            errors=[str(e)],
            status_code=500,
        )

    @app.errorhandler(404)
    def handle_not_found(e):
        return ResponseHelper.error(message="Resource not found", status_code=404)

    # Serve output files (images, videos, audio)
    output_path = Path(config.output_dir).resolve()
    
    @app.route("/output/<path:filename>")
    def serve_output(filename):
        return send_from_directory(output_path, filename)

    # Redirect root to Swagger docs
    @app.route("/")
    def index():
        return redirect("/docs")

    # Start worker
    worker_service.start()

    return app


if __name__ == "__main__":
    app = create_app()
    config = app.config["config_service"]
    app.run(
        host="0.0.0.0",
        port=config.flask_port,
        debug=config.get("FLASK_DEBUG", "false").lower() == "true",
    )
