from typing import Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from my_research.api.v1.schemas.base import OperationStatusOut
from my_research.api.v1.schemas.patient import EditPatientIn, PatientOut, RegPatientIn, SensitivePatientOut
from my_research.core.enumerations import UserRoles
from my_research.db.collections.conlusion import ConlusionFields
from my_research.db.collections.patient import PatientFields
from my_research.db.collections.research import ResearchFields
from my_research.deps.user_deps import get_strict_current_user, make_strict_depends_on_roles
from my_research.models.patient import Patient
from my_research.models.research import Research

from my_research.models.user import User
from my_research.services.patient import check_patients, create_patient, get_patient, get_patients, search_patients
from my_research.core.consts import db
from my_research.services.research import get_patient_researches

router = APIRouter()


@router.post('/patient.create', response_model=Optional[SensitivePatientOut], tags=['Patient'])
async def reg_patient(
        user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.employee, UserRoles.dev])),
        reg_patient_in: RegPatientIn = Body(...)
):
    patient = await get_patient(insurance_policy_number=reg_patient_in.insurance_policy_number)
    if patient is not None:
        raise HTTPException(status_code=400, detail="patient is exist")
        
    patient_created = await create_patient(
        fullname=reg_patient_in.fullname, date_birth=reg_patient_in.date_birth, 
        insurance_policy_number=reg_patient_in.insurance_policy_number,
        additional_params=reg_patient_in.additional_params
    )

    return SensitivePatientOut.parse_dbm_kwargs(
        **patient_created.dict()
    )


@router.put('/patient.edit', response_model=Optional[SensitivePatientOut], tags=['Patient'])
async def get_patient_by_id(
        user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.employee, UserRoles.dev])),
        edit_patient_in: EditPatientIn = Body(...)
):
    patient = await get_patient(id_=edit_patient_in.patient_id)
    if patient is None:
        raise HTTPException(status_code=400, detail="patient is None")

    patient_by_policy_number = await get_patient(insurance_policy_number=edit_patient_in.insurance_policy_number)
    if patient_by_policy_number is not None and patient_by_policy_number.int_id != patient.int_id:
        raise HTTPException(status_code=400, detail="patient by policy number is exist")
    
    await db.patient_collection.update_document_by_id(id_=edit_patient_in.patient_id, set_={
        PatientFields.fullname: edit_patient_in.fullname,
        PatientFields.date_birth: edit_patient_in.date_birth,
        PatientFields.insurance_policy_number: edit_patient_in.insurance_policy_number,
        PatientFields.additional_params: edit_patient_in.additional_params,
    })
    updated_patient = await get_patient(id_=edit_patient_in.patient_id)
    return PatientOut.parse_dbm_kwargs(**updated_patient.dict())
    


@router.get('/patient.all', response_model=list[PatientOut], tags=['Patient'])
async def get_all_patients(
    user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.employee, UserRoles.dev, UserRoles.user])),
    st: Optional[int] = Query(default=0), count: Optional[int] = Query(default=10)
    ):

    count_docs = await db.patient_collection.count_documents()
    if st + 1 > count_docs:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="wrong pagination params")

    if st + count + 1 > count_docs or st < 0:
        count = count_docs - st

    return [PatientOut.parse_dbm_kwargs(**patient.dict()) for patient in await get_patients()][st: st + count: 1]


@router.get('/patient.by_id', response_model=Optional[SensitivePatientOut], tags=['Patient'])
async def get_patient_by_id(
        user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.employee, UserRoles.dev, UserRoles.user])),
        patient_id: int = Query(...)
):
    patient = await get_patient(id_=patient_id)
    if patient is None:
        raise HTTPException(status_code=400, detail="patient is None")

    return PatientOut.parse_dbm_kwargs(**patient.dict())

@router.delete('/patient.delete', response_model=OperationStatusOut, tags=['Patient'])
async def delete_patient(
        user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.employee, UserRoles.dev])),
        patient_id: int = Query(...)
):
    patient = await get_patient(id_=patient_id)
    if patient is None:
        raise HTTPException(status_code=400, detail="patient is None")
    
    researches: list[Research] = await get_patient_researches(patient_id=patient_id)
    for research in researches:
        await db.research_collection.remove_by_int_id(int_id=research.int_id)
        await db.conlusion_collection.remove_documents({ConlusionFields.research_id: research.int_id})
    await db.patient_collection.remove_by_int_id(int_id=patient_id)

    return OperationStatusOut(is_done=True)
    
    
@router.get('/patient.search_by_fio', response_model=list[PatientOut], tags=['Patient'])
async def search_patient(
    q: Optional[str] = Query(default=None),
    user: User = Depends(get_strict_current_user)
):
    return [PatientOut.parse_dbm_kwargs(**patient.dict()) for patient in (await search_patients(insurance_policy_number=q))]