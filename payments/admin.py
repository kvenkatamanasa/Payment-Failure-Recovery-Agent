from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "payment_id",
        "order_id",
        "amount",
        "payment_method",
        "bank",
        "status",
        "retry_count",
        "revenue_recovered",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_method",
        "bank",
    )

    search_fields = (
        "payment_id",
        "order_id",
        "failure_reason",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )