from typing import Optional
from my_research.api.v1.schemas.base import BaseOutDBMSchema, BaseSchemaIn


class RegConlusionIn(BaseSchemaIn):
    research_id: Optional[int]
    name: Optional[str]
    coord_text: Optional[str]
    desc: Optional[str]
    diagnosis: Optional[str]

class ConlusionOut(BaseOutDBMSchema):
    research_id: Optional[int]
    name: Optional[str]
    coord_text: Optional[str]
    desc: Optional[str]
    diagnosis: Optional[str]
    
class SensitiveConlusionOut(ConlusionOut):
    ...