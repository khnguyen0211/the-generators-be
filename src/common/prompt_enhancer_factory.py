"""Factory for creating provider-specific prompt enhancers."""

import logging
from .base_prompt_enhancer import BasePromptEnhancer

logger = logging.getLogger("the_generators")


class OpenAIPromptEnhancer(BasePromptEnhancer):
    """OpenAI GPT-based prompt enhancer."""

    SYSTEM_PROMPT = """You are a professional prompt enhancer. Transform simple prompts into detailed, vivid descriptions.

Given:
1. User's original prompt
2. Category with required format components
3. Example prompts for reference
4. Style references

Your task:
1. Analyze which format components are missing
2. Select appropriate styles from the references
3. Creatively fill in missing details while preserving user's intent
4. Return an enhanced prompt covering ALL required format components

Rules:
- Keep the user's core idea intact
- Be vivid and specific
- Use style terms from the provided references
- Output ONLY the enhanced prompt, no explanations"""

    def __init__(self, config):
        from openai import OpenAI
        self._config = config
        self._client = OpenAI(api_key=config.openai_api_key)

    def enhance(self, prompt: str, category: str, category_data: dict, style_reference: str) -> str:
        """Enhance prompt using OpenAI GPT."""
        format_list = ", ".join(category_data["format"])
        examples = "\n\n".join(category_data["examples"])

        user_message = f"""Category: {category_data["name"]}

Required format components: {format_list}

User prompt: {prompt}

Example prompts for this category:
{examples}

Style references (use these terms when describing visual elements):
{style_reference}

Now enhance the user prompt to include all required format components:"""

        model = self._config.prompt_enhancer_openai_model
        logger.info(f"[ENHANCER] Calling OpenAI | model={model}")

        response = self._client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        return response.choices[0].message.content.strip()


class HuggingFacePromptEnhancer(BasePromptEnhancer):
    """HuggingFace Inference API prompt enhancer."""

    SYSTEM_PROMPT = """You are a professional prompt enhancer. Transform simple prompts into detailed, vivid descriptions.

Rules:
- Keep the user's core idea intact
- Be vivid and specific with visual details
- Use the provided style terms
- Output ONLY the enhanced prompt, no explanations"""

    API_URL = "https://router.huggingface.co/v1/chat/completions"

    def __init__(self, config):
        self._config = config
        self._api_key = config.huggingface_api_key

    def enhance(self, prompt: str, category: str, category_data: dict, style_reference: str) -> str:
        """Enhance prompt using HuggingFace Inference API."""
        import requests

        format_list = ", ".join(category_data["format"])
        examples = "\n\n".join(category_data["examples"][:1])

        user_message = f"""Enhance this prompt for {category_data["name"]}.

Required components: {format_list}

Original prompt: {prompt}

Example style:
{examples}

Style terms to use: {style_reference}

Enhanced prompt:"""

        model = self._config.prompt_enhancer_huggingface_model
        logger.info(f"[ENHANCER] Calling HuggingFace | model={model}")

        response = requests.post(
            self.API_URL,
            headers={"Authorization": f"Bearer {self._api_key}"},
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                "max_tokens": 800,
                "temperature": 0.7
            },
            timeout=60
        )

        if response.status_code != 200:
            logger.error(f"[ENHANCER] HuggingFace API error: {response.text[:200]}")
            raise Exception(f"HuggingFace enhancer error: {response.status_code}")

        result = response.json()
        return result["choices"][0]["message"]["content"].strip()


class PromptEnhancerFactory:
    """Factory to create provider-specific prompt enhancers."""

    @staticmethod
    def create(provider: str, config) -> BasePromptEnhancer:
        """Create enhancer based on provider."""
        if provider == "openai":
            return OpenAIPromptEnhancer(config)
        elif provider == "huggingface":
            return HuggingFacePromptEnhancer(config)
        else:
            logger.warning(f"[ENHANCER] No enhancer for provider '{provider}', using OpenAI")
            return OpenAIPromptEnhancer(config)
