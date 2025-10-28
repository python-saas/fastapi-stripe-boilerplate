class SubscriptionRequest(BaseModel):
    price_id: str  # e.g., "price_1234567890"
    customer_email: str

@app.post("/create-subscription-checkout")
async def create_subscription_checkout(request: SubscriptionRequest):
    try:
        # Create or get customer
        customers = await stripe.Customer.list_async(email=request.customer_email, limit=1)

        if customers.data:
            customer = customers.data[0]
        else:
            customer = await stripe.Customer.create_async(email=request.customer_email)

        # Create checkout session for subscription
        checkout_session = await stripe.checkout.Session.create_async(
            customer=customer.id,
            payment_method_types=["card"],
            line_items=[{
                "price": request.price_id,
                "quantity": 1,
            }],
            mode="subscription",
            success_url=f"{settings.domain}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.domain}/cancel",
        )

        return {"checkout_url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
