"""Prompt templates and enhancement hints for text-to-image domain."""

ORIENTATION_HINTS = {
    "portrait": "Photorealistic, shot on DSLR, natural lighting, vertical composition, portrait orientation. ",
    "landscape": "Photorealistic, shot on DSLR, natural lighting, horizontal composition, landscape orientation. ",
}


def enhance_prompt(prompt: str, orientation: str) -> str:
    # Prepend orientation and realism hints to user prompt
    hint = ORIENTATION_HINTS.get(orientation, "")
    return hint + prompt
