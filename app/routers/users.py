from fastapi import APIRouter, Depends, HTTPException
from passlib.hash import pbkdf2_sha256

from app.database.shared import get_users_collection
from app.routers.models import UserCreate, UserResponse, UserAuthentication

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=UserResponse)
async def create_user(payload: UserCreate, users = Depends(get_users_collection)):
    existing_user = await users.find_one({"email": payload.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken.")
    
    payload.password = pbkdf2_sha256.hash(payload.password)
    user_doc = payload.model_dump(by_alias=True)
    result = await users.insert_one(user_doc)
    
    user = {**user_doc, "id": str(result.inserted_id)}
    return user

@router.post("/login", response_model=UserResponse)
async def authenticate(payload: UserAuthentication, users = Depends(get_users_collection)):
    existing_user = await users.find_one({"email": payload.email})
    if not existing_user:
        raise HTTPException(status_code=400, detail="Wrong username or password given.")
    
    valid_password = pbkdf2_sha256.verify(payload.password, existing_user["password"])
    if not valid_password:
        raise HTTPException(status_code=400, detail="Authentication failed.")
    
    user = {**existing_user, "id": str(existing_user['_id'])}
    return user