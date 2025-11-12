# ==========================================
# config.py (sécurisé pour Render)
# ==========================================
import os

# Clés Chargily (lues depuis Render)
CHARGILY_PUBLIC_KEY = os.getenv("CHARGILY_PUBLIC_KEY")
CHARGILY_SECRET = os.getenv("CHARGILY_SECRET_KEY")

# Google Sheets
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

# URLs de redirection
SUCCESS_URL = os.getenv("SUCCESS_URL", "https://ecopay-nfc-pro.onrender.com/success")
FAIL_URL = os.getenv("FAIL_URL", "https://ecopay-nfc-pro.onrender.com/failure")
