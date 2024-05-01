from rest_framework import serializers
from vendor_api.models import *


class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendors
        fields = [
            "name",
            "contact_details",
            "address",
            "vendor_code",
            "on_time_delivery_rate",
            "quality_rating_avg",
            "average_response_time",
            "fulfillment_rate",
        ]

class PurchaseOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class HistoricalPerformanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = HistoricalPerformance
        fields = [
            "on_time_delivery_rate",
            "quality_rating_avg",
            "average_response_time",
            "fulfillment_rate",
        ]
