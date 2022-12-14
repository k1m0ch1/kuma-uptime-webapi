from fastapi import APIRouter, Request
from pydantic import BaseModel
from uptime_kuma_api import NotificationType

from utils import kuma_uptime

router = APIRouter()

class Notification(BaseModel):
    name: str
    type: NotificationType
    isDefault: bool = False,
    applyExisting: bool = False

@router.get("/notifications")
async def getNotif(request: Request):
    kuma = kuma_uptime.init(request.headers.get('Authorization'))
    if kuma is False:
        return {"message": "Not Found"}

    data = kuma.get_notifications()

    kuma.logout()
    kuma.disconnect()
    return data