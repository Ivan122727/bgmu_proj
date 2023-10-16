from my_research.api.v1.schemas.base import BaseOutDBMSchema, BaseSchemaIn


class ResearchOut(BaseOutDBMSchema):
    patient_id: int
    type: str
    filename: str
    user_id: int


class SensitiveResearchOut(ResearchOut):
    ...