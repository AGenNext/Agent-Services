"""
AI ROI Measurement Module

Track and measure return on investment for AI implementations.
"""

from dataclasses import dataclass, field
from typing import Optional, list
from enum import Enum
from datetime import datetime, timedelta
import json


class MetricType(Enum):
    """Types of ROI metrics."""
    COST_SAVINGS = "cost_savings"
    REVENUE = "revenue"
    TIME_SAVINGS = "time_savings"
    PRODUCTIVITY = "productivity"
    CUSTOMER_SATISFACTION = "customer_satisfaction"
    ERROR_REDUCTION = "error_reduction"
    THROUGHPUT = "throughput"


class Timeframe(Enum):
    """Measurement timeframes."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


@dataclass
class ROIMetric:
    """A single ROI metric."""
    metric_type: MetricType
    baseline_value: float      # Before AI
    current_value: float       # After AI
    timestamp: datetime
    
    @property
    def change(self) -> float:
        """Calculate percentage change."""
        if self.baseline_value == 0:
            return 0
        return ((self.current_value - self.baseline_value) / self.baseline_value) * 100
    
    @property
    def absolute_change(self) -> float:
        """Calculate absolute change."""
        return self.current_value - self.baseline_value
    
    @property
    def is_improvement(self) -> bool:
        """Check if metric improved."""
        if self.metric_type in [MetricType.COST_SAVINGS, MetricType.TIME_SAVINGS, MetricType.ERROR_REDUCTION]:
            return self.change < 0
        return self.change > 0


@dataclass
class CostFactor:
    """Cost factor for ROI calculation."""
    name: str
    monthly_cost: float       # Monthly cost in USD
    usage_months: int = 12   # Months of usage
    category: str = "api"    # api, infrastructure, labor, etc.
    
    @property
    def annual_cost(self) -> float:
        return self.monthly_cost * self.usage_months


@dataclass
class Benefit:
    """Benefit for ROI calculation."""
    name: str
    monthly_value: float      # Monthly savings/revenue
    usage_months: int = 12
    category: str = "labor"     # labor, revenue, efficiency, etc.
    
    @property
    def annual_value(self) -> float:
        return self.monthly_value * self.usage_months


@dataclass
class ROIResult:
    """ROI calculation result."""
    total_costs: float
    total_benefits: float
    roi_percentage: float
    payback_period_months: float
    npv: float             # Net Present Value
   annual_benefit: float


class ROICalculator:
    """Calculate ROI for AI implementations."""
    
    def __init__(
        self,
        costs: list[CostFactor],
        benefits: list[Benefit],
        discount_rate: float = 0.10
    ):
        self.costs = costs
        self.benefits = benefits
        self.discount_rate = discount_rate
        self._metrics: list[ROIMetric] = []
    
    def calculate(self) -> ROIResult:
        """Calculate ROI metrics."""
        total_costs = sum(c.annual_cost for c in self.costs)
        total_benefits = sum(b.annual_value for b in self.benefits)
        
        roi_percentage = ((total_benefits - total_costs) / total_costs * 100) if total_costs > 0 else 0
        
        # Payback period
        monthly_net = sum(b.monthly_value for b in self.benefits) - sum(c.monthly_cost for c in self.costs)
        payback_months = total_costs / monthly_net if monthly_net > 0 else float('inf')
        
        # NPV (5 year projection)
        npv = self._calculate_npv(5)
        
        return ROIResult(
            total_costs=total_costs,
            total_benefits=total_benefits,
            roi_percentage=roi_percentage,
            payback_period_months=payback_months,
            npv=npv,
            annual_benefit=total_benefits - total_costs
        )
    
    def _calculate_npv(self, years: int) -> float:
        """Calculate Net Present Value."""
        npv = 0
        monthly_net = sum(b.monthly_value for b in self.benefits) - sum(c.monthly_cost for c in self.costs)
        
        for year in range(1, years + 1):
            cash_flow = monthly_net * 12
            npv += cash_flow / ((1 + self.discount_rate) ** year)
        
        return npv
    
    def record_metrics(self, metrics: list[ROIMetric]):
        """Record actual metrics."""
        self._metrics.extend(metrics)
    
    def get_metrics_summary(self) -> list[dict]:
        """Get metrics summary."""
        return [
            {
                "type": m.metric_type.value,
                "baseline": m.baseline_value,
                "current": m.current_value,
                "change_pct": round(m.change, 2),
                "improvement": m.is_improvement,
            }
            for m in self._metrics
        ]


# Standard ROI templates for AI use cases
ROI_TEMPLATES = {
    "chatbot": {
        "costs": [
            {"name": "API costs", "monthly": 500, "category": "api"},
            {"name": "Implementation", "monthly": 200, "category": "labor", "usage_months": 1},
            {"name": "Maintenance", "monthly": 100, "category": "labor"},
        ],
        "benefits": [
            {"name": "Support savings", "monthly": 2000, "category": "labor"},
            {"name": "Faster resolution", "monthly": 500, "category": "efficiency"},
        ]
    },
    "content_generation": {
        "costs": [
            {"name": "API costs", "monthly": 300, "category": "api"},
            {"name": "Tool subscription", "monthly": 100, "category": "software"},
        ],
        "benefits": [
            {"name": "Content production", "monthly": 1500, "category": "labor"},
            {"name": "Faster time to market", "monthly": 500, "category": "revenue"},
        ]
    },
    "rag": {
        "costs": [
            {"name": "Vector DB", "monthly": 200, "category": "infrastructure"},
            {"name": "API costs", "monthly": 400, "category": "api"},
            {"name": "Implementation", "monthly": 500, "category": "labor", "usage_months": 1},
        ],
        "benefits": [
            {"name": "Search time savings", "monthly": 800, "category": "efficiency"},
            {"name": "Reduced errors", "monthly": 300, "category": "efficiency"},
            {"name": "Better decisions", "monthly": 400, "category": "revenue"},
        ]
    },
    "code_assistant": {
        "costs": [
            {"name": "Tool license", "monthly": 200, "category": "software"},
            {"name": "API costs", "monthly": 100, "category": "api"},
        ],
        "benefits": [
            {"name": "Productivity gain", "monthly": 1500, "category": "efficiency"},
            {"name": "Faster development", "monthly": 1000, "category": "labor"},
        ]
    },
}


class ROITracker:
    """Track ROI over time."""
    
    def __init__(self, use_case: str):
        self.use_case = use_case
        self._snapshots: list[dict] = []
        self._start_date = datetime.now()
    
    def add_snapshot(self, metrics: dict):
        """Add a metrics snapshot."""
        self._snapshots.append({
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics
        })
    
    def get_trend(self) -> str:
        """Get ROI trend."""
        if len(self._snapshots) < 2:
            return "insufficient_data"
        
        first = self._snapshots[0]["metrics"].get("roi", 0)
        last = self._snapshots[-1]["metrics"].get("roi", 0)
        
        if last > first + 10:
            return "improving"
        elif last < first - 10:
            return "declining"
        return "stable"
    
    def get_summary(self) -> dict:
        """Get ROI summary."""
        if not self._snapshots:
            return {"status": "no_data"}
        
        return {
            "use_case": self.use_case,
            "start_date": self._start_date.isoformat(),
            "snapshots": len(self._snapshots),
            "trend": self.get_trend(),
            "latest_roi": self._snapshots[-1]["metrics"].get("roi", 0),
        }


# Quick ROI calculation
def calculate_roi(use_case: str, scale_factor: float = 1.0) -> dict:
    """Quick ROI calculation for a use case."""
    template = ROI_TEMPLATES.get(use_case)
    
    if not template:
        return {"error": f"Unknown use case: {use_case}"}
    
    # Scale costs and benefits
    costs = [
        CostFactor(
            name=c["name"],
            monthly_cost=c["monthly"] * scale_factor,
            usage_months=c.get("usage_months", 12),
            category=c.get("category", "api")
        )
        for c in template["costs"]
    ]
    
    benefits = [
        Benefit(
            name=b["name"],
            monthly_value=b["monthly"] * scale_factor,
            usage_months=b.get("usage_months", 12),
            category=b.get("category", "labor")
        )
        for b in template["benefits"]
    ]
    
    calculator = ROICalculator(costs, benefits)
    result = calculator.calculate()
    
    return {
        "use_case": use_case,
        "annual_costs": result.total_costs,
        "annual_benefits": result.total_benefits,
        "roi_percentage": round(result.roi_percentage, 2),
        "payback_months": round(result.payback_period_months, 1),
        "5_year_npv": round(result.npv, 2),
    }


# Example usage
if __name__ == "__main__":
    # Calculate ROI for chatbot
    result = calculate_roi("chatbot")
    print(f"ROI for {result['use_case']}:")
    print(f"  Annual Costs: ${result['annual_costs']:,.0f}")
    print(f"  Annual Benefits: ${result['annual_benefits']:,.0f}")
    print(f"  ROI: {result['roi_percentage']}%")
    print(f"  Payback: {result['payback_months']} months")