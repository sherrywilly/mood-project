from django.db import models
from django.contrib.auth import get_user_model
from mood.models import *

# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(CustomUser,on_delete = models.CASCADE, related_name="sent_message")
    receiver = models.ForeignKey(CustomUser,on_delete = models.CASCADE, related_name="recieve_message")
    message = models.TextField()
    files = models.FileField(upload_to='chat',null=True,blank=True)
    sender_delete = models.BooleanField(default=False)
    receiver_delete = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("date_created",)

