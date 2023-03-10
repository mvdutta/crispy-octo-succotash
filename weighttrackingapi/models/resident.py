from django.db import models


class Resident(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    room_num = models.IntegerField()
    admission_wt = models.DecimalField(max_digits=5, decimal_places=1)
    usual_wt = models.IntegerField()
    height = models.IntegerField()
    admission_date = models.DateField(auto_now=False, auto_now_add=False)


