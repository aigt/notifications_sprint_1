from fastapi import APIRouter

from api.v1.add_notification.view import add_notification

api_router = APIRouter()

api_router.include_router(
    add_notification,
    prefix="/add_notification",
    tags=["Notifications"],
)
