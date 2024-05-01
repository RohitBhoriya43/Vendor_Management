from django.contrib import admin
from django.urls import path

from vendor_api.view.basic_authentication_or_superuser_login import CreateBasicAuthentication, LoginSuperUser
from vendor_api.view.purchase_order_tracking import PurchaseOrderTracking
from vendor_api.view.update_acknowlegment import UpdateAcknowledgment
from vendor_api.view.vendor_performance import VendorPerformance
from vendor_api.view.vendor_profile import VendorProfileManagement

urlpatterns = [
    path('vendors/', VendorProfileManagement.as_view(),name='List all Vendor'),
    path('vendors/', VendorProfileManagement.as_view(),name='Create a new vendor'),
    path('vendors/<vendor_id>/', VendorProfileManagement.as_view(),name='Retrieve a specific vendor details'),
    path('vendors/<vendor_id>/', VendorProfileManagement.as_view(),name='Update a vendor details'),
    path('vendors/<vendor_id>/', VendorProfileManagement.as_view(),name='Delete a vendor'),
    path('vendors/<vendor_id>/performance', VendorPerformance.as_view(),name='get the vendor performance'),
    path('purchase_orders/', PurchaseOrderTracking.as_view(),name='List all purchase orders with an option to filter by vendor'),
    path('purchase_orders/', PurchaseOrderTracking.as_view(),name='Create a purchase order '),
    path('purchase_orders/<po_id>/', PurchaseOrderTracking.as_view(),name='Retrieve details of a specific purchase order'),
    path('purchase_orders/<po_id>/', PurchaseOrderTracking.as_view(),name='Update a purchase order'),
    path('purchase_orders/<po_id>/', PurchaseOrderTracking.as_view(),name='Delete a purchase order'),
    path('purchase_orders/<po_id>/acknowledge', UpdateAcknowledgment.as_view(),name='recalculate the average_response_time'),
    path('vendor/superuser_login/', LoginSuperUser.as_view(),name='login super user'),
    path('vendor/basic_user_created/', CreateBasicAuthentication.as_view(),name='create basic authentication'),
]
