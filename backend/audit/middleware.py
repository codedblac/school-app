from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .utils import log_action

class AuditMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Store IP for later use in logging
        ip = self.get_client_ip(request)
        request.ip_address = ip

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = getattr(request, 'ip_address', None)
    log_action(user=user, action='logged_in', description='User logged in', ip_address=ip)

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ip = getattr(request, 'ip_address', None)
    log_action(user=user, action='logged_out', description='User logged out', ip_address=ip)
