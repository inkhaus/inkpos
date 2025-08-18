from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from app.database.shared import get_enquiries_collection
from app.routers.models import EnquiryCreate, EnquiryResponse

router = APIRouter(
    prefix="/enquiries",
    tags=["enquiries"],
)

@router.post("/", response_model=EnquiryResponse)
async def create_enquiry(payload: EnquiryCreate, enquiries = Depends(get_enquiries_collection)):
    enquiry_doc = payload.model_dump(by_alias=True)
    result = await enquiries.insert_one(enquiry_doc)

    enquiry = {**enquiry_doc, "id": str(result.inserted_id)}
    return enquiry

@router.get("/", response_model=List[EnquiryResponse])
async def get_enquiries(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    enquiries = Depends(get_enquiries_collection)
):
    cursor = enquiries.find().skip(skip).limit(limit).sort("createdAt", -1)
    existing_enquiries = await cursor.to_list(length=limit)
    for enquiry in existing_enquiries:
        enquiry["id"] = str(enquiry["_id"])
        del enquiry["_id"]

    return existing_enquiries