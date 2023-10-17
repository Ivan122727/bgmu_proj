from pathlib import Path
from typing import Optional
from uuid import uuid4
from fastapi import APIRouter, Body, Depends, File, Form, HTTPException, Query, Request, UploadFile
from my_research.api.v1.schemas.base import OperationStatusOut
from my_research.api.v1.schemas.conlusion import ConlusionOut, EditConlusionIn, RegConlusionIn, SensitiveConlusionOut

from my_research.api.v1.schemas.research import SensitiveResearchOut
from my_research.core.enumerations import UserRoles
from my_research.core.settings import STATIC_DIRPATH
from my_research.db.collections.conlusion import ConlusionFields
from my_research.deps.user_deps import get_strict_current_user, make_strict_depends_on_roles
from my_research.models.user import User
from my_research.services.conlusion import create_conlusion, get_conlusion, get_research_conclusions
from my_research.services.patient import get_patient
from my_research.services.research import create_research, get_patient_researches, get_research
from my_research.core.consts import db

router = APIRouter()

@router.post('/conlusion.create', response_model=Optional[SensitiveConlusionOut], tags=['Research'])
async def reg_conlusion(
    user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.employee, UserRoles.dev])),
    reg_conlusion_in: RegConlusionIn = Body(...)
):
    research = await get_research(id_=reg_conlusion_in.research_id)
    if research is None:
        raise HTTPException(status_code=400, detail="research is None")

    created_conlusion = await create_conlusion(
        research_id=reg_conlusion_in.research_id, name=reg_conlusion_in.name, 
        desc=reg_conlusion_in.desc, diagnosis=reg_conlusion_in.diagnosis, 
        coord_text=reg_conlusion_in.coord_text
        )
    return SensitiveConlusionOut.parse_dbm_kwargs(
        **created_conlusion.dict()
    )


@router.post('/conlusion.edit', response_model=SensitiveConlusionOut, tags=['Research'])
async def edit_conlusion(
    user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.employee, UserRoles.dev])),
    edit_conlusion_in: EditConlusionIn = Body(...),
):
    conlusion = await get_conlusion(id_=edit_conlusion_in.conlusion_id)
    if conlusion is None:
        raise HTTPException(status_code=400, detail="conlusion is None") 

    await db.conlusion_collection.update_document_by_id(id_=edit_conlusion_in.conlusion_id, set_={
        ConlusionFields.name: edit_conlusion_in.name,
        ConlusionFields.coord_text: edit_conlusion_in.coord_text,
        ConlusionFields.desc: edit_conlusion_in.desc,
        ConlusionFields.diagnosis: edit_conlusion_in.diagnosis,
    })
    updated_conlusion = await get_conlusion(id_=edit_conlusion_in.conlusion_id)
    return ConlusionOut.parse_dbm_kwargs(**updated_conlusion.dict())


@router.get('/conlusion.all', response_model=list[SensitiveConlusionOut], tags=['Research'])
async def get_all_conlusions(
    user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.employee, UserRoles.dev])),
    research_id: int = Query(...)
    ):
    research = await get_research(id_=research_id)
    if research is None:
        raise HTTPException(status_code=400, detail="research is none")
    return [SensitiveConlusionOut.parse_dbm_kwargs(**conlusion.dict()) for conlusion in await get_research_conclusions(research_id=research_id)]


@router.get('/conlusion.by_id', response_model=Optional[SensitiveConlusionOut], tags=['Research'])
async def get_conlusion_by_id(
    user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.employee, UserRoles.dev])), 
    conlusion_id: int = Query(...)
    ):
    conlusion = await get_conlusion(id_=conlusion_id)
    if conlusion is None:
        raise HTTPException(status_code=400, detail="conlusion is none")
    return SensitiveConlusionOut.parse_dbm_kwargs(**conlusion.dict())


@router.get('/conlusion.delete', response_model=OperationStatusOut, tags=['Research'])
async def delete_conlusion(
    user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.employee, UserRoles.dev])), 
    conlusion_id: int = Query(...)
    ):
        conlusion = await get_conlusion(id_=conlusion_id)
        if conlusion is None:
            raise HTTPException(status_code=400, detail="conlusion is none")
             
        await db.conlusion_collection.remove_by_int_id(int_id=conlusion_id)
        return OperationStatusOut(is_done=True)