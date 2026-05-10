"""
AI Research Module

Research AI topics, papers, and staying updated with latest developments.
"""

from dataclasses import dataclass, field
from typing import Optional, list
from enum import Enum
import json
from datetime import datetime


class ResearchCategory(Enum):
    """Research categories."""
    PAPER = "paper"
    MODEL = "model"
    TECHNIQUE = "technique"
    TOOL = "tool"
    NEWS = "news"
    BENCHMARK = "benchmark"


class PaperStatus(Enum):
    """Paper reading status."""
    UNREAD = "unread"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REFERENCED = "referenced"


@dataclass
class Paper:
    """AI Research Paper."""
    id: str
    title: str
    authors: list[str]
    year: int
    category: str
    abstract: str
    arxiv_id: Optional[str] = None
    github: Optional[str] = None
    paper_with_code: Optional[str] = None
    status: PaperStatus = PaperStatus.UNREAD
    notes: str = ""
    tags: list[str] = field(default_factory=list)
    
    @property
    def url(self) -> str:
        if self.arxiv_id:
            return f"https://arxiv.org/abs/{self.arxiv_id}"
        return f"https://arxiv.org/abs/{self.id}"


@dataclass
class Model:
    """AI Model information."""
    id: str
    name: str
    provider: str
    released: str
    parameters: str
    context_length: int
    capabilities: list[str]
    pricing: Optional[dict] = None
    github: Optional[str] = None


@dataclass
class Technique:
    """AI Technique."""
    id: str
    name: str
    category: str
    description: str
    paper_refs: list[str] = field(default_factory=list)
    implementations: list[str] = field(default_factory=list)
    difficulty: str = "intermediate"


@dataclass
class ResearchQuery:
    """Research query."""
    query: str
    category: Optional[ResearchCategory] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    limit: int = 10


@dataclass
class ResearchResult:
    """Research result."""
    title: str
    summary: str
    source: str
    url: str
    date: str
    relevance_score: float


# Curated resources library
PAPERS = {
    "transformer": Paper(
        id="1706.03762",
        title="Attention Is All You Need",
        authors=["Vaswani", "Shazeer", "Parmar", "et al."],
        year=2017,
        category="transformer",
        abstract="We propose a new network architecture, the Transformer, based solely on attention mechanisms.",
        arxiv_id="1706.03762",
        github="tensorflow/tensor2tensor",
        status=PaperStatus.COMPLETED,
        tags=["transformer", "attention", "NLP"]
    ),
    "gpt3": Paper(
        id="2005.14165",
        title="Language Models are Few-Shot Learners",
        authors=["Brown", "Mann", "Ryd", "et al."],
        year=2020,
        category="language_model",
        abstract="We show that scaling language models greatly improves task-agnostic few-shot performance.",
        arxiv_id="2005.14165",
        status=PaperStatus.COMPLETED,
        tags=["gpt", "few-shot", "scaling"]
    ),
    "rlhf": Paper(
        id="2203.02155",
        title="Training Language Models to Follow Instructions with Human Feedback",
        authors=["Stiennon", "Chen", "Madasu", "et al."],
        year=2022,
        category="alignment",
        abstract="We collect human feedback to fine-tune language models.",
        arxiv_id="2203.02155",
        status=PaperStatus.REFERENCED,
        tags=["rlhf", "alignment", "chatgpt"]
    ),
    "rope": Paper(
        id="2304.08613",
        title="RoFormer: Enhanced Position Representation with Rotary Position Embedding",
        authors=["Su", "Lu", "Pan", "et al."],
        year=2023,
        category="transformer",
        abstract="We introduce Rotary Position Embedding (RoPE) for better position encoding.",
        arxiv_id="2304.08613",
        status=PaperStatus.UNREAD,
        tags=["position", "embedding", "efficient"]
    ),
    "sft": Paper(
        id="2401.01373",
        title="Scalable Online Preference Learning",
        authors=["Xiao", "Ji", "Chen"],
        year=2024,
        category="alignment",
        abstract="Online methods for learning from preferences.",
        arxiv_id="2401.01373",
        status=PaperStatus.UNREAD,
        tags=["sft", "online"]
    ),
}

MODELS = {
    "gpt4": Model(
        id="gpt4",
        name="GPT-4",
        provider="OpenAI",
        released="2023",
        parameters="1.8T (estimated)",
        context_length=128000,
        capabilities=["chat", "vision", "tool_use", "function_calling"],
        pricing={"input": 30, "output": 60}
    ),
    "claude3": Model(
        id="claude3",
        name="Claude 3 Opus",
        provider="Anthropic",
        released="2024",
        parameters="~200B",
        context_length=200000,
        capabilities=["chat", "vision", "tool_use", "extended_thinking"],
        pricing={"input": 15, "output": 75}
    ),
    "gemini": Model(
        id="gemini",
        name="Gemini 1.5 Pro",
        provider="Google",
        released="2024",
        parameters="~1.5T",
        context_length=1000000,
        capabilities=["chat", "vision", "long_context", "multimodal"],
        pricing={"input": 1.25, "output": 5}
    ),
    "llama3": Model(
        id="llama3",
        name="Llama 3",
        provider="Meta",
        released="2024",
        parameters="70B",
        context_length=8192,
        capabilities=["open", "instruction", "code"],
        pricing=None,
        github="meta-llama/llama3"
    ),
}

TECHNIQUES = {
    "chain_of_thought": Technique(
        id="cot",
        name="Chain of Thought",
        category="reasoning",
        description="Generate intermediate reasoning steps before final answer.",
        paper_refs=["2201.11903"],
        implementations=["langchain", "llama_index"],
        difficulty="intermediate"
    ),
    "retrieval_augmented": Technique(
        id="rag",
        name="Retrieval Augmented Generation",
        category="architecture",
        description="Augment LLM with external knowledge retrieval.",
        paper_refs=["2205.11453"],
        implementations=["langchain", "llamaindex"],
        difficulty="intermediate"
    ),
    "re_act": Technique(
        id="react",
        name="ReAct",
        category="reasoning",
        description="Combine reasoning and acting for task solving.",
        paper_refs=["2210.03629"],
        implementations=["langchain", "transformers"],
        difficulty="advanced"
    ),
    "constitutional_ai": Technique(
        id="cai",
        name="Constitutional AI",
        category="alignment",
        description="AI guiding principles for harmless outputs.",
        paper_refs=["2302.07487"],
        implementations=[],
        difficulty="advanced"
    ),
}


class ResearchManager:
    """Manage AI research and reading list."""
    
    def __init__(self):
        self.papers = PAPERS.copy()
        self.models = MODELS.copy()
        self.techniques = TECHNIQUES.copy()
        self._reading_list: list[str] = []
    
    def search_papers(self, query: str) -> list[Paper]:
        """Search papers."""
        query = query.lower()
        results = []
        
        for paper in self.papers.values():
            if query in paper.title.lower():
                results.append(paper)
            elif query in paper.abstract.lower():
                results.append(paper)
            elif any(query in tag for tag in paper.tags):
                results.append(paper)
        
        return results[:10]
    
    def search_models(self, query: str) -> list[Model]:
        """Search models."""
        query = query.lower()
        results = []
        
        for model in self.models.values():
            if query in model.name.lower():
                results.append(model)
            elif query in model.provider.lower():
                results.append(model)
        
        return results[:10]
    
    def search_techniques(self, query: str) -> list[Technique]:
        """Search techniques."""
        query = query.lower()
        results = []
        
        for tech in self.techniques.values():
            if query in tech.name.lower():
                results.append(tech)
            elif query in tech.description.lower():
                results.append(tech)
        
        return results[:10]
    
    def add_paper(self, paper: Paper):
        """Add paper to library."""
        self.papers[paper.id] = paper
    
    def update_status(self, paper_id: str, status: PaperStatus):
        """Update paper status."""
        if paper_id in self.papers:
            self.papers[paper_id].status = status
    
    def get_reading_list(self) -> list[Paper]:
        """Get reading list."""
        return [self.papers[id] for id in self._reading_list if id in self.papers]
    
    def add_to_reading_list(self, paper_id: str):
        """Add to reading list."""
        if paper_id not in self._reading_list:
            self._reading_list.append(paper_id)
    
    def compare_models(self) -> dict:
        """Compare models."""
        return {
            "models": {
                m.id: {
                    "name": m.name,
                    "provider": m.provider,
                    "context": m.context_length,
                    "capabilities": m.capabilities,
                    "pricing": m.pricing,
                }
                for m in self.models.values()
            }
        }
    
    def get_trending_techniques(self) -> list[Technique]:
        """Get trending techniques."""
        return list(self.techniques.values())[:5]
    
    def export_library(self) -> dict:
        """Export research library."""
        return {
            "papers": len(self.papers),
            "models": len(self.models),
            "techniques": len(self.techniques),
            "reading_list": len(self._reading_list),
        }
    
    def get_summary(self) -> dict:
        """Get research summary."""
        return {
            "papers": len(self.papers),
            "models": len(self.models),
            "techniques": len(self.techniques),
            "trending": [t.name for t in self.get_trending_techniques()],
        }


# Research topics
RESEARCH_TOPICS = {
    "LLM": ["scaling", "alignment", "reasoning", "memory", "agents"],
    "Vision": ["multimodal", "image_understanding", "video_understanding"],
    "Audio": ["speech_recognition", "voice_synthesis", "music_generation"],
    "Robotics": ["embodied_ai", "manipulation", "navigation"],
    "Efficiency": ["quantization", "distillation", "pruning", "speculative_decoding"],
    "Safety": ["jailbreak", "alignment", "interpretability", "constitutional"],
}

RESEARCH_TEMPLATES = {
    "new_model": """
## Model Research: {model_name}
- Provider: {provider}
- Release Date: {released}
- Parameters: {parameters}
- Context Length: {context}
- Capabilities: {capabilities}
- Pricing: {pricing}
- Key Paper: {paper}
- GitHub: {github}
""",
    "new_technique": """
## Technique: {name}
- Category: {category}
- Description: {description}
- Difficulty: {difficulty}
- Key Paper: {paper_ref}
- Implementations: {implementations}
""",
}


# Quick search
def search_research(query: str) -> dict:
    """Quick research search."""
    manager = ResearchManager()
    
    papers = manager.search_papers(query)
    models = manager.search_models(query)
    techniques = manager.search_techniques(query)
    
    return {
        "papers": [
            {"title": p.title, "year": p.year, "abstract": p.abstract[:100]}
            for p in papers
        ],
        "models": [
            {"name": m.name, "provider": m.provider, "capabilities": m.capabilities}
            for m in models
        ],
        "techniques": [
            {"name": t.name, "description": t.description[:50]}
            for t in techniques
        ],
    }


# Example
if __name__ == "__main__":
    # Search for "transformer"
    results = search_research("transformer")
    print("Search results for 'transformer':")
    print(f"  Papers: {len(results['papers'])}")
    print(f"  Models: {len(results['models'])}")
    print(f"  Techniques: {len(results['techniques'])}")