import pymongo

from my_research.db.collections.base import BaseCollection, BaseFields


class ResearchFields(BaseFields):
    patient_id = "patient_id"
    type = "type"
    filename = "filename"
    user_id = "user_id"


class ResearchCollection(BaseCollection):
    COLLECTION_NAME = "research"

    async def ensure_indexes(self):
        await super().ensure_indexes()
        self.pymongo_collection.create_index(
            [(ResearchFields.int_id, pymongo.ASCENDING)],
            unique=True, sparse=True
        )
