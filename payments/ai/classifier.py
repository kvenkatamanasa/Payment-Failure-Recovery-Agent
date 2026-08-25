def classify_failure(payment):
    """
    Classify the likely cause of a payment failure.
    """

    failure_reason = (payment.failure_reason or "").lower()

    if "timeout" in failure_reason:
        return {
            "failure_type": "Payment Timeout",
            "confidence": 0.92
        }

    if "declined" in failure_reason:
        return {
            "failure_type": "Payment Declined",
            "confidence": 0.94
        }

    if "insufficient" in failure_reason:
        return {
            "failure_type": "Insufficient Funds",
            "confidence": 0.96
        }

    if "network" in failure_reason:
        return {
            "failure_type": "Network Error",
            "confidence": 0.89
        }

    return {
        "failure_type": "Unknown Payment Failure",
        "confidence": 0.50
    }