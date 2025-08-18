from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query

from app.database.shared import get_sales_collection
from app.routers.models import SaleCreate, SaleResponse

router = APIRouter(
    prefix="/sales",
    tags=["sales"],
)

@router.post("/", response_model=SaleResponse)
async def create_sale(payload: SaleCreate, sales = Depends(get_sales_collection)):
    sale_doc = payload.model_dump(by_alias=True)
    result = await sales.insert_one(sale_doc)
    sale = {**sale_doc, "id": str(result.inserted_id)}

    return sale

@router.get("/", response_model=List[SaleResponse])
async def get_sales(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    sales = Depends(get_sales_collection)
):
    cursor = sales.find().skip(skip).limit(limit).sort("createdAt", -1)
    existing_sales = await cursor.to_list(length=limit)
    for sale in existing_sales:
        sale["id"] = str(sale["_id"])
        del sale["_id"]

    return existing_sales

@router.get("/search", response_model=List[SaleResponse])
async def search_sales(
    start_date: datetime = Query(description="Start datetime (ISO format)"),
    end_date: datetime = Query(description="End datetime (ISO format)"),
    sales = Depends(get_sales_collection)
):
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="start_date must be before end_date")
    
    cursor = sales.find(
        {
            "createdAt": {
                "$gte": start_date,
                "$lte": end_date,
            }
        }
    )

    matched_sales = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        matched_sales.append(SaleResponse(**doc))

    return matched_sales
