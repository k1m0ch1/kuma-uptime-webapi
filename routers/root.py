from fastapi import APIRouter, Request
from pydantic import BaseModel

from utils import kuma_uptime

router = APIRouter()

@router.get("/status")
async def status(request: Request):
    kuma = kuma_uptime.init(request.headers.get('Authorization'))
    if kuma is False:
        return {"message": "Not Found"}
    dataStatus = {
        "database_size": kuma.get_database_size(),
        "info": kuma.info(),
        "uptime": kuma.uptime(),
        "avg_ping": kuma.avg_ping(),
        "heartbeat": kuma.get_heartbeats(),
        "settings": kuma.get_settings()
    }

    kuma.disconnect()
    return dataStatus
