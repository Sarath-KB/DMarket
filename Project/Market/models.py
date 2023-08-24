from django.db import models
from Guest.models import tbl_market_reg
from Admin.models import *
# Create your models here.
class tbl_market_product(models.Model):
    pdt_name=models.CharField(max_length=50)
    pdt_rate=models.IntegerField()
    pdt_dis=models.CharField(max_length=100)
    pdt_stock=models.FloatField()
    pdt_image=models.FileField(upload_to='MarketProduct/')
    subcategory=models.ForeignKey(tbl_subcat,on_delete=models.CASCADE)
    market=models.ForeignKey(tbl_market_reg,on_delete=models.CASCADE)

class tbl_events(models.Model):
    event_name=models.CharField(max_length=100)
    event_fdate=models.DateField(null=True)
    event_tdate=models.DateField(null=True)
    event_details=models.CharField(max_length=500)
    event_photo=models.FileField(upload_to='MarketEvents/')
    market=models.ForeignKey(tbl_market_reg,on_delete=models.CASCADE)
    status=models.CharField(max_length=1,default="0")