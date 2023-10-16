from pydantic import Field
from typing import Optional

from bson import ObjectId
from my_research.db.collections.mailcode import MailCodeFields
from my_research.models.base import BaseDBM
from my_research.models.user import User


class MailCode(BaseDBM):
    # db fields
    to_mail: str = Field(alias=MailCodeFields.to_mail)
    code: str = Field(alias=MailCodeFields.code)
    type: str = Field(alias=MailCodeFields.type)
    to_user_oid: Optional[ObjectId] = Field(alias=MailCodeFields.to_user_oid)
    to_user: Optional[User] = Field(default=None)
