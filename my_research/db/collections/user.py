from typing import Optional
from xml.dom.minidom import Document
import pymongo

from my_research.db.collections.base import BaseCollection, BaseFields


class UserFields(BaseFields):
    fullname = "fullname"
    roles = "roles"
    tokens = "tokens"
    mail = "mail"

class UserCollection(BaseCollection):
    COLLECTION_NAME = "user"
    
    async def ensure_indexes(self):
        await super().ensure_indexes()
        self.pymongo_collection.create_index(
            [(UserFields.int_id, pymongo.ASCENDING), (UserFields.mail, pymongo.ASCENDING)],
            unique=True, sparse=True
        )

    async def find_document_by_mail(
            self, mail: str
    ) -> Optional[Document]:
        return await self.find_document({UserFields.mail: mail})