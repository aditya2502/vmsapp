from django.contrib import admin

# Register your models here.
from .models import Vendor, PurchaseOrder, HistoricalPerformance

class VendorAdmin(admin.ModelAdmin):
    list_display=('name', 'vendor_code', 'address')
    
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display=('po_number', 'vendor', 'status')
    list_filter=('vendor',)



admin.site.register(Vendor,VendorAdmin)
admin.site.register(PurchaseOrder,PurchaseOrderAdmin)
admin.site.register(HistoricalPerformance)

