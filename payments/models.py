from django.db import models
from django.contrib.auth.models import User


# ============================================================
# PAYMENT MODEL
# ============================================================

class Payment(models.Model):
    """
    Stores payment transaction information,
    failure detection, AI diagnosis, recovery action,
    recovery result and recovered revenue.
    """

    # --------------------------------------------------------
    # CUSTOMER
    # --------------------------------------------------------

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="payments"
    )

    # --------------------------------------------------------
    # PAYMENT INFORMATION
    # --------------------------------------------------------

    payment_id = models.CharField(
        max_length=255,
        unique=True
    )

    order_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    payment_method = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    bank = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # --------------------------------------------------------
    # FAILURE DETECTION
    # --------------------------------------------------------

    failure_type = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    failure_reason = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    cancellation_reason = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=50,
        default="FAILED"
    )

    # --------------------------------------------------------
    # RETRY INFORMATION
    # --------------------------------------------------------

    retry_count = models.PositiveIntegerField(
        default=0
    )

    # --------------------------------------------------------
    # AI DIAGNOSIS
    # --------------------------------------------------------

    ai_diagnosis = models.TextField(
        blank=True,
        null=True
    )

    ai_confidence = models.FloatField(
        blank=True,
        null=True
    )

    # --------------------------------------------------------
    # RECOVERY
    # --------------------------------------------------------

    recovery_action = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    recovery_result = models.TextField(
        blank=True,
        null=True
    )

    revenue_recovered = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    # --------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # --------------------------------------------------------
    # STRING REPRESENTATION
    # --------------------------------------------------------

    def __str__(self):
        return self.payment_id


# ============================================================
# RECOVERY AUDIT MODEL
# ============================================================

class RecoveryAudit(models.Model):
    """
    Complete audit trail for:

    1. Failure Detection
    2. AI Diagnosis
    3. Safety Guardrail
    4. Recovery Decision
    5. Recovery Execution
    """

    # --------------------------------------------------------
    # PAYMENT
    # --------------------------------------------------------

    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name="recovery_audits"
    )

    # --------------------------------------------------------
    # FAILURE DETECTION
    # --------------------------------------------------------

    failure_type = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    cancellation_reason = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # --------------------------------------------------------
    # AI ANALYSIS
    # --------------------------------------------------------

    root_cause = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    recommended_action = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    confidence = models.FloatField(
        blank=True,
        null=True
    )

    # --------------------------------------------------------
    # SAFETY GUARDRAIL
    # --------------------------------------------------------

    policy_action = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    allowed = models.BooleanField(
        default=False
    )

    risk_level = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    # --------------------------------------------------------
    # RECOVERY EXECUTION
    # --------------------------------------------------------

    executed = models.BooleanField(
        default=False
    )

    result = models.TextField(
        blank=True,
        null=True
    )

    reason = models.TextField(
        blank=True,
        null=True
    )

    # --------------------------------------------------------
    # TIMESTAMP
    # --------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # --------------------------------------------------------
    # STRING REPRESENTATION
    # --------------------------------------------------------

    def __str__(self):
        return f"Audit {self.id} - {self.payment.payment_id}"