
from django.db import models
from django.contrib.auth.models import User


class SWOTAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    idea = models.TextField()
    strengths = models.TextField()
    weaknesses = models.TextField()
    opportunities = models.TextField()
    threats = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.category} - {self.user.username}'


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback from {self.user.username}'

# Create your models here.
