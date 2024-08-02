from django.db import models
from account.models import Account


# Create your models here.

class Conversation(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    message = models.TextField(max_length=1000)
    response = models.TextField(max_length=2000)
    timestamp = models.DateTimeField(auto_now_add=True)
    context = models.JSONField(default=dict)

    def __str__(self):
        return f'{self.user.username} - {self.timestamp}'



    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = 'Conversations'

