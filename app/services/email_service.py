def send_order_confirmation_email(
    email: str,
    order_id: int,
):
    print(
        f"Sending order confirmation "
        f"to {email} for order {order_id}"
    )