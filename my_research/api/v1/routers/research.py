from pathlib import Path
from typing import Optional
from uuid import uuid4
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, Request, UploadFile

from my_research.api.v1.schemas.research import SensitiveResearchOut
from my_research.core.enumerations import UserRoles
from my_research.core.settings import STATIC_DIRPATH
from my_research.deps.user_deps import get_strict_current_user, make_strict_depends_on_roles
from my_research.models.user import User
from my_research.services.patient import get_patient
from my_research.services.research import create_research, get_patient_researches, get_research


router = APIRouter()

@router.post('/research.create', response_model=Optional[SensitiveResearchOut], tags=['Research'])
async def reg_research(
    request: Request,
    user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.employee, UserRoles.dev])),
    patient_id: int = Form(...),
    result: str = Form(...),
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
        patient_id=patient.int_id, result=result, type=type,
        filename=filename, user_id=user.int_id
    )
    return SensitiveResearchOut.parse_dbm_kwargs(
        **research.dict()
    )


@router.get('/research.all', response_model=list[SensitiveResearchOut], tags=['Research'])
async def get_all_research(
    user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.employee, UserRoles.dev])),
    patient_id: int = Query(...)
    ):
    patient = await get_patient(id_=patient_id)
    if patient is None:
        raise HTTPException(status_code=400, detail="patient is none")
    return [SensitiveResearchOut.parse_dbm_kwargs(**research.dict()) for research in await get_patient_researches(patient_id=patient_id)]


@router.get('/research.by_id', response_model=Optional[SensitiveResearchOut], tags=['Research'])
async def get_research_by_int_id(
    user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.employee, UserRoles.dev])), 
    research_id: int = Query(...)
    ):
    research = await get_research(id_=research_id)
    if research is None:
        raise HTTPException(status_code=400, detail="research is none")
    return SensitiveResearchOut.parse_dbm_kwargs(**research.dict())