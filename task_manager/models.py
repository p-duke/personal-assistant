from django.db import models
from django.utils import timezone

# Create your models here.
class Task(models.Model):

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        NORMAL = "normal", "Normal"
        HIGH = "high", "High"

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        COMPLETE = "complete", "Complete"

    title = models.CharField(max_length=255)
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.NORMAL
    )
    due_date = models.DateTimeField(null=True, blank=True)
    estimated_duration = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Duration in minutes"
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.OPEN
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["status", "due_date", "-priority", "created_at"]

    def mark_complete(self):
        self.status = Status.COMPLETE
        self.completed_at = timezone.now()
        self.save(update_fields=["status", "completed_at", "updated_at"])

    def __str__(self):
        return self.title

