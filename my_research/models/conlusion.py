from pydantic import Field
from typing import Optional
from my_research.db.collections.conlusion import ConlusionFields
from my_research.models.base import BaseDBM

class Conlusion(BaseDBM):
    # db fields
    research_id: Optional[int] = Field(alias=ConlusionFields.research_id)
    name: Optional[str] = Field(alias=ConlusionFields.name)
    coord_text: Optional[str] = Field(alias=ConlusionFields.coord_text)
    desc: Optional[str] = Field(alias=ConlusionFields.desc)
    diagnosis: Optional[str] = Field(alias=ConlusionFields.diagnosis)