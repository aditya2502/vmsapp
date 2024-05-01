from .models import HistoricalPerformance,PurchaseOrder,Vendor  
from rest_framework import serializers # type: ignore


class  VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields='__all__'
        
class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields="__all__"
        
class HistoricalOrderSerializer(serializers.ModelSerializer):    
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'