from decimal import Decimal

from payments.models import Payment
from payments.ai.classifier import classify_failure
from payments.ai.diagnosis import diagnose_payment
from payments.ai.policy import evaluate_recovery_policy


def create_test_payments(count=50):
    """
    Create synthetic payment failures for batch testing.
    """

    failure_types = [
        "timeout",
        "insufficient funds",
        "declined",
        "network error",
        "unknown error",
    ]

    payments = []

    for i in range(count):

        failure_reason = failure_types[i % len(failure_types)]

        payment = Payment.objects.create(
            payment_id=f"batch_test_{i + 1:03d}",
            order_id=f"order_{i + 1:03d}",
            amount=Decimal("1000.00"),
            payment_method="UPI",
            bank="Test Bank",
            failure_reason=failure_reason,
            status="Failed",
            retry_count=0,
            ai_diagnosis="",
            ai_confidence=0.0,
            recovery_action="",
            recovery_result="",
            revenue_recovered=Decimal("0.00"),
        )

        payments.append(payment)

    return payments


def run_batch_test(payments):
    """
    Run classifier, diagnosis and policy evaluation
    for all test payments.
    """

    results = []

    for payment in payments:

        classification = classify_failure(payment)

        diagnosis = diagnose_payment(payment)

        policy = evaluate_recovery_policy(
            payment,
            diagnosis
        )

        results.append({
            "payment_id": payment.payment_id,
            "actual_failure": payment.failure_reason,
            "predicted_failure":
                classification["failure_type"],
            "ml_confidence":
                classification["confidence"],
            "recommended_action":
                diagnosis["recommended_action"],
            "allowed":
                policy["allowed"],
        })

    return results