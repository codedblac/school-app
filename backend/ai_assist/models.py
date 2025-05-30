from django.db import models
from django.conf import settings  # Use the dynamic reference to avoid circular import

class AIInteractionLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prompt = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI Interaction by {self.user.get_full_name()} at {self.created_at}"
