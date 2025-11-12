# ===================================
# chargily_service.py
# ===================================
import os
from chargily_pay import ChargilyClient
from chargily_pay.settings import CHARGILIY_URL
from chargily_pay.entity import Product, Price, Checkout

# URLs de redirection
SUCCESS_URL = os.environ.get("SUCCESS_URL", "https://ecopay-nfc-pro.onrender.com/success")
FAIL_URL = os.environ.get("FAIL_URL", "https://ecopay-nfc-pro.onrender.com/fail")

# -----------------------------
# Récupérer les clés depuis Render
# -----------------------------
CHARGILY_PUBLIC_KEY = os.environ.get("CHARGILY_PUBLIC_KEY")
CHARGILY_SECRET = os.environ.get("CHARGILY_SECRET_KEY")  # attention au nom exact

if not CHARGILY_PUBLIC_KEY or not CHARGILY_SECRET:
    raise ValueError("Les clés CHARGILY_PUBLIC_KEY et CHARGILY_SECRET_KEY doivent être définies en variables d'environnement")

# -----------------------------
# Initialiser le client Chargily
# -----------------------------
chargily = ChargilyClient(CHARGILY_PUBLIC_KEY, CHARGILY_SECRET, CHARGILIY_URL)

# -----------------------------
# Créer un checkout
# -----------------------------
def create_checkout(amount_dzd, product_name, success_url=None, failure_url=None):
    try:
        amount = int(float(amount_dzd))
        if amount <= 0:
            raise ValueError("Le montant doit être supérieur à 0")

        success_url = success_url or SUCCESS_URL
        failure_url = failure_url or FAIL_URL

        # 1️⃣ Créer le produit
        product = Product(name=product_name, description=product_name)
        product_response = chargily.create_product(product)
        product_id = product_response.get("id")
        if not product_id:
            raise Exception(f"Erreur création produit : {product_response}")

        # 2️⃣ Créer le prix
        price = Price(amount=amount, currency="dzd", product_id=product_id)
        price_response = chargily.create_price(price)
        price_id = price_response.get("id")
        if not price_id:
            raise Exception(f"Erreur création prix : {price_response}")

        # 3️⃣ Créer le checkout
        checkout = Checkout(
            items=[{"price": price_id, "quantity": 1}],
            success_url=success_url,
            failure_url=failure_url
        )
        checkout_response = chargily.create_checkout(checkout)
        checkout_url = checkout_response.get("checkout_url")
        if not checkout_url:
            raise Exception(f"Erreur création checkout : {checkout_response}")

        return checkout_url

    except Exception as e:
        print(f"❌ Erreur create_checkout: {e}")
        raise
