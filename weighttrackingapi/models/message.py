from django.db import models


class Message(models.Model):
    # recipient = models.ManyToManyField(
    #     "Employee", through="EmployeeMessage", related_name='message_recipient')
    subject = models.CharField(max_length=100)
    message_body = models.TextField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    read = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    sender = models.ForeignKey(
        "Employee", on_delete=models.CASCADE, related_name='message_sender')


