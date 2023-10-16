from typing import Optional
from my_research.api.v1.schemas.base import BaseOutDBMSchema, BaseSchemaOut


class UserOut(BaseOutDBMSchema):
    roles: list[str] = []
    mail: Optional[str]
    fullname: Optional[str]


class SensitiveUserOut(UserOut):
    current_token: str


class UserExistsStatusOut(BaseSchemaOut):
    is_exists: bool