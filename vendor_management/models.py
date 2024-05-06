from django.db import models
from django.db.models import Count, Avg
from datetime import timedelta
from django.db.models import ExpressionWrapper, F, DurationField


# Create your models here.

def vendor_code():
    last_vendor = Vendor.objects.all().order_by('-created_date').first()

    if not last_vendor:
        updated_num = 'VMC000'  # Start with GFL000 if no orders exist
    else:
        last_number = last_vendor.vendor_code
        last_number_int = int(last_number.split('C')[-1])
        new_invoice_number_int = str(last_number_int + 1)
        updated_num = 'VMC' + new_invoice_number_int.zfill(3)  
     
    return updated_num

def po_number():
    last_purchase = PurchaseOrder.objects.all().order_by('-created_date').first()

    if not last_purchase:
        updated_num = 'VPN000' 
    else:
        last_number = last_purchase.po_number
        last_number_int = int(last_number.split('N')[-1])
        new_number_int = str(last_number_int + 1)
        updated_num = 'VPN' + new_number_int.zfill(3)  
     
    return updated_num
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=20,null=True, blank=True,unique=True,default=vendor_code)
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True,)
    average_response_time = models.FloatField(null=True,)
    fulfillment_rate = models.FloatField(null=True,)
    created_date = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)
    def __str__(self):
        return self.name
    
class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=20,null=True, blank=True,unique=True,default=po_number)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    C_STATUS = (
         ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
        ('completed', 'completed'),
    )
    status = models.CharField(max_length=20, choices=C_STATUS, null=True, blank=True, default='Pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)

    def __str__(self):
        return self.po_number
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == 'completed':
            self.update_vendor_metrics()

    def update_vendor_metrics(self):
        vendor = self.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')

        if completed_pos.exists():
            on_time_delivered_pos = completed_pos.filter(delivery_date__lte=F('acknowledgment_date'))
            on_time_delivery_rate = (on_time_delivered_pos.count() / completed_pos.count()) * 100
            vendor.on_time_delivery_rate = on_time_delivery_rate

            completed_pos_with_ratings = completed_pos.exclude(quality_rating__isnull=True)
            quality_rating_avg = completed_pos_with_ratings.aggregate(avg_rating=Avg('quality_rating'))['avg_rating'] or 0
            vendor.quality_rating_avg = quality_rating_avg

            response_times = completed_pos.filter(acknowledgment_date__isnull=False).annotate(
                response_time=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=DurationField())
            ).aggregate(avg_response_time=Avg('response_time'))['avg_response_time']
            average_response_time = response_times.total_seconds() / completed_pos.count() if response_times else 0
            vendor.average_response_time = average_response_time

            fulfilled_pos = completed_pos.exclude(status='Cancelled')
            fulfillment_rate = (fulfilled_pos.count() / completed_pos.count()) * 100
            vendor.fulfillment_rate = fulfillment_rate
        else:
            vendor.on_time_delivery_rate = 0
            vendor.quality_rating_avg = 0
            vendor.average_response_time = 0
            vendor.fulfillment_rate = 0

        vendor.save()


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor} - {self.date}"

