from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import uuid4
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, Request, UploadFile
from my_research.api.v1.schemas.base import OperationStatusOut

from my_research.api.v1.schemas.research import ResearchOut, SensitiveResearchOut
from my_research.core.enumerations import UserRoles
from my_research.core.settings import STATIC_DIRPATH
from my_research.db.collections.conlusion import ConlusionFields
from my_research.db.collections.research import ResearchFields
from my_research.deps.user_deps import make_strict_depends_on_roles
from my_research.models.user import User
from my_research.services.patient import get_patient
from my_research.services.research import create_research, get_patient_researches, get_research, researches_by_date
from my_research.core.consts import db, settings
from my_research.utils.helpers import create_zip_archive

router = APIRouter()

@router.post('/research.create', response_model=Optional[SensitiveResearchOut], tags=['Research'])
async def reg_research(
    request: Request,
    user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.employee, UserRoles.dev])),
    patient_id: int = Form(...),
    type: str = Form(...),
    uploaded_res: Optional[UploadFile] = File(None),
):
    patient = await get_patient(id_=patient_id)
    if patient is None:
        raise HTTPException(status_code=400, detail="patient is none")
    filename = None
    if uploaded_res is not None:
        filename: str = str(uuid4())
        type_: str = uploaded_res.filename.split('.')[-1].strip()
        if type_:
            filename += '.' + type_

        path = Path(STATIC_DIRPATH).joinpath(filename)
        with open(path, mode='wb') as f:
            f.write(await uploaded_res.read())
    research = await create_research(
        patient_id=patient.int_id, type=type,
        filename=filename, user_id=user.int_id
    )
    return SensitiveResearchOut.parse_dbm_kwargs(
        **research.dict()
    )



@router.put('/research.edit', response_model=Optional[SensitiveResearchOut], tags=['Research'])
async def edit_research(
    request: Request,
    user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.employee, UserRoles.dev])),
    research_id: int = Form(...),
    type: str = Form(...),
    uploaded_res: Optional[UploadFile] = File(None),
):
    filename = None
    if uploaded_res is not None:
        filename: str = str(uuid4())
        type_: str = uploaded_res.filename.split('.')[-1].strip()
        if type_:
            filename += '.' + type_

        path = Path(STATIC_DIRPATH).joinpath(filename)
        with open(path, mode='wb') as f:
            f.write(await uploaded_res.read())
    
    await db.research_collection.update_document_by_id(id_=research_id, set_={
        ResearchFields.type: type,
        ResearchFields.filename: filename
    })
    await db.conlusion_collection.remove_documents({ConlusionFields.research_id: research_id})
    updated_research = await get_research(id_=research_id)
    return ResearchOut.parse_dbm_kwargs(**updated_research.dict())
    

@router.get('/research.all', response_model=list[SensitiveResearchOut], tags=['Research'])
async def get_all_research(
    user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.employee, UserRoles.dev, UserRoles.user])),
    patient_id: int = Query(...), st: Optional[int] = Query(default=0), 
    count: Optional[int] = Query(default=10)
    ):
    patient = await get_patient(id_=patient_id)
    if patient is None:
        raise HTTPException(status_code=400, detail="patient is none")
        
    count_docs = await db.research_collection.count_documents()
    if st + 1 > count_docs or st < 0:
        raise HTTPException(status_code=400, detail="wrong pagination params")

    if st + count + 1 > count_docs:
        count = count_docs - st

    return [SensitiveResearchOut.parse_dbm_kwargs(**research.dict()) for research in await get_patient_researches(patient_id=patient_id)][st: st + count: 1]


@router.get('/research.by_id', response_model=Optional[SensitiveResearchOut], tags=['Research'])
async def delete_research(
    user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.employee, UserRoles.dev, UserRoles.user])), 
    research_id: int = Query(...)
    ):
    research = await get_research(id_=research_id)
    if research is None:
        raise HTTPException(status_code=400, detail="research is none")
    return SensitiveResearchOut.parse_dbm_kwargs(**research.dict())

@router.delete('/research.delete', response_model=OperationStatusOut, tags=['Research'])
async def delete_research(
    user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.employee, UserRoles.dev])), 
    research_id: int = Query(...)
    ):
    research = await get_research(id_=research_id)
    if research is None:
        raise HTTPException(status_code=400, detail="research is none")
    
    await db.research_collection.remove_by_int_id(int_id=research_id)
    await db.conlusion_collection.remove_documents({ConlusionFields.research_id: research_id})
    return OperationStatusOut(is_done=True)




@router.get('/research.get_sample', tags=['Research'])
async def get_sample(
    from_dt: str = Query(...),
    to_dt: str = Query(...)
):
    researches = await researches_by_date(from_dt=from_dt, to_dt=to_dt)
    file_paths = list()
    for research in researches:
        file_paths.append(f"{STATIC_DIRPATH}/{research.filename}")
    zip_file_path = str(uuid4())
    create_zip_archive(file_paths=file_paths, zip_file_path=f"{STATIC_DIRPATH}/{zip_file_path}")
    return {
            "url_imgs": f"{settings.api_url}/static/{zip_file_path}", 
            "count_researches": len(researches),
            "researches": researches
    }