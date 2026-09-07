class PaymentGatewaySimulator:
    """
    Simulated payment gateway.

    This does not connect to any real payment provider.
    It is used only for development and testing.
    """

    def __init__(self):
        self.payments = {}

    def create_payment(
        self,
        payment_id,
        amount,
        failure_reason=None
    ):
        """
        Create a simulated payment.
        """

        payment = {
            "payment_id": payment_id,
            "amount": amount,
            "status": "failed" if failure_reason else "created",
            "failure_reason": failure_reason,
            "attempts": 0,
        }

        self.payments[payment_id] = payment

        return payment

    def get_payment(self, payment_id):
        """
        Get a simulated payment.
        """

        return self.payments.get(payment_id)

    def retry_payment(self, payment_id):
        """
        Simulate a payment retry.

        The retry is bounded by the recovery agent,
        not by this simulator.
        """

        payment = self.payments.get(payment_id)

        if not payment:
            return {
                "success": False,
                "message": "Payment not found",
            }

        payment["attempts"] += 1

        # Simulate successful recovery after one retry
        if payment["attempts"] == 1:

            payment["status"] = "success"
            payment["failure_reason"] = None

            return {
                "success": True,
                "status": "success",
                "message":
                    "Payment successfully recovered",
            }

        return {
            "success": False,
            "status": payment["status"],
            "message":
                "Payment retry was unsuccessful",
        }

    def cancel_payment(self, payment_id):
        """
        Simulate cancellation.
        """

        payment = self.payments.get(payment_id)

        if not payment:
            return {
                "success": False,
                "message": "Payment not found",
            }

        payment["status"] = "cancelled"

        return {
            "success": True,
            "status": "cancelled",
            "message":
                "Payment cancelled",
        }