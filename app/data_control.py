"""
Data Control Module

Privacy, governance, and data processing controls for AI services.
"""

from dataclasses import dataclass, field
from typing import Optional, list
from enum import Enum
from datetime import datetime, timedelta
import hashlib
import json


class DataRetention(Enum):
    """Data retention policies."""
    NEVER = "never"           # Don't store anything
    SESSION = "session"       # Session only
    SHORT = "short"           # 24 hours
    MEDIUM = "medium"          # 7 days
    LONG = "long"             # 30 days
    PERMANENT = "permanent"    # Indefinite


class DataRegion(Enum):
    """Data residency regions."""
    US = "us"
    EU = "eu"
    UK = "uk"
    APAC = "apac"
    LOCAL = "local"           # On-premise only


class DataClassification(Enum):
    """Data sensitivity levels."""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


@dataclass
class DataPolicy:
    """Data processing policy."""
    retention: DataRetention = DataRetention.SHORT
    region: DataRegion = DataRegion.US
    classification: DataClassification = DataClassification.INTERNAL
    allow_logging: bool = False
    allow_anonymization: bool = True
    encrypt_at_rest: bool = True
    encrypt_in_transit: bool = True
    
    def to_dict(self) -> dict:
        return {
            "retention": self.retention.value,
            "region": self.region.value,
            "classification": self.classification.value,
            "allow_logging": self.allow_logging,
            "allow_anonymization": self.allow_anonymization,
            "encrypt_at_rest": self.encrypt_at_rest,
            "encrypt_in_transit": self.encrypt_in_transit,
        }


@dataclass
class DataAccessLog:
    """Audit log entry."""
    timestamp: datetime
    action: str
    user_id: str
    resource: str
    classification: DataClassification
    allowed: bool
    ip_address: Optional[str] = None


class DataController:
    """Controls data processing and access."""
    
    def __init__(self, policy: Optional[DataPolicy] = None):
        self.policy = policy or DataPolicy()
        self._audit_log: list[DataAccessLog] = []
        self._pii_patterns = {
            "email": r'[\w.-]+@[\w.-]+\.\w+',
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
            "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
        }
    
    def anonymize(self, data: str, preserve_format: bool = True) -> str:
        """Anonymize PII in data."""
        import re
        
        result = data
        
        # Redact email
        result = re.sub(self._pii_patterns["email"], "[EMAIL]", result)
        
        # Redact phone
        result = re.sub(self._pii_patterns["phone"], "[PHONE]", result)
        
        # Redact SSN
        result = re.sub(self._pii_patterns["ssn"], "[SSN]", result)
        
        # Redact credit cards
        result = re.sub(self._pii_patterns["credit_card"], "[CARD]", result)
        
        return result
    
    def hash_for_audit(self, data: str) -> str:
        """Create audit hash of data."""
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def should_store(self, data: str, classification: DataClassification) -> bool:
        """Check if data should be stored."""
        policy_map = {
            DataClassification.PUBLIC: [DataRetention.LONG, DataRetention.PERMANENT],
            DataClassification.INTERNAL: [DataRetention.MEDIUM, DataRetention.LONG],
            DataClassification.CONFIDENTIAL: [DataRetention.SHORT, DataRetention.MEDIUM],
            DataClassification.RESTRICTED: [DataRetention.NEVER, DataRetention.SESSION],
        }
        allowed = policy_map.get(classification, [DataRetention.NEVER])
        return self.policy.retention in allowed
    
    def log_access(
        self,
        action: str,
        user_id: str,
        resource: str,
        classification: DataClassification,
        allowed: bool,
        ip_address: Optional[str] = None
    ):
        """Log data access for audit."""
        entry = DataAccessLog(
            timestamp=datetime.now(),
            action=action,
            user_id=user_id,
            resource=resource,
            classification=classification,
            allowed=allowed,
            ip_address=ip_address
        )
        self._audit_log.append(entry)
    
    def get_audit_log(
        self,
        since: Optional[datetime] = None,
        user_id: Optional[str] = None
    ) -> list[dict]:
        """Get filtered audit log."""
        logs = self._audit_log
        
        if since:
            logs = [l for l in logs if l.timestamp >= since]
        
        if user_id:
            logs = [l for l in logs if l.user_id == user_id]
        
        return [
            {
                "timestamp": l.timestamp.isoformat(),
                "action": l.action,
                "user_id": l.user_id,
                "resource": l.resource,
                "classification": l.classification.value,
                "allowed": l.allowed,
            }
            for l in logs
        ]
    
    def export_policy(self) -> dict:
        """Export data policy as JSON."""
        return self.policy.to_dict()


@dataclass
class RegionConfig:
    """Regional data configuration."""
    region: DataRegion
    allowed_providers: list[str]
    latency_target_ms: int = 100
    
    @classmethod
    def for_region(cls, region: DataRegion) -> "RegionConfig":
        configs = {
            DataRegion.US: cls(
                region=DataRegion.US,
                allowed_providers=["openai", "anthropic", "google", "aws_bedrock"],
                latency_target_ms=100
            ),
            DataRegion.EU: cls(
                region=DataRegion.EU,
                allowed_providers=["openai", "anthropic", "google", "aws_bedrock"],
                latency_target_ms=150
            ),
            DataRegion.UK: cls(
                region=DataRegion.UK,
                allowed_providers=["openai", "anthropic"],
                latency_target_ms=120
            ),
            DataRegion.APAC: cls(
                region=DataRegion.APAC,
                allowed_providers=["openai", "google", "anthropic"],
                latency_target_ms=200
            ),
            DataRegion.LOCAL: cls(
                region=DataRegion.LOCAL,
                allowed_providers=["ollama", "llama.cpp"],
                latency_target_ms=10
            ),
        }
        return configs.get(region, configs[DataRegion.US])


# Quick policy check
def check_data_policy(data: str, policy: DataPolicy) -> dict:
    """Check if data complies with policy."""
    controller = DataController(policy)
    
    # Check for PII
    has_pii = bool(controller.anonymize(data) != data)
    
    # Check storage
    can_store = controller.should_store(
        data, 
        DataClassification.RESTRICTED if has_pii else DataClassification.INTERNAL
    )
    
    return {
        "compliant": can_store,
        "has_pii": has_pii,
        "should_anonymize": has_pii,
        "retention_allowed": policy.retention.value,
    }


if __name__ == "__main__":
    # Example: check data policy
    data = "Contact john@example.com at 555-123-4567"
    result = check_data_policy(data, DataPolicy())
    print(f"Data: {data[:30]}...")
    print(f"Compliant: {result['compliant']}")
    print(f"Has PII: {result['has_pii']}")