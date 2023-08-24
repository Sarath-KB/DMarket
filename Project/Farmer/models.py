from django.db import models
from Admin.models import tbl_subcat
from Guest.models import tbl_farmer_reg
from Market.models import *
# Create your models here.
class tbl_farmer_product(models.Model):
    pdt_name=models.CharField(max_length=50)
    pdt_rate=models.IntegerField()
    pdt_dis=models.CharField(max_length=100)
    pdt_stock=models.FloatField()
    pdt_image=models.FileField(upload_to='FarmerProduct/')
    subcategory=models.ForeignKey(tbl_subcat,on_delete=models.CASCADE)
    farmer=models.ForeignKey(tbl_farmer_reg,on_delete=models.CASCADE)

class tbl_m_booking(models.Model):
    farmer=models.ForeignKey(tbl_farmer_reg,on_delete=models.CASCADE)
    booking_status=models.IntegerField(default="0")
    booking_date=models.DateField(auto_now_add=True)
    payment_date=models.DateField(null=True)
    date_time=models.DateTimeField(auto_now_add=True)

class tbl_m_cart(models.Model):
    bookingid=models.ForeignKey(tbl_m_booking,on_delete=models.CASCADE)
    productid=models.ForeignKey(tbl_market_product,on_delete=models.CASCADE)
    mquantity=models.FloatField(max_length=1,default="0")
    cart_status=models.IntegerField(default="0")