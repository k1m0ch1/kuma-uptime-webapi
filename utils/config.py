import logging

from os import environ

_ = environ.get

KUMA_URL        =   _("KUMA_URL", "https://localhost")

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)