from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from app.routers.routes import api_routers

app = FastAPI(
    title="InkHaus-GH Point of Sale APIs",
    summary="API documentation of sales management APIs at InkHaus-GH",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

for router in api_routers:
    app.include_router(router, prefix="/v1")

@app.get("/")
async def index():
    return RedirectResponse("/docs")