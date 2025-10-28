from fastapi import Request

@app.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    try:
        # Verify webhook signature. This ensures the call really comes from Stripe
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle different event types
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_session(session)

    elif event['type'] == 'customer.subscription.created':
        subscription = event['data']['object']
        handle_subscription_created(subscription)

    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        handle_subscription_updated(subscription)

    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        handle_subscription_deleted(subscription)

    elif event['type'] == 'invoice.payment_succeeded':
        invoice = event['data']['object']
        handle_invoice_paid(invoice)

    elif event['type'] == 'invoice.payment_failed':
        invoice = event['data']['object']
        handle_invoice_failed(invoice)

    return {"status": "success"}

def handle_checkout_session(session):
    """Called when checkout is completed"""
    customer_email = session.get('customer_details', {}).get('email')
    print(f"Payment successful for {customer_email}")
    # TODO: Update database
    # TODO: Send confirmation email
    # TODO: Grant access to product

def handle_subscription_created(subscription):
    """Called when subscription is created"""
    customer_id = subscription['customer']
    print(f"Subscription created for customer {customer_id}")
    # TODO: Update user's subscription status in database

def handle_subscription_updated(subscription):
    """Called when subscription is updated (plan change, etc)"""
    customer_id = subscription['customer']
    status = subscription['status']
    print(f"Subscription updated for {customer_id}: {status}")
    # TODO: Update database

def handle_subscription_deleted(subscription):
    """Called when subscription is cancelled"""
    customer_id = subscription['customer']
    print(f"Subscription cancelled for {customer_id}")
    # TODO: Revoke access
    # TODO: Send cancellation email

def handle_invoice_paid(invoice):
    """Called when recurring payment succeeds"""
    customer_id = invoice['customer']
    print(f"Invoice paid for {customer_id}")
    # TODO: Extend subscription
    # TODO: Send receipt

def handle_invoice_failed(invoice):
    """Called when recurring payment fails"""
    customer_id = invoice['customer']
    print(f"Payment failed for {customer_id}")
    # TODO: Send payment failed email
    # TODO: Maybe pause access after grace period
