from fastapi import HTTPException
from pydantic import BaseModel
import stripe

# Define products server-side (never trust client amounts!)
PRODUCTS = {
    "ebook": {"name": "Python SaaS eBook", "amount": 2900},  # $29.00
    "course": {"name": "FastAPI Masterclass", "amount": 9900},  # $99.00
    "template": {"name": "SaaS Template", "amount": 7900},  # $79.00
}

class CheckoutRequest(BaseModel):
    product_id: str


@app.post("/create-checkout-session")
async def create_checkout_session(request: CheckoutRequest):
    # Validate product exists
    if request.product_id not in PRODUCTS:
        raise HTTPException(status_code=400, detail="Invalid product")

    product = PRODUCTS[request.product_id]

    try:
        checkout_session = await stripe.checkout.Session.create_async(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": product["name"],
                    },
                    "unit_amount": product["amount"],
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=f"{settings.domain}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.domain}/cancel",
        )
        return {"checkout_url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
