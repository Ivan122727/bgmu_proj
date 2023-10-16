from pydantic import Field
from typing import Optional
from my_research.core.enumerations import UserRoles
from my_research.db.collections.user import UserFields
from my_research.models.base import BaseDBM
from my_research.utils.role_utils import roles_to_list

class User(BaseDBM):
    # db fields
    fullname: Optional[str] = Field(alias=UserFields.fullname)
    roles: list[str] = Field(alias=UserFields.roles, default=[])
    tokens: list[str] = Field(alias=UserFields.tokens, default=[])
    mail: Optional[str] = Field(alias=UserFields.mail)

    def compare_roles(self, needed_roles: UserRoles) -> bool:
        needed_roles = roles_to_list(needed_roles)
        return bool(set(needed_roles) & set(self.roles))