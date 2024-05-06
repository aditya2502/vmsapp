from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from rest_framework import generics
from django.http import JsonResponse
from rest_framework.response import Response
from VmsApp.calculations import calculate_on_time_delivery_rate, calculate_quality_rating_avg, calculate_average_response_time, \
calculate_fulfillment_rate
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


class VendorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class HistoricalPerformanceListCreateAPIView(generics.ListCreateAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer

class HistoricalPerformanceView(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = HistoricalPerformanceSerializer

    def retrieve(self, request, id):
        historical_performance = HistoricalPerformance.objects.get(vendor_id=id)
        serializer = HistoricalPerformanceSerializer(historical_performance)
        return Response(serializer.data)

class HistoricalPerformanceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer

class VendorPerformanceAPIView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def retrieve(self, request, *args, **kwargs):
        vendor = self.get_object()
        on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
        quality_rating_avg = calculate_quality_rating_avg(vendor)
        average_response_time = calculate_average_response_time(vendor)
        fulfillment_rate = calculate_fulfillment_rate(vendor)

        data = {
            'on_time_delivery_rate': on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg,
            'average_response_time': average_response_time,
            'fulfillment_rate': fulfillment_rate,
        }
        return Response(data)

class AcknowledgePurchaseOrderAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.acknowledgment_date = timezone.now()
            instance.save()
            vendor = instance.vendor
            vendor.average_response_time = calculate_average_response_time(vendor)
            vendor.save()

            return JsonResponse({'message': 'Purchase order acknowledged successfully'})
        except PurchaseOrder.DoesNotExist:
            return JsonResponse({'error': 'Purchase order not found'}, status=404)