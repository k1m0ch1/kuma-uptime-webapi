import base64
import os
from uptime_kuma_api import UptimeKumaApi, UptimeKumaException

from utils import config

def init(AUTH_HEADER):
    if "Basic " not in AUTH_HEADER:
        return False
    USERNAME, PASSWORD = base64.b64decode(AUTH_HEADER.split("Basic ")[1]).decode("utf-8").split(":")
    kuma = UptimeKumaApi(config.KUMA_URL)
    try:
        kuma.login(USERNAME, PASSWORD)
    except UptimeKumaException:
        kuma.disconnect()
        return False

    return kuma