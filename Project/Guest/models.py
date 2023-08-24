from django.db import models
from Admin.models import *
# Create your models here.
class tbl_cus_reg(models.Model):
    cus_name=models.CharField(max_length=50)
    cus_contact=models.CharField(max_length=12)
    cus_email=models.CharField(max_length=50)
    cus_address=models.CharField(max_length=100)
    cus_locplace=models.ForeignKey(tbl_local_place,on_delete=models.CASCADE)
    cus_photo=models.FileField(upload_to='CustomerPhoto/')
    cus_pass=models.CharField(max_length=50)
    cus_doj=models.DateField(auto_now_add=True)

class tbl_farmer_reg(models.Model):
    far_name=models.CharField(max_length=50)
    far_email=models.CharField(max_length=50)
    far_contact=models.CharField(max_length=12)
    far_address=models.CharField(max_length=100)
    farmer_type=models.ForeignKey(tbl_farmtype,on_delete=models.CASCADE)
    locplace=models.ForeignKey(tbl_local_place,on_delete=models.CASCADE)
    far_photo=models.FileField(upload_to='FarmerPhoto/')
    far_proof=models.FileField(upload_to='FarmerproofPhoto/')
    far_pass=models.CharField(max_length=50)
    far_doj=models.DateField(auto_now_add=True)
    far_status=models.CharField(max_length=1,default="0")

class tbl_market_reg(models.Model):
    mar_name=models.CharField(max_length=50)
    mar_email=models.CharField(max_length=50)
    mar_contact=models.CharField(max_length=12)
    mar_address=models.CharField(max_length=100)
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
    marphoto=models.FileField(upload_to='MarketPhoto/')
    marproof=models.FileField(upload_to='Marketproof/')
    marpassword=models.CharField(max_length=50)
    mar_doj=models.DateField(auto_now_add=True) 
    mar_status=models.CharField(max_length=1,default="0")

class tbl_complaint(models.Model):
    complaint_con=models.CharField(max_length=500)
    sdate=models.DateField(auto_now_add=True)
    rdate=models.DateField(null=True)
    replay=models.CharField(max_length=500)
    status=models.CharField(max_length=1,default="0")
    com_type=models.ForeignKey(tbl_complainttype,on_delete=models.SET_NULL,null=True)
    market=models.ForeignKey(tbl_market_reg,on_delete=models.SET_NULL,null=True)
    farmer=models.ForeignKey(tbl_farmer_reg,on_delete=models.SET_NULL,null=True)
    customer=models.ForeignKey(tbl_cus_reg,on_delete=models.SET_NULL,null=True)
    subadmin=models.ForeignKey(tbl_subadmin,on_delete=models.SET_NULL,null=True)

class tbl_feedback(models.Model):
    feedback_con=models.CharField(max_length=500)
    date=models.DateField(auto_now_add=True)
    market=models.ForeignKey(tbl_market_reg,on_delete=models.SET_NULL,null=True)
    farmer=models.ForeignKey(tbl_farmer_reg,on_delete=models.SET_NULL,null=True)
    customer=models.ForeignKey(tbl_cus_reg,on_delete=models.SET_NULL,null=True)
    subadmin=models.ForeignKey(tbl_subadmin,on_delete=models.SET_NULL,null=True)