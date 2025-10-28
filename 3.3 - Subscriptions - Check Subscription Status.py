from fastapi import Depends, HTTPException, Header

async def require_active_subscription(
    # In your app, ensure customer_email value comes
    # from the authenticated user him/herself
    customer_email: str = Depends(customer_email_dependency)
):
    customers = await stripe.Customer.list_async(
        email=customer_email,
        limit=1
    )

    if not customers.data:
        raise HTTPException(
            status_code=403,
            detail="No customer found"
        )

    customer = customers.data[0]

    # Get subscriptions
    subscriptions = await stripe.Subscription.list_async(
        customer=customer.id,
        status="active",
        limit=1
    )

    if not subscriptions.data:
        raise HTTPException(
            status_code=403,
            detail="No active subscription"
        )

    return subscriptions.data[0]

@app.get("/premium-content")
async def premium_content(subscription = Depends(require_active_subscription)):
    return {
        "message": "Welcome to premium content!",
        "subscription_id": subscription.id
    }
