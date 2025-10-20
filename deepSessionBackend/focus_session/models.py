from django.db import models
from django.conf import settings
from django.utils import timezone


class FocusSession(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
    ]
    focus_session_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='focus_sessions')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    goal_name = models.CharField(max_length=255, blank=True, null=True)  # optional: “Deep work”, “Study”, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def complete_session(self):
        if self.end_time:
            duration = (self.end_time - self.start_time).total_seconds() / 60
            self.duration_minutes = int(duration)
        self.status = 'completed'
        self.save()
