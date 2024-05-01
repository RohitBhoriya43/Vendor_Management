from django.db import models

from vendor_api.choices import PurchaseOrderStatus
from vendor_api.models.vendors import Vendors



class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=200,null=True,unique=True)
    vendor = models.ForeignKey(Vendors,on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.IntegerField(null=True,blank=True)
    status=models.CharField(max_length=200,choices=PurchaseOrderStatus.choices,default=PurchaseOrderStatus.pending)
    quality_rating = models.FloatField(null=True,blank=True)
    issue_date=models.DateTimeField(auto_now_add=True, blank=True)
    acknowledgment_date=models.DateTimeField(null=True, blank=True)


    class Meta:
        db_table= "purchase_order"
    