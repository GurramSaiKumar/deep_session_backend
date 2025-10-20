from django.conf import settings
from django.db import models
from django.utils import timezone


class NewFocusSession(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('interrupted', 'Interrupted'),
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='new_focus_sessions')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    target_duration_seconds = models.PositiveIntegerField(default=0)  # User-set duration in seconds
    actual_duration_seconds = models.PositiveIntegerField(default=0)  # Calculated on end
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    goal_name = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    interrupted = models.BooleanField(default=False)

    def complete_session(self, interrupted=False, notes=None):
        if self.end_time:
            duration = int((self.end_time - self.start_time).total_seconds())
            self.actual_duration_seconds = duration
        self.status = 'interrupted' if interrupted else 'completed'
        self.interrupted = interrupted
        if notes is not None:
            self.notes = notes
        self.save()