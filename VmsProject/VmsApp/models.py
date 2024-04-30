from django.db import models 

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



class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    date = models.DateField(primary_key=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time =  models.FloatField()
    
    
    
