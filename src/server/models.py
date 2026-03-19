"""Swagger request/response models."""

from flask_restx import fields
from server.swagger import api

# Common response model
api_response = api.model("ApiResponse", {
    "status_code": fields.Integer(description="HTTP status code"),
    "message": fields.String(description="Response message"),
    "errors": fields.List(fields.String, description="Error messages"),
    "data": fields.Raw(description="Response data"),
})

# Job models
job_data = api.model("JobData", {
    "job_id": fields.String(description="Unique job identifier"),
    "job_type": fields.String(description="Type of job"),
    "status": fields.String(description="Job status", enum=["pending", "processing", "completed", "failed"]),
    "result": fields.Raw(description="Job result when completed"),
    "error": fields.String(description="Error message if failed"),
    "created_at": fields.String(description="Job creation timestamp"),
    "updated_at": fields.String(description="Last update timestamp"),
})

# Text to Image models
generate_request = api.model("GenerateRequest", {
    "prompt": fields.String(required=True, description="Text description of the image", example="A beautiful sunset over mountains"),
    "provider": fields.String(description="AI provider", enum=["openai", "replicate", "stability", "huggingface"], example="openai"),
    "orientation": fields.String(description="Output orientation", enum=["portrait", "landscape"], example="landscape"),
    "quality": fields.String(description="Image quality (OpenAI only)", enum=["standard", "hd"], example="standard"),
    "category": fields.String(description="Image category for prompt enhancement (optional, auto-detected if not provided)",
                              enum=["portrait", "landscape", "product", "food", "architecture", "abstract", "wildlife", "street", "fantasy", "fashion", "stilllife", "vintage", "conceptual"],
                              example="landscape"),
})

generate_response_data = api.model("GenerateResponseData", {
    "job_id": fields.String(description="Job ID to track progress"),
    "status": fields.String(description="Initial job status"),
})

model_info = api.model("ModelInfo", {
    "provider": fields.String(description="Provider name"),
    "model": fields.String(description="Model name"),
    "is_default": fields.Boolean(description="Is default provider"),
})

models_response_data = api.model("ModelsResponseData", {
    "models": fields.List(fields.Nested(model_info)),
})

# Text to Video models
video_generate_request = api.model("VideoGenerateRequest", {
    "prompt": fields.String(required=True, description="Text description of the video", example="A cat walking on the beach"),
    "provider": fields.String(description="AI provider", enum=["openai"], example="openai"),
    "orientation": fields.String(description="Video orientation", enum=["portrait", "landscape"], example="landscape"),
    "category": fields.String(description="Video category for prompt enhancement (optional, auto-detected if not provided)", 
                              enum=["cinematic", "animation", "fashion", "product", "nature", "travel", "music", "sports", "news", "educational", "gaming", "historical"],
                              example="cinematic"),
})

# Text to Speech models
tts_generate_request = api.model("TTSGenerateRequest", {
    "prompt": fields.String(required=True, description="Text to convert to speech", example="Hello, welcome to The Generators API."),
    "provider": fields.String(description="AI provider", enum=["openai"], example="openai"),
    "voice": fields.String(description="Voice preset", enum=["alloy", "ash", "ballad", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer", "verse"], example="alloy"),
    "response_format": fields.String(description="Audio output format", enum=["mp3", "opus", "aac", "flac", "wav", "pcm"], example="mp3"),
    "speed": fields.Float(description="Speech speed (0.25 to 4.0)", example=1.0),
})

# Image to Video models
image_to_video_generate_request = api.model("ImageToVideoGenerateRequest", {
    "image_url": fields.String(required=True, description="Source image URL", example="https://example.com/photo.jpg"),
    "prompt": fields.String(required=True, description="Animation prompt", example="A cat slowly turning its head"),
    "provider": fields.String(description="AI provider", enum=["openai"], example="openai"),
    "orientation": fields.String(description="Video orientation", enum=["portrait", "landscape"], example="portrait"),
})

# Health check models
service_status = api.model("ServiceStatus", {
    "api": fields.String(description="API server status"),
    "queue": fields.String(description="Queue service status (redis/memory)"),
    "worker": fields.String(description="Background worker status"),
    "database": fields.String(description="Database service status (postgres)"),
})

health_data = api.model("HealthData", {
    "status": fields.String(description="Overall health status", enum=["healthy", "degraded"]),
    "environment": fields.String(description="Current environment"),
    "services": fields.Nested(service_status),
})
