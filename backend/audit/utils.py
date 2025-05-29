from .models import AuditLog
from django.contrib.contenttypes.models import ContentType

def log_action(user=None, action='', instance=None, description='', ip_address=None):
    content_type = None
    object_id = None
    
    if instance:
        content_type = ContentType.objects.get_for_model(instance)
        object_id = instance.pk

    AuditLog.objects.create(
        user=user,
        action=action,
        content_type=content_type,
        object_id=object_id,
        description=description,
        ip_address=ip_address
    )
