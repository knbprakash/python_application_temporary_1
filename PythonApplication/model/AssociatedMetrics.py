from dataclasses import dataclass
from typing import Optional

@dataclass
class AssociatedMetrics:
    incident_response_time: Optional[int] = None
    incident_resolution_time: Optional[int] = None
    api_availability: Optional[int] = None
    patch_management: Optional[int] = None
    environment_recovery_initiation_time: Optional[int] = None
