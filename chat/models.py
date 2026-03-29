from django.db import models


class ChatMessage(models.Model):
    message = models.TextField()
    response = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
