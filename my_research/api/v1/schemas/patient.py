from my_research.api.v1.schemas.base import BaseOutDBMSchema, BaseSchemaIn


class RegPatientIn(BaseSchemaIn):
    fullname: str
    date_birth: str
    insurance_policy_number: str


class EditPatientIn(BaseSchemaIn):
    patient_id: int
    fullname: str
    date_birth: str
    insurance_policy_number: str

class PatientOut(BaseOutDBMSchema):
    fullname: str
    date_birth: str
    insurance_policy_number: str


class SensitivePatientOut(PatientOut):
    ...