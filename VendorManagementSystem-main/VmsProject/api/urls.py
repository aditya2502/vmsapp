from django.urls import path
from .views import (
    VendorListCreateView,
    VendorRetrieveUpdateDeleteView,
    PurchaseOrderListCreateView,
    PurchaseOrderRetrieveUpdateDeleteView,
    VendorPerformanceView,
    AcknowledgePurchaseOrderView,
)

# Define the URL patterns for the API app
urlpatterns = [
    path('vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),  # Vendor list and creation
    path('vendors/<int:pk>/', VendorRetrieveUpdateDeleteView.as_view(), name='vendor-retrieve-update-delete'),  # Vendor details, update, and delete
    path('vendors/<int:pk>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'),  # Vendor performance details
    path('purchase_orders/', PurchaseOrderListCreateView.as_view(), name='purchase-order-list-create'),  # Purchase order list and creation  
    #    - GET /api/purchase_orders/?vendor=1: List all purchase orders filtered by vendor
    path('purchase_orders/<int:pk>/', PurchaseOrderRetrieveUpdateDeleteView.as_view(), name='purchase-order-retrieve-update-delete'),  # Purchase order details, update, and delete
    path('purchase_orders/<int:pk>/acknowledge/', AcknowledgePurchaseOrderView.as_view(), name='acknowledge-purchase-order'),  # Acknowledge a purchase order

]

