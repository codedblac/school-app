from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from students.models import Student

class FeeCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # default fee amount

    def __str__(self):
        return self.name
    class Meta:
        permissions = [
            ("manage_payments", "Can add, change or delete payments"),
            ("view_all_payments", "Can view all payments in the system"),
        ]

class PaymentMethod(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., M-Pesa, Cash, Card

    def __str__(self):
        return self.name

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    fee_category = models.ForeignKey(FeeCategory, on_delete=models.SET_NULL, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    transaction_reference = models.CharField(max_length=255, blank=True, null=True)  # e.g., M-Pesa transaction code
    paid_on = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='recorded_payments')

    class Meta:
        ordering = ['-paid_on']

    def __str__(self):
        return f"{self.student} paid {self.amount_paid} for {self.fee_category}"

class Invoice(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='invoices')
    fee_category = models.ForeignKey(FeeCategory, on_delete=models.SET_NULL, null=True)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    generated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-generated_on']

    def __str__(self):
        return f"Invoice {self.id} for {self.student} - {self.fee_category}"
    
    class Meta:
        permissions = [
            ("view_all_invoices", "Can view all invoices in the system"),
        ]


