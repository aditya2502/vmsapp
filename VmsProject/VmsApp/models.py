from django.db import models 
from django.db.models import F, Count,Sum

# Create your models here.
class Vendor(models.Model):
    name  = models.CharField(max_length=256)
    contact_details =models.TextField(max_length=20)
    address = models.TextField(max_length=500)
    vendor_code = models.CharField(max_length=50)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    fulfillment_rate = models.FloatField()
    average_response_time = models.FloatField()
    
    def __str__(self):
        return self.name
 
class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=10, primary_key=True)
    vendor  = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date   = models.DateTimeField()
    delivery_date=  models.DateTimeField()
    items        = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=55)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgememt_date = models.DateTimeField()
    
    def __str__(self):
        return f'{self.po_number} - {self.vendor} - {self.status}'
    
    def on_time_delivery_rate(vendor):
       completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed', delivery_date__isnull=False)
       on_time_orders = completed_orders.filter(delivery_date__lte=F('promised_delivery_date'))
       total_completed_orders = completed_orders.count()
       total_on_time_orders = on_time_orders.count()   
       on_time_delivery_rate = (total_on_time_orders / total_completed_orders) * 100 if total_completed_orders > 0 else 0   
       vendor.on_time_delivery_rate = on_time_delivery_rate
       vendor.save()
       
    def update_vendor_quality_rating_average(vendor):
       completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
    
       total_completed_orders = completed_orders.count()
    
       if total_completed_orders > 0:
           quality_rating_sum = completed_orders.aggregate(sum_quality_rating=models.Sum('quality_rating'))['sum_quality_rating']
           quality_rating_average = quality_rating_sum / total_completed_orders
       else:
           quality_rating_average = None
    
           vendor.quality_rating = quality_rating_average
           vendor.save()
           

def update_vendor_average_response_time(vendor):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
    
    total_completed_orders = completed_orders.count()
    
    if total_completed_orders > 0:
        response_times = completed_orders.annotate(response_time=Sum(F('acknowledgment_date') - F('issue_date')) / Count('id'))
        average_response_time = response_times.aggregate(avg_response_time=Sum('response_time'))['avg_response_time']
    else:
        average_response_time = None
    
    vendor.average_response_time = average_response_time
    vendor.save()
    
    def update_vendor_fulfilment_rate(vendor):
       total_orders = PurchaseOrder.objects.filter(vendor=vendor)
       completed_orders = total_orders.filter(status='completed', issues__isnull=True)
    
       total_order_count = total_orders.count()
       fulfilled_order_count = completed_orders.count()
    
       fulfilment_rate = (fulfilled_order_count / total_order_count) * 100 if total_order_count > 0 else 0
    
       vendor.fulfilment_rate = fulfilment_rate
       vendor.save()




class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    date = models.DateField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time =  models.FloatField()
    
    def __str__(self):
        return self.vendor + self.date
    
    
    
    
