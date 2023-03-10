from django.db import models


class Message(models.Model):
    subject = models.CharField(max_length=100)
    message_body = models.TextField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    read = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)


                                                   