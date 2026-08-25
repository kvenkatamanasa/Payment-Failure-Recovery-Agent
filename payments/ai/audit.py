from payments.models import RecoveryAudit


def create_recovery_audit(
    payment,
    diagnosis,
    policy,
    execution_result
):
    """
    Store a complete record of the recovery decision.
    """

    audit = RecoveryAudit.objects.create(
        payment=payment,

        failure_type=diagnosis.get(
            "failure_type"
        ),

        root_cause=diagnosis.get(
            "root_cause"
        ),

        recommended_action=diagnosis.get(
            "recommended_action"
        ),

        policy_action=policy.get(
            "action"
        ),

        allowed=policy.get(
            "allowed",
            False
        ),

        executed=execution_result.get(
            "executed",
            False
        ),

        result=execution_result.get(
            "result"
        ),

        reason=(
            diagnosis.get("reason")
            or policy.get("reason")
        ),

        risk_level=diagnosis.get(
            "risk_level"
        ),

        confidence=diagnosis.get(
            "confidence",
            0.0
        ),
    )

    return audit