from django.db import models
from Guest.models import *
from Farmer.models import *
from Market.models import *
# Create your models here.
class tbl_farmer_booking(models.Model):
    user=models.ForeignKey(tbl_cus_reg,on_delete=models.CASCADE)
    booking_status=models.CharField(max_length=1,default="0")
    booking_date=models.DateField(auto_now_add=True)
    fpayment_date=models.DateField(null=True)
    date_time=models.DateTimeField(auto_now_add=True)

class tbl_farmer_cart(models.Model):
    bookingid=models.ForeignKey(tbl_farmer_booking,on_delete=models.CASCADE)
    productid=models.ForeignKey(tbl_farmer_product,on_delete=models.CASCADE)
    fquantity=models.FloatField(max_length=1,default="0")
    fcart_status=models.IntegerField(default="0")

class tbl_market_booking(models.Model):
    user=models.ForeignKey(tbl_cus_reg,on_delete=models.CASCADE)
    booking_status=models.CharField(max_length=1,default="0")
    booking_date=models.DateField(auto_now_add=True)
    mpayment_date=models.DateField(null=True)
    date_time=models.DateTimeField(auto_now_add=True)

class tbl_market_cart(models.Model):
    bookingid=models.ForeignKey(tbl_market_booking,on_delete=models.CASCADE)
    productid=models.ForeignKey(tbl_market_product,on_delete=models.CASCADE)
    mquantity=models.FloatField(max_length=1,default="0")
    mcart_status=models.IntegerField(default="0")

class applyevent(models.Model):
    event=models.ForeignKey(tbl_events,on_delete=models.CASCADE)
    customer=models.ForeignKey(tbl_cus_reg,on_delete=models.SET_NULL,null=True)
    farmer=models.ForeignKey(tbl_farmer_reg,on_delete=models.SET_NULL,null=True)
    replay=models.CharField(max_length=500,null=True)
    status=models.CharField(max_length=1,default="0")