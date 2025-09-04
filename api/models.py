from django.db import models
from django.utils import timezone

from users.models import CustomUser


# Create your models here.
class Task(models.Model):
    PRIORITY_CHOICES = [
        ("0", "None"),
        ("1", "High"),
        ("2", "Medium"),
        ("3", "Low")
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_done = models.BooleanField(default=False)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default=0)
    deadline = models.DateTimeField(blank=True, null=True)

    def str(self):
        return self.name
