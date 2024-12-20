from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
import os
import requests

app = FastAPI()

SHOPIFY_API_KEY = '8ff194747831deaed9c0542462366a9e'
SHOPIFY_API_SECRET = 'c6cceed16f61f22e4d62ba9379da55e8'
REDIRECT_URI = "https://app-public-rust.vercel.app/shopify/callback"

# Basic ping endpoint for testing
@app.get("/ping")
def ping():
    return {"message": "pong"}

# Step 1: Installation endpoint
# Step 1: Installation endpoint
@app.get("/install")
def install(request: Request, shop: str = None):
    if not shop:
        with open("install.html", "r") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)

    # Redirect to Shopify OAuth authorization page
    oauth_url = (
        f"https://{shop}/admin/oauth/authorize?"
        f"client_id={SHOPIFY_API_KEY}&scope=read_products,write_orders&redirect_uri={REDIRECT_URI}"
    )
    return RedirectResponse(url=oauth_url)

# Step 2: Handle the OAuth callback and exchange the code for an access token
@app.get("/shopify/callback")
def callback(request: Request):
    params = request.query_params
    code = params.get("code")
    shop = params.get("shop")

    if not code or not shop:
        raise HTTPException(status_code=400, detail="Invalid callback parameters")

    # Exchange authorization code for access token
    token_url = f"https://{shop}/admin/oauth/access_token"
    response = requests.post(token_url, json={
        "client_id": SHOPIFY_API_KEY,
        "client_secret": SHOPIFY_API_SECRET,
        "code": code
    })

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        # Save the access_token in your database (pseudo code)
        # save_access_token(shop, access_token)

        # Redirect to datatram.ai after successful installation
        return RedirectResponse(url="https://datatram.ai")
    else:
        raise HTTPException(status_code=response.status_code, detail="OAuth token exchange failed")
