"""Flask app entry point."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flask import Flask
from flask_cors import CORS

from services.config_service import ConfigService
from services.logger_service import LoggerService
from helpers.response_helper import ResponseHelper


def create_app() -> Flask:
    """Factory function to create Flask app."""
    app = Flask(__name__)

    config = ConfigService()
    config.load()

    logger = LoggerService(config)
    logger.setup()

    CORS(app)

    app.config["config_service"] = config
    app.config["logger_service"] = logger

    logger.info(f"App started in '{config.environment}' environment")

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

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return ResponseHelper.success(
            data={"status": "healthy", "environment": config.environment},
            message="Service is running",
        )

    # TODO: Register domain blueprints
    # from domain.text_to_image.routes import text_to_image_bp
    # app.register_blueprint(text_to_image_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    config = app.config["config_service"]
    app.run(
        host="0.0.0.0",
        port=config.flask_port,
        debug=config.get("FLASK_DEBUG", "false").lower() == "true",
    )
