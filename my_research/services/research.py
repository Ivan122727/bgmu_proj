from typing import Optional
from my_research.db.collections.base import Id

from my_research.db.collections.research import ResearchFields
from my_research.core.consts import db
from my_research.models.research import Research

async def create_research(
        *,
        patient_id: Optional[int] = None,
        type: Optional[str] = None,
        filename: Optional[str] = None,
        user_id: Optional[int] = None,
):
    doc_to_insert = {
        ResearchFields.patient_id: patient_id,
        ResearchFields.type: type,
        ResearchFields.filename: filename,
        ResearchFields.user_id: user_id
    }
    inserted_doc = await db.research_collection.insert_document(doc_to_insert)
    created_research = Research.parse_document(inserted_doc)
    return created_research

async def get_research(
        *,
        id_: Optional[Id] = None,
        int_id: Optional[int] = None,
) -> Optional[Research]:
    filter_ = {}
    if id_ is not None:
        filter_.update(db.research_collection.create_id_filter(id_=id_))
    if int_id is not None:
        filter_[ResearchFields.int_id] = int_id

    if not filter_:
        raise ValueError("not filter_")

    doc = await db.research_collection.find_document(filter_=filter_)
    if doc is None:
        return None
    return Research.parse_document(doc)

async def get_patient_researches(*, roles: Optional[list[str]] = None, patient_id: Optional[int]) -> list[Research]:
    researches = [Research.parse_document(doc) async for doc in db.research_collection.create_cursor() if doc[ResearchFields.patient_id] == patient_id]
    if roles is not None:
        researches = [research for research in researches if research.compare_roles(roles)]
    return researches