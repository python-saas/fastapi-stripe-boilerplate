# setup_stripe_products.py - Run this once to create your products
import stripe
import os
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Basic plan
basic_product = stripe.Product.create(name="Basic Plan")
basic_price = stripe.Price.create(
    product=basic_product.id,
    unit_amount=999,  # $9.99
    currency="usd",
    recurring={"interval": "month"}
)

# Pro plan
pro_product = stripe.Product.create(name="Pro Plan")
pro_price = stripe.Price.create(
    product=pro_product.id,
    unit_amount=2999,  # $29.99
    currency="usd",
    recurring={"interval": "month"}
)

print(f"Basic Plan Price ID: {basic_price.id}")
print(f"Pro Plan Price ID: {pro_price.id}")
