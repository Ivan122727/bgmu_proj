import pymongo

from my_research.db.collections.base import BaseCollection, BaseFields


class ConlusionFields(BaseFields):
    research_id = "research_id"
    name = "name"
    coord_data = "coord_data"
    desc = "desc"
    diagnosis = "diagnosis"


class ConlusionCollection(BaseCollection):
    COLLECTION_NAME = "conlusion"

    async def ensure_indexes(self):
        await super().ensure_indexes()
        self.pymongo_collection.create_index(
            [(ConlusionFields.int_id, pymongo.ASCENDING)],
            unique=True, sparse=True
        )
