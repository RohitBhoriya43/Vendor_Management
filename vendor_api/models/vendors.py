from django.db import models
from django.contrib.auth.models import AbstractUser



class Vendors(AbstractUser):
    name = models.CharField(max_length=200,null=True, blank=True)
    contact_details = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    vendor_code = models.CharField(max_length=200,null=True,unique=True)
    on_time_delivery_rate=models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True,blank=True)
    average_response_time=models.FloatField(null=True, blank=True)
    fulfillment_rate=models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "vendors"
    