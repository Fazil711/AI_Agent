from fastapi import APIRouter
from app.api.v1.endpoints import chat, document, history # Ensure these exist

api_router = APIRouter() # <--- This name MUST match exactly

api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(document.router, prefix="/documents", tags=["Documents"])
api_router.include_router(history.router, prefix="/history", tags=["History"])