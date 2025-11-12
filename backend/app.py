# app.py
from flask import Flask, request, redirect, render_template
from sheets_service import get_sheet_data
from chargily_service import create_checkout
from config import SUCCESS_URL, FAIL_URL

app = Flask(__name__)

# -------------------
# Page d'accueil / Menu
# -------------------
@app.route('/')
def home():
    vendor_id = request.args.get('vendor_id', 'cafe_express')  # valeur par défaut
    data = get_sheet_data()  # lit toutes les feuilles

    if vendor_id not in data:
        return "<h2>Vendeur inconnu</h2>", 404

    vendor = data[vendor_id]

    # Extraire toutes les catégories
    categories = sorted({p.get('category', 'Divers') for p in vendor['products'].values()})

    return render_template(
        "home.html",
        vendor=vendor,
        vendor_id=vendor_id,
        categories=categories
    )

# -------------------
# Endpoint paiement
# -------------------
@app.route('/pay')
def pay():
    vendor_id = request.args.get('vendor_id')
    product_id = request.args.get('product_id')

    if not vendor_id:
        return 'Vendeur non spécifié', 400

    data = get_sheet_data()
    if vendor_id not in data:
        return 'Vendeur inconnu', 404
    vendor = data[vendor_id]

    if not product_id:
        return redirect(f"/?vendor_id={vendor_id}")

    if product_id not in vendor['products']:
        return 'Produit inconnu', 404

    product = vendor['products'][product_id]

    success_url = f"{SUCCESS_URL}?vendor_id={vendor_id}"
    failure_url = f"{FAIL_URL}?vendor_id={vendor_id}"

    # Crée l'URL de paiement via Chargily
    payment_url = create_checkout(
        product['price'],
        f"{product['name']} - {vendor['name']}",
        success_url=success_url,
        failure_url=failure_url
    )

    return redirect(payment_url)

# -------------------
# Page de succès paiement
# -------------------
@app.route("/success")
def success():
    vendor_id = request.args.get("vendor_id")
    return render_template("success.html", vendor_id=vendor_id)

# -------------------
# Page échec paiement
# -------------------
@app.route("/failure")
def failure():
    vendor_id = request.args.get("vendor_id")
    return render_template("failure.html", vendor_id=vendor_id)

# -------------------
# Démarrage serveur
# -------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

