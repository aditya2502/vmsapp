from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework import status
from rest_framework.decorators import api_view

class VendorListCreateView(generics.ListCreateAPIView):
    # API view to list and create Vendor objects
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    # API view to retrieve, update, and delete Vendor objects
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    # API view to list and create PurchaseOrder objects
     queryset = PurchaseOrder.objects.all()
     serializer_class = PurchaseOrderSerializer
     
     def get_queryset(self):
        queryset = super().get_queryset()
        vendor = self.request.query_params.get('vendor')
        if vendor:
            queryset = queryset.filter(vendor_reference=vendor)
        return queryset
    
class PurchaseOrderRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    # API view to retrieve, update, and delete PurchaseOrder objects
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    
class VendorPerformanceView(generics.RetrieveAPIView):
    # API view to retrieve performance metrics for a Vendor
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    
    from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Vendor

@api_view(['GET'])
def get_vendor_performance(request, vendor_id):
    try:
        vendor = Vendor.objects.get(id=vendor_id)
        performance_metrics = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating': vendor.quality_rating,
            'response_time': vendor.response_time.total_seconds(),
            'fulfilment_rate': vendor.fulfilment_rate
        }
        return Response(performance_metrics)
    except Vendor.DoesNotExist:
        return Response({"error": "Vendor not found"}, status=404)
