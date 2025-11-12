import os
from dotenv import load_dotenv  # <-- ajoute cette ligne !

# config.py
# =========================
# Configuration projet EcoPay NFC PRO
# =========================

# -----------------
# Google Sheet
# -----------------
# ID de ta feuille Google Sheet
#GOOGLE_SHEET_ID = "1ad06u17H-JZ3tj3VKZaQgcwwqgGT5eHmK18Qf0JHYdo"
GOOGLE_SHEET_ID ="1vDH4bKbYUvlzy5aQwWxLRBsu2Vy0EAETS2x41Oqnamg"
# -----------------
# Chargily API
# -----------------
load_dotenv()

SUCCESS_URL = os.getenv("SUCCESS_URL")
FAIL_URL = os.getenv("FAIL_URL")

CHARGILY_PUBLIC_KEY = os.getenv("CHARGILY_PUBLIC_KEY")
CHARGILY_SECRET = os.getenv("CHARGILY_SECRET")
CHARGILY_URL = os.getenv("CHARGILY_URL")

# -----------------

# -----------------
# Paramètres supplémentaires
# -----------------
# Tu peux ajouter ici d’autres configs comme la devise par défaut, langue, etc.
DEFAULT_CURRENCY = "dzd"
