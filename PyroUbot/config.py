import os

from dotenv import load_dotenv

load_dotenv(".env")

API_ID: int = os.getenv('API_ID', "29901775")
API_HASH: str = os.getenv('API_HASH', "10aa90e6142d4f5897dd9b3c30529a35")

BOT_TOKEN = os.getenv("BOT_TOKEN")

OWNER_ID = int(os.getenv("OWNER_ID"))

LOGS_MAKER_UBOT = int(os.getenv("LOGS_MAKER_UBOT"))

MAX_BOT = int(os.getenv("MAX_BOT"))

RMBG_API = os.getenv("RMBG_API")

OPENAI_KEY = os.getenv("OPENAI_KEY")

MONGO_URL = os.getenv("MONGO_URL")

DOMAIN = os.getenv("DOMAIN", "https://private-pokebot.fahri4you.my.id")

PLTA = os.getenv("PLTA", "ptla_gIlkuBVuHY2262QSg1EuvA5fopgzr7LrZweZMGCZpBI")

CAPI_KEY = os.getenv("CAPI_KEY", "ptlc_ybJMpanSG9WBNFoSfkPz3sbOXfHr0BvhDhTWdJSsniA")

EGG = os.getenv("EGG", "15")

LOC = os.getenv("LOC", "1")
