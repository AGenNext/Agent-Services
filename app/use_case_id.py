"""
AI Use Case Identification Module

Identifies and recommends AI use cases based on business context.
"""

from dataclasses import dataclass, field
from typing import Optional, list
from enum import Enum
import json


class Industry(Enum):
    """Business industries."""
    ECOMMERCE = "ecommerce"
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    EDUCATION = "education"
    MANUFACTURING = "manufacturing"
    RETAIL = "retail"
    TRAVEL = "travel"
    REAL_ESTATE = "real_estate"
    LEGAL = "legal"
    MARKETING = "marketing"
    HR = "hr"
    IT = "it"
    MEDIA = "media"


class UseCaseCategory(Enum):
    """AI use case categories."""
    CUSTOMER_SERVICE = "customer_service"
    CONTENT = "content"
    DATA_ANALYTICS = "data_analytics"
    AUTOMATION = "automation"
    SECURITY = "security"
    SEARCH = "search"
    RECOMMENDATION = "recommendation"
    TRANSCRIPTION = "transcription"
    TRANSLATION = "translation"


class Complexity(Enum):
    """Implementation complexity."""
    LOW = "low"       # Ready to use
    MEDIUM = "medium"   # Some customization
    HIGH = "high"      # Full development


@dataclass
class UseCase:
    """An AI use case."""
    id: str
    name: str
    description: str
    category: UseCaseCategory
    complexity: Complexity
    industry: list[Industry]
    providers: list[str]
    estimated_setup_time: str
    benefits: list[str]
    requirements: list[str] = field(default_factory=list)


# Use case library
USE_CASES = [
    # Customer Service
    UseCase(
        id="chatbot",
        name="AI Chatbot",
        description="Intelligent customer support chatbot that answers questions and resolves issues.",
        category=UseCaseCategory.CUSTOMER_SERVICE,
        complexity=Complexity.MEDIUM,
        industry=[Industry.ECOMMERCE, Industry.RETAIL, Industry.FINANCE],
        providers=["openai", "anthropic", "google"],
        estimated_setup_time="1-2 weeks",
        benefits=["24/7 support", "Reduced costs", "Faster response"],
    ),
    UseCase(
        id="support-triage",
        name="Support Ticket Triage",
        description="Automatically categorize and route support tickets to the right team.",
        category=UseCaseCategory.CUSTOMER_SERVICE,
        complexity=Complexity.LOW,
        industry=[Industry.IT, Industry.FINANCE, Industry.ECOMMERCE],
        providers=["openai", "anthropic"],
        estimated_setup_time="2-3 days",
        benefits=["Faster routing", "Better classification"],
    ),
    
    # Content
    UseCase(
        id="content_generation",
        name="Content Generation",
        description="Generate marketing copy, product descriptions, and social media posts.",
        category=UseCaseCategory.CONTENT,
        complexity=Complexity.LOW,
        industry=[Industry.MARKETING, Industry.ECOMMERCE, Industry.MEDIA],
        providers=["openai", "anthropic", "mistral"],
        estimated_setup_time="1 week",
        benefits=["Faster content", "Consistent tone"],
    ),
    UseCase(
        id="email_generation",
        name="Email Generation",
        description="Generate personalized email responses and campaigns.",
        category=UseCaseCategory.CONTENT,
        complexity=Complexity.LOW,
        industry=[Industry.MARKETING, Industry.SALES, Industry.HR],
        providers=["openai", "google"],
        estimated_setup_time="1 week",
        benefits=["Personalization", "Scale"],
    ),
    
    # Data Analytics
    UseCase(
        id="sentiment_analysis",
        name="Sentiment Analysis",
        description="Analyze customer feedback and social media for sentiment.",
        category=UseCaseCategory.DATA_ANALYTICS,
        complexity=Complexity.MEDIUM,
        industry=[Industry.MARKETING, Industry.RETAIL, Industry.HEALTHCARE],
        providers=["openai", "google", "aws_bedrock"],
        estimated_setup_time="1-2 weeks",
        benefits=["Customer insights", "Trend detection"],
    ),
    UseCase(
        id="document_qa",
        name="Document Q&A",
        description="Answer questions from documents, policies, and knowledge bases.",
        category=UseCaseCategory.DATA_ANALYTICS,
        complexity=Complexity.MEDIUM,
        industry=[Industry.LEGAL, Industry.HR, Industry.IT],
        providers=["openai", "anthropic", "google"],
        estimated_setup_time="2-3 weeks",
        benefits=["Fast lookup", "Consistent answers"],
    ),
    UseCase(
        id="data_extraction",
        name="Data Extraction",
        description="Extract structured data from unstructured documents.",
        category=UseCaseCategory.DATA_ANALYTICS,
        complexity=Complexity.MEDIUM,
        industry=[Industry.FINANCE, Industry.LEGAL, Industry.HEALTHCARE],
        providers=["anthropic", "google", "openai"],
        estimated_setup_time="2-4 weeks",
        benefits=["Automation", "Accuracy"],
    ),
    
    # Automation
    UseCase(
        id="workflow_automation",
        name="Workflow Automation",
        description="Automate business processes with AI decision-making.",
        category=UseCaseCategory.AUTOMATION,
        complexity=Complexity.HIGH,
        industry=[Industry.IT, Industry.FINANCE, Industry.MANUFACTURING],
        providers=["openai", "anthropic"],
        estimated_setup_time="1-2 months",
        benefits=["Efficiency", "Consistency"],
    ),
    UseCase(
        id="code_assistant",
        name="Code Assistant",
        description="Help developers write, review, and debug code.",
        category=UseCaseCategory.AUTOMATION,
        complexity=Complexity.LOW,
        industry=[Industry.IT],
        providers=["openai", "anthropic", "google"],
        estimated_setup_time="1-2 days",
        benefits=["Productivity", "Better code"],
    ),
    
    # Search
    UseCase(
        id="semantic_search",
        name="Semantic Search",
        description="Natural language search across documents and knowledge bases.",
        category=UseCaseCategory.SEARCH,
        complexity=Complexity.MEDIUM,
        industry=[Industry.IT, Industry.LEGAL, Industry.HR],
        providers=["openai", "google", "aws_bedrock"],
        estimated_setup_time="2-3 weeks",
        benefits=["Better results", "Natural queries"],
    ),
    UseCase(
        id="rag",
        name="RAG System",
        description="Retrieval-augmented generation for accurate answers.",
        category=UseCaseCategory.SEARCH,
        complexity=Complexity.HIGH,
        industry=[Industry.FINANCE, Industry.LEGAL, Industry.HEALTHCARE],
        providers=["openai", "anthropic", "google"],
        estimated_setup_time="3-4 weeks",
        benefits=["Accuracy", "Fresh data"],
    ),
    
    # Recommendation
    UseCase(
        id="product_recommendations",
        name="Product Recommendations",
        description="AI-powered product recommendations for customers.",
        category=UseCaseCategory.RECOMMENDATION,
        complexity=Complexity.MEDIUM,
        industry=[Industry.ECOMMERCE, Industry.RETAIL],
        providers=["openai", "google"],
        estimated_setup_time="2-3 weeks",
        benefits=["Higher conversion", "Personalization"],
    ),
    
    # Transcription
    UseCase(
        id="meeting_transcription",
        name="Meeting Transcription",
        description="Transcribe and summarize meetings with action items.",
        category=UseCaseCategory.TRANSCRIPTION,
        complexity=Complexity.LOW,
        industry=[Industry.IT, Industry.HR, Industry.MARKETING],
        providers=["openai", "google"],
        estimated_setup_time="1-2 days",
        benefits=["Documentation", "Time savings"],
    ),
    
    # Translation
    UseCase(
        id="translation",
        name="Multi-language Translation",
        description="Translate content to multiple languages.",
        category=UseCaseCategory.TRANSLATION,
        complexity=Complexity.LOW,
        industry=[Industry.ECOMMERCE, Industry.MEDIA, Industry.TRAVEL],
        providers=["openai", "google", "deepl"],
        estimated_setup_time="1 week",
        benefits=["Global reach", "Speed"],
    ),
]


# Industry mapping
INDUSTRY_KEYWORDS = {
    Industry.ECOMMERCE: ["shop", "store", "product", "buy", "cart", "checkout", "order"],
    Industry.HEALTHCARE: ["patient", "doctor", "medical", "health", "hospital", "clinic"],
    Industry.FINANCE: ["bank", "payment", "invoice", "account", "transaction", "investment"],
    Industry.EDUCATION: ["student", "course", "learning", "teacher", "school", "education"],
    Industry.RETAIL: ["store", "shop", "retail", "inventory", "purchase"],
    Industry.IT: ["software", "code", "developer", "tech", "api", "system"],
    Industry.MARKETING: ["campaign", "brand", "social", "advertising", "content"],
    Industry.LEGAL: ["legal", "contract", "law", "compliance", "regulation"],
    Industry.HR: ["employee", "hiring", "recruitment", "benefits", "payroll"],
}


class UseCaseIdentifier:
    """Identify appropriate AI use cases."""
    
    def __init__(self, industry: Optional[Industry] = None):
        self.industry = industry
        self._use_cases = {uc.id: uc for uc in USE_CASES}
    
    def identify_from_text(self, description: str) -> list[UseCase]:
        """Identify use cases from business description."""
        description = description.lower()
        
        # Determine industry
        detected_industry = self._detect_industry(description)
        
        # Score use cases
        scored = []
        for uc in USE_CASES:
            score = self._score_use_case(uc, description, detected_industry)
            if score > 0:
                scored.append((score, uc))
        
        # Sort by score
        scored.sort(key=lambda x: -x[0])
        return [uc for _, uc in scored[:5]]
    
    def _detect_industry(self, text: str) -> Optional[Industry]:
        """Detect industry from text."""
        text = text.lower()
        
        scores = {}
        for industry, keywords in INDUSTRY_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text)
            scores[industry] = score
        
        if scores:
            best = max(scores.items(), key=lambda x: x[1])
            if best[1] > 0:
                return best[0]
        
        return self.industry
    
    def _score_use_case(self, uc: UseCase, industry: Optional[Industry]) -> float:
        """Score a use case match."""
        score = 0
        
        # Industry match
        if industry and industry in uc.industry:
            score += 3
        
        # Category expertise
        score += uc.complexity.value == "low" and 2 or 1
        
        return score
    
    def get_by_industry(self, industry: Industry) -> list[UseCase]:
        """Get use cases for an industry."""
        return [uc for uc in USE_CASES if industry in uc.industry]
    
    def get_by_category(self, category: UseCaseCategory) -> list[UseCase]:
        """Get use cases by category."""
        return [uc for uc in USE_CASES if uc.category == category]
    
    def get_by_complexity(self, complexity: Complexity) -> list[UseCase]:
        """Get use cases by complexity."""
        return [uc for uc in USE_CASES if uc.complexity == complexity]
    
    def recommend(
        self,
        industry: Optional[Industry] = None,
        complexity: Optional[Complexity] = None,
        category: Optional[UseCaseCategory] = None
    ) -> list[UseCase]:
        """Get recommended use cases."""
        results = USE_CASES
        
        if industry:
            results = [uc for uc in results if industry in uc.industry]
        
        if complexity:
            results = [uc for uc in results if uc.complexity == complexity]
        
        if category:
            results = [uc for uc in results if uc.category == category]
        
        return results[:10]


@dataclass
class UseCaseRecommendation:
    """A use case recommendation."""
    use_case: UseCase
    match_score: float
    matched_reason: str


def recommend_use_cases(
    business_description: str,
    industry: Optional[str] = None,
    complexity: Optional[str] = None
) -> list[dict]:
    """Recommend AI use cases based on business."""
    
    # Parse inputs
    ind = Industry(industry.lower()) if industry else None
    comp = Complexity(complexity.lower()) if complexity else None
    
    # Identify
    identifier = UseCaseIdentifier(ind)
    use_cases = identifier.identify_from_text(business_description)
    
    # Apply filters
    if comp:
        use_cases = [uc for uc in use_cases if uc.complexity == comp]
    
    return [
        {
            "id": uc.id,
            "name": uc.name,
            "description": uc.description,
            "category": uc.category.value,
            "complexity": uc.complexity.value,
            "setup_time": uc.estimated_setup_time,
            "providers": uc.providers,
            "benefits": uc.benefits,
        }
        for uc in use_cases[:5]
    ]


# CLI
if __name__ == "__main__":
    # Example: identify use cases
    desc = "We run an online store selling electronics and need to automate customer support"
    recommendations = recommend_use_cases(desc, industry="ecommerce")
    
    print(f"Found {len(recommendations)} use cases:")
    for r in recommendations:
        print(f"  - {r['name']} ({r['complexity']})")
        print(f"    {r['description'][:60]}...")