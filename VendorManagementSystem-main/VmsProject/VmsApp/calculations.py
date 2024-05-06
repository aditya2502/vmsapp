from .models import Vendor, PurchaseOrder, HistoricalPerformance
from django.db.models import Avg, ExpressionWrapper, F, fields
from django.utils import timezone

# Function to calculate on-time delivery rate  
def calculate_on_time_delivery_rate(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    on_time_deliveries = completed_pos.filter(delivery_date__lte=F('delivery_date')).count()
    total_completed_pos = completed_pos.count()
    if total_completed_pos == 0:
        return 0
    return (on_time_deliveries / total_completed_pos) * 100

# Function to calculate quality rating average
def calculate_quality_rating_avg(vendor):
    completed_pos_with_rating = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
    if completed_pos_with_rating.exists():
        return completed_pos_with_rating.aggregate(Avg('quality_rating'))['quality_rating__avg']
    return "Not Enough Rating"

def calculate_average_response_time(vendor):
    acknowledged_pos = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
    if acknowledged_pos.exists():
        avg_response_time = acknowledged_pos.aggregate(
            average_response_time=Avg(
                ExpressionWrapper(
                    F('acknowledgment_date') - F('issue_date'),
                    output_field=fields.DurationField()
                )
            )
        )['average_response_time']
        if avg_response_time is not None:
            # avg_response_time is a timedelta object, so convert it to hours
            return avg_response_time.total_seconds() / 3600
    return 0

# Function to calculate fulfillment rate
def calculate_fulfillment_rate(vendor):
    total_pos = PurchaseOrder.objects.filter(vendor=vendor)
    successfully_fulfilled_pos = total_pos.filter(status='completed').count()
    if total_pos.exists():
        return (successfully_fulfilled_pos / total_pos.count()) * 100
    return 0

 # Create historical performance record after every 5 completed orders
def create_historical_performance(self):
    completed_orders_count = PurchaseOrder.objects.filter(
        vendor=self.vendor,
        status='completed',
    ).count()

    # Check if the number of completed orders is a multiple of 5
    if completed_orders_count > 0 and completed_orders_count % 5 == 0:
        HistoricalPerformance.objects.create(
            vendor=self.vendor,
            date=timezone.now(),
            on_time_delivery_rate=self.vendor.on_time_delivery_rate,
            quality_rating_avg=self.vendor.quality_rating_avg,
            average_response_time=self.vendor.average_response_time,
            fulfillment_rate=self.vendor.fulfillment_rate
        )
        
        
        
        
        