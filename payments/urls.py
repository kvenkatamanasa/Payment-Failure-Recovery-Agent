from django.urls import path

from . import views


urlpatterns = [

    # ============================================================
    # AUTHENTICATION
    # ============================================================

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    path(
        "signup/",
        views.signup_view,
        name="signup"
    ),

    path(
        "register/",
        views.register_view,
        name="register"
    ),

    # ============================================================
    # DASHBOARD
    # ============================================================

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    # ============================================================
    # PAYMENT
    # ============================================================

    path(
        "make-payment/",
        views.make_payment,
        name="make_payment"
    ),

    path(
        "payment-result/<int:payment_id>/",
        views.payment_result,
        name="payment_result"
    ),

    # ============================================================
    # ADMIN
    # ============================================================

    path(
        "recovery-dashboard/",
        views.recovery_dashboard,
        name="recovery_dashboard"
    ),

    path(
        "audit-trail/",
        views.audit_trail,
        name="audit_trail"
    ),
]