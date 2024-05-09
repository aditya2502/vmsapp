from django.db import models
from django.db.models import F, Count
from datetime import timedelta
from django.utils import timezone


# vendor model with required fields
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(unique=True, max_length=50)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


# purchase order model with required fields and methods for computing performance
class PurchaseOrder(models.Model):
    po_number = models.CharField(unique=True, max_length=50)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(null=True, blank=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.po_number} - {self.vendor} - {self.status}'
        

    def calculate_on_time_delivery_rate(self):
        # Calculate on-time delivery rate for the vendor
        completed_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            status='completed',
            delivery_date__lte=models.F('acknowledgment_date')
        ).count()

        all_completed_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            status='completed'
        ).count()

        if all_completed_orders > 0:
            self.vendor.on_time_delivery_rate = (completed_orders / all_completed_orders) * 100
            self.vendor.save()

    def calculate_quality_rating_avg(self):
        # Calculate quality rating average for the vendor
        completed_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            status='completed',
            quality_rating__isnull=False
        )

        total_rating = sum(order.quality_rating for order in completed_orders)
        num_orders = completed_orders.count()

        if num_orders > 0:
            self.vendor.quality_rating_avg = total_rating / num_orders
            self.vendor.save()

    def calculate_average_response_time(self):
        # Calculate average response time for the vendor
        completed_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            acknowledgment_date__isnull=False,
            issue_date__isnull=False
        )

        response_times = [(order.acknowledgment_date - order.issue_date).seconds 
        for order in completed_orders
        if order.acknowledgment_date and order.issue_date  # Check for missing data
        ]

        if response_times:
            average_response_time = sum(response_times) / len(response_times)
            self.vendor.average_response_time = average_response_time
            self.vendor.save()

    def calculate_fulfillment_rate(self):
        # Calculate fulfillment rate for the vendor
        successful_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            status='completed'
        ).count()

        cancelled_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            status='cancelled'
        ).count()

        if (cancelled_orders+ successful_orders) > 0:
            fulfillment_rate = (successful_orders / (cancelled_orders+ successful_orders)) * 100
            self.vendor.fulfillment_rate = fulfillment_rate
            self.vendor.save()


    def create_historical_performance(self):
        # Create historical performance record after every 5 completed orders
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

# HistoricalPerformance model to store historical performance data
class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f'{self.vendor} - {self.date}'