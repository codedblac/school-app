from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment, Invoice
from django.core.mail import send_mail
from django.conf import settings
from .models import Payment


@receiver(post_save, sender=Payment)
def mark_invoice_paid(sender, instance, **kwargs):
    invoices = Invoice.objects.filter(student=instance.student, fee_category=instance.fee_category, is_paid=False)
    for invoice in invoices:
        if instance.amount_paid >= invoice.amount_due:
            invoice.is_paid = True
            invoice.save()


@receiver(post_save, sender=Payment)
def payment_notification(sender, instance, created, **kwargs):
    if not created:
        return

    user_email = instance.student.user.email
    subject = "Payment Confirmation"
    message = (
        f"Dear {instance.student.user.get_full_name()},\n\n"
        f"Your payment of KES {instance.amount_paid} for {instance.fee_category.name} "
        f"has been received successfully on {instance.paid_on.strftime('%Y-%m-%d %H:%M')}.\n\n"
        f"Transaction Reference: {instance.transaction_reference}\n\n"
        "Thank you.\nSchool Finance Department"
    )
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
    except Exception as e:
        print(f"Failed to send payment confirmation email: {e}")