from datetime import date
from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    CONTRACT = "contract"
    NATIONAL_ID = "national_id"
    MEDICAL_CLEARANCE = "medical_clearance"


class ContractExtractionSchema(BaseModel):
    # Removing default=None forces Pydantic to add these to "required": [...]
    # while 'Optional' allows the model to output either a string or null.
    first_name: Optional[str] = Field(
        ...,
        description="Employee first name (e.g. 'Andreea')",
    )
    last_name: Optional[str] = Field(
        ...,
        description="Employee last name / surname (e.g. 'Dumitrescu')",
    )
    national_id: Optional[str] = Field(
        ...,
        description="13-digit CNP or National ID number",
    )
    role: Optional[str] = Field(
        ...,
        description="Job title / function stated in the contract",
    )
    department: Optional[str] = Field(
        ...,
        description="Corporate department name",
    )
    start_date: Optional[date] = Field(
        ...,
        description="Contract start or effective date (YYYY-MM-DD)",
    )
    manager_id: Optional[str] = Field(
        ...,
        description="Manager ID if stated, else null",
    )
    employment_type: Optional[str] = Field(
        ...,
        description="Employment type: 'full_time', 'part_time', or 'contractor'",
    )
    work_location: Optional[str] = Field(
        ...,
        description="Work arrangement: 'onsite', 'remote', or 'hybrid'",
    )
    location: Optional[str] = Field(
        ...,
        description="Office location or base city",
    )
    shipping_address: Optional[str] = Field(
        ...,
        description="Residential / delivery street address with city",
    )
    contact_phone: Optional[str] = Field(
        ...,
        description="Contact phone number",
    )


class NationalIDExtractionSchema(BaseModel):
    first_name: Optional[str] = Field(..., description="Given name(s)")
    last_name: Optional[str] = Field(..., description="Surname / family name")
    national_id: Optional[str] = Field(..., description="13-digit National ID / CNP")


class MedicalClearanceExtractionSchema(BaseModel):
    medical_clearance_status: bool = Field(
        ...,
        description="True if cleared / fit for work; False if unfit or unconfirmed",
    )
    issue_date: Optional[date] = Field(
        ...,
        description="Examination date (YYYY-MM-DD)",
    )


DOCUMENT_SCHEMA_MAP = {
    DocumentType.CONTRACT: ContractExtractionSchema,
    DocumentType.NATIONAL_ID: NationalIDExtractionSchema,
    DocumentType.MEDICAL_CLEARANCE: MedicalClearanceExtractionSchema,
}


class ExtractionResponse(BaseModel):
    status: str = "success"
    document_type: DocumentType
    filename: str
    confidence_flags: list[str] = Field(default_factory=list)
    data: Union[
        ContractExtractionSchema,
        NationalIDExtractionSchema,
        MedicalClearanceExtractionSchema,
    ]