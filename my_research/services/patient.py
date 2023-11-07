from typing import Optional
from my_research.db.collections.base import Id
from my_research.db.collections.conlusion import ConlusionFields

from my_research.db.collections.patient import PatientFields
from my_research.db.collections.research import ResearchFields
from my_research.models.patient import Patient
from my_research.core.consts import db
from my_research.services.conlusion import get_research_conclusions
from my_research.services.research import get_patient_researches

async def create_patient(
        *,
        fullname: Optional[str] = None,
        date_birth: Optional[str] = None,
        insurance_policy_number: Optional[str] = None,
        additional_params: list[dict] = None
        
):
    doc_to_insert = {
        PatientFields.fullname: fullname,
        PatientFields.date_birth: date_birth,
        PatientFields.insurance_policy_number: insurance_policy_number,
        PatientFields.additional_params: additional_params
    }
    inserted_doc = await db.patient_collection.insert_document(doc_to_insert)
    created_patient = Patient.parse_document(inserted_doc)
    return created_patient

async def get_patient(
        *,
        id_: Optional[Id] = None,
        int_id: Optional[int] = None,
        insurance_policy_number: Optional[str] = None
) -> Optional[Patient]:
    filter_ = {}
    if id_ is not None:
        filter_.update(db.patient_collection.create_id_filter(id_=id_))
    if int_id is not None:
        filter_[PatientFields.int_id] = int_id
    if insurance_policy_number is not None:
        filter_[PatientFields.insurance_policy_number] = insurance_policy_number

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


def check_patients(array1: list[str], array2: list[str])->bool:
    for word in array1:
        if word in array2:
            return True
    return False