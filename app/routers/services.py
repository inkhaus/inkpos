from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.database.shared import get_products_collection
from app.routers.models import ProductCreate, ProductResponse

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

def db_product_to_response(db_product) -> ProductResponse:
    return ProductResponse(
        id=str(db_product['_id']),
        title=db_product['title'],
        description=db_product['description'],
        unitPrice=db_product['unit_price'],
        artworkUrl=db_product['artwork_url'],
        businessUnit=db_product['business_unit'],
        createdAt=db_product['created_at'],
    )

@router.post("/", response_model=ProductResponse)
async def create_product(payload: ProductCreate, products = Depends(get_products_collection)):
    existing_product = await products.find_one({"title": payload.title})
    if existing_product:
        raise HTTPException(status_code=400, detail="Product already defined.")
    
    product_doc = payload.model_dump(by_alias=True)
    result = await products.insert_one(product_doc)

    product = {**product_doc, "id": str(result.inserted_id)}
    return product

@router.get("/", response_model=List[ProductResponse])
async def get_products(products = Depends(get_products_collection)):
    existing_products = await products.find().to_list(length=None)
    products = []
    for prod in existing_products:
        products.append({**prod, "id": str(prod['_id'])})
    
    return products