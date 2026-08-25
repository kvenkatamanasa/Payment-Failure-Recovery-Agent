from payments.models import Payment


# ---------------------------------------------------------
# Payment cancellation reasons
# ---------------------------------------------------------

CANCELLATION_REASONS = [
    "Customer requested cancellation",
    "Duplicate payment detected",
    "Payment authorization failed",
    "Payment expired",
    "Invalid payment details",
    "Fraud risk detected",
    "Insufficient funds",
    "Merchant cancelled payment",
    "Order cancelled",
    "Payment already completed",
]


# ---------------------------------------------------------
# Main payment diagnosis function
# ---------------------------------------------------------

def diagnose_payment(payment):
    """
    AI-style diagnosis and safety decision for a payment.

    The function:
    1. Identifies the failure type.
    2. Determines the likely root cause.
    3. Calculates a confidence value.
    4. Determines recovery probability.
    5. Applies safety guardrails.
    6. Returns a structured diagnosis.
    """

    # -----------------------------------------------------
    # Get payment information safely
    # -----------------------------------------------------

    payment_id = getattr(payment, "payment_id", None)

    failure_type = getattr(
        payment,
        "failure_type",
        "Payment Timeout"
    )

    retry_count = getattr(
        payment,
        "retry_count",
        0
    )

    cancellation_reason = getattr(
        payment,
        "cancellation_reason",
        None
    )

    # -----------------------------------------------------
    # PAYMENT TIMEOUT
    # -----------------------------------------------------

    if failure_type == "Payment Timeout":

        ml_confidence = 0.92

        # Safety guardrail:
        # Do not automatically retry if already retried.

        if retry_count >= 1:

            root_cause = "Repeated payment timeout"

            confidence = 0.88

            recovery_probability = "Low"

            recommended_action = "Escalate to human review"

            reason = (
                "The payment has already been retried. "
                "Further automatic retries could create "
                "unnecessary customer friction."
            )

            risk_level = "Medium"

            allowed = False

        else:

            root_cause = (
                "Temporary payment gateway or network timeout"
            )

            confidence = 0.88

            recovery_probability = "High"

            recommended_action = "Retry payment"

            reason = (
                "The payment timeout appears temporary and "
                "the payment has not been retried yet."
            )

            risk_level = "Low"

            allowed = True

        return {
            "payment_id": payment_id,
            "failure_type": failure_type,
            "ml_confidence": ml_confidence,
            "root_cause": root_cause,
            "confidence": confidence,
            "recovery_probability": recovery_probability,
            "recommended_action": recommended_action,
            "reason": reason,
            "risk_level": risk_level,
            "allowed": allowed,
        }

    # -----------------------------------------------------
    # PAYMENT CANCELLED
    # -----------------------------------------------------

    if failure_type == "Payment Cancelled":

        ml_confidence = 0.94

        # Use the cancellation reason if available.
        # Otherwise use a safe default.

        if cancellation_reason in CANCELLATION_REASONS:

            selected_reason = cancellation_reason

        else:

            selected_reason = (
                "Customer requested cancellation"
            )

        # -------------------------------------------------
        # Cancellation-specific diagnosis
        # -------------------------------------------------

        if selected_reason == "Customer requested cancellation":

            root_cause = "Customer intentionally cancelled payment"

            confidence = 0.96

            recovery_probability = "Low"

            recommended_action = "Do not retry payment"

            reason = (
                "The customer requested cancellation. "
                "Automatically retrying the payment could "
                "create an unwanted transaction."
            )

            risk_level = "High"

            allowed = False

        elif selected_reason == "Duplicate payment detected":

            root_cause = "Duplicate payment submission"

            confidence = 0.95

            recovery_probability = "Low"

            recommended_action = "Do not retry payment"

            reason = (
                "A duplicate payment was detected. "
                "Retrying could result in duplicate charges."
            )

            risk_level = "High"

            allowed = False

        elif selected_reason == "Payment authorization failed":

            root_cause = "Payment authorization failure"

            confidence = 0.93

            recovery_probability = "Low"

            recommended_action = "Escalate to human review"

            reason = (
                "The payment authorization failed. "
                "The payment should not be automatically retried "
                "without further verification."
            )

            risk_level = "High"

            allowed = False

        elif selected_reason == "Payment expired":

            root_cause = "Payment session expired"

            confidence = 0.91

            recovery_probability = "Medium"

            recommended_action = "Request new payment"

            reason = (
                "The original payment session has expired. "
                "A new payment attempt should be initiated."
            )

            risk_level = "Medium"

            allowed = False

        elif selected_reason == "Invalid payment details":

            root_cause = "Invalid payment information"

            confidence = 0.94

            recovery_probability = "Low"

            recommended_action = "Request updated payment details"

            reason = (
                "The supplied payment information is invalid. "
                "The customer must provide valid payment details."
            )

            risk_level = "High"

            allowed = False

        elif selected_reason == "Fraud risk detected":

            root_cause = "Potential fraudulent transaction"

            confidence = 0.97

            recovery_probability = "Very Low"

            recommended_action = "Escalate to human review"

            reason = (
                "The transaction was flagged for potential fraud. "
                "Automatic recovery is not permitted."
            )

            risk_level = "Critical"

            allowed = False

        elif selected_reason == "Insufficient funds":

            root_cause = "Insufficient account balance"

            confidence = 0.95

            recovery_probability = "Low"

            recommended_action = "Request alternative payment method"

            reason = (
                "The account does not have sufficient funds "
                "to complete the payment."
            )

            risk_level = "High"

            allowed = False

        elif selected_reason == "Merchant cancelled payment":

            root_cause = "Merchant cancelled the transaction"

            confidence = 0.96

            recovery_probability = "Low"

            recommended_action = "Do not retry payment"

            reason = (
                "The merchant cancelled the payment. "
                "Automatic retry is not appropriate."
            )

            risk_level = "High"

            allowed = False

        elif selected_reason == "Order cancelled":

            root_cause = "Related order was cancelled"

            confidence = 0.96

            recovery_probability = "Low"

            recommended_action = "Do not retry payment"

            reason = (
                "The related order was cancelled. "
                "The associated payment should not be retried."
            )

            risk_level = "High"

            allowed = False

        elif selected_reason == "Payment already completed":

            root_cause = "Payment was already completed"

            confidence = 0.98

            recovery_probability = "Very Low"

            recommended_action = "Do not retry payment"

            reason = (
                "Another transaction has already completed "
                "the payment. Retrying could cause a duplicate charge."
            )

            risk_level = "Critical"

            allowed = False

        else:

            root_cause = "Payment cancellation"

            confidence = 0.90

            recovery_probability = "Low"

            recommended_action = "Escalate to human review"

            reason = (
                "The payment was cancelled and requires "
                "additional verification."
            )

            risk_level = "Medium"

            allowed = False

        return {
            "payment_id": payment_id,
            "failure_type": failure_type,
            "cancellation_reason": selected_reason,
            "ml_confidence": ml_confidence,
            "root_cause": root_cause,
            "confidence": confidence,
            "recovery_probability": recovery_probability,
            "recommended_action": recommended_action,
            "reason": reason,
            "risk_level": risk_level,
            "allowed": allowed,
        }

    # -----------------------------------------------------
    # PAYMENT DECLINED
    # -----------------------------------------------------

    if failure_type == "Payment Declined":

        return {
            "payment_id": payment_id,
            "failure_type": failure_type,
            "ml_confidence": 0.93,
            "root_cause": "Payment was declined by the payment provider",
            "confidence": 0.91,
            "recovery_probability": "Low",
            "recommended_action": "Request alternative payment method",
            "reason": (
                "The payment provider declined the transaction. "
                "Automatic retry is not recommended."
            ),
            "risk_level": "High",
            "allowed": False,
        }

    # -----------------------------------------------------
    # INSUFFICIENT FUNDS
    # -----------------------------------------------------

    if failure_type == "Insufficient Funds":

        return {
            "payment_id": payment_id,
            "failure_type": failure_type,
            "ml_confidence": 0.95,
            "root_cause": "Insufficient funds",
            "confidence": 0.94,
            "recovery_probability": "Low",
            "recommended_action": "Request alternative payment method",
            "reason": (
                "The payment account does not have sufficient funds."
            ),
            "risk_level": "High",
            "allowed": False,
        }

    # -----------------------------------------------------
    # UNKNOWN FAILURE TYPE
    # -----------------------------------------------------

    return {
        "payment_id": payment_id,
        "failure_type": failure_type,
        "ml_confidence": 0.75,
        "root_cause": "Unknown payment failure",
        "confidence": 0.70,
        "recovery_probability": "Unknown",
        "recommended_action": "Escalate to human review",
        "reason": (
            "The failure type is not recognized by the "
            "automatic recovery policy."
        ),
        "risk_level": "High",
        "allowed": False,
    }