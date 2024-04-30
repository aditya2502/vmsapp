from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework import status

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
    serializer_class = PurchaseOrderSerializer
    
class PurchaseOrderRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    # API view to retrieve, update, and delete PurchaseOrder objects
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    
class VendorPerformanceView(generics.RetrieveAPIView):
    # API view to retrieve performance metrics for a Vendor
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer