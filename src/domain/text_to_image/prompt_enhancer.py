"""Image prompt enhancer using LLM."""

import logging
from openai import OpenAI
from .prompts import IMAGE_CATEGORIES, IMAGE_STYLES, DEFAULT_CATEGORY, VALID_CATEGORIES

logger = logging.getLogger("the_generators")

ENHANCER_SYSTEM_PROMPT = """You are a professional image prompt enhancer. Transform simple prompts into detailed, vivid image descriptions.

Given:
1. User's original prompt
2. Image category with required format components
3. Example prompts for reference
4. Style references (lighting, color, composition, etc.)

Your task:
1. Analyze which format components are missing from user's prompt
2. Select appropriate styles from the style references that match the mood and theme
3. Creatively fill in the missing details while preserving user's intent
4. Return an enhanced prompt that covers ALL required format components

Rules:
- Keep the user's core idea intact
- Be vivid and specific with visual details
- Use specific style terms from the provided style references when describing lighting, colors, composition, etc.
- Match the style of the example prompts
- Output ONLY the enhanced prompt, no explanations or labels"""


class PromptEnhancer:
    """Enhances image prompts using LLM."""

    def __init__(self, config):
        self._config = config
        self._client = OpenAI(api_key=config.openai_api_key)

    def enhance(self, prompt: str, category: str = None) -> dict:
        """Enhance prompt with category detection and LLM."""
        if category and category in VALID_CATEGORIES:
            detected_category = category
        else:
            detected_category = self._detect_category(prompt)

        category_data = IMAGE_CATEGORIES[detected_category]
        enhanced_prompt = self._call_llm(prompt, category_data)

        logger.info(f"[ENHANCER] Image prompt enhanced | category={detected_category}")

        return {
            "enhanced_prompt": enhanced_prompt,
            "category": detected_category
        }

    def _detect_category(self, prompt: str) -> str:
        """Detect category from prompt using keyword matching."""
        prompt_lower = prompt.lower()
        best_match = DEFAULT_CATEGORY
        best_score = 0

        for cat_key, cat_data in IMAGE_CATEGORIES.items():
            score = sum(1 for kw in cat_data["keywords"] if kw in prompt_lower)
            if score > best_score:
                best_score = score
                best_match = cat_key

        logger.debug(f"[ENHANCER] Category detected: {best_match} (score={best_score})")
        return best_match

    def _call_llm(self, prompt: str, category_data: dict) -> str:
        """Call LLM to enhance the prompt."""
        format_list = ", ".join(category_data["format"])
        examples = "\n\n".join(category_data["examples"])
        style_reference = self._build_style_reference()

        user_message = f"""Category: {category_data["name"]}

Required format components: {format_list}

User prompt: {prompt}

Example prompts for this category:
{examples}

Style references (use these terms when describing visual elements):
{style_reference}

Now enhance the user prompt to include all required format components:"""

        logger.info(f"[ENHANCER] Calling LLM | model={self._config.prompt_enhancer_model}")

        response = self._client.chat.completions.create(
            model=self._config.prompt_enhancer_model,
            messages=[
                {"role": "system", "content": ENHANCER_SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        return response.choices[0].message.content.strip()

    def _build_style_reference(self) -> str:
        """Build condensed style reference for LLM."""
        relevant_styles = ["lighting", "color_tones", "composition", "camera_angles", "visual_aesthetics", "lens_effects"]
        lines = []
        for key in relevant_styles:
            if key in IMAGE_STYLES:
                style = IMAGE_STYLES[key]
                options = ", ".join(style["options"][:12])
                lines.append(f"- {style['name']}: {options}...")
        return "\n".join(lines)
