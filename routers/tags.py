from fastapi import APIRouter, Request
from pydantic import BaseModel

from utils import kuma_uptime

router = APIRouter()

class Tag(BaseModel):
    name: str
    color: str

@router.get("/tags")
async def getTags(request: Request):
    kuma = kuma_uptime.init(request.headers.get('Authorization'))
    if kuma is False:
        return {"message": "Not Found"}

    data = kuma.get_tags()

    kuma.logout()
    kuma.disconnect()
    return data

@router.post("/tag")
async def addNewTag(tag: Tag, request: Request):
    kuma = kuma_uptime.init(request.headers.get('Authorization'))
    if kuma is False:
        return {"message": "Not Found"}

    data = await request.json()

    dataReturn = kuma.add_tag(tag.name, tag.color)

    kuma.logout()
    kuma.disconnect()
    return dataReturn