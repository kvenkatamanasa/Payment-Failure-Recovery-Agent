from decimal import Decimal
import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect, render

from .models import Payment, RecoveryAudit


# ============================================================
# ADMIN ACCESS
# ============================================================

def admin_required(view_function):
    """
    Allows access only to logged-in staff/admin users.
    """

    return login_required(
        user_passes_test(
            lambda user: user.is_staff,
            login_url="home"
        )(view_function)
    )


# ============================================================
# LOGIN
# ============================================================

def login_view(request):
    """
    Login page for customers and administrators.
    """

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                f"Welcome, {user.username}!"
            )

            next_url = request.POST.get(
                "next"
            ) or request.GET.get(
                "next"
            )

            if next_url:
                return redirect(next_url)

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "registration/login.html"
    )


# ============================================================
# LOGOUT
# ============================================================

@login_required
def logout_view(request):
    """
    Logout the current Django user.
    """

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("login")


# ============================================================
# SIGNUP / REGISTER
# ============================================================

def signup_view(request):
    """
    Customer registration.
    """

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = UserCreationForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            login(
                request,
                user
            )

            messages.success(
                request,
                "Account created successfully."
            )

            return redirect("dashboard")

    else:

        form = UserCreationForm()

    return render(
        request,
        "registration/signup.html",
        {
            "form": form
        }
    )


# Compatibility alias
register_view = signup_view


# ============================================================
# FAILURE SCENARIOS
# ============================================================

FAILURE_SCENARIOS = [
    "Payment Timeout",
    "Network Error",
    "Insufficient Balance",
    "Payment Declined",
    "Bank Error",
    "UPI Failure",
    "Gateway Server Error",
    "Invalid Payment Details",
    "Authentication Failure",
]


# ============================================================
# FAILURE DETECTION
# ============================================================

def detect_failure(payment):
    """
    Detects the failure type from the payment failure reason.
    """

    reason = (
        payment.failure_reason or ""
    ).strip().lower()

    if not reason:

        return (
            "Unknown Failure",
            "The payment gateway did not provide a failure reason."
        )

    if (
        "timeout" in reason
        or "timed out" in reason
    ):

        return (
            "Payment Timeout",
            "Temporary payment gateway or network timeout."
        )

    if "network" in reason:

        return (
            "Network Error",
            "Network communication with the payment gateway failed."
        )

    if (
        "insufficient" in reason
        or "low balance" in reason
    ):

        return (
            "Insufficient Balance",
            "The account does not have sufficient funds."
        )

    if (
        "declined" in reason
        or "decline" in reason
        or "rejected" in reason
    ):

        return (
            "Payment Declined",
            "The bank or payment gateway declined the transaction."
        )

    if (
        "bank error" in reason
        or "bank failure" in reason
        or "bank" in reason
    ):

        return (
            "Bank Error",
            "The bank was unable to process the transaction."
        )

    if "upi" in reason:

        return (
            "UPI Failure",
            "The UPI transaction could not be completed."
        )

    if (
        "server" in reason
        or "gateway" in reason
    ):

        return (
            "Gateway Server Error",
            "The payment gateway encountered a server-side problem."
        )

    if (
        "invalid" in reason
        or "incorrect details" in reason
        or "wrong details" in reason
    ):

        return (
            "Invalid Payment Details",
            "The supplied payment information is invalid."
        )

    if (
        "authentication" in reason
        or "auth" in reason
        or "verification failed" in reason
    ):

        return (
            "Authentication Failure",
            "Payment authentication could not be completed."
        )

    return (
        "Unknown Failure",
        f"The payment gateway reported: {payment.failure_reason}"
    )


# ============================================================
# AI DIAGNOSIS
# ============================================================

def ai_diagnose(
    payment,
    failure_type,
    root_cause
):
    """
    Rule-based AI diagnosis engine.
    """

    if failure_type == "Payment Timeout":

        diagnosis = (
            "The transaction most likely failed because of a "
            "temporary payment gateway or network timeout."
        )

        confidence = 0.92
        action = "Retry payment"

    elif failure_type == "Network Error":

        diagnosis = (
            "The transaction appears to have failed because "
            "of a temporary network communication problem."
        )

        confidence = 0.90
        action = "Retry payment"

    elif failure_type == "Insufficient Balance":

        diagnosis = (
            "The payment failed because the available account "
            "balance may be insufficient."
        )

        confidence = 0.96

        action = (
            "Request customer to use another payment method"
        )

    elif failure_type == "Payment Declined":

        diagnosis = (
            "The transaction was declined by the bank or "
            "payment gateway."
        )

        confidence = 0.94

        action = (
            "Request customer to use another payment method"
        )

    elif failure_type == "Bank Error":

        diagnosis = (
            "The bank appears to have encountered a temporary "
            "processing problem."
        )

        confidence = 0.88
        action = "Retry payment"

    elif failure_type == "UPI Failure":

        diagnosis = (
            "The UPI transaction could not be completed. "
            "A temporary UPI or bank-side problem is possible."
        )

        confidence = 0.87
        action = "Retry payment"

    elif failure_type == "Gateway Server Error":

        diagnosis = (
            "The payment gateway appears to have encountered "
            "a server-side processing error."
        )

        confidence = 0.91
        action = "Retry payment"

    elif failure_type == "Invalid Payment Details":

        diagnosis = (
            "The payment information appears to contain "
            "invalid or incomplete details."
        )

        confidence = 0.95

        action = (
            "Request customer to correct payment details"
        )

    elif failure_type == "Authentication Failure":

        diagnosis = (
            "Payment authentication could not be completed."
        )

        confidence = 0.93
        action = "Request customer authentication"

    else:

        diagnosis = (
            "The available payment information does not "
            "identify a specific failure cause."
        )

        confidence = 0.65
        action = "Retry payment"

    return (
        diagnosis,
        confidence,
        action
    )


# ============================================================
# SAFETY GUARDRAIL
# ============================================================

def safety_guardrail(
    payment,
    recommended_action
):
    """
    Determines whether the recovery action is safe.
    """

    amount = (
        payment.amount
        or Decimal("0.00")
    )

    # --------------------------------------------------------
    # HIGH VALUE TRANSACTION
    # --------------------------------------------------------

    if amount > Decimal("10000.00"):

        return {

            "allowed": False,

            "policy_action":
                "Manual review required",

            "risk_level":
                "HIGH",

            "reason": (
                "High-value payment requires manual verification "
                "before automated recovery."
            )
        }

    # --------------------------------------------------------
    # SAFE ACTIONS
    # --------------------------------------------------------

    safe_actions = [

        "Retry payment",

        "Request customer to use another payment method",

        "Request customer to correct payment details",

        "Request customer authentication",
    ]

    if recommended_action in safe_actions:

        return {

            "allowed": True,

            "policy_action":
                recommended_action,

            "risk_level":
                "LOW",

            "reason": (
                "Action passed the payment safety policy."
            )
        }

    # --------------------------------------------------------
    # UNSAFE ACTION
    # --------------------------------------------------------

    return {

        "allowed": False,

        "policy_action":
            "Manual review required",

        "risk_level":
            "MEDIUM",

        "reason": (
            "Recovery action is not approved by the safety policy."
        )
    }


# ============================================================
# RECOVERY EXECUTION
# ============================================================

def execute_recovery(
    payment,
    guardrail
):
    """
    Executes the recovery action only after safety approval.
    """

    # --------------------------------------------------------
    # BLOCKED ACTION
    # --------------------------------------------------------

    if not guardrail["allowed"]:

        payment.status = "FAILED"

        payment.recovery_result = (
            "Recovery action was blocked by the safety guardrail."
        )

        payment.revenue_recovered = (
            Decimal("0.00")
        )

        return {

            "executed": False,

            "status": "FAILED",

            "result": (
                "Recovery action was blocked by "
                "the safety guardrail."
            ),

            "revenue_recovered":
                Decimal("0.00")
        }

    action = guardrail["policy_action"]

    # --------------------------------------------------------
    # RETRY PAYMENT
    # --------------------------------------------------------

    if action == "Retry payment":

        payment.retry_count += 1

        payment.status = "RECOVERED"

        payment.recovery_result = (
            "Simulated retry executed successfully"
        )

        payment.revenue_recovered = (
            payment.amount
        )

        return {

            "executed": True,

            "status": "RECOVERED",

            "result": (
                "Simulated retry executed successfully"
            ),

            "revenue_recovered":
                payment.amount
        }

    # --------------------------------------------------------
    # CUSTOMER ACTION REQUIRED
    # --------------------------------------------------------

    payment.status = "FAILED"

    payment.recovery_result = (
        "Customer action required before recovery."
    )

    payment.revenue_recovered = (
        Decimal("0.00")
    )

    return {

        "executed": False,

        "status": "FAILED",

        "result": (
            "Customer action required before recovery."
        ),

        "revenue_recovered":
            Decimal("0.00")
    }


# ============================================================
# DASHBOARD
# ============================================================

@login_required
def dashboard(request):
    """
    Main dashboard for customers and administrators.
    """

    if request.user.is_staff:

        payments = Payment.objects.all()

    else:

        payments = Payment.objects.filter(
            user=request.user
        )

    total_payments = payments.count()

    failed_payments = payments.filter(
        status__iexact="FAILED",
        revenue_recovered__lte=0
    ).count()

    recovered_payments = payments.filter(
        revenue_recovered__gt=0
    ).count()

    revenue_recovered = (
        payments.aggregate(
            total=Sum("revenue_recovered")
        )["total"]
        or Decimal("0.00")
    )

    revenue_at_risk = (
        payments.filter(
            status__iexact="FAILED",
            revenue_recovered__lte=0
        ).aggregate(
            total=Sum("amount")
        )["total"]
        or Decimal("0.00")
    )

    if total_payments > 0:

        recovery_rate = (
            recovered_payments /
            total_payments
        ) * 100

    else:

        recovery_rate = 0

    payments = payments.order_by("-id")

    context = {

        "current_user":
            request.user,

        "is_admin":
            request.user.is_staff,

        "payments":
            payments,

        "total_payments":
            total_payments,

        "failed_payments":
            failed_payments,

        "recovered_payments":
            recovered_payments,

        "revenue_recovered":
            revenue_recovered,

        "revenue_at_risk":
            revenue_at_risk,

        "recovery_rate":
            round(
                recovery_rate,
                2
            ),
    }

    return render(
        request,
        "payments/dashboard.html",
        context
    )


# ============================================================
# HOME
# ============================================================

@login_required
def home(request):
    """
    Compatibility view.
    """

    return dashboard(request)


# ============================================================
# MAKE PAYMENT
# ============================================================

@login_required
def make_payment(request):
    """
    Creates a simulated payment and runs:

    1. Failure detection
    2. AI diagnosis
    3. Safety guardrail
    4. Recovery execution
    5. Audit trail
    """

    if request.method == "POST":

        payment_id = request.POST.get(
            "payment_id",
            ""
        ).strip()

        order_id = request.POST.get(
            "order_id",
            ""
        ).strip()

        amount = request.POST.get(
            "amount",
            ""
        ).strip()

        payment_method = request.POST.get(
            "payment_method",
            "UPI"
        ).strip()

        bank = request.POST.get(
            "bank",
            "Test Bank"
        ).strip()

        failure_reason = request.POST.get(
            "failure_reason",
            ""
        ).strip()

        if not failure_reason:

            failure_reason = random.choice(
                FAILURE_SCENARIOS
            )

        # ----------------------------------------------------
        # AMOUNT VALIDATION
        # ----------------------------------------------------

        try:

            amount_value = Decimal(
                amount
            )

            if amount_value <= 0:
                raise ValueError

        except (
            TypeError,
            ValueError,
            ArithmeticError
        ):

            messages.error(
                request,
                "Please enter a valid payment amount."
            )

            return render(
                request,
                "payments/make_payment.html"
            )

        # ----------------------------------------------------
        # GENERATE IDs
        # ----------------------------------------------------

        next_number = (
            Payment.objects.count() + 1
        )

        if not payment_id:

            payment_id = (
                f"user_{request.user.id}_payment_"
                f"{next_number}"
            )

        if not order_id:

            order_id = (
                f"user_{request.user.id}_order_"
                f"{next_number}"
            )

        # ----------------------------------------------------
        # CREATE PAYMENT
        # ----------------------------------------------------

        payment = Payment.objects.create(

            user=request.user,

            payment_id=payment_id,

            order_id=order_id,

            amount=amount_value,

            payment_method=payment_method,

            bank=bank,

            failure_type="",

            failure_reason=failure_reason,

            cancellation_reason=None,

            status="FAILED",

            retry_count=0,

            ai_diagnosis="",

            ai_confidence=None,

            recovery_action="",

            recovery_result="",

            revenue_recovered=Decimal("0.00")
        )

        # ====================================================
        # 1. FAILURE DETECTION
        # ====================================================

        failure_type, root_cause = detect_failure(
            payment
        )

        payment.failure_type = failure_type

        # ====================================================
        # 2. AI DIAGNOSIS
        # ====================================================

        (
            diagnosis,
            confidence,
            recommended_action
        ) = ai_diagnose(
            payment,
            failure_type,
            root_cause
        )

        payment.ai_diagnosis = diagnosis

        payment.ai_confidence = confidence

        payment.recovery_action = recommended_action

        # ====================================================
        # 3. SAFETY GUARDRAIL
        # ====================================================

        guardrail = safety_guardrail(
            payment,
            recommended_action
        )

        # ====================================================
        # 4. RECOVERY EXECUTION
        # ====================================================

        recovery = execute_recovery(
            payment,
            guardrail
        )

        payment.status = (
            recovery["status"]
        )

        payment.recovery_result = (
            recovery["result"]
        )

        payment.revenue_recovered = (
            recovery["revenue_recovered"]
        )

        payment.save()

        # ====================================================
        # 5. AUDIT TRAIL
        # ====================================================

        RecoveryAudit.objects.create(

            payment=payment,

            failure_type=failure_type,

            cancellation_reason=(
                payment.cancellation_reason
            ),

            root_cause=root_cause,

            recommended_action=(
                recommended_action
            ),

            confidence=confidence,

            policy_action=(
                guardrail["policy_action"]
            ),

            allowed=(
                guardrail["allowed"]
            ),

            risk_level=(
                guardrail["risk_level"]
            ),

            executed=(
                recovery["executed"]
            ),

            result=(
                recovery["result"]
            ),

            reason=(
                guardrail["reason"]
            )
        )

        return redirect(
            "payment_result",
            payment_id=payment.id
        )

    return render(
        request,
        "payments/make_payment.html"
    )


# ============================================================
# PAYMENT RESULT
# ============================================================

@login_required
def payment_result(
    request,
    payment_id
):
    """
    Displays complete payment failure/recovery details.
    """

    # --------------------------------------------------------
    # ACCESS CONTROL
    # --------------------------------------------------------

    if request.user.is_staff:

        payment = get_object_or_404(
            Payment,
            id=payment_id
        )

    else:

        payment = get_object_or_404(
            Payment,
            id=payment_id,
            user=request.user
        )

    # --------------------------------------------------------
    # LATEST AUDIT
    # --------------------------------------------------------

    latest_audit = (
        RecoveryAudit.objects
        .filter(
            payment=payment
        )
        .order_by("-id")
        .first()
    )

    # --------------------------------------------------------
    # FAILURE TYPE
    # --------------------------------------------------------

    failure_type = (
        payment.failure_type
        or ""
    ).strip()

    if (
        not failure_type
        and latest_audit
    ):

        failure_type = (
            latest_audit.failure_type
            or ""
        ).strip()

    if not failure_type:

        failure_type = (
            "Unknown Failure"
        )

    # --------------------------------------------------------
    # CONFIDENCE
    # --------------------------------------------------------

    confidence_percent = None

    if payment.ai_confidence is not None:

        confidence_percent = round(
            float(
                payment.ai_confidence
            ) * 100,
            1
        )

    # --------------------------------------------------------
    # DEFAULT VALUES
    # --------------------------------------------------------

    ai_diagnosis = (
        payment.ai_diagnosis
        or "Not analyzed"
    )

    recovery_action = (
        payment.recovery_action
        or "Not available"
    )

    recovery_result = (
        payment.recovery_result
        or "No recovery attempt"
    )

    # --------------------------------------------------------
    # CONTEXT
    # --------------------------------------------------------

    context = {

        "payment":
            payment,

        "audit":
            latest_audit,

        "latest_audit":
            latest_audit,

        "failure_type":
            failure_type,

        "confidence_percent":
            confidence_percent,

        "ai_diagnosis":
            ai_diagnosis,

        "recovery_action":
            recovery_action,

        "recovery_result":
            recovery_result,

        "is_admin":
            request.user.is_staff,
    }

    return render(
        request,
        "payments/payment_result.html",
        context
    )


# ============================================================
# ADMIN RECOVERY DASHBOARD
# ============================================================

@admin_required
def recovery_dashboard(request):

    total_payments = (
        Payment.objects.count()
    )

    recovered_payments = (
        Payment.objects.filter(
            revenue_recovered__gt=0
        ).count()
    )

    failed_payments = (
        Payment.objects.filter(
            status__iexact="FAILED",
            revenue_recovered__lte=0
        ).count()
    )

    blocked_actions = (
        RecoveryAudit.objects.filter(
            allowed=False
        ).count()
    )

    revenue_recovered = (
        Payment.objects.aggregate(
            total=Sum(
                "revenue_recovered"
            )
        )["total"]
        or Decimal("0.00")
    )

    if total_payments > 0:

        recovery_rate = (
            recovered_payments /
            total_payments
        ) * 100

    else:

        recovery_rate = 0

    failure_type_distribution = (
        Payment.objects
        .filter(
            status__iexact="FAILED",
            revenue_recovered__lte=0
        )
        .exclude(
            failure_type__isnull=True
        )
        .exclude(
            failure_type__exact=""
        )
        .values(
            "failure_type"
        )
        .annotate(
            count=Count("id")
        )
        .order_by("-count")
    )

    context = {

        "total_payments":
            total_payments,

        "failed_payments":
            failed_payments,

        "recovered_payments":
            recovered_payments,

        "blocked_actions":
            blocked_actions,

        "revenue_recovered":
            revenue_recovered,

        "recovery_rate":
            round(
                recovery_rate,
                2
            ),

        "failure_type_distribution":
            failure_type_distribution,
    }

    return render(
        request,
        "payments/recovery_dashboard.html",
        context
    )


# ============================================================
# AUDIT TRAIL
# ============================================================

@admin_required
def audit_trail(request):

    audits = (
        RecoveryAudit.objects
        .select_related("payment")
        .order_by("-id")
    )

    return render(
        request,
        "payments/audit_trail.html",
        {
            "audits": audits
        }
    )