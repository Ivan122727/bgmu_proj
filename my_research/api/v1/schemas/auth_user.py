from my_research.api.v1.schemas.base import BaseSchemaIn


class AuthUserIn(BaseSchemaIn):
    mail: str
    code: str