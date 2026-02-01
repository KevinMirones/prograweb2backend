from fastapi import FastAPI
from app.routers.routes_v1 import api_router_v1
from app.routers import auth, chat
from fastapi.middleware.cors import CORSMiddleware

PROJECT_NAME = "PROYECTO_PROGRAMACIÓN_WEB_II"
PROJECT_DESCRIPTION = "API para Sistema de información para registro de ventas de servicios computacionales."
API_V1_STR: str = "/api/v1"

app = FastAPI(
    title= PROJECT_NAME,
    description=PROJECT_DESCRIPTION,
    openapi_url="/api/openapi.json",
)

API_V1_STR: str = "/api/v1"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router_v1, prefix=API_V1_STR)
app.include_router(auth.router, prefix=API_V1_STR)
app.include_router(chat.router, prefix=API_V1_STR)
