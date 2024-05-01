from django.contrib import admin
from vendor_api.models import *

# Register your models here.

@admin.register(Vendors)
class VendorAdmin(admin.ModelAdmin):
    list_display=("name","contact_details","vendor_code","address")


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display=("po_number","vendor","order_date","delivery_date")


@admin.register(HistoricalPerformance)
class HistoricalPerformanceAdmin(admin.ModelAdmin):
    list_display=("vendor","date",)


