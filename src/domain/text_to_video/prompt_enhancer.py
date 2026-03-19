"""Video prompt enhancer using LLM."""

import logging
from common.prompt_enhancer_factory import PromptEnhancerFactory
from .prompts import VIDEO_CATEGORIES, VIDEO_STYLES, DEFAULT_CATEGORY, VALID_CATEGORIES

logger = logging.getLogger("the_generators")


class PromptEnhancer:
    """Enhances video prompts using provider-specific LLM."""

    def __init__(self, config, provider: str = "openai"):
        self._config = config
        self._provider = provider

    def enhance(self, prompt: str, category: str = None) -> dict:
        """Enhance prompt with category detection and LLM."""
        if category and category in VALID_CATEGORIES:
            detected_category = category
        else:
            detected_category = self._detect_category(prompt)

        category_data = VIDEO_CATEGORIES[detected_category]
        style_reference = self._build_style_reference()

        enhancer = PromptEnhancerFactory.create(self._provider, self._config)
        enhanced_prompt = enhancer.enhance(prompt, detected_category, category_data, style_reference)

        logger.info(f"[ENHANCER] Video prompt enhanced | category={detected_category} | provider={self._provider}")

        return {
            "enhanced_prompt": enhanced_prompt,
            "category": detected_category
        }

    def _detect_category(self, prompt: str) -> str:
        """Detect category from prompt using keyword matching."""
        prompt_lower = prompt.lower()
        best_match = DEFAULT_CATEGORY
        best_score = 0

        for cat_key, cat_data in VIDEO_CATEGORIES.items():
            score = sum(1 for kw in cat_data["keywords"] if kw in prompt_lower)
            if score > best_score:
                best_score = score
                best_match = cat_key

        logger.debug(f"[ENHANCER] Category detected: {best_match} (score={best_score})")
        return best_match

    def _build_style_reference(self) -> str:
        """Build condensed style reference for LLM."""
        relevant_styles = ["lighting", "color_tones", "camera_movements", "camera_angles", "visual_aesthetics"]
        lines = []
        for key in relevant_styles:
            if key in VIDEO_STYLES:
                style = VIDEO_STYLES[key]
                options = ", ".join(style["options"][:15])
                lines.append(f"- {style['name']}: {options}...")
        return "\n".join(lines)
