from typing import List
from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException, Query

from app.database.shared import get_appointments_collection
from app.routers.models import FotostoreAppointmentCreate, FotostoreAppointmentResponse

router = APIRouter(
    prefix="/appointments",
    tags=["appointments"]
)

@router.post("/", response_model=FotostoreAppointmentResponse)
async def create_appointment(payload: FotostoreAppointmentCreate, appointments = Depends(get_appointments_collection)):
    appointment_doc = payload.model_dump(by_alias=True)
    if isinstance(appointment_doc["day"], date):
        appointment_doc["day"] = datetime.combine(appointment_doc["day"], datetime.min.time())

    result = await appointments.insert_one(appointment_doc)

    appointment = {**appointment_doc, "id": str(result.inserted_id)}
    return appointment

@router.get("/", response_model=List[FotostoreAppointmentResponse])
async def get_appointments(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    appointments = Depends(get_appointments_collection)
):
    cursor = appointments.find().skip(skip).limit(limit).sort("createdAt", -1)
    existing_appointments = await cursor.to_list(length=limit)
    for appointment in existing_appointments:
        appointment["id"] = str(appointment["_id"])
        del appointment["_id"]

    return existing_appointments