from .models import Vendor, PurchaseOrder
from django.db.models import Count, Avg

# Function to calculate on-time delivery rate
def calculate_on_time_delivery_rate(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    on_time_deliveries = completed_pos.filter(delivery_date__lte=PurchaseOrder('delivery_date')).count()
    total_completed_pos = completed_pos.count()
    if total_completed_pos == 0:
        return 0
    return (on_time_deliveries / total_completed_pos) * 100


# Function to calculate quality rating average
def calculate_quality_rating_avg(vendor):
    completed_pos_with_rating = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
    if completed_pos_with_rating.exists():
        return completed_pos_with_rating.aggregate(Avg('quality_rating'))['quality_rating__avg']
    return 0

# Function to calculate average response time
def calculate_average_response_time(vendor):
    acknowledged_pos = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
    if acknowledged_pos.exists():
        avg_response_time = acknowledged_pos.aggregate(Avg(PurchaseOrder('acknowledgment_date') - PurchaseOrder('issue_date')))['acknowledgment_date__avg']
        return avg_response_time.total_seconds() / 3600 # Convert to hours
    return 0

# Function to calculate fulfillment rate
def calculate_fulfillment_rate(vendor):
    total_pos = PurchaseOrder.objects.filter(vendor=vendor)
    successfully_fulfilled_pos = total_pos.filter(status='completed').exclude(quality_rating__lt=3).count()
    if total_pos.exists():
        return (successfully_fulfilled_pos / total_pos.count()) * 100
    return 0