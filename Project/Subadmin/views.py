from django.shortcuts import render,redirect
from Guest.models import *
from Admin.models import tbl_subadmin,tbl_district
# Create your views here.
from datetime import date
def home(request):
    if 'subadmin_id' in request.session:
        subadmin=tbl_subadmin.objects.get(id=request.session["subadmin_id"])
        return render(request,"Subadmin/Home.html",{'sub':subadmin})
    else:
        return redirect("webguest:login")

def my_pro(request):
    if 'subadmin_id' in request.session:
        data=tbl_subadmin.objects.get(id=request.session["subadmin_id"])
        return render(request,"Subadmin/My_profile.html",{'data':data})
    else:
        return redirect("webguest:login")

def editprofile(request):
    if 'subadmin_id' in request.session:
        prodata=tbl_subadmin.objects.get(id=request.session["subadmin_id"])
        if request.method=="POST":
            prodata.sad_name=request.POST.get('txtname')
            prodata.sad_contact=request.POST.get('txtcon')
            prodata.sad_email=request.POST.get('txtemail')
            prodata.sad_address=request.POST.get('txtaddress')
            prodata.save()
            ep=1
            return render(request,"Subadmin/Edit_profile.html",{'ep':ep})
        else:
            return render(request,"Subadmin/Edit_profile.html",{'prodata':prodata})
    else:
        return redirect("webguest:login")

def editpropic(request):
    subdata=tbl_subadmin.objects.get(id=request.session["subadmin_id"])
    if request.method=="POST":
        subdata.sad_photo=request.FILES.get('txtpic')
        subdata.save()
        pic=1
        return render(request,"Subadmin/Edit_pro_pic.html",{'pic':pic})
    else:
        return render(request,"Subadmin/Edit_pro_pic.html",{'data':subdata})

def changepassword(request):
    if 'subadmin_id' in request.session:
        if request.method=="POST":
            ccount=tbl_subadmin.objects.filter(id=request.session["subadmin_id"],sad_pass=request.POST.get('txtcurpass')).count()
            if ccount>0:
                if request.POST.get('txtnewpass')==request.POST.get('txtconpass'):
                    subadmindata=tbl_subadmin.objects.get(id=request.session["subadmin_id"],sad_pass=request.POST.get('txtcurpass'))
                    subadmindata.sad_pass=request.POST.get('txtnewpass')
                    subadmindata.save()
                    er3=3
                    return render(request,"Subadmin/Change_password.html",{'er':er3})
                else:
                    er1=1
                    return render(request,"Subadmin/Change_password.html",{'er':er1})
            else:
                er2=2
                return render(request,"Subadmin/Change_password.html",{'er':er2})
        else:
            return render(request,"Subadmin/Change_password.html")
    else:
        return redirect("webguest:login")

def new_market(request):
    if 'subadmin_id' in request.session:
        districtid=tbl_district.objects.get(id=request.session["subadmin_district"])
        mardata=tbl_market_reg.objects.filter(mar_status=0,place__district=districtid)
        return render(request,"Subadmin/New_market.html",{'market':mardata})
    else:
        return redirect("webguest:login")

def approvemarket(request,apid):
    marketdata=tbl_market_reg.objects.get(id=apid)
    marketdata.mar_status=1
    marketdata.save()
    st=1
    return render(request,"Subadmin/Accepted_market.html",{'st':st})

def rejectmarket(request,rjid):
    marketdata=tbl_market_reg.objects.get(id=rjid)
    marketdata.mar_status=2
    marketdata.save()
    st=2
    return render(request,"Subadmin/Accepted_market.html",{'st':st})

def accepted_market(request):
    if 'subadmin_id' in request.session:
        districtid=tbl_district.objects.get(id=request.session["subadmin_district"])
        mardata=tbl_market_reg.objects.filter(mar_status=1,place__district=districtid)
        return render(request,"Subadmin/Accepted_market.html",{'accdata':mardata})
    else:
        return redirect("webguest:login")

def rejected_market(request):
    if 'subadmin_id' in request.session:
        districtid=tbl_district.objects.get(id=request.session["subadmin_district"])
        mardata=tbl_market_reg.objects.filter(mar_status=2,place__district=districtid)    
        return render(request,"Subadmin/Rejected_market.html",{'rjmarket':mardata})
    else:
        return redirect("webguest:login")

def new_farmer(request):
    if 'subadmin_id' in request.session:
        disid=tbl_district.objects.get(id=request.session["subadmin_district"])
        fardata=tbl_farmer_reg.objects.filter(far_status=0,locplace__pla__district=disid)
        return render(request,"Subadmin/New_farmer.html",{'farmer':fardata})
    else:
        return redirect("webguest:login")

def approvefarmer(request,apid):
    farmerdata=tbl_farmer_reg.objects.get(id=apid)
    farmerdata.far_status=1
    farmerdata.save()
    st=1
    return render(request,"Subadmin/New_farmer.html",{'st':st})

def rejectfarmer(request,rjid):
    farmerdata=tbl_farmer_reg.objects.get(id=rjid)
    farmerdata.far_status=2
    farmerdata.save()
    st=2
    return render(request,"Subadmin/New_farmer.html",{'st':st})

def accepted_farmer(request):
    if 'subadmin_id' in request.session:
        disid=tbl_district.objects.get(id=request.session["subadmin_district"])
        fardata=tbl_farmer_reg.objects.filter(far_status=1,locplace__pla__district=disid)
        return render(request,"Subadmin/Accepted_farmer.html",{'farmer':fardata})
    else:
        return redirect("webguest:login")

def rejected_farmer(request):
    if 'subadmin_id' in request.session:
        disid=tbl_district.objects.get(id=request.session["subadmin_district"])
        fardata=tbl_farmer_reg.objects.filter(far_status=2,locplace__pla__district=disid)
        return render(request,"Subadmin/Rejected_farmer.html",{'farmer':fardata})
    else:
        return redirect("webguest:login")

def complaint(request):
    if 'subadmin_id' in request.session:
        comtype=tbl_complainttype.objects.all()
        subdata=tbl_subadmin.objects.get(id=request.session["subadmin_id"])
        if request.method=="POST":
            comtype=tbl_complainttype.objects.get(id=request.POST.get("txtcomtype"))
            tbl_complaint.objects.create(complaint_con=request.POST.get("txtcomcon"),subadmin=subdata,com_type=comtype)
            ins=1
            return render(request,"Subadmin/Complaint.html",{'ins':ins})
        else:
            return render(request,"Subadmin/Complaint.html",{'type':comtype})
    else:
        return redirect("webguest:login")
    

def feedback(request):
    if 'subadmin_id' in request.session:
        subdata=tbl_subadmin.objects.get(id=request.session["subadmin_id"])
        if request.method=="POST":
            tbl_feedback.objects.create(feedback_con=request.POST.get("txtfeedback"),subadmin=subdata)
            ins1=1
            return render(request,"Subadmin/Feedback.html",{'ins1':ins1})
        else:
            return render(request,"Subadmin/Feedback.html")
    else:
        return redirect("webguest:login")

def viewcomplaints(request):
    if 'subadmin_id' in request.session:
        userdata=tbl_cus_reg.objects.all()
        usercom=tbl_complaint.objects.filter(status=0,customer__in=userdata,customer__cus_locplace__pla__district=request.session["subadmin_district"])
        mdata=tbl_market_reg.objects.all()
        marcom=tbl_complaint.objects.filter(status=0,market__in=mdata,market__place__district=request.session["subadmin_district"])
        fadata=tbl_farmer_reg.objects.all()
        facom=tbl_complaint.objects.filter(status=0,farmer__in=fadata,farmer__locplace__pla__district=request.session["subadmin_district"])
        return render(request,"Subadmin/View_complaints.html",{'customer':usercom,'market':marcom,'farmer':facom})
    else:
        return redirect("webguest:login")

def sendreply(request,comid):
    comdata=tbl_complaint.objects.get(id=comid)
    if request.method=="POST":
        comdata.replay=request.POST.get('txtreplay')
        comdata.status=1
        comdata.rdate=date.today()
        comdata.save()
        se=1
        return render(request,"Subadmin/Reply.html",{'send':se})
    else:
        return render(request,"Subadmin/Reply.html",{'comdata':comdata})

def replyedcom(request):
    if 'subadmin_id' in request.session:
        userdata=tbl_cus_reg.objects.all()
        usercom=tbl_complaint.objects.filter(status=1,customer__in=userdata,customer__cus_locplace__pla__district=request.session["subadmin_district"])
        mdata=tbl_market_reg.objects.all()
        marcom=tbl_complaint.objects.filter(status=1,market__in=mdata,market__place__district=request.session["subadmin_district"])
        fadata=tbl_farmer_reg.objects.all()
        facom=tbl_complaint.objects.filter(status=1,farmer__in=fadata,farmer__locplace__pla__district=request.session["subadmin_district"])
        return render(request,"Subadmin/Replyed_com.html",{'customer':usercom,'market':marcom,'farmer':facom})
    else:
        return redirect("webguest:login")

def reply(request):
    if 'subadmin_id' in request.session:
        reply=tbl_complaint.objects.filter(subadmin=request.session["subadmin_id"])
        return render(request,"Subadmin/View_reply.html",{'subad':reply})
    else:
        return redirect("webguest:login")

def logout(request):
    del request.session["subadmin_id"]
    return redirect("webguest:login")

def customerreport(request):
    subdis=tbl_district.objects.get(id=request.session['subadmin_district'])
    # print(subdis)
    if request.method=="POST":
        if request.POST.get('txtfdate')!="" and request.POST.get('txttdate')!="":
            report=tbl_cus_reg.objects.filter(cus_locplace__pla__district=subdis,cus_doj__gte=request.POST.get('txtfdate'),cus_doj__lte=request.POST.get('txttdate'))
            return render(request,"Subadmin/Customer_report.html",{'cusre':report})
        elif request.POST.get('txtfdate')!="":
            report=tbl_cus_reg.objects.filter(cus_locplace__pla__district=subdis,cus_doj__gte=request.POST.get('txtfdate'))
            return render(request,"Subadmin/Customer_report.html",{'cusre':report})
        elif request.POST.get('txttdate')!="":
            report=tbl_cus_reg.objects.filter(cus_locplace__pla__district=subdis,cus_doj__lte=request.POST.get('txttdate'))
            return render(request,"Subadmin/Customer_report.html",{'cusre':report})
        else:
            return render(request,"Subadmin/Customer_report.html")
    else:
        return render(request,"Subadmin/Customer_report.html")

def farmerreport(request):
    subdis=tbl_district.objects.get(id=request.session['subadmin_district'])
    if request.method=="POST":
        if request.POST.get('txtfdate')!="" and request.POST.get('txttdate')!="":
            report=tbl_farmer_reg.objects.filter(locplace__pla__district=subdis,far_doj__gte=request.POST.get('txtfdate'),far_doj__lte=request.POST.get('txttdate'))
            return render(request,"Subadmin/Farmer_report.html",{'farre':report})
        elif request.POST.get('txtfdate')!="":
            report=tbl_farmer_reg.objects.filter(locplace__pla__district=subdis,far_doj__gte=request.POST.get('txtfdate'))
            return render(request,"Subadmin/Farmer_report.html",{'farre':report})
        elif request.POST.get('txttdate')!="":
            report=tbl_farmer_reg.objects.filter(locplace__pla__district=subdis,far_doj__lte=request.POST.get('txttdate'))
            return render(request,"Subadmin/Farmer_report.html",{'farre':report})
        else:
            return render(request,"Subadmin/Farmer_report.html")
    else:
        return render(request,"Subadmin/Farmer_report.html")

def marketreport(request):
    subdis=tbl_district.objects.get(id=request.session['subadmin_district'])
    if request.method=="POST":
        if request.POST.get('txtfdate')!="" and request.POST.get('txttdate')!="":
            report=tbl_market_reg.objects.filter(place__district=subdis,mar_doj__gte=request.POST.get('txtfdate'),mar_doj__lte=request.POST.get('txttdate'))
            return render(request,"Subadmin/Market_report.html",{'marre':report})
        elif request.POST.get('txtfdate')!="":
            report=tbl_market_reg.objects.filter(place__district=subdis,mar_doj__gte=request.POST.get('txtfdate'))
            return render(request,"Subadmin/Market_report.html",{'marre':report})
        elif request.POST.get('txttdate')!="":
            report=tbl_market_reg.objects.filter(place__district=subdis,mar_doj__lte=request.POST.get('txttdate'))
            return render(request,"Subadmin/Market_report.html",{'marre':report})
        else:
            return render(request,"Subadmin/Market_report.html")
    else:
        return render(request,"Subadmin/Market_report.html")
