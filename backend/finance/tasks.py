from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
from .models import Invoice
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_payment_due_reminders():
    upcoming_due_date = now().date() + timedelta(days=3)
    invoices_due = Invoice.objects.filter(is_paid=False, due_date=upcoming_due_date)

    for invoice in invoices_due:
        user_email = invoice.student.user.email
        subject = "Payment Due Reminder"
        message = (
            f"Dear {invoice.student.user.get_full_name()},\n\n"
            f"This is a reminder that your payment of KES {invoice.amount_due} "
            f"for {invoice.fee_category.name} is due on {invoice.due_date}.\n\n"
            "Please make payment before the due date to avoid penalties.\n"
            "Thank you.\nSchool Finance Department"
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
