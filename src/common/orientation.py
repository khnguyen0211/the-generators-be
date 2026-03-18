"""Shared orientation model for all generation domains."""

import logging

logger = logging.getLogger("the_generators")

VALID_ORIENTATIONS = ["portrait", "landscape"]

SIZE_MAP = {
    ("landscape", "text_to_image"): "1792x1024",
    ("portrait", "text_to_image"): "1024x1792",
    ("landscape", "text_to_video"): "1280x720",
    ("portrait", "text_to_video"): "720x1280",
    ("landscape", "image_to_video"): "1280x720",
    ("portrait", "image_to_video"): "720x1280",
}


def resolve_size(orientation: str, domain: str) -> str:
    # Resolve orientation + domain to pixel size string
    if orientation not in VALID_ORIENTATIONS:
        raise ValueError(f"Invalid orientation: '{orientation}'. Must be one of: {VALID_ORIENTATIONS}")

    key = (orientation, domain)
    if key not in SIZE_MAP:
        raise ValueError(f"Unsupported domain: '{domain}'")

    size = SIZE_MAP[key]
    logger.info(f"[ORIENTATION] Resolved {orientation} + {domain} -> {size}")
    return size
