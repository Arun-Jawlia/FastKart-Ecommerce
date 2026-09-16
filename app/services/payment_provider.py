import secrets


def create_provider_payment(
    amount,
    currency,
):
    return {
        "provider_payment_id": (
            "mock_"
            + secrets.token_hex(10)
        ),
        "amount": amount,
        "currency": currency,
        "status": "SUCCESS",
    }