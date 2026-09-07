from payments.ai.payment_gateway import (
    PaymentGatewaySimulator
)


def execute_recovery(
    payment,
    policy,
    gateway=None
):
    """
    Execute a recovery action only when
    the safety policy allows it.

    Uses the Payment Gateway Simulator.
    """

    if gateway is None:
        gateway = PaymentGatewaySimulator()

    # --------------------------------------------------
    # SAFETY GUARDRAIL
    # --------------------------------------------------

    if not policy.get("allowed", False):

        return {
            "executed": False,
            "action": policy.get(
                "action",
                "Escalate to human review"
            ),
            "result":
                "Blocked by safety policy",
            "message":
                "Automatic recovery was not permitted.",
        }

    action = policy.get("action")

    # --------------------------------------------------
    # RETRY PAYMENT
    # --------------------------------------------------

    if action == "Retry payment":

        gateway_payment = gateway.get_payment(
            payment.payment_id
        )

        if not gateway_payment:

            gateway_payment = gateway.create_payment(
                payment_id=payment.payment_id,
                amount=float(payment.amount),
                failure_reason=payment.failure_reason,
            )

        gateway_result = gateway.retry_payment(
            payment.payment_id
        )

        payment.retry_count += 1
        payment.recovery_action = "Retry payment"

        if gateway_result["success"]:

            payment.recovery_result = (
                "Payment recovered successfully"
            )

            payment.revenue_recovered = (
                payment.amount
            )

        else:

            payment.recovery_result = (
                gateway_result["message"]
            )

        payment.save()

        return {
            "executed": True,
            "action": "Retry payment",
            "result":
                gateway_result["message"],
            "gateway_status":
                gateway_result.get("status"),
            "message":
                "Recovery action executed "
                "through the Payment Gateway Simulator.",
        }

    # --------------------------------------------------
    # ALTERNATE PAYMENT METHOD
    # --------------------------------------------------

    if action in [
        "Request alternate payment method",
        "Suggest alternate payment method",
    ]:

        payment.recovery_action = action

        payment.recovery_result = (
            "Alternate payment method requested"
        )

        payment.save()

        return {
            "executed": True,
            "action": action,
            "result":
                "Alternate payment method requested",
            "message":
                "Customer should provide "
                "an alternate payment method.",
        }

    # --------------------------------------------------
    # UNKNOWN ACTION
    # --------------------------------------------------

    return {
        "executed": False,
        "action": action,
        "result": "Blocked",
        "message":
            "Unknown recovery action. "
            "Human review required.",
    }