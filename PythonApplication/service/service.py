from model.AgreementResponseEnvelopeDto import AgreementResponseEnvelopeDto
from model.SLAResponseDto import SLAResponseDto
from werkzeug.datastructures import FileStorage

class SLAService:
    def processDocuments(file: FileStorage):
        sla_1 = SLAResponseDto('SLA 1')

        response = AgreementResponseEnvelopeDto()
        response.sla_responses.append(sla_1)

        return response
