from django.db import models

from django.db import models
from accounts.models import User

class AIInteractionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI Interaction by {self.user.username} at {self.created_at}"
