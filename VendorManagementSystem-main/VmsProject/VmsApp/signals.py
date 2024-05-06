from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder
from VmsApp.calculations import calculate_on_time_delivery_rate, calculate_quality_rating_avg, calculate_average_response_time, \
calculate_fulfillment_rate

# Signal receiver function to handle actions when a PurchaseOrder is saved
@receiver(post_save, sender=PurchaseOrder)
def purchase_order_saved(sender, instance, created, **kwargs):
    # Logic to execute when a PurchaseOrder is saved
    # This could include triggering calculations or updates
    
    vendor = instance.vendor

    # import ipdb; ipdb.set_trace();
    if instance.status == 'completed':    # Check if the purchase order status is 'completed'
        vendor.calculate_on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
        vendor.calculate_quality_rating_avg = calculate_quality_rating_avg(vendor)
        vendor.calculate_fulfillment_rate = calculate_fulfillment_rate(vendor)
        vendor.calculate_average_response_time = calculate_average_response_time(vendor)


    if instance.status == 'cancelled':    # Check if the purchase order status is 'cancelled'
        vendor.calculate_fulfillment_rate=instance.calculate_fulfillment_rate()

    if instance.acknowledgment_date is not None:
        vendor.calculate_average_response_time=instance.calculate_average_response_time()
    
    instance.save()

