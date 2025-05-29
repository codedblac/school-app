from django.core.mail import send_mail
from django.conf import settings

def notify_payment_failure(student, fee_category, amount, reason):
    user_email = student.user.email
    subject = "Payment Failed"
    message = (
        f"Dear {student.user.get_full_name()},\n\n"
        f"Your attempted payment of KES {amount} for {fee_category.name} has failed.\n"
        f"Reason: {reason}\n\n"
        "Please try again or contact support.\nSchool Finance Department"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
