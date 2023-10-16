from typing import Optional
from xml.dom.minidom import Document
import pymongo

from my_research.db.collections.base import BaseCollection, BaseFields


class PatientFields(BaseFields):
    patient_id = "patient_id"
    fullname = "fullname"
    date_birth = "date_birth"
    insurance_policy_number = "insurance_policy_number"


class PatientCollection(BaseCollection):
    COLLECTION_NAME = "patient"

    async def ensure_indexes(self):
        await super().ensure_indexes()
        self.pymongo_collection.create_index(
            [(PatientFields.int_id, pymongo.ASCENDING)],
            unique=True, sparse=True
        )

    async def find_document_by_insurance_policy_number(
            self, insurance_policy_number: str
    ) -> Optional[Document]:
        return await self.find_document({PatientFields.insurance_policy_number: insurance_policy_number})