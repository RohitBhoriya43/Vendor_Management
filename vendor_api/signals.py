from vendor_api.view.imports import *
from django.utils import timezone

#@receiver(post_save,sender=PurchaseOrder)
def update_historical_performance_and_vendor_metrics(sender,instance,**kwargs):

    data = {}
    vendor_obj = instance.vendor
    print(vendor_obj)
    
    if instance.status == PurchaseOrderStatus.completed:
        print(instance.status)
        vendor_code = instance.vendor.vendor_code

        completed_pos = PurchaseOrder.objects.filter(vendor__vendor_code= vendor_code,status=PurchaseOrderStatus.completed)
        total_completed_pos = completed_pos.count()
        on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now()).count()
        print(on_time_deliveries)
        on_time_delivery_rate = on_time_deliveries/total_completed_pos if total_completed_pos > 0 else 0
        data.update({"on_time_delivery_rate":format(on_time_delivery_rate,".4f")})
    
    if instance.quality_rating is not None:
        quality_rating_avg = PurchaseOrder.objects.filter(vendor= vendor_obj,status=PurchaseOrderStatus.completed,quality_rating__isnull=False).aggregate(models.Avg("quality_rating"))["quality_rating__avg"]
        data.update({"quality_rating_avg":format(quality_rating_avg,".4f")})
    

    if instance.acknowledgment_date is not None:
        completed_acknow_pos = PurchaseOrder.objects.filter(vendor= vendor_obj,status=PurchaseOrderStatus.completed,acknowledgment_date__isnull=False)
        if completed_acknow_pos.count()==0:
            average_response_time =0
        else:
            total_response_time = sum((po.acknowledgment_date-po.issue_date).total_seconds()/3600 for po in completed_acknow_pos)
            average_response_time = total_response_time / completed_acknow_pos.count()
        
        data.update({"average_response_time":format(average_response_time,".4f")})
    
    vendor_po_objs = PurchaseOrder.objects.filter(vendor= vendor_obj)
    successfully_fulfilled_po = vendor_po_objs.filter(status=PurchaseOrderStatus.completed)
    fulfillment_rate = successfully_fulfilled_po.count() / vendor_po_objs.count() if vendor_po_objs.count()>0 else 0

    data.update({"fulfillment_rate":format(fulfillment_rate,".4f")})

    print(data)

    HistoricalPerformance.objects.update_or_create(vendor=vendor_obj,defaults=data)

    vendor_obj.on_time_delivery_rate = data.get("on_time_delivery_rate") if data.get("on_time_delivery_rate") is not None else 0
    vendor_obj.fulfillment_rate = fulfillment_rate
    vendor_obj.average_response_time = data.get("average_response_time") if data.get("average_response_time") is not None else 0
    vendor_obj.quality_rating_avg = data.get("quality_rating_avg") if data.get("quality_rating_avg") is not None else 0
    vendor_obj.save()



#@receiver(post_save,sender=PurchaseOrder)
def update_average_response_time(sender,instance,**kwargs):
    vendor_obj = instance.vendor
    completed_acknow_pos = PurchaseOrder.objects.filter(vendor= vendor_obj,status=PurchaseOrderStatus.completed,acknowledgment_date__isnull=False)
    if completed_acknow_pos.count()==0:
        average_response_time =0
    else:
        total_response_time = sum((po.acknowledgment_date-po.issue_date).total_seconds() for po in completed_acknow_pos)
        average_response_time = total_response_time / completed_acknow_pos.count()
    print(average_response_time)
    HistoricalPerformance.objects.update_or_create(vendor=vendor_obj,defaults={"average_response_time":average_response_time})
    vendor_obj.average_response_time = average_response_time
    vendor_obj.save()

        

            
