@app.post("/create-portal-session")
async def create_portal_session(customer_email: str):
    try:
        # Get customer
        customers = await stripe.Customer.list_async(email=customer_email, limit=1)
        if not customers.data:
            raise HTTPException(status_code=404, detail="Customer not found")

        customer = customers.data[0]

        # Create portal session
        portal_session = await stripe.billing_portal.Session.create_async(
            customer=customer.id,
            return_url=f"{settings.domain}/dashboard",
        )

        return {"portal_url": portal_session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
