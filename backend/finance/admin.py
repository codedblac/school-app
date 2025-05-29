from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import FeeCategory, PaymentMethod, Payment, Invoice

@admin.register(FeeCategory)
class FeeCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'description']
    search_fields = ['name']

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'fee_category', 'amount_paid', 'payment_method', 'paid_on', 'recorded_by']
    list_filter = ['fee_category', 'payment_method', 'paid_on']
    search_fields = ['student__user__username', 'transaction_reference']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['student', 'fee_category', 'amount_due', 'due_date', 'is_paid', 'generated_on']
    list_filter = ['is_paid', 'due_date']
    search_fields = ['student__user__username']
