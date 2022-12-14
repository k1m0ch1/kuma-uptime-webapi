from fastapi import APIRouter, Request
from pydantic import BaseModel

from utils import kuma_uptime

router = APIRouter()

class StatusPage(BaseModel):
    slug: str
    title: str

@router.get("/status_pages")
async def getStatusPage(request: Request):
    kuma = kuma_uptime.init(request.headers.get('Authorization'))
    if kuma is False:
        return {"message": "Not Found"}

    data = kuma.get_status_pages()

    kuma.logout()
    kuma.disconnect()
    return data

@router.post("/status_page")
async def addNewStatusPage(status_page: StatusPage, request: Request):
    kuma = kuma_uptime.init(request.headers.get('Authorization'))
    if kuma is False:
        return {"message": "Not Found"}

    dataReturn = kuma.add_status_page(status_page.slug, status_page.title)

    kuma.logout()
    kuma.disconnect()
    return dataReturn