from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from bson import ObjectId
from pymongo import ReturnDocument

from app.database.shared import get_enquiries_collection
from app.routers.models import EnquiryCreate, EnquiryResponse, EnquiryStatusUpdate

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

@router.patch("/{enquiry_id}/status", response_model=EnquiryResponse)
async def update_enquiry_status(enquiry_id: str, update: EnquiryStatusUpdate, enquiries = Depends(get_enquiries_collection)):
    if not ObjectId.is_valid(enquiry_id):
        raise HTTPException(status_code=400, detail="Invalid enquiry id")
    
    result = await enquiries.find_one_and_update(
        {"_id": ObjectId(enquiry_id)},
        {"$set": {"status": update.status, "updatedBy": update.updated_by, "responderNote": update.responder_note}},
        return_document = ReturnDocument.AFTER
    )

    if not result:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    
    enquiry = {**result, "id": str(result["_id"])}
    return enquiry
    