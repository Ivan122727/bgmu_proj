from typing import Optional
from fastapi import APIRouter, Body, Depends, HTTPException
from my_research.api.v1.schemas.patient import PatientOut, RegPatientIn, SensitivePatientOut
from my_research.core.enumerations import UserRoles
from my_research.deps.user_deps import make_strict_depends_on_roles

from my_research.models.user import User
from my_research.services.patient import create_patient, get_patient, get_patients
from my_research.core.consts import db

router = APIRouter()


@router.post('/patient.create', response_model=Optional[SensitivePatientOut], tags=['Patient'])
async def reg_patient(
        user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.employee, UserRoles.dev])),
        reg_patient_in: RegPatientIn = Body(...)
):
    patient = await db.patient_collection.find_document_by_insurance_policy_number(insurance_policy_number=reg_patient_in.insurance_policy_number)
    
    if patient is not None:
        raise HTTPException(status_code=400, detail="patient is exist")
        
    patient_created = await create_patient(fullname=reg_patient_in.fullname, date_birth=reg_patient_in.date_birth, insurance_policy_number=reg_patient_in.insurance_policy_number)

    return SensitivePatientOut.parse_dbm_kwargs(
        **patient_created.dict()
    )



@router.get('/patient.all', response_model=list[PatientOut], tags=['Patient'])
async def get_all_patients(user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.employee, UserRoles.dev]))):
    return [PatientOut.parse_dbm_kwargs(**patient.dict()) for patient in await get_patients()]


@router.get('/patient.by_id', response_model=Optional[PatientOut], tags=['Patient'])
async def get_patient_by_int_id(int_id: int):
    patient = await get_patient(id_=int_id)
    if patient is None:
        raise HTTPException(status_code=400, detail="patient is none")
    return PatientOut.parse_dbm_kwargs(**patient.dict())