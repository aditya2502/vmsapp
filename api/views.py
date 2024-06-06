from rest_framework import generics
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework import status
from django.utils import timezone

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class YourProtectedView(APIView):
    def get(self, request):
        # A protected view requiring JWT authentication and permission
        return Response({'message': 'This is a protected view.'})


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class VendorListCreateView(generics.ListCreateAPIView):
    # API view to list and create Vendor objects
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class VendorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    # API view to retrieve, update, and delete Vendor objects
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    # API view to list and create PurchaseOrder objects
    serializer_class = PurchaseOrderSerializer
    def get_queryset(self):
        queryset = PurchaseOrder.objects.all()
        # Check if vendor_id is provided in the query parameters
        vendor_id = self.request.query_params.get('vendor', None)
        if vendor_id:
            # Filter by vendor_id if it's provided
            queryset = queryset.filter(vendor__id=vendor_id)

        return queryset

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PurchaseOrderRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    # API view to retrieve, update, and delete PurchaseOrder objects
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
# special api view
class VendorPerformanceView(generics.RetrieveAPIView):
    # API view to retrieve performance metrics for a Vendor
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    def retrieve(self, request, *args, **kwargs):
        # Retrieve performance metrics for a specific Vendor
        instance = self.get_object()
        performance_data = {
            'on_time_delivery_rate': instance.on_time_delivery_rate,
            'quality_rating_avg': instance.quality_rating_avg,
            'average_response_time': instance.average_response_time,
            'fulfillment_rate': instance.fulfillment_rate,
        }
        return Response(performance_data)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
# extra api
class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
    # API view to acknowledge a PurchaseOrder and trigger recalculation
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()

        # Update acknowledgment_date
        instance.acknowledgment_date = timezone.now()
        instance.save()

        # Trigger the recalculation of average_response_time
        instance.calculate_average_response_time()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)