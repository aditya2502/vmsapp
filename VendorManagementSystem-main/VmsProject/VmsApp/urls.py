# urls.py
from django.urls import path
from .views import (
    VendorListCreateAPIView,
    VendorRetrieveUpdateDestroyAPIView,
    PurchaseOrderListCreateAPIView,
    PurchaseOrderRetrieveUpdateDestroyAPIView,
    VendorPerformanceAPIView,
    AcknowledgePurchaseOrderAPIView,
    HistoricalPerformanceListCreateAPIView,
    HistoricalPerformanceRetrieveUpdateDestroyAPIView

)

urlpatterns = [
    path('api/vendors/', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('api/vendors/<int:pk>/', VendorRetrieveUpdateDestroyAPIView.as_view(), name='vendor-retrieve-update-destroy'),
    path('api/purchase_orders/', PurchaseOrderListCreateAPIView.as_view(), name='purchase-order-list-create'),
    path('api/purchase_orders/<int:pk>/', PurchaseOrderRetrieveUpdateDestroyAPIView.as_view(), name='purchase-order-retrieve-update-destroy'),
    path('api/history_orders/', HistoricalPerformanceListCreateAPIView.as_view(), name='purchase-order-list-create'),
    path('api/history_orders/<int:pk>/', HistoricalPerformanceRetrieveUpdateDestroyAPIView.as_view(), name='purchase-order-retrieve-update-destroy'),
    path('api/vendors/<int:pk>/performance/', VendorPerformanceAPIView.as_view(), name='vendor-performance'),
    path('api/purchase_orders/<int:pk>/acknowledge/', AcknowledgePurchaseOrderAPIView.as_view(), name='vendor-acknowledge'),
]


