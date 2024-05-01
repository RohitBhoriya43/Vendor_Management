from django.db import models

from vendor_api.models.vendors import Vendors



class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendors,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True, blank=True)
    on_time_delivery_rate=models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True,blank=True)
    average_response_time=models.FloatField(null=True, blank=True)
    fulfillment_rate=models.FloatField(null=True, blank=True)


    class Meta:
        db_table = "historical_performance"
    