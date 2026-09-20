from datetime import date
from typing import Any, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field


class ContractExtractionSchema(BaseModel):
    role: Optional[str] = Field(
        None,
        description="Job title or position ('Functia', 'Postul', 'Functie')",
    )
    department: Optional[str] = Field(
        None,
        description="Department or division ('Departament')",
    )
    start_date: Optional[date] = Field(
        None,
        description="Contract start date or effective date ('Data inceperii', 'Data intrarii in vigoare') in YYYY-MM-DD",
    )
    manager_id: Optional[str] = Field(
        None,
        description="Direct supervisor or manager ID if specified",
    )
    employment_type: Optional[str] = Field(
        "full_time",
        description="full_time, part_time, contractor, intern ('norma intreaga', 'timp partial')",
    )
    work_location: Optional[str] = Field(
        "onsite",
        description="remote, hybrid, or onsite ('telemunca', 'hibrid', 'la sediu')",
    )
    location: Optional[str] = Field(
        "Romania",
        description="Office location or country",
    )


class NationalIDExtractionSchema(BaseModel):
    first_name: Optional[str] = Field(
        None,
        description="First name / Given name ('Prenume')",
    )
    last_name: Optional[str] = Field(
        None,
        description="Last name / Family name / Surname ('Nume')",
    )
    national_id: Optional[str] = Field(
        None,
        description="National ID number, CNP, or card number ('CNP', 'Seria/Nr')",
    )


class HardwareDeliveryExtractionSchema(BaseModel):
    shipping_address: Optional[str] = Field(
        None,
        description="Full delivery / courier address ('Adresa de livrare', 'Strada', 'Oras')",
    )
    contact_phone: Optional[str] = Field(
        None,
        description="Contact telephone number for courier delivery ('Telefon')",
    )


class MedicalClearanceExtractionSchema(BaseModel):
    medical_clearance_status: bool = Field(
        False,
        description="True if cleared / fit for work ('APT', 'APT PENTRU MUNCA'); False if unfit ('INAPT') or absent",
    )
    issue_date: Optional[date] = Field(
        None,
        description="Date of medical examination or certificate issue date ('Data examinarii', 'Data emiterii') in YYYY-MM-DD",
    )
    
class DocumentType(str, Enum):
    CONTRACT = "contract"
    NATIONAL_ID = "national_id"
    HARDWARE_DELIVERY = "hardware_delivery"
    MEDICAL_CLEARANCE = "medical_clearance"

DOCUMENT_SCHEMA_MAP = {
    DocumentType.CONTRACT: ContractExtractionSchema,
    DocumentType.NATIONAL_ID: NationalIDExtractionSchema,
    DocumentType.HARDWARE_DELIVERY: HardwareDeliveryExtractionSchema,
    DocumentType.MEDICAL_CLEARANCE: MedicalClearanceExtractionSchema,
}

class ExtractionResponse(BaseModel):
    status: str = "success"
    document_type: DocumentType
    filename: str
    confidence_flags: list[str] = Field(
        default_factory=list,
        description="Non-blocking warnings (e.g., blurry image, missing non-critical field, OCR mismatch)",
    )
    data: Union[
        ContractExtractionSchema,
        NationalIDExtractionSchema,
        HardwareDeliveryExtractionSchema,
        MedicalClearanceExtractionSchema,
    ]