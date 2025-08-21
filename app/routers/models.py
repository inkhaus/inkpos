from datetime import datetime, date
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field

class AccountType(str, Enum):
    admin = "admin"
    sales = "sales"

class UserBase(BaseModel):
    email: EmailStr
    account_type: AccountType = Field(alias="accountType")
    created_at: datetime = Field(alias="createdAt", default_factory=datetime.utcnow)

class UserCreate(UserBase):
    password: str
    

class UserResponse(UserBase):
    id: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class UserAuthentication(BaseModel):
    email: EmailStr
    password: str

class BusinessUnit(str, Enum):
    inkhaus = "inkhaus"
    snaphaus = "snaphaus"

class ProductBase(BaseModel):
    title: str
    description: Optional[str] = Field(default="")
    unit_price: int = Field(alias="unitPrice")
    artwork_url: Optional[str] = Field(alias="artworkUrl")
    business_unit: BusinessUnit = Field(alias="businessUnit")
    created_at: datetime = Field(alias="createdAt", default_factory=datetime.utcnow)
    minimum_order_quantity: int = Field(alias="minimumOrderQuantity", default=1)

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class PaymentChannel(str, Enum):
    cash = "cash"
    mobile_money = "mobile_money"
    bank_transfer = "bank_transfer"

class SaleEntry(BaseModel):
    service: str
    unit_price: int = Field(alias="unitPrice")
    quantity: int = Field(default=1)
    created_at: datetime = Field(alias="createdAt", default_factory=datetime.utcnow)

class Customer(BaseModel):
    fullname: str
    phone_number: Optional[str] = Field(alias="phoneNumber")
    email: Optional[str]
    created_at: datetime = Field(alias="createdAt", default_factory=datetime.utcnow)

class SaleCreate(BaseModel):
    entries: List[SaleEntry]
    customer: Customer
    total_price: int
    payment_channel: PaymentChannel = Field(alias="paymentChannel")
    created_at: datetime = Field(alias="createdAt", default_factory=datetime.utcnow)
    recorded_by: EmailStr = Field(alias="recordedBy")
    note: Optional[str]

class SaleResponse(SaleCreate):
    id: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class EnquiryStatus(str, Enum):
    pending_response = "pending_response"
    responded_to_enquirer = "responded_to_enquirer"
    should_be_ignored = "should_be_ignored"

class ServiceCategory(str, Enum):
    t_shirts_customization = "t_shirt_printing_and_customization"
    branded_items_customization = "branded_items_and_customization"
    photography_and_videography = "photography_and_videography"

class EnquiryBase(BaseModel):
    fullname: str
    phone_number: str = Field(alias="phoneNumber")
    service_category: ServiceCategory = Field(alias="serviceCategory")
    message: str
    status: EnquiryStatus = Field(default=EnquiryStatus.pending_response)
    updated_by: Optional[EmailStr] = Field(alias="updatedBy")
    responder_note: Optional[str] = Field(alias="responderNote")

class EnquiryCreate(EnquiryBase):
    created_at: datetime = Field(alias="createdAt", default_factory=datetime.utcnow)

class EnquiryStatusUpdate(BaseModel):
    status: EnquiryStatus
    updated_by: EmailStr = Field(alias="updatedBy")
    responder_note: str = Field(alias="responderNote")

class EnquiryResponse(EnquiryCreate):
    id: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class FotostoreAppointmentStatus(str, Enum):
    pending_fulfilment = "pending_fulfilment"
    cancelled = "cancelled"
    fulfilled = "fulfilled"

class FotostorePurpose(str, Enum):
    photoshoot = "photoshoot"
    rental = "rental"

class FotostoreAppointmentBase(BaseModel):
    fullname: str
    phone_number: str = Field(alias="phoneNumber")
    purpose: FotostorePurpose
    day: date
    time: int = Field(ge=7, le=20)
    status: FotostoreAppointmentStatus = Field(default=FotostoreAppointmentStatus.pending_fulfilment)
    special_request: Optional[str] = Field(alias="specialRequest")

class FotostoreAppointmentCreate(FotostoreAppointmentBase):
    created_at: datetime = Field(alias="createdAt", default_factory=datetime.utcnow)
    updated_by: Optional[EmailStr] = Field(alias="updatedBy")

class FotostoreAppointmentResponse(FotostoreAppointmentCreate):
    id: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class FotostoreAppointmentUpdate(BaseModel):
    status: FotostoreAppointmentStatus
    updated_by: EmailStr = Field(alias="updatedBy")

class ExpenseCategory(str, Enum):
    electricity = "electricity"
    water = "water"
    food = "food"
    internet = "internet"
    other_utility = "other_utility"
    materials_purchase = "materials_purchase"
    third_party_service = "third_party_service"

class Payee(BaseModel):
    fullname: str
    phone_number: str = Field(alias="phoneNumber")
    email_address: Optional[str] = Field(alias="emailAddress")

class ExpenseCreate(BaseModel):
    amount: int
    category: ExpenseCategory
    evidence: str
    notes: Optional[str]
    payee: Payee
    created_at: datetime = Field(alias="createdAt", default_factory=datetime.utcnow)

class ExpenseResponse(ExpenseCreate):
    id: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

