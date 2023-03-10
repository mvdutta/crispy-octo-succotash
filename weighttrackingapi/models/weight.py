from django.db import models


class Weight(models.Model):
    resident = models.ForeignKey("Resident", on_delete= models.CASCADE, related_name='resident_weight')
    date = models.DateField(auto_now=False, auto_now_add=False)
    weight = models.DecimalField(max_digits=5, decimal_places=1)
