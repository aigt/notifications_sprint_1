from fastapi import APIRouter

from api.v1.welcome_notification.view import welcome_router

api_router = APIRouter()

api_router.include_router(welcome_router, prefix="/welcome", tags=["welcome"])
