from typing import Optional
from my_research.api.v1.schemas.base import BaseOutDBMSchema, BaseSchemaIn


class RegConlusionIn(BaseSchemaIn):
    research_id: Optional[int]
    name: Optional[str]
    coord_data: Optional[dict]
    desc: Optional[str]
    diagnosis: Optional[str]

class EditConlusionIn(BaseSchemaIn):
    conlusion_id: int
    name: Optional[str]
    coord_data: Optional[dict]
    desc: Optional[str]
    diagnosis: Optional[str]

class ConlusionOut(BaseOutDBMSchema):
    research_id: Optional[int]
    name: Optional[str]
    coord_data: Optional[dict]
    desc: Optional[str]
    diagnosis: Optional[str]
    
class SensitiveConlusionOut(ConlusionOut):
    ...