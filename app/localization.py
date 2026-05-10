"""
AI Localization Module

Supports multi-language processing and local deployment options.
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum
import json


class Language(Enum):
    # Supported languages
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    ITALIAN = "it"
    PORTUGUESE = "pt"
    CHINESE = "zh"
    JAPANESE = "ja"
    KOREAN = "ko"
    ARABIC = "ar"
    RUSSIAN = "ru"
    HINDI = "hi"
    DUTCH = "nl"
    POLISH = "pl"
    TURKISH = "tr"
    VIETNAMESE = "vi"
    THAI = "th"
    INDONESIAN = "id"
    
    @property
    def display_name(self) -> str:
        names = {
            "en": "English",
            "es": "Español",
            "fr": "Français",
            "de": "Deutsch",
            "it": "Italiano",
            "pt": "Português",
            "zh": "中文",
            "ja": "日本語",
            "ko": "한국어",
            "ar": "العربية",
            "ru": "Русский",
            "hi": "हिन्दी",
            "nl": "Nederlands",
            "pl": "Polski",
            "tr": "Türkçe",
            "vi": "Tiếng Việt",
            "th": "ไทย",
            "id": "Bahasa Indonesia",
        }
        return names.get(self.value, self.value)
    
    @property
    def prompt_cost_multiplier(self) -> float:
        """Multi-language models may cost more."""
        # Premium languages that typically cost more
        premium = {"zh": 1.5, "ja": 1.5, "ko": 1.3, "ar": 1.3}
        return premium.get(self.value, 1.0)


# Model capabilities per language
LANGUAGE_CAPABILITIES = {
    "gpt-4o": {
        "supports": ["en", "es", "fr", "de", "it", "pt", "zh", "ja", "ko", "ar", "ru", "hi", "nl", "pl", "vi", "th", "id", "tr"],
        "quality": "native",
    },
    "claude-3-5-sonnet": {
        "supports": ["en", "es", "fr", "de", "it", "pt", "zh", "ja", "ko"],
        "quality": "excellent",
    },
    "gemini-1.5-pro": {
        "supports": ["en", "es", "fr", "de", "it", "pt", "zh", "ja", "ko", "hi", "th", "vi", "id"],
        "quality": "good",
    },
    "llama3.3": {  # Ollama local
        "supports": ["en", "es", "fr", "de", "it", "pt", "zh", "ja", "ko", "ar", "ru"],
        "quality": "good",
        "local": True,
    },
    "qwen2.5": {
        "supports": ["en", "zh", "ja", "ko", "ar", "ru"],
        "quality": "good",
        "local": True,
    },
}


@dataclass
class LocalizationConfig:
    language: Language
    detect_language: bool = True
    native_prompt: bool = False
    prefer_local: bool = False


class LocalAIModel:
    """Local AI model for offline/private inference."""
    
    MODELS = {
        "ollama": {
            "llama3.3": {"size": "70B", "ram": "140GB", "languages": ["en", "zh", "multi"]},
            "llama3.2": {"size": "90B", "ram": "48GB", "languages": ["en", "multi"]},
            "qwen2.5": {"size": "72B", "ram": "144GB", "languages": ["en", "zh", "multi"]},
            "mistral": {"size": "7B", "ram": "14GB", "languages": ["en"]},
        },
        "llama.cpp": {
            "llama3.2-7b": {"size": "7B", "ram": "14GB", "quantized": "Q4_K_M"},
            "mistral-7b": {"size": "7B", "ram": "8GB", "quantized": "Q4_K_M"},
        },
    }
    
    @classmethod
    def list_models(cls, backend: str = "ollama") -> dict:
        """List available local models."""
        return cls.MODELS.get(backend, {})
    
    @classmethod
    def get_requirements(cls, model: str, backend: str = "ollama") -> dict:
        """Get hardware requirements for a model."""
        models = cls.MODELS.get(backend, {})
        return models.get(model, {})


class LocalizationService:
    """Service for handling multi-language AI requests."""
    
    def __init__(self, config: Optional[LocalizationConfig] = None):
        self.config = config or LocalizationConfig(
            language=Language.ENGLISH,
            detect_language=True
        )
    
    def detect_language(self, text: str) -> Language:
        """Detect language from text."""
        # Simple detection based on character ranges
        if any('\u4e00' <= c <= '\u9fff' for c in text):
            return Language.CHINESE
        if any('\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff' for c in text):
            return Language.JAPANESE
        if any('\uac00' <= c <= '\ud7af' for c in text):
            return Language.KOREAN
        if any('\u0600' <= c <= '\u06ff' for c in text):
            return Language.ARABIC
        if any('\u0900' <= c <= '\u097f' for c in text):
            return Language.HINDI
        # Default to English for Latin script
        return Language.ENGLISH
    
    def get_best_provider(self, language: Language, quality: str = "good") -> list[str]:
        """Get best providers for a language."""
        providers = []
        for model, caps in LANGUAGE_CAPABILITIES.items():
            if language.value in caps.get("supports", []):
                if caps.get("quality") in ["native", "excellent"] or caps.get("quality") == quality:
                    # Prefer local if available
                    if caps.get("local") and self.config.prefer_local:
                        providers.insert(0, model)
                    else:
                        providers.append(model)
        return providers[:3]
    
    def translate_prompt(self, text: str, target: Language, style: str = "natural") -> str:
        """Generate translation prompt for LLM."""
        if target == Language.ENGLISH:
            return f"Translate to English: {text}"
        return f"Translate to {target.display_name}: {text}"
    
    def build_localization_prompt(
        self,
        text: str,
        source_lang: Optional[Language] = None,
        target_lang: Language = Language.ENGLISH
    ) -> str:
        """Build prompt for localization."""
        source = source_lang.display_name if source_lang else "the original language"
        return f"""Translate the following text from {source} to {target_lang.display_name}.
Keep the original meaning, tone, and formatting.

Original text:
{text}

Translation:"""


@dataclass
class LocalizationResult:
    detected_language: Optional[Language]
    target_language: Language
    supported: bool
    best_provider: Optional[str]
    requires_translation: bool


def check_localization_support(
    text: str,
    target_language: str = "en",
    prefer_local: bool = False
) -> LocalizationResult:
    """Check if localization is supported."""
    service = LocalizationService(LocalizationConfig(
        language=Language(target_language),
        detect_language=True,
        prefer_local=prefer_local
    ))
    
    detected = service.detect_language(text)
    target = Language(target_language)
    providers = service.get_best_provider(detected)
    
    return LocalizationResult(
        detected_language=detected,
        target_language=target,
        supported=len(providers) > 0,
        best_provider=providers[0] if providers else None,
        requires_translation=detected != target
    )


# Supported languages list
SUPPORTED_LANGUAGES = [lang for lang in Language]


if __name__ == "__main__":
    # Example: check localization support
    text = "你好世界"
    result = check_localization_support(text)
    print(f"Text: {text}")
    print(f"Detected: {result.detected_language.display_name}")
    print(f"Best provider: {result.best_provider}")