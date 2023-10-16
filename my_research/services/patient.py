from typing import Optional
from my_research.db.collections.base import Id

from my_research.db.collections.patient import PatientFields
from my_research.models.patient import Patient
from my_research.core.consts import db

async def create_patient(
        *,
        fullname: Optional[str] = None,
        date_birth: Optional[str] = None,
        insurance_policy_number: Optional[str] = None,
):
    doc_to_insert = {
        PatientFields.fullname: fullname,
        PatientFields.date_birth: date_birth,
        PatientFields.insurance_policy_number: insurance_policy_number
    }
    inserted_doc = await db.patient_collection.insert_document(doc_to_insert)
    created_patient = Patient.parse_document(inserted_doc)
    return created_patient

async def get_patient(
        *,
        id_: Optional[Id] = None,
        int_id: Optional[int] = None,
) -> Optional[Patient]:
    filter_ = {}
    if id_ is not None:
        filter_.update(db.patient_collection.create_id_filter(id_=id_))
    if int_id is not None:
        filter_[PatientFields.int_id] = int_id

    if not filter_:
        raise ValueError("not filter_")

    doc = await db.patient_collection.find_document(filter_=filter_)
    if doc is None:
        return None
    return Patient.parse_document(doc)

async def get_patients(*, roles: Optional[list[str]] = None) -> list[Patient]:
    patients = [Patient.parse_document(doc) async for doc in db.patient_collection.create_cursor()]
    if roles is not None:
        patients = [patient for patient in patients if patients.compare_roles(roles)]
    return patients