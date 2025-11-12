# sheets_service.py
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import GOOGLE_SHEET_ID

# -------------------
# Création du fichier credentials.json depuis la variable d'environnement (Render)
# -------------------
GOOGLE_CREDS_JSON = os.environ.get("GOOGLE_CREDS_JSON")
if GOOGLE_CREDS_JSON:
    try:
        with open("credentials.json", "w") as f:
            parsed = json.loads(GOOGLE_CREDS_JSON)
            json.dump(parsed, f)
        print("✅ credentials.json créé depuis GOOGLE_CREDS_JSON")
    except Exception as e:
        print(f"⚠️ Impossible de créer credentials.json : {e}")
else:
    print("⚠️ GOOGLE_CREDS_JSON non défini, utilisez un fichier credentials.json localement")

# -------------------
# Configuration de l'accès Google Sheets
# -------------------
scope = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]

def get_all_sheets():
    """
    Retourne la liste des noms de toutes les feuilles du Google Sheet.
    """
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(GOOGLE_SHEET_ID)
        return [ws.title for ws in sheet.worksheets()]
    except Exception as e:
        print(f"Erreur lors de la récupération des feuilles : {e}")
        return []

def get_sheet_data(sheet_name=None):
    """
    Récupère les données d'un vendor depuis une feuille spécifique.
    Si sheet_name=None, lit toutes les feuilles et combine les vendors.
    """
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(GOOGLE_SHEET_ID)

        data = {}

        if sheet_name:  # Si on fournit un vendor précis (une feuille)
            worksheets = [sheet.worksheet(sheet_name)]
        else:  # sinon, toutes les feuilles
            worksheets = sheet.worksheets()

        for ws in worksheets:
            rows = ws.get_all_records()
            # Déduire vendor_id à partir du nom de la feuille si pas fourni
            vendor_id = ws.title.lower().replace(" ", "_")
            vendor_name = rows[0].get("vendor_name", ws.title) if rows else ws.title

            vendor_data = {
                "name": vendor_name,
                "products": {}
            }

            for row in rows:
                product_id = str(row.get("product_id")).strip()
                if not product_id:
                    continue
                vendor_data["products"][product_id] = {
                    "name": row.get("product_name", f"Produit {product_id}"),
                    "price": float(row.get("price_dzd", 0)),
                    "category": row.get("category", "Divers"),
                    "image": row.get("image_url", "https://via.placeholder.com/300")
                }

            data[vendor_id] = vendor_data

        return data

    except FileNotFoundError:
        print("Erreur : credentials.json introuvable")
        return {}
    except gspread.SpreadsheetNotFound:
        print("Erreur : Google Sheet introuvable ou ID incorrect")
        return {}
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return {}
