from django.shortcuts import render,redirect
from Guest.models import *
from Admin.models import *
from django.core.mail import send_mail
from django.conf import settings
import random
# Create your views here.
def index(request):
    return render(request,"Guest/index.html")

def about(request):
    return render(request,"Guest/about.html")

def service(request):
    return render(request,"Guest/service.html")

def contact(request):
    return render(request,"Guest/contact.html")

def adminlogin(request):
    if request.method=="POST":
        username=request.POST.get("txtusername")
        password=request.POST.get("txtpassword")
        if (username=="admin") and (password=="admin2255"):
            request.session["adm_name"]="admin"
            return redirect("webadmin:home")
        else:
            sc=1
            return render(request,"Guest/Admin_login.html",{'sc':sc})
    else:
        return render(request,"Guest/Admin_login.html")

def login(request):
    if request.method=="POST":
        msg="Invalid"
        Email=request.POST.get('txtusname')
        Password=request.POST.get('txtpassword')
        subadmin_count=tbl_subadmin.objects.filter(sad_email=Email,sad_pass=Password,sad_status=1).count()
        subadmin_s2=tbl_subadmin.objects.filter(sad_email=Email,sad_pass=Password,sad_status=2).count()
        customer_count=tbl_cus_reg.objects.filter(cus_email=Email,cus_pass=Password).count()
        farmer_count=tbl_farmer_reg.objects.filter(far_email=Email,far_pass=Password,far_status=1).count()
        farmer_s0=tbl_farmer_reg.objects.filter(far_email=Email,far_pass=Password,far_status=0).count()
        farmer_s2=tbl_farmer_reg.objects.filter(far_email=Email,far_pass=Password,far_status=2).count()
        market_count=tbl_market_reg.objects.filter(mar_email=Email,marpassword=Password,mar_status=1).count()
        market_s0=tbl_market_reg.objects.filter(mar_email=Email,marpassword=Password,mar_status=0).count()
        market_s2=tbl_market_reg.objects.filter(mar_email=Email,marpassword=Password,mar_status=2).count()
        if subadmin_count>0:
            subadmin_data=tbl_subadmin.objects.get(sad_email=Email,sad_pass=Password)
            request.session["subadmin_id"]=subadmin_data.id
            request.session["subadmin_name"]=subadmin_data.sad_name
            request.session["subadmin_district"]=subadmin_data.district.id
            return redirect("websubadmin:home")
        elif subadmin_s2>0:
            submsg=1
            return render(request,"Guest/Login.html",{'submsg':submsg})
        elif market_count>0:
            market_data=tbl_market_reg.objects.get(mar_email=Email,marpassword=Password)
            request.session["market_id"]=market_data.id
            request.session["market_name"]=market_data.mar_name
            return redirect("webmarket:home")
        elif market_s0>0:
            marmsg0="pending"
            return render(request,"Guest/Login.html",{'mar1':marmsg0})
        elif market_s2>0:
            marmsg2="rejected"
            return render(request,"Guest/Login.html",{'mar2':marmsg2})
        elif farmer_count>0:
            farmer_data=tbl_farmer_reg.objects.get(far_email=Email,far_pass=Password)
            request.session["farmer_id"]=farmer_data.id
            request.session["farmer_name"]=farmer_data.far_name
            request.session["farmer_place"]=farmer_data.locplace.pla.id
            return redirect("webfarmer:home")
        elif farmer_s0>0:
            farmsg0="pending"
            return render(request,"Guest/Login.html",{'far0':farmsg0})
        elif farmer_s2>0:
            farmsg2="rejected"
            return render(request,"Guest/Login.html",{'far2':farmsg2})
        elif customer_count>0:
            customer_data=tbl_cus_reg.objects.get(cus_email=Email,cus_pass=Password)
            request.session["customer_id"]=customer_data.id
            request.session["customer_name"]=customer_data.cus_name
            request.session["customer_place"]=customer_data.cus_locplace.pla.id
            return redirect("webcustomer:home")
        else:
            return render(request,"Guest/Login.html",{'msg':msg})
    else:
        return render(request,"Guest/Login.html")

def cus_reg(request):
    district=tbl_district.objects.all()
    if request.method=="POST":
        if (request.POSt.get('txtpassword')) == (request.POST.get('txtconpassword')):
            fname=request.POST.get('txtfirstname')
            lname=request.POST.get('txtlastname')
            fullname=fname +" "+ lname
            locplace=tbl_local_place.objects.get(id=request.POST.get('sellocplace'))
            tbl_cus_reg.objects.create(cus_name=fullname,cus_contact=request.POST.get('txtcontact'),cus_email=request.POST.get('txtemail'),cus_address=request.POST.get('txtaddress'),cus_locplace=locplace,cus_photo=request.FILES.get('txtphoto'),cus_pass=request.POST.get('txtpassword'))
            cusinsmsg="inserted"
            return render(request,"Guest/Customer_reg.html",{'dis':district,'cusinsmsg':cusinsmsg})
        else:
            err=1
            return render(request,"Guest/Customer_reg.html",{'passs':err})
    else:
        return render(request,"Guest/Customer_reg.html",{'dis':district})

def ajaxlocplace(request):
    placedata=tbl_place.objects.get(id=request.GET.get('disd'))
    locdata=tbl_local_place.objects.filter(pla=placedata)
    return render(request,"Guest/Ajaxlocplace.html",{'data':locdata})

def freg(request):
    dis=tbl_district.objects.all()
    fatype=tbl_farmtype.objects.all()
    if request.method=="POST":
        if (request.POST.get('txtpass')) == (request.POST.get('txtconpass')):
            firstn=request.POST.get('txtfname')
            lastn=request.POST.get('txtlname')
            fulln=firstn+ " " +lastn
            localp=tbl_local_place.objects.get(id=request.POST.get('sellocplace'))
            farmert=tbl_farmtype.objects.get(id=request.POST.get('selfarmtype'))
            tbl_farmer_reg.objects.create(far_name=fulln,far_email=request.POST.get('txtemail'),far_contact=request.POST.get('txtcontact'),far_address=request.POST.get('txtaddress'),farmer_type=farmert,locplace=localp,far_photo=request.FILES.get('txtphoto'),far_proof=request.FILES.get('txtproof'),far_pass=request.POST.get('txtpass'))
            farinsmsg="inserterd"
            return render(request,"Guest/Farmer_reg.html",{'ddata':dis,'farmer':fatype,'farinsmsg':farinsmsg})
        else:
            err=1
            return render(request,"Guest/Farmer_reg.html",{'passs':err})
    else:
        return render(request,"Guest/Farmer_reg.html",{'ddata':dis,'farmer':fatype})

def marketreg(request):
    disdata=tbl_district.objects.all()
    if request.method=="POST":
        if (request.POST.get('txtpassword')) == (request.POST.get('txtconpassword')):
            pdata=tbl_place.objects.get(id=request.POST.get('selplace'))
            tbl_market_reg.objects.create(mar_name=request.POST.get('txtname'),mar_email=request.POST.get('txtemail'),mar_contact=request.POST.get('txtcontact'),mar_address=request.POST.get('txtaddress'),place=pdata,marphoto=request.FILES.get('txtphoto'),marproof=request.FILES.get('txtproof'),marpassword=request.POST.get('txtpassword'))
            marinsmsg="inserted"
            return render(request,"Guest/Market_reg.html",{'ddistrict':disdata,'marinsmsg':marinsmsg})
        else:
            err=1
            return render(request,"Guest/Market_reg.html",{'passs':err})
    else:
        return render(request,"Guest/Market_reg.html",{'ddistrict':disdata})

def ForgetPassword(request):
    
    if request.method=="POST":
        otp=random.randint(10000, 999999)
        request.session["otp"]=otp
        request.session["femail"]=request.POST.get('txtemail')
        send_mail(
            'Respected Sir/Madam ',#subject
            "\rYour OTP for Reset Password Is"+str(otp),#body
            settings.EMAIL_HOST_USER,
            [request.POST.get('txtemail')],
        )
        return redirect("webguest:verification")
    else:
        return render(request,"Guest/ForgetPassword.html")

def OtpVerification(request):
    if request.method=="POST":
        otp=int(request.session["otp"])
        if int(request.POST.get('txtotp'))==otp:
            return redirect("webguest:create")
    return render(request,"Guest/OTPVerification.html")

def CreateNewPass(request):
    if request.method=="POST":
        if request.POST.get('txtpassword2')==request.POST.get('txtpassword3'):
            usercount=tbl_cus_reg.objects.filter(cus_email=request.session["femail"]).count()
            marketcount=tbl_market_reg.objects.filter(mar_email=request.session["femail"]).count()
            farmercount=tbl_farmer_reg.objects.filter(far_email=request.session["femail"]).count()
            subadmincount=tbl_subadmin.objects.filter(sad_email=request.session["femail"]).count()
            if usercount>0:
                user=tbl_cus_reg.objects.get(cus_email=request.session["femail"])
                user.cus_pass=request.POST.get('txtpassword2')
                user.save()
                return redirect("webguest:login")

            elif marketcount>0:
                doc=tbl_market_reg.objects.get(mar_email=request.session["femail"])
                doc.marpassword=request.POST.get('txtpassword2')
                doc.save()
                return redirect("webguest:login")

            elif farmercount>0:
                con=tbl_farmer_reg.objects.get(far_email=request.session["femail"])
                con.far_pass=request.POST.get('txtpassword2')
                con.save()
                return redirect("webguest:login")

            else:
                hos=tbl_subadmin.objects.get(sad_email=request.session["femail"])
                hos.sad_pass=request.POST.get('txtpassword2')
                hos.save()
                return redirect("webguest:login")
    else:       
        return render(request,"Guest/CreateNewPassword.html")

def ajaxemail(request):
    usercount=tbl_cus_reg.objects.filter(cus_email=request.GET.get("email")).count()
    marketcount=tbl_market_reg.objects.filter(mar_email=request.GET.get("email")).count()
    farmercount=tbl_farmer_reg.objects.filter(far_email=request.GET.get("email")).count()
    subadmincount=tbl_subadmin.objects.filter(sad_email=request.GET.get("email")).count()
    if usercount>0 or marketcount>0 or farmercount>0 or subadmincount>0:
        return render(request,"Guest/Ajaxemail.html",{'mess':1})
    else:
         return render(request,"Guest/Ajaxemail.html")