from pydantic import Field
from typing import Optional
from my_research.db.collections.patient import PatientFields
from my_research.models.base import BaseDBM

class Patient(BaseDBM):
    # db fields
    fullname: Optional[str] = Field(alias=PatientFields.fullname)
    date_birth: Optional[str] = Field(alias=PatientFields.date_birth)
    insurance_policy_number: Optional[str] = Field(alias=PatientFields.insurance_policy_number)
    additional_params: dict = Field(alias=PatientFields.additional_params, default={})