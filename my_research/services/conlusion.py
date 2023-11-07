from typing import Optional
from my_research.db.collections.base import Id
from my_research.db.collections.conlusion import ConlusionFields

from my_research.core.consts import db
from my_research.models.conlusion import Conlusion

async def create_conlusion(
        *,
        research_id: Optional[int] = None,
        name: Optional[str] = None,
        coord_data: Optional[dict] = None,
        desc: Optional[str] = None,
        diagnosis: Optional[str] = None,
):

    doc_to_insert = {
        ConlusionFields.research_id: research_id,
        ConlusionFields.name: name,
        ConlusionFields.coord_data: coord_data,
        ConlusionFields.desc: desc,
        ConlusionFields.diagnosis: diagnosis
    }
    inserted_doc = await db.conlusion_collection.insert_document(doc_to_insert)
    created_research = Conlusion.parse_document(inserted_doc)
    return created_research

async def get_conlusion(
        *,
        id_: Optional[Id] = None,
        int_id: Optional[int] = None,
) -> Optional[Conlusion]:
    filter_ = {}
    if id_ is not None:
        filter_.update(db.conlusion_collection.create_id_filter(id_=id_))
    if int_id is not None:
        filter_[ConlusionFields.int_id] = int_id

    if not filter_:
        raise ValueError("not filter_")

    doc = await db.conlusion_collection.find_document(filter_=filter_)
    if doc is None:
        return None
    return Conlusion.parse_document(doc)

async def get_research_conclusions(*, roles: Optional[list[str]] = None, research_id: Optional[int]) -> list[Conlusion]:
    conlusions = [Conlusion.parse_document(doc) async for doc in db.conlusion_collection.create_cursor() if doc[ConlusionFields.research_id] == research_id]
    if roles is not None:
        conlusions = [conlusion for conlusion in conlusions if conlusion.compare_roles(roles)]
    return conlusions