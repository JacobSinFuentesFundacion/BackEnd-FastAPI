from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import stripe
from dotenv import load_dotenv
import os
import time

load_dotenv()
stripe.api_key = os.getenv("API_STRIPE_KEY")

app = FastAPI(
    title="Donation Jacob API",
    description="API for donation Jacob",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)



@app.get("/", name="Root")
async def root():
    return {
        "message": "Hello, API!"
    }


@app.get("/get-link", name="Get link donate")
async def root():
    return {
        "message": "Okay",
        "link": os.getenv("DONATE_LINK")
    }


@app.get("/get-pays", name="Get pays")
async def get_pays():
    charges = stripe.Charge.list(limit=10)
    charges_latest = sorted(
        charges.data, key=lambda x: x.created, reverse=True)[:10]

    pays = []
    for charge in charges_latest:
        pays.append({
            "name": charge.billing_details.name,
            "time_created": charge.created,
            "amount": charge.amount,
            "currency": charge.currency,
            "country": charge.billing_details.address.country,
        })

    return {
        "message": "Okay",
        "timestamp": time.time(),
        "pays": pays
    }
