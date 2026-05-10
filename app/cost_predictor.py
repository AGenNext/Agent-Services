"""
Cost Prediction Module for LLM Providers

Estimates costs for different LLM providers based on input/output tokens.
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class Provider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    OLLAMA = "ollama"
    OPENROUTER = "openrouter"
    AWS_BEDROCK = "aws_bedrock"
    AZURE = "azure"
    MISTRAL = "mistral"
    IBM_WATSON = "ibm_watson"
    SALESFORCE = "salesforce"


# Pricing per 1M tokens (USD)
PRICING = {
    Provider.OPENAI: {
        "gpt-4o": {"input": 5.00, "output": 15.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-4-turbo": {"input": 10.00, "output": 30.00},
        "gpt-4": {"input": 30.00, "output": 60.00},
        "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    },
    Provider.ANTHROPIC: {
        "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
        "claude-3-5-sonnet-20240620": {"input": 3.00, "output": 15.00},
        "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
        "claude-3-sonnet-20240229": {"input": 3.00, "output": 15.00},
        "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
    },
    Provider.GOOGLE: {
        "gemini-2.0-flash-exp": {"input": 0.00, "output": 0.00},  # Free
        "gemini-2.0-flash": {"input": 0.075, "output": 0.30},
        "gemini-1.5-pro": {"input": 1.25, "output": 5.00},
        "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
    },
    Provider.OLLAMA: {
        # Local - no API costs, just hardware
        "llama3.3": {"input": 0.00, "output": 0.00},
        "llama3.2": {"input": 0.00, "output": 0.00},
        "qwen2.5": {"input": 0.00, "output": 0.00},
        "mistral": {"input": 0.00, "output": 0.00},
    },
    Provider.OPENROUTER: {
        # Varies by underlying provider
        "openai/gpt-4o": {"input": 4.50, "output": 18.00},
        "anthropic/claude-3.5-sonnet": {"input": 3.00, "output": 15.00},
        "google/gemini-1.5-pro": {"input": 1.00, "output": 5.00},
        "meta/llama-3.1-405b-instruct": {"input": 3.50, "output": 3.50},
    },
    Provider.AWS_BEDROCK: {
        "anthropic.claude-3-5-sonnet-20241022-v1:0": {"input": 3.00, "output": 15.00},
        "anthropic.claude-3-opus-20240229-v1:0": {"input": 15.00, "output": 75.00},
        "anthropic.claude-3-sonnet-20240229-v1:0": {"input": 3.00, "output": 15.00},
        "anthropic.claude-3-haiku-20240307-v1:0": {"input": 0.25, "output": 1.25},
    },
    Provider.AZURE: {
        "gpt-4o": {"input": 2.50, "output": 7.50},
        "gpt-4-turbo": {"input": 2.50, "output": 7.50},
        "gpt-35-turbo": {"input": 0.50, "output": 1.50},
    },
    Provider.MISTRAL: {
        "mistral-large-latest": {"input": 2.00, "output": 6.00},
        "mistral-small-latest": {"input": 0.20, "output": 0.60},
    },
    Provider.IBM_WATSON: {
        "watsonx-ai": {"input": 1.50, "output": 1.50},
    },
    Provider.SALESFORCE: {
        "salesforce-einstein": {"input": 2.00, "output": 2.00},
    },
}


@dataclass
class CostEstimate:
    input_cost: float
    output_cost: float
    input_tokens: int
    output_tokens: int
    total_cost: float
    provider: str
    model: str


class CostPredictor:
    """Predicts costs for LLM API calls."""
    
    def __init__(self, provider: Provider, model: Optional[str] = None):
        self.provider = provider
        self.model = model
    
    def estimate(
        self, 
        input_tokens: int, 
        output_tokens: int,
        include_cache: bool = False
    ) -> CostEstimate:
        """Estimate cost for a request."""
        model = self.model or self._get_default_model()
        pricing = PRICING.get(self.provider, {}).get(model, {"input": 0, "output": 0})
        
        # Adjust for cached tokens if applicable
        input_rate = pricing.get("input", 0)
        if include_cache and self.provider == Provider.ANTHROPIC:
            input_rate *= 0.10  # 90% discount for cached input
        
        input_cost = (input_tokens / 1_000_000) * input_rate
        output_cost = (output_tokens / 1_000_000) * pricing.get("output", 0)
        
        return CostEstimate(
            input_cost=round(input_cost, 6),
            output_cost=round(output_cost, 6),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_cost=round(input_cost + output_cost, 6),
            provider=self.provider.value,
            model=model
        )
    
    def _get_default_model(self) -> str:
        """Get default model for provider."""
        defaults = {
            Provider.OPENAI: "gpt-4o",
            Provider.ANTHROPIC: "claude-3-5-sonnet-20241022",
            Provider.GOOGLE: "gemini-1.5-flash",
            Provider.OLLAMA: "llama3.3",
            Provider.OPENROUTER: "openai/gpt-4o",
            Provider.AWS_BEDROCK: "anthropic.claude-3-5-sonnet-20241022-v1:0",
            Provider.AZURE: "gpt-4o",
            Provider.MISTRAL: "mistral-large-latest",
            Provider.IBM_WATSON: "watsonx-ai",
            Provider.SALESFORCE: "salesforce-einstein",
        }
        return defaults.get(self.provider, "default")
    
    @staticmethod
    def compare_providers(
        provider: Provider,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> list[CostEstimate]:
        """Compare costs across all providers for the same request."""
        estimates = []
        for p in Provider:
            try:
                predictor = CostPredictor(p, model)
                estimate = predictor.estimate(input_tokens, output_tokens)
                estimates.append(estimate)
            except Exception:
                continue
        
        # Sort by total cost
        return sorted(estimates, key=lambda x: x.total_cost)


def estimate_request(
    provider: str,
    model: str,
    input_tokens: int,
    output_tokens: int
) -> dict:
    """Quick estimate function."""
    try:
        p = Provider(provider.lower())
        predictor = CostPredictor(p, model)
        est = predictor.estimate(input_tokens, output_tokens)
        return {
            "input_cost": est.input_cost,
            "output_cost": est.output_cost,
            "total_cost": est.total_cost,
            "provider": est.provider,
            "model": est.model,
        }
    except ValueError as e:
        return {"error": str(e)}


# Example usage
if __name__ == "__main__":
    # Compare GPT-4o across different providers
    estimates = CostPredictor.compare_providers(
        Provider.OPENAI,
        "gpt-4o",
        input_tokens=1000,
        output_tokens=500
    )
    
    print("Cost Comparison for 1K input + 500 output tokens:")
    print("-" * 50)
    for est in estimates[:5]:
        print(f"{est.provider:15} ${est.total_cost:.4f}")