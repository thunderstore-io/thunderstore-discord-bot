import os
from dotenv import load_dotenv
from thunderbot.tools.stringDecode import base64_decode

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
API_KEY = os.getenv("THUNDERSTORE_API_KEY_ID")
URL = os.getenv("THUNDERSTORE_API_URL")

try:
    USER_KEY = base64_decode(os.getenv("THUNDERSTORE_API_SECRET"))
except TypeError:
    print("Env var THUNDERSTORE_API_SECRET not found or cant decode")

USER_ALGORITHM = os.getenv("THUNDERSTORE_API_ALGORITHM")
PACKAGE_REFRESH_TIME = os.getenv("PACKAGE_REFRESH_TIME")

if API_KEY is None:
    raise Exception("Env var API_KEY not found")
if URL is None:
    raise Exception("Env var THUNDERSTORE_API_URL not found")
if USER_KEY is None:
    raise Exception("Env var THUNDERSTORE_API_SECRET not found")
if USER_ALGORITHM is None:
    raise Exception("Env var THUNDERSTORE_API_ALGORITHM not found")
if PACKAGE_REFRESH_TIME is None:
    raise Exception("Env var PACKAGE_REFRESH_TIME not found")
if TOKEN is None:
    raise Exception("Env TOKEN not found")

SER_PREF = {562704639141740588: ['!', 'quack'],  # ror2
            806549677209944084: ['!', 'quack'],  # dsp
            807356896637354004: ['!', 'quack'],  # valh
            782438773690597389: ['!', 'quack']}  # mtfo


PACKAGE_DICT = []
NAME_LIST = []
