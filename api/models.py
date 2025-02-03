from django.db import models
from django.utils import timezone

from users.models import CustomUser


# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_done = models.BooleanField(default=False)
    deadline = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name