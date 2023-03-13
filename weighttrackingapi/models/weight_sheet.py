from django.db import models


class WeightSheet(models.Model):
    employee = models.ForeignKey(
        "Employee", on_delete=models.CASCADE, related_name='employee_field')
    date = models.DateField(auto_now=False, auto_now_add=False)
    resident = resident = models.ForeignKey(
        "Resident", on_delete=models.CASCADE, related_name='resident_sheet')
    reweighed = models.BooleanField(default=False)
    refused = models.BooleanField(default=False)
    not_in_room = models.BooleanField(default=False)
    daily_wts = models.BooleanField(default=False)
    show_alert = models.BooleanField(default=False)
    scale_type = models.CharField(max_length=50, null=True)



