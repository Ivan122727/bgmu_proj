from pydantic import Field
from typing import Optional
from my_research.db.collections.research import ResearchFields
from my_research.models.base import BaseDBM
from my_research.models.conlusion import Conlusion

class ResearchWithConlusions(BaseDBM):
    # db fields
    patient_id: Optional[int] = Field(alias=ResearchFields.patient_id)
    type: Optional[str] = Field(alias=ResearchFields.type)
    filename: Optional[str] = Field(alias=ResearchFields.filename)
    user_id: Optional[int] = Field(alias=ResearchFields.user_id)
    conlusions: Optional[list[Conlusion]] = Field(alias="conlusions", default=[])