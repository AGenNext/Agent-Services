"""
Data Generation Module

Synthetic data generation for testing and augmentation.
"""

from dataclasses import dataclass, field
from typing import Optional, Callable
from enum import Enum
import random
import string
import json
from datetime import datetime, timedelta


class DataType(Enum):
    """Types of data to generate."""
    USER = "user"
    PRODUCT = "product"
    REVIEW = "review"
    TRANSACTION = "transaction"
    LOG = "log"
    DOCUMENT = "document"
    CONVERSATION = "conversation"


class DistributionType(Enum):
    """Data distribution types."""
    UNIFORM = "uniform"
    NORMAL = "normal"
    EXPONENTIAL = "exponential"
    ZIPFIAN = "zipfian"


@dataclass
class GenerationConfig:
    """Configuration for data generation."""
    count: int = 100
    format: str = "json"
    seed: Optional[int] = None
    distribution: DistributionType = DistributionType.UNIFORM
    include_metadata: bool = True


# Synthetic data generators
class UserGenerator:
    """Generate synthetic user data."""
    
    FIRST_NAMES = [
        "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
        "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
        "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Lisa", "Daniel", "Nancy"
    ]
    
    LAST_NAMES = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"
    ]
    
    DOMAINS = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "example.com"]
    
    @classmethod
    def generate(cls, include_email: bool = True) -> dict:
        """Generate a single user."""
        first = random.choice(cls.FIRST_NAMES)
        last = random.choice(cls.LAST_NAMES)
        
        user = {
            "id": f"user_{random.randint(10000, 99999)}",
            "first_name": first,
            "last_name": last,
            "name": f"{first} {last}",
        }
        
        if include_email:
            domain = random.choice(cls.DOMAINS)
            user["email"] = f"{first.lower()}.{last.lower()}@{domain}"
        
        return user
    
    @classmethod
    def generate_batch(cls, count: int) -> list[dict]:
        """Generate multiple users."""
        return [cls.generate() for _ in range(count)]


class ProductGenerator:
    """Generate synthetic product data."""
    
    CATEGORIES = [
        "Electronics", "Clothing", "Books", "Home", "Sports", "Toys",
        "Beauty", "Automotive", "Garden", "Health"
    ]
    
    ADJECTIVES = [
        "Premium", "Classic", "Modern", "Vintage", "Essential", "Pro",
        "Ultra", "Mini", "Smart", "Eco"
    ]
    
    PRODUCTS = [
        "Widget", "Gadget", "Device", "Tool", "Kit", "Set",
        "System", "Pack", "Bundle", "Collection"
    ]
    
    @classmethod
    def generate(cls, category: Optional[str] = None) -> dict:
        """Generate a single product."""
        cat = category or random.choice(cls.CATEGORIES)
        adj = random.choice(cls.ADJECTIVES)
        prod = random.choice(cls.PRODUCTS)
        
        return {
            "id": f"prod_{random.randint(1000, 9999)}",
            "name": f"{adj} {prod}",
            "category": cat,
            "price": round(random.uniform(9.99, 999.99), 2),
            "in_stock": random.choice([True, True, True, False]),
            "rating": round(random.uniform(3.0, 5.0), 1),
        }
    
    @classmethod
    def generate_batch(cls, count: int) -> list[dict]:
        """Generate multiple products."""
        return [cls.generate() for _ in range(count)]


class ReviewGenerator:
    """Generate synthetic review data."""
    
    TEMPLATES = [
        "Great {aspect}! Highly recommend.",
        "Not bad, but could be better.",
        "Excellent quality. Worth the price.",
        "Decent product for the price.",
        "Amazing! Best I've ever used.",
        "Terrible. Do not buy.",
        "Pretty good, works as expected.",
        "Exceeded my expectations!",
    ]
    
    ASPECTS = ["product", "service", "quality", "delivery", "value"]
    
    @classmethod
    def generate(cls, product_id: Optional[str] = None) -> dict:
        """Generate a single review."""
        template = random.choice(cls.TEMPLATES)
        aspect = random.choice(cls.ASPECTS)
        
        return {
            "id": f"rev_{random.randint(10000, 99999)}",
            "product_id": product_id or f"prod_{random.randint(1000, 9999)}",
            "rating": random.randint(1, 5),
            "title": template.format(aspect=aspect),
            "text": f"{template.format(aspect=aspect)} " + " ".join([
                "Would buy again." if random.random() > 0.5
                else "Fast shipping." if random.random() > 0.5
                else "Good value."
                for _ in range(3)
            ]),
            "verified": random.random() > 0.3,
            "date": cls._random_date(),
        }
    
    @classmethod
    def _random_date(cls) -> str:
        """Generate random date."""
        days_ago = random.randint(0, 365)
        date = datetime.now() - timedelta(days=days_ago)
        return date.strftime("%Y-%m-%d")
    
    @classmethod
    def generate_batch(cls, count: int) -> list[dict]:
        """Generate multiple reviews."""
        return [cls.generate() for _ in range(count)]


class TransactionGenerator:
    """Generate synthetic transaction data."""
    
    STATUSES = ["completed", "pending", "failed", "refunded"]
    METHODS = ["credit_card", "debit_card", "paypal", "bank_transfer"]
    
    @classmethod
    def generate(cls, user_id: Optional[str] = None) -> dict:
        """Generate a single transaction."""
        return {
            "id": f"txn_{random.randint(100000, 999999)}",
            "user_id": user_id or f"user_{random.randint(10000, 99999)}",
            "amount": round(random.uniform(10.00, 5000.00), 2),
            "currency": "USD",
            "status": random.choice(cls.STATUSES),
            "method": random.choice(cls.METHODS),
            "timestamp": datetime.now().isoformat(),
        }
    
    @classmethod
    def generate_batch(cls, count: int) -> list[dict]:
        """Generate multiple transactions."""
        return [cls.generate() for _ in range(count)]


class LogGenerator:
    """Generate synthetic log data."""
    
    LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    
    MESSAGES = [
        "Request processed successfully",
        "User logged in",
        "Cache miss for key",
        "Database query executed",
        "API call completed",
        "Connection established",
        "Timeout waiting for response",
        "Invalid input received",
    ]
    
    @classmethod
    def generate(cls) -> dict:
        """Generate a single log entry."""
        return {
            "timestamp": datetime.now().isoformat(),
            "level": random.choice(cls.LEVELS),
            "message": random.choice(cls.MESSAGES),
            "service": f"service-{random.randint(1, 5)}",
            "trace_id": ''.join(random.choices(string.ascii_lowercase, k=16)),
        }
    
    @classmethod
    def generate_batch(cls, count: int) -> list[dict]:
        """Generate multiple log entries."""
        return [cls.generate() for _ in range(count)]


class ConversationGenerator:
    """Generate synthetic conversation data."""
    
    INTENTS = [
        "greeting", "help", "complaint", "inquiry", "feedback",
        "order", "refund", "support", "cancel", "question"
    ]
    
    GREETINGS = [
        "Hello!", "Hi there!", "Hey!", "Good morning!", 
        "Thanks for reaching out!"
    ]
    
    RESPONSES = [
        "I'd be happy to help with that.",
        "Let me look into this for you.",
        "Certainly! Here's what I can do.",
        "Great question! Here's the answer.",
        "I understand. Let me assist you.",
    ]
    
    @classmethod
    def generate(cls, turns: int = 4) -> dict:
        """Generate a conversation with multiple turns."""
        messages = []
        
        # User starts
        messages.append({
            "role": "user",
            "content": random.choice(cls.GREETINGS),
            "intent": "greeting"
        })
        
        # Bot responds
        messages.append({
            "role": "assistant", 
            "content": random.choice(cls.RESPONSES),
            "intent": "acknowledgment"
        })
        
        # Additional turns
        for _ in range(turns - 2):
            intent = random.choice(cls.INTENTS)
            messages.append({
                "role": random.choice(["user", "assistant"]),
                "content": f"Message about {intent}",
                "intent": intent
            })
        
        return {
            "conversation_id": f"conv_{random.randint(10000, 99999)}",
            "messages": messages,
            "status": random.choice(["active", "closed"]),
        }
    
    @classmethod
    def generate_batch(cls, count: int) -> list[dict]:
        """Generate multiple conversations."""
        return [cls.generate() for _ in range(count)]


# Factory
class DataGenerator:
    """Factory for creating synthetic data."""
    
    GENERATORS = {
        DataType.USER: UserGenerator,
        DataType.PRODUCT: ProductGenerator,
        DataType.REVIEW: ReviewGenerator,
        DataType.TRANSACTION: TransactionGenerator,
        DataType.LOG: LogGenerator,
        DataType.CONVERSATION: ConversationGenerator,
    }
    
    @classmethod
    def generate(
        cls,
        data_type: DataType,
        count: int = 100,
        config: Optional[GenerationConfig] = None
    ) -> list[dict]:
        """Generate synthetic data."""
        generator = cls.GENERATORS.get(data_type)
        
        if not generator:
            raise ValueError(f"Unknown data type: {data_type}")
        
        if config and config.seed:
            random.seed(config.seed)
        
        return generator.generate_batch(count)
    
    @classmethod
    def generate_json(
        cls,
        data_type: DataType,
        count: int = 100,
        config: Optional[GenerationConfig] = None
    ) -> str:
        """Generate JSON string."""
        data = cls.generate(data_type, count, config)
        return json.dumps(data, indent=2)
    
    @classmethod
    def generate_csv_headers(cls, data_type: DataType) -> list[str]:
        """Get CSV headers for data type."""
        samples = cls.generate(data_type, 1)
        if samples:
            return list(samples[0].keys())
        return []


# CLI
if __name__ == "__main__":
    # Example: generate data
    users = DataGenerator.generate(DataType.USER, 3)
    print(f"Generated {len(users)} users:")
    for u in users:
        print(f"  - {u['name']} ({u.get('email', 'no email')})")