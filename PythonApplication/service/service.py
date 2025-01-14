from model.AgreementResponseEnvelopeDto import AgreementResponseEnvelopeDto
from model.SLAResponseDto import SLAResponseDto

class Service:
    def processDocuments():
        sla_1 = SLAResponseDto('SLA 1')

        response = AgreementResponseEnvelopeDto()
        response.sla_responses.append(sla_1)

        return response
