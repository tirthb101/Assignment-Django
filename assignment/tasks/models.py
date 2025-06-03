from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')  # task owner

    subject = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    module = models.CharField(max_length=100)
    assigned_to = models.CharField(max_length=100)
    approver = models.CharField(max_length=100)
    estimated_minutes = models.PositiveIntegerField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    source = models.CharField(max_length=200)
    out_of_duties_task = models.BooleanField(default=False)
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], default='medium')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
    ], default='pending')
    completion_percentage = models.PositiveIntegerField(default=0)  # 0 to 100
    attachments = models.FileField(upload_to='attachments/', blank=True, null=True)

    # is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.subject
