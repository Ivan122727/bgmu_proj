from my_research.api.v1.schemas.base import BaseSchemaIn


class RegUserIn(BaseSchemaIn):
    mail: str
    fullname: str
    code: str