
from django.contrib import admin
from .models import Order, Consultation, UserProfile


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'reference',
        'name',
        'email',
        'total',
        'payment_method',
        'payment_status',
        'status',
        'created_at',
    )

    list_filter = (
        'payment_status',
        'payment_method',
        'status',
        'created_at',
    )

    search_fields = (
        'reference',
        'name',
        'email',
        'phone',
    )

    readonly_fields = (
        'reference',
        'customer_token',
        'created_at',
        'paid_at',
    )


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = (
        'reference', 'name', 'email', 'service', 'status', 'created_at'
    )
    list_filter = ('status', 'service', 'created_at')
    search_fields = ('reference', 'name', 'email', 'service')
    readonly_fields = ('reference', 'created_at')


admin.site.register(UserProfile)
