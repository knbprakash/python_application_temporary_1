from dataclasses import dataclass, field

from model.SLAResponseDto import SLAResponseDto

@dataclass
class AgreementResponseEnvelopeDto:
    sla_responses: list[SLAResponseDto] = field(default_factory=list)
