from dataclasses import dataclass
from AssociatedMetrics import AssociatedMetrics
from typing import Optional

@dataclass
class SLAResponseDto:
    name: str
    invlolved_parties: str
    concerned_system: str
    description: str
    associated_metrics: Optional[AssociatedMetrics] = None

