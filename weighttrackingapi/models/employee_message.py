from django.db import models


class EmployeeMessage(models.Model):
    sender = models.ForeignKey(
        "Employee", on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(
        "Employee", on_delete=models.CASCADE, related_name='recipient')
    message = models.ForeignKey(
        "Message", on_delete=models.CASCADE, related_name='employee_message')
