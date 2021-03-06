from pydantic import BaseModel


class SummaryPayloadSchema(BaseModel):
    url: str  # AnyUrl ?


class SummaryResponseSchema(SummaryPayloadSchema):
    id: int
