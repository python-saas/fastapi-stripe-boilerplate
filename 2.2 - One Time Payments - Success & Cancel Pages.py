@app.get("/success")
async def payment_success(session_id: str):
    try:
        session = await stripe.checkout.Session.retrieve_async(session_id)

        if session.payment_status == "paid":
            # TODO: Here, you could save the order to your database
            # TODO: Here, you could send a confirmation email to the user
            return {"status": "success", "customer_email": session.customer_details.email}

        return {"status": "pending"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/cancel")
async def payment_cancel():
    return {"message": "Payment cancelled"}
