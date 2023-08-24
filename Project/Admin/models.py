from django.db import models

# Create your models here.
class tbl_district(models.Model):
    district_name=models.CharField(max_length=50)

class tbl_complainttype(models.Model):
    comp_type_name=models.CharField(max_length=50)

class tbl_catageory(models.Model):
    cat_name=models.CharField(max_length=50)
    cat_status=models.CharField(max_length=1,default="1")

class tbl_place(models.Model):
    place_name=models.CharField(max_length=50)
    district=models.ForeignKey(tbl_district,on_delete=models.CASCADE)

class tbl_subcat(models.Model):
    subcat_name=models.CharField(max_length=50)
    cat=models.ForeignKey(tbl_catageory,on_delete=models.CASCADE)

class tbl_local_place(models.Model):
    loc_place_name=models.CharField(max_length=50)
    pla=models.ForeignKey(tbl_place,on_delete=models.CASCADE)

class tbl_subadmin(models.Model):
    sad_name=models.CharField(max_length=50)
    sad_contact=models.CharField(max_length=10)
    sad_email=models.CharField(max_length=50)
    sad_address=models.CharField(max_length=100)
    district=models.ForeignKey(tbl_district,on_delete=models.CASCADE)
    sad_photo=models.FileField(upload_to='SubadminPhoto/')
    sad_pass=models.CharField(max_length=50)
    sad_doj=models.DateField(auto_now_add=True)
    sad_status=models.CharField(max_length=1,default="1")

class tbl_farmtype(models.Model):
    farm_type=models.CharField(max_length=50)

