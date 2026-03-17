"""Swagger/OpenAPI configuration."""

from flask_restx import Api

api = Api(
    title="The Generators API",
    version="1.0.0",
    description="AI Content Generation API - Generate images, videos, and audio from text",
    doc="/docs",
    prefix="/api",
)

# Namespaces
ns_jobs = api.namespace("jobs", description="Job status operations")
ns_text_to_image = api.namespace("text-to-image", description="Text to Image generation")
ns_health = api.namespace("health", description="Health check operations")
