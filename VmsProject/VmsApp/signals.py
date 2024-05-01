from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=PurchaseOrder)
def update_on_time_delivery_rate(sender, instance, created, **kwargs):
    if instance.status == 'completed' and instance.delivery_date:
        vendor = instance.vendor
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_orders = completed_orders.filter(delivery_date__lte=instance.promised_delivery_date)
        on_time_delivery_rate = (on_time_orders.count() / completed_orders.count()) * 100
        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.save()
        
@receiver(post_save, sender=PurchaseOrder)
def update_quality_rating_average(sender, instance, created, **kwargs):
    if instance.status == 'completed' and instance.quality_rating is not None:
        vendor = instance.vendor
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
        if completed_orders.exists():
            quality_rating_average = completed_orders.aggregate(avg_quality_rating=models.Avg('quality_rating'))['avg_quality_rating']
            vendor.quality_rating = quality_rating_average
            vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_average_response_time(sender, instance, created, **kwargs):
    if instance.acknowledgment_date:
        vendor = instance.vendor
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
        if completed_orders.exists():
            response_times = (order.acknowledgment_date - order.issue_date).days 
            for order in completed_orders :
                average_response_time = sum(response_times) / len(response_times)
                vendor.average_response_time = average_response_time
            vendor.save()
            
@receiver(post_save, sender=PurchaseOrder)
def update_fulfilment_rate(sender, instance, created, **kwargs):
    vendor = instance.vendor
    total_orders = PurchaseOrder.objects.filter(vendor=vendor)
    fulfilled_orders = total_orders.filter(status='completed', issues__isnull=True)
    
    if total_orders.exists():
        fulfilment_rate = (fulfilled_orders.count() / total_orders.count()) * 100
        vendor.fulfilment_rate = fulfilment_rate
        vendor.save()


