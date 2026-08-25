from decimal import Decimal


MAX_AUTOMATIC_RETRIES = 1
HIGH_VALUE_THRESHOLD = Decimal("50000")


def evaluate_recovery_policy(payment, diagnosis):
    """
    Decide whether the recommended recovery action is safe to execute.
    """

    retry_count = payment.retry_count or 0
    amount = payment.amount or Decimal("0")

    action = diagnosis.get("recommended_action")
    risk_level = diagnosis.get("risk_level")

    # --------------------------------------------------
    # DEFAULT POLICY RESULT
    # --------------------------------------------------

    policy = {
        "allowed": False,
        "action": "Escalate to human review",
        "reason": "Recovery action is not permitted by policy.",
        "risk_level": risk_level,
    }

    # --------------------------------------------------
    # RULE 1 — ALREADY RETRIED
    # --------------------------------------------------

    if retry_count >= MAX_AUTOMATIC_RETRIES:

        policy.update({
            "allowed": False,
            "action": "Escalate to human review",
            "reason":
                "Maximum automatic retry limit has been reached.",
        })

        return policy

    # --------------------------------------------------
    # RULE 2 — HIGH VALUE TRANSACTION
    # --------------------------------------------------

    if amount >= HIGH_VALUE_THRESHOLD:

        policy.update({
            "allowed": False,
            "action": "Human approval required",
            "reason":
                "High-value transactions require human approval.",
            "risk_level": "High",
        })

        return policy

    # --------------------------------------------------
    # RULE 3 — RETRY PAYMENT
    # --------------------------------------------------

    if action == "Retry payment":

        if risk_level == "Low":

            policy.update({
                "allowed": True,
                "action": "Retry payment",
                "reason":
                    "A single bounded retry is permitted for this "
                    "low-risk failure.",
            })

        return policy

    # --------------------------------------------------
    # RULE 4 — ALTERNATE PAYMENT METHOD
    # --------------------------------------------------

    if action in [
        "Request alternate payment method",
        "Suggest alternate payment method",
    ]:

        policy.update({
            "allowed": True,
            "action": action,
            "reason":
                "Using an alternate payment method does not "
                "repeat the failed transaction.",
        })

        return policy

    # --------------------------------------------------
    # RULE 5 — HUMAN REVIEW
    # --------------------------------------------------

    if action in [
        "Escalate to human review",
        "Human approval required",
    ]:

        policy.update({
            "allowed": False,
            "action": action,
            "reason":
                "This action requires human intervention.",
        })

        return policy

    return policy