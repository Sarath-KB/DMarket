from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *
from datetime import date
# Create your views here.

def home(request):
    if 'adm_name' in request.session:
        return render(request,"Admin/Home.html")
    else:
        return redirect("webguest:adminlogin")

def logout(request):
    del request.session["adm_name"]
    return redirect("webguest:adminlogin")

def district(request):
    if 'adm_name' in request.session:
        districtdata=tbl_district.objects.all()
        if request.method=="POST":
            tbl_district.objects.create(district_name=request.POST.get('txtname'))
            insmsg="inserted"
            return render(request,"Admin/District.html",{'district':districtdata,'insmsg':insmsg})
        else:
            return render(request,"Admin/District.html",{'district':districtdata})
    else:
        return redirect("webguest:adminlogin")

def deletedistrict(request,did):
    tbl_district.objects.get(id=did).delete()
    delete=1
    return render(request,"Admin/District.html",{'dele':delete})

def editdistrict(request,eid):
    data=tbl_district.objects.get(id=eid) 
    if request.method=="POST":
        data.district_name=request.POST.get('txtname')
        data.save()
        up=1
        return render(request,"Admin/District.html",{'up':up})
    else:
        return render(request,"Admin/District.html",{'editdis':data})

def complainttype(request):
    complainttype_data=tbl_complainttype.objects.all()
    if 'adm_name' in request.session:    
        if request.method=="POST":
            tbl_complainttype.objects.create(comp_type_name=request.POST.get('txtcomtype'))
            cominsmsg="inserted"
            return render(request,"Admin/Complaint_type.html",{'comtype':complainttype_data,'cominsmsg':cominsmsg})
        else:    
            return render(request,"Admin/Complaint_type.html",{'comtype':complainttype_data})
    else:
        return redirect("webguest:adminlogin")

def deletecomtype(request,comtypeid):
    tbl_complainttype.objects.get(id=comtypeid).delete()
    de=1
    return render(request,"Admin/Complaint_type.html",{'de':de})

def editcomtype(request,comtypeeid):
    typedata=tbl_complainttype.objects.get(id=comtypeeid)
    if request.method=="POST":
        typedata.comp_type_name=request.POST.get('txtcomtype')
        typedata.save()
        ed=1
        return render(request,"Admin/Complaint_type.html",{'ed':ed})
    else:
        return render(request,"Admin/Complaint_type.html",{'editcomtype':typedata})

def subadmin(request):
    districtdata=tbl_district.objects.all()
    saddata=tbl_subadmin.objects.filter(sad_status=1)
    if 'adm_name' in request.session:
        if request.method=="POST":
            dis=tbl_district.objects.get(id=request.POST.get('seldis'))
            tbl_subadmin.objects.create(sad_name=request.POST.get('txtname'),sad_contact=request.POST.get('txtnum'),sad_email=request.POST.get('txtemail'),sad_address=request.POST.get('txtaddress'),district=dis,sad_photo=request.FILES.get('txtphoto'),sad_pass=request.POST.get('txtpass'))
            subinsmsg="inserted"
            return render(request,"Admin/Add_sub_admin.html",{'district':districtdata,'sadmin':saddata,'subinsmsg':subinsmsg})
        else:    
            return render(request,"Admin/Add_sub_admin.html",{'district':districtdata,'sadmin':saddata})
    else:
        return redirect("webguest:adminlogin")

def deletesadmin(request,sadid):
    subdata=tbl_subadmin.objects.get(id=sadid)
    subdata.sad_status=2
    subdata.save()
    re=1
    return render(request,"Admin/Add_sub_admin.html",{'re':re})

def resubadmin(request):
    saddata=tbl_subadmin.objects.filter(sad_status=2)
    return render(request,"Admin/Rejected_sub_admin.html",{'resub':saddata})

def reapproveadmin(request,reapid):
    subredata=tbl_subadmin.objects.get(id=reapid)
    subredata.sad_status=1
    subredata.save()
    reap=1
    return render(request,"Admin/Rejected_sub_admin.html",{'re':reap})

def place(request):
    districtdata=tbl_district.objects.all()
    placedata=tbl_place.objects.all()
    if 'adm_name' in request.session:
        if request.method=="POST":
            dis=tbl_district.objects.get(id=request.POST.get('seldis'))
            tbl_place.objects.create(place_name=request.POST.get('txtplace'),district=dis)
            plainsmsg="inserted"
            return render(request,"Admin/Place.html",{'district':districtdata,'place':placedata,'plainsmsg':plainsmsg})
        else:
            return render(request,"Admin/Place.html",{'district':districtdata,'place':placedata})
    else:
        return redirect("webguest:adminlogin")

def editplace(request,pid):
    districtdata=tbl_district.objects.all()
    data=tbl_place.objects.get(id=pid)
    if request.method=="POST":
        dis=request.POST.get('seldis')
        data.district=tbl_district.objects.get(id=dis)
        data.place_name=request.POST.get('txtplace')
        data.save()
        up=1
        return render(request,"Admin/Place.html",{'up':up})
    else:
        return render(request,"Admin/Place.html",{'district':districtdata,'data':data})

def deleteplace(request,pid):
    tbl_place.objects.get(id=pid).delete()
    de=1
    return render(request,"Admin/Place.html",{'de':de})

def local_place(request):
    districtdata=tbl_district.objects.all()
    locdata=tbl_local_place.objects.all()
    if 'adm_name' in request.session:
        if request.method=="POST":
            place=tbl_place.objects.get(id=request.POST.get('selplace'))
            tbl_local_place.objects.create(loc_place_name=request.POST.get('txtlocplace'),pla=place)
            locinsmsg="inserted"
            return render(request,"Admin/Local_place.html",{'district':districtdata,'loc':locdata,'locinsmsg':locinsmsg})
        else:
            return render(request,"Admin/Local_place.html",{'district':districtdata,'loc':locdata})
    else:
        return redirect("webguest:adminlogin")

def deletelocplace(request,locplaid):
    tbl_local_place.objects.get(id=locplaid).delete()
    de=1
    return render(request,"Admin/Local_place.html",{'de':de})

def catagory(request):
    catadata=tbl_catageory.objects.filter(cat_status=1)
    if 'adm_name' in request.session:
        if request.method=="POST":
            tbl_catageory.objects.create(cat_name=request.POST.get('txtcat'))
            catinsmsg="inserted"
            return render(request,"Admin/Catageory.html",{'cata':catadata,'catinsmsg':catinsmsg})
        else: 
            return render(request,"Admin/Catageory.html",{'cata':catadata})
    else:
        return redirect("webguest:adminlogin")

def deletecategory(request,catid):
    catadata=tbl_catageory.objects.get(id=catid)
    catadata.cat_status=2
    catadata.save()
    dele=1
    return render(request,"Admin/Catageory.html",{'dele':dele})

def editcategory(request,editcatid):
    catdata=tbl_catageory.objects.get(id=editcatid)
    if request.method=="POST":
        catdata.cat_name=request.POST.get('txtcat')
        catdata.save()
        edi=1
        return render(request,"Admin/Catageory.html",{'edi':edi})
    else:
        return render(request,"Admin/Catageory.html",{'editdata':catdata})

def rejectcatagory(request):
    recat=tbl_catageory.objects.filter(cat_status=2)
    return render(request,"Admin/Rejected_catagory.html",{'recat':recat})

def reapprovecat(request,reapcat):
    reapcatdata=tbl_catageory.objects.get(id=reapcat)
    reapcatdata.cat_status=1
    reapcatdata.save()
    reap=1
    return render(request,"Admin/Rejected_catagory.html",{'reap':reap})

def sub_cat(request):
    catagorydata=tbl_catageory.objects.filter(cat_status=1)
    subdata=tbl_subcat.objects.all()
    if 'adm_name' in request.session:
        if request.method=="POST":
            subcat=tbl_catageory.objects.get(id=request.POST.get('selcat'))
            tbl_subcat.objects.create(subcat_name=request.POST.get('txtsubcat'),cat=subcat)
            subcatinsmsg="inserted"
            return render(request,"Admin/Sub_catagory.html",{'catdata':catagorydata,'subcat':subdata,'subcatinsmsg':subcatinsmsg})
        else:
            return render(request,"Admin/Sub_catagory.html",{'catdata':catagorydata,'subcat':subdata})
    else:
        return redirect("webguest:adminlogin")

def deletesubcat(request,scatid):
    scatdata=tbl_subcat.objects.get(id=scatid).delete()
    de=1
    return render(request,"Admin/Sub_catagory.html",{'de':de})

def editsubcat(request,edsubid):
    cate=tbl_catageory.objects.filter(cat_status=1)
    subcatdata=tbl_subcat.objects.get(id=edsubid)
    if request.method=="POST":
        subcatdata.cat=tbl_catageory.objects.get(id=request.POST.get('selcat'))
        subcatdata.subcat_name=request.POST.get('txtsubcat')
        subcatdata.save()
        ed=1
        return render(request,"Admin/Sub_catagory.html",{'ed':ed})
    else:
        return render(request,"Admin/Sub_catagory.html",{'catdata':cate,'sdata':subcatdata})

def ajaxplace(request):
    districtdata=tbl_district.objects.get(id=request.GET.get('disd'))
    placedata=tbl_place.objects.filter(district=districtdata)
    return render(request,"Admin/Ajaxplace.html",{'data':placedata})

def farmtype(request):
    fmtype=tbl_farmtype.objects.all()
    if 'adm_name' in request.session:
        if request.method=="POST":
            tbl_farmtype.objects.create(farm_type=request.POST.get('txtfarmtype'))
            farinsmsg="inserted"
            return render(request,"Admin/Farm_type.html",{'fmdata':fmtype,'farinsmsg':farinsmsg})
        else:
            return render(request,"Admin/Farm_type.html",{'fmdata':fmtype})
    else:
        return redirect("webguest:adminlogin")

def deletefarmtype(request,fmtypeid):
    fmdata=tbl_farmtype.objects.get(id=fmtypeid).delete()
    de=1
    return render(request,"Admin/Farm_type.html",{'d':de})

def editfarmtype(request,edfmid):
    editfmdata=tbl_farmtype.objects.get(id=edfmid)
    if request.method=="POST":
        editfmdata.farm_type=request.POST.get('txtfarmtype')
        editfmdata.save()
        ed=1
        return render(request,"Admin/Farm_type.html",{'ed':ed})
    else:
        return render(request,"Admin/Farm_type.html",{'editdata':editfmdata})

def viewuser(request):
    userdata=tbl_cus_reg.objects.all()
    if 'adm_name' in request.session:
        return render(request,"Admin/View_users.html",{'user':userdata})
    else:
        return redirect("webguest:adminlogin")

def viewfeedback(request):
    data=tbl_feedback.objects.all()
    if 'adm_name' in request.session:
        return render(request,"Admin/Feedbacks.html",{'data':data})
    else:
        return redirect("webguest:adminlogin")
    
def viewcomplaint(request):
    sadmindata=tbl_subadmin.objects.all()
    if 'adm_name' in request.session:
        subcom=tbl_complaint.objects.filter(status=0,subadmin__in=sadmindata)
        return render(request,"Admin/View_complaint.html",{'subad':subcom})
    else:
        return redirect("webguest:adminlogin")

def reply(request,cmpid):
    data=tbl_complaint.objects.get(id=cmpid)
    if 'adm_name' in request.session:
        if request.method=="POST":
            data.replay=request.POST.get("txtreply")
            data.status=1
            data.rdate=date.today()
            data.save()
            send=1
            return render(request,"Admin/Reply.html",{'se':send})
        else:
            return render(request,"Admin/Reply.html",{'data':data})
    else:
        return redirect("webguest:adminlogin")

def replyedcomplaint(request):
    sadmindata=tbl_subadmin.objects.all()
    if 'adm_name' in request.session:
        subcom=tbl_complaint.objects.filter(status=1,subadmin__in=sadmindata)
        return render(request,"Admin/Replyed_complaint.html",{'subad':subcom})
    else:
        return redirect("webguest:adminlogin")

def customerreport(request):
    # print(subdis)
    if request.method=="POST":
        if request.POST.get('txtfdate')!="" and request.POST.get('txttdate')!="":
            report=tbl_cus_reg.objects.filter(cus_doj__gte=request.POST.get('txtfdate'),cus_doj__lte=request.POST.get('txttdate'))
            return render(request,"Admin/Customer_report.html",{'cusre':report})
        elif request.POST.get('txtfdate')!="":
            report=tbl_cus_reg.objects.filter(cus_doj__gte=request.POST.get('txtfdate'))
            return render(request,"Admin/Customer_report.html",{'cusre':report})
        elif request.POST.get('txttdate')!="":
            report=tbl_cus_reg.objects.filter(cus_doj__lte=request.POST.get('txttdate'))
            return render(request,"Admin/Customer_report.html",{'cusre':report})
        else:
            return render(request,"Admin/Customer_report.html")
    else:
        return render(request,"Admin/Customer_report.html")

def farmerreport(request):
    if request.method=="POST":
        if request.POST.get('txtfdate')!="" and request.POST.get('txttdate')!="":
            report=tbl_farmer_reg.objects.filter(far_doj__gte=request.POST.get('txtfdate'),far_doj__lte=request.POST.get('txttdate'))
            return render(request,"Admin/Farmer_report.html",{'farre':report})
        elif request.POST.get('txtfdate')!="":
            report=tbl_farmer_reg.objects.filter(far_doj__gte=request.POST.get('txtfdate'))
            return render(request,"Admin/Farmer_report.html",{'farre':report})
        elif request.POST.get('txttdate')!="":
            report=tbl_farmer_reg.objects.filter(far_doj__lte=request.POST.get('txttdate'))
            return render(request,"Admin/Farmer_report.html",{'farre':report})
        else:
            return render(request,"Admin/Farmer_report.html")
    else:
        return render(request,"Admin/Farmer_report.html")

def marketreport(request):
    if request.method=="POST":
        if request.POST.get('txtfdate')!="" and request.POST.get('txttdate')!="":
            report=tbl_market_reg.objects.filter(mar_doj__gte=request.POST.get('txtfdate'),mar_doj__lte=request.POST.get('txttdate'))
            return render(request,"Admin/Market_report.html",{'marre':report})
        elif request.POST.get('txtfdate')!="":
            report=tbl_market_reg.objects.filter(mar_doj__gte=request.POST.get('txtfdate'))
            return render(request,"Admin/Market_report.html",{'marre':report})
        elif request.POST.get('txttdate')!="":
            report=tbl_market_reg.objects.filter(mar_doj__lte=request.POST.get('txttdate'))
            return render(request,"Admin/Market_report.html",{'marre':report})
        else:
            return render(request,"Admin/Market_report.html")
    else:
        return render(request,"Admin/Market_report.html")