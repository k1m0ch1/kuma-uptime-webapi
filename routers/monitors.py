from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional
from uptime_kuma_api import MonitorType, AuthMethod

from utils import kuma_uptime

router = APIRouter()

@router.get("/monitors")
async def getMonitors(request: Request):
    kuma = kuma_uptime.init(request.headers.get('Authorization'))
    if kuma is False:
        return {"message": "Not Found"}

    data = kuma.get_monitors()

    kuma.logout()
    kuma.disconnect()
    return data

@router.get("/monitor/{monitor_id}/{hours}")
async def getMonitorBeats(request: Request, monitor_id, hours):
    kuma = kuma_uptime.init(request.headers.get('Authorization'))
    if kuma is False:
        return {"message": "Not Found"}

    data = kuma.get_monitor_beats(monitor_id, hours)

    kuma.logout()
    kuma.disconnect()
    return data

@router.post("/monitor/tag")
async def tagsToMonitor(request: Request):
    kuma = kuma_uptime.init(request.headers.get('Authorization'))
    if kuma is False:
        return {"message": "Not Found"}
    
    data = await request.json()

    dataResponse = kuma.add_monitor_tag(
        tag_id=data['tag_id'],
        monitor_id=data['monitor_id'],
        value=data['value'])

    kuma.logout()
    kuma.disconnect()
    return data


class HttpOption(BaseModel):
    method: str = "GET"
    body: str = None
    headers: str = None
    auth_method: AuthMethod = AuthMethod.NONE
    basic_auth_user: str = None
    basic_auth_pass: str = None
    auth_domain: str = None
    auth_workstation: str = None

class Interval(BaseModel):
    check: int = 60
    retry: int = 60
    resend: int = 0
    max_retries: int = 0

class DNS(BaseModel):
    dns_resolve_server: str = "1.1.1.1"
    dns_resolve_type: str = "A"

class MQTT(BaseModel):
    username: str = None
    password: str = None
    topic: str = None
    success_message: str = None

# SQLSERVER, POSTGRES
class DatabaseConnection(BaseModel):
    database_connection_string: str = None
    database_query: str = None

class Docker(BaseModel):
    docker_container: str = ""
    docker_host: str = None

class Monitor(BaseModel):
    type: MonitorType
    name: str
    url: str
    keyword: str = None
    http_options: Optional[HttpOption]
    interval: Optional[Interval]
    upside_down: bool = False
    notification_id_list: list = None
    expiry_notification: bool = False
    ignore_tls: bool = False
    max_redirects: int = 1
    accepted_statuscodes: list = None # ex: ["200-299", "100"]
    proxy_id: int = None
    hostname: str = None # DNS, PING, STEAM, MQTT
    port: int = 53
    dns: Optional[DNS]
    mqtt: Optional[MQTT]
    docker: Optional[Docker]


@router.post("/monitor/add")
async def addHost(mon: Monitor, request: Request):
    data = await request.json()

    kuma = kuma_uptime.init(request.headers.get('Authorization'))
    if kuma is False:
        return {"message": "Not Found"}

    if mon.http_options is None:
        mon.http_options = HttpOption()
    
    if mon.dns is None:
        mon.dns = DNS()
    
    if mon.interval is None:
        mon.interval = Interval()

    result = kuma.add_monitor(
        type = mon.type,
        name = mon.name,
        url = mon.url,
        keyword = mon.keyword,
        method = mon.http_options.method,
        body = mon.http_options.body,
        headers = mon.http_options.headers,
        authMethod = mon.http_options.auth_method,
        basic_auth_user = mon.http_options.basic_auth_user,
        basic_auth_pass = mon.http_options.basic_auth_pass,
        authDomain = mon.http_options.auth_domain,
        authWorkstation = mon.http_options.auth_workstation,
        interval = mon.interval.check,
        retryInterval = mon.interval.retry,
        resendInterval = mon.interval.resend,
        maxretries = mon.interval.max_retries,
        upsideDown = mon.upside_down,
        notificationIDList = mon.notification_id_list,
        expiryNotification = mon.expiry_notification,
        ignoreTls = mon.ignore_tls,
        maxredirects = mon.max_redirects,
        accepted_statuscodes = mon.accepted_statuscodes,
        proxyId = mon.proxy_id,
        hostname = mon.hostname,
        port = mon.port,
        dns_resolve_server = mon.dns.dns_resolve_server,
        dns_resolve_type = mon.dns.dns_resolve_type,
    )

    kuma.logout()
    kuma.disconnect()

    return result