from django.shortcuts import render,redirect
from django.utils import timezone
from Admin.models import *
from Guest.models import *
from Farmer.models import *
from Market.models import *
from Customer.models import *
from datetime import date
from datetime import datetime
import random
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.
def home(request):
    if 'customer_id' in request.session:
        current_datetime = timezone.now()
        bookd=[]
        #print(current_datetime)
        # cus=tbl_cus_reg.objects.get(id=request.session["customer_id"])
        cartsdata=tbl_farmer_cart.objects.filter(fcart_status=2)
        for k in cartsdata:
            if k.bookingid.id in bookd:
                continue
            else:
                bookd.append(k.bookingid.id)
        fbook=tbl_farmer_booking.objects.filter(booking_status__lt=3,booking_status__gt=0).exclude(id__in=bookd)
        

        for i in fbook:
            start_time=i.date_time
            email=i.user.cus_email
            time_difference = current_datetime - start_time
            hours_difference = time_difference.total_seconds() // 3600
            #print(hours_difference)
            if hours_difference > 24:
                send_mail(
                            'Respected Sir/Madam ',#subject
                            "\rYour order was cancelled becacuse of"
                            "\r1, You didn't collect the product from the outlet within 24 hours. "
                            "\r2, if it is online payment, your amount will be refunded within two or three days."
                            "\r By"
                            "\r D MARKET" ,#body
                            settings.EMAIL_HOST_USER,
                            [email],
                        )
                cartdata=tbl_farmer_cart.objects.filter(bookingid=i.id)
                for j in cartdata:
                    pdt=j.productid.id
                    pdtdata=tbl_farmer_product.objects.get(id=pdt)
                    stock=pdtdata.pdt_stock            
                    s=stock*1000
                    quantity=j.fquantity
                    q=quantity*1000
                    t=s+q
                    total=t/1000
                    pdtdata.pdt_stock=total
                    pdtdata.save()
                tbl_farmer_booking.objects.get(id=i.id).delete()
        marbookid=[]
        mcartdatas=tbl_market_cart.objects.filter(mcart_status=2)
        for a in mcartdatas:
            if a.bookingid.id in marbookid:
                continue
            else:
                marbookid.append(a.bookingid.id)
        mbook=tbl_market_booking.objects.filter(booking_status__lt=3,booking_status__gt=0).exclude(id__in=marbookid)

        
        for i in mbook:
            start_time=i.date_time
            email=i.user.cus_email
            time_difference = current_datetime - start_time
            hours_difference = time_difference.total_seconds() // 3600
            #print(type(hours_difference))
            # print(hours_difference)
            if hours_difference >= 24:
                send_mail(
                            'Respected Sir/Madam ',#subject
                            "\rYour order was cancelled becacuse of"
                            "\r1, You didn't collect the product from the outlet within 24 hours. "
                            "\r2, if it is online payment, your amount will be refunded within two or three days."
                            "\r By"
                            "\r D MARKET" ,#body
                            settings.EMAIL_HOST_USER,
                            [email],
                        )
                mcartdata=tbl_market_cart.objects.filter(bookingid=i.id)
                for j in mcartdata:
                    mpdt=j.productid.id
                    mpdtdata=tbl_market_product.objects.get(id=mpdt)
                    mstock=mpdtdata.pdt_stock
                    ms=mstock*1000
                    mqun=j.mquantity
                    mq=mqun*1000
                    mt=ms+mq
                    mtotal=mt/1000
                    mpdtdata.pdt_stock=mtotal
                    mpdtdata.save()
                tbl_market_booking.objects.get(id=i.id).delete()
        cdate=date.today()
        placedata=tbl_place.objects.get(id=request.session["customer_place"])
        eventdata=tbl_events.objects.filter(market__place=placedata,event_tdate__gte=cdate)
        user=tbl_cus_reg.objects.get(id=request.session['customer_id'])
        return render(request,"Customer/Home.html",{'event':eventdata,'user':user})
    else:
        return redirect("webguest:login")

def logout(request):
    del request.session["customer_id"]
    return redirect("webguest:login")

def my_pro(request):
    if 'customer_id' in request.session:
        data=tbl_cus_reg.objects.get(id=request.session["customer_id"])
        return render(request,"Customer/My_profile.html",{'data':data})
    else:
        return redirect("webguest:login")

def editpropic(request):
    if 'customer_id' in request.session:
        cusprodata=tbl_cus_reg.objects.get(id=request.session["customer_id"])
        if request.method=="POST" and request.FILES:
            cusprodata.cus_photo=request.FILES.get("txtpropic")
            cusprodata.save()
            ins=1
            return render(request,"Customer/Edit_pro_pic.html",{'inserted':ins})
        else:
            return render(request,"Customer/Edit_pro_pic.html",{'picdata':cusprodata})
    else:
        return redirect("webguest:login")

def editprofile(request):
    if 'customer_id' in request.session:
        prodata=tbl_cus_reg.objects.get(id=request.session["customer_id"])
        if request.method=="POST":
            prodata.cus_name=request.POST.get('txtname')
            prodata.cus_contact=request.POST.get('txtcon')
            prodata.cus_email=request.POST.get('txtemail')
            prodata.cus_address=request.POST.get('txtaddress')
            prodata.save()
            ed=1
            return render(request,"Customer/Edit_profile.html",{'ed':ed})
        else:
            return render(request,"Customer/Edit_profile.html",{'prodata':prodata})
    else:
        return redirect("webguest:login")

def changepassword(request):
    if 'customer_id' in request.session:
        if request.method=="POST":
            ccount=tbl_cus_reg.objects.filter(id=request.session["customer_id"],cus_pass=request.POST.get('txtcurpass')).count()
            if ccount>0:
                if request.POST.get('txtnewpass')==request.POST.get('txtconpass'):
                    userdata=tbl_cus_reg.objects.get(id=request.session["customer_id"],cus_pass=request.POST.get('txtcurpass'))
                    userdata.cus_pass=request.POST.get('txtnewpass')
                    userdata.save()
                    er3=3
                    return render(request,"Customer/Change_password.html",{'er':er3})
                else:
                    er1=1
                    return render(request,"Customer/Change_password.html",{'er':er1})
            else:
                er2=2
                return render(request,"Customer/Change_password.html",{'er':er2})
        else:
            return render(request,"Customer/Change_password.html")
    else:
        return redirect("webguest:login")

def search_far(request):
    if 'customer_id' in request.session:
        disdata=tbl_district.objects.all()
        fardata=tbl_farmer_reg.objects.filter(far_status=1)
        return render(request,"Customer/Search_farmer.html",{'dis':disdata,'far':fardata})
    else:
        return redirect("webguest:login")

def search_mar(request):
    if 'customer_id' in request.session:
        disdata=tbl_district.objects.all()
        mardata=tbl_market_reg.objects.filter(mar_status=1)
        return render(request,"Customer/Search_market.html",{'dis':disdata,'mar':mardata})
    else:
        return redirect("webguest:login")

def marketpro(request,marketid):
    if 'customer_id' in request.session:
        marketdata=tbl_market_reg.objects.get(id=marketid)
        return render(request,"Customer/Market_profile.html",{'mardata':marketdata})
    else:
        return redirect("webguest:login")

def marketpdt(request,markpdtid):
    if 'customer_id' in request.session:
        cat=tbl_catageory.objects.filter(cat_status=1)
        request.session["mdid"]=markpdtid
        marketdata=tbl_market_product.objects.filter(market=markpdtid)
        return render(request,"Customer/Market_pdt.html",{'mdata':marketdata,'cat':cat})
    else:
        return redirect("webguest:login")

def ajaxmarketproduct(request):
    if request.GET.get("sub")!="":
        subdata=tbl_subcat.objects.get(id=request.GET.get("sub"))
        marpdt=tbl_market_product.objects.filter(subcategory=subdata,market=request.session["mdid"])
        return render(request,"Customer/ajaxmarketpdt.html",{'mdata':marpdt})
    else:
        cat=tbl_catageory.objects.get(id=request.GET.get("cat"))
        marpdt=tbl_market_product.objects.filter(subcategory__cat=cat,market=request.session["mdid"])
        return render(request,"Customer/ajaxmarketpdt.html",{'mdata':marpdt})

def marketcart(request,marketpdtid):
    if 'customer_id' in request.session:
        mpdtdetails=tbl_market_product.objects.get(id=marketpdtid)
        cusdata=tbl_cus_reg.objects.get(id=request.session["customer_id"])
        mbookcount=tbl_market_booking.objects.filter(user=cusdata,booking_status=0).count()
        if mbookcount>0:
            mbookdata=tbl_market_booking.objects.get(user=cusdata,booking_status=0)
            cartcount=tbl_market_cart.objects.filter(bookingid=mbookdata,productid=mpdtdetails).count()
            if cartcount>0:
                er=1
                return render(request,"Customer/Market_pdt.html",{'error':er})
            else:
                tbl_market_cart.objects.create(bookingid=mbookdata,productid=mpdtdetails)
                ins=1
                return render(request,"Customer/Market_pdt.html",{'ins':ins})
        else:
            tbl_market_booking.objects.create(user=cusdata)
            mbookcount=tbl_market_booking.objects.filter(user=cusdata,booking_status=0).count()
            if mbookcount>0:
                mbookdata=tbl_market_booking.objects.get(user=cusdata,booking_status=0)
                cartcount=tbl_market_cart.objects.filter(bookingid=mbookdata,productid=mpdtdetails).count()
                if cartcount>0:
                    er=1
                    return render(request,"Customer/Market_pdt.html",{'error':er})
                else:
                    tbl_market_cart.objects.create(bookingid=mbookdata,productid=mpdtdetails)
                    ins=1
                    return render(request,"Customer/Market_pdt.html",{'ins':ins})
            else:
                return render(request,"Customer/Market_pdt.html")
    else:
        return redirect("webguest:login")

def ajaxmarket(request):
    if request.GET.get("pid")!="":
        placedata=tbl_place.objects.get(id=request.GET.get("pid"))
        mardata=tbl_market_reg.objects.filter(mar_status=1,place=placedata)
        return render(request,"Customer/ajaxmarket.html",{'mar':mardata})
    else:
        districtdata=tbl_district.objects.get(id=request.GET.get('did'))
        mardata=tbl_market_reg.objects.filter(mar_status=1,place__district=districtdata)
        return render(request,"Customer/ajaxmarket.html",{'mar':mardata})
        
def ajaxfarmer(request):
    if request.GET.get("lpid")!="":
        lplacedata=tbl_local_place.objects.get(id=request.GET.get("lpid"))
        fardata=tbl_farmer_reg.objects.filter(far_status=1,locplace=lplacedata)
        return render(request,"Customer/ajaxfarmer.html",{'fardata':fardata})
    elif request.GET.get("pid")!="":
        placedata=tbl_place.objects.get(id=request.GET.get("pid"))
        fardata=tbl_farmer_reg.objects.filter(far_status=1,locplace__pla=placedata)
        return render(request,"Customer/ajaxfarmer.html",{'fardata':fardata})
    else:
        districtdata=tbl_district.objects.get(id=request.GET.get('did'))
        fardata=tbl_farmer_reg.objects.filter(far_status=1,locplace__pla__district=districtdata)
        return render(request,"Customer/ajaxfarmer.html",{'fardata':fardata})

def farmarpro(request,farid):
    if 'customer_id' in request.session:
        fardata=tbl_farmer_reg.objects.get(id=farid)
        return render(request,"Customer/Farmer_profile.html",{'data':fardata})
    else:
        return redirect("webguest:login")

def farmerpdt(request,farpdtid):
    if 'customer_id' in request.session:
        farpdtdata=tbl_farmer_product.objects.filter(farmer=farpdtid)
        return render(request,"Customer/Farmer_pdt.html",{'data':farpdtdata})
    else:
        return redirect("webguest:login")

def AddCart(request,pdtid):
    if 'customer_id' in request.session:
        pdtdetails=tbl_farmer_product.objects.get(id=pdtid)
        cusdata=tbl_cus_reg.objects.get(id=request.session["customer_id"])
        bookcount=tbl_farmer_booking.objects.filter(user=cusdata,booking_status=0).count()
        if bookcount>0:
            bookdata=tbl_farmer_booking.objects.get(user=cusdata,booking_status=0)
            cartcount=tbl_farmer_cart.objects.filter(bookingid=bookdata,productid=pdtdetails).count()
            if cartcount>0:
                er=1
                return render(request,"Customer/Farmer_pdt.html",{'error':er})
            else:
                tbl_farmer_cart.objects.create(bookingid=bookdata,productid=pdtdetails)
                ins=1
                return render(request,"Customer/Farmer_pdt.html",{'ins':ins})
        else:     
            tbl_farmer_booking.objects.create(user=cusdata)
            bookcount=tbl_farmer_booking.objects.filter(user=cusdata,booking_status=0).count()
            if bookcount>0:
                bookdata=tbl_farmer_booking.objects.get(user=cusdata,booking_status=0)
                cartcount=tbl_farmer_cart.objects.filter(bookingid=bookdata,productid=pdtdetails).count()
                if cartcount>0:
                    er=1
                    return render(request,"Customer/Farmer_pdt.html",{'error':er})
                else:
                    tbl_farmer_cart.objects.create(bookingid=bookdata,productid=pdtdetails)
                    ins=1
                    return render(request,"Customer/Farmer_pdt.html",{'ins':ins})
            else:
                return render(request,"Customer/Search_farmer.html")
    else:
        return redirect("webguest:login")

def mycart(request):
    if 'customer_id' in request.session:
        cartdata=tbl_farmer_cart.objects.filter(bookingid__user=request.session["customer_id"],bookingid__booking_status=0)
        cartcount=tbl_farmer_cart.objects.filter(bookingid__user=request.session["customer_id"],bookingid__booking_status=0).count()
        mcartdata=tbl_market_cart.objects.filter(bookingid__user=request.session["customer_id"],bookingid__booking_status=0)
        mcartcount=tbl_market_cart.objects.filter(bookingid__user=request.session["customer_id"],bookingid__booking_status=0).count()
        mtotal=ftotal=0
        if (cartcount>0)&(mcartcount>0):
            for i in cartdata:
                ftotal=ftotal + (float(i.fquantity) * float(i.productid.pdt_rate))
                ftotal=int(ftotal)
            for i in mcartdata:
                mtotal=mtotal + (float(i.mquantity) * float(i.productid.pdt_rate))
                mtotal=int(mtotal)
            cart=1
            return render(request,"Customer/My_cart.html",{'mdata':mcartdata,'mtot':mtotal,'cdata':cartdata,'ftot':ftotal,'cart':cart})
        elif mcartcount>0:
            for i in mcartdata:
                mtotal=mtotal + (float(i.mquantity) * float(i.productid.pdt_rate))
                mtotal=int(mtotal)
            cart=2
            return render(request,"Customer/My_cart.html",{'mdata':mcartdata,'mtot':mtotal,'cart':cart})
        elif cartcount>0:
            for i in cartdata:
                ftotal=ftotal + (float(i.fquantity) * float(i.productid.pdt_rate))
                ftotal=int(ftotal)
            cart=3
            return render(request,"Customer/My_cart.html",{'cdata':cartdata,'ftot':ftotal,'cart':cart})
        else:
            cart=4
            return render(request,"Customer/My_cart.html",{'cart':cart})
    else:
        return redirect("webguest:login")
    

def deletecartitem(request,catdelid):
    tbl_farmer_cart.objects.get(id=catdelid).delete()
    dele=1
    return render(request,"Customer/My_cart.html",{'de':dele})

def mdeletecartitem(request,mcartid):
    tbl_market_cart.objects.get(id=mcartid).delete()
    dele=1
    return render(request,"Customer/My_cart.html",{'de':dele})
    
def ajaxcartamt(request):
    cdata=tbl_farmer_cart.objects.get(id=request.GET.get("cartid"))
    qudata=request.GET.get("qid")
    cdata.fquantity=qudata
    cdata.save()
    return redirect("webcustomer:mycart")

def ajaxmarketpdtamt(request):
    madata=tbl_market_cart.objects.get(id=request.GET.get("cartid"))
    qdata=request.GET.get("qid")
    madata.mquantity=qdata
    madata.save()
    return redirect("webcustomer:mycart")

def mpaymmentoffline(request):
    quantity=tbl_market_cart.objects.filter(bookingid__booking_status=0,bookingid__user=request.session["customer_id"])
    for a in quantity:
        if a.mquantity<=0:
            tbl_market_cart.objects.get(id=a.id).delete()

    qun=tbl_market_cart.objects.filter(bookingid__booking_status=0,bookingid__user=request.session["customer_id"])
    quncount=tbl_market_cart.objects.filter(bookingid__booking_status=0,bookingid__user=request.session["customer_id"]).count()
    for i in qun:
        prdata=tbl_market_product.objects.get(id=i.productid.id)
        stock=prdata.pdt_stock
        st=stock*1000
        mqun=i.mquantity
        mq=mqun*1000
        bal=st-mq
        tbal=bal/1000
        if mq>st:
            out=1
            return render(request,"Customer/My_cart.html",{'sout':out})
        else:
            prdatas=tbl_market_product.objects.get(id=i.productid.id)
            prdata.pdt_stock=tbal
            prdata.save()
            bkid=i.bookingid.id
            bookdata=tbl_market_booking.objects.get(id=bkid)
            bookdata.date_time=timezone.now()
            bookdata.save()
            if tbal==0:
                use=tbl_cus_reg.objects.get(id=request.session["customer_id"])
                da=tbl_market_cart.objects.filter(bookingid__booking_status=0,productid=prdatas)
                for j in da:
                    if j.bookingid.user!=use:
                        j.mquantity=0
                        j.save()
                da1=tbl_m_cart.objects.filter(bookingid__booking_status=0,productid=prdatas)
                for p in da1:
                    p.mquantity=0
                    p.save()
                bid=qun[0].bookingid.id
                bdata=tbl_market_booking.objects.get(id=bid)
                # bdata.mpayment_date=date.today()
                bdata.booking_status=2
                bdata.save()
                bk=1
                # return render(request,"Customer/Home.html",{'book':bk})
            else:
                bid=qun[0].bookingid.id
                bdata=tbl_market_booking.objects.get(id=bid)
                # bdata.mpayment_date=date.today()
                bdata.booking_status=2
                bdata.save()
                bk=1
                # return render(request,"Customer/Home.html",{'book':bk})
    # print(quncount)
    user=tbl_cus_reg.objects.get(id=request.session["customer_id"])
    email=user.cus_email
    name=user.cus_name
    send_mail(
            'Respected ' + str(name),#subject
            "\rYou ordered "+str(quncount)+" items. Your payment type is cash on delivery."
            "Thank you for choosing us for your shopping needs! We truly appreciate your visit and hope you had a wonderful experience exploring our products."
            "We value your patronage and want to express our gratitude for your support." 
            "Our team is committed to providing exceptional service, and we hope we met or even exceeded your expectations during your shopping trip."
            "If you have any feedback or suggestions, we would love to hear from you. "
            "Your input helps us improve our services and ensure we continue to deliver a fantastic shopping experience."
            "Once again, thank you for shopping with us. We look forward to serving you again in the future. Have a fantastic day!"
            "Best regards,"
            "D MARKET"
            "\r <<<<  WARNNING : BOOKING VALIDITY ONLY FOR 24 HOHURS  >>>>",#body
            settings.EMAIL_HOST_USER,
            [email],
        )
    return redirect("webcustomer:home")

def mpayment(request,mamt):
    quantity=tbl_market_cart.objects.filter(bookingid__booking_status=0,bookingid__user=request.session["customer_id"])
    for a in quantity:
        if a.mquantity<=0:
            tbl_market_cart.objects.get(id=a.id).delete()

    if request.method=="POST":
        quncount=tbl_market_cart.objects.filter(bookingid__booking_status=0,bookingid__user=request.session["customer_id"]).count()
        qun=tbl_market_cart.objects.filter(bookingid__booking_status=0,bookingid__user=request.session["customer_id"])
        for i in qun:
            pdata=tbl_market_product.objects.get(id=i.productid.id)
            stock=pdata.pdt_stock
            st=stock*1000
            mqun=i.mquantity
            mq=mqun*1000
            bal=st-mq
            tbal=bal/1000
            if mq>st:
                out=1
                return render(request,"Customer/Mpayment.html",{'out':out})
            #else:
            datas=tbl_market_product.objects.get(id=i.productid.id)
            datas.pdt_stock=tbal
            bkid=i.bookingid.id
            bookdata=tbl_market_booking.objects.get(id=bkid)
            bookdata.date_time=timezone.now()
            bookdata.save()
            datas.save()
            #########################
            
            if tbal==0:
                use=tbl_cus_reg.objects.get(id=request.session["customer_id"])
                dms=tbl_market_cart.objects.filter(bookingid__booking_status=0,productid=datas)
                for j in dms:
                    if j.bookingid.user!=use:
                        j.mquantity=0
                        j.save()
                dms1=tbl_m_cart.objects.filter(bookingid__booking_status=0,productid=datas)
                for p in dms1:
                    p.mquantity=0
                    p.save()
                bid=qun[0].bookingid.id
                bdata=tbl_market_booking.objects.get(id=bid)
                bdata.mpayment_date=date.today()
                bdata.booking_status=1
                bdata.save()
                # return redirect("webcustomer:loader")
            else:
                bid=qun[0].bookingid.id
                bdata=tbl_market_booking.objects.get(id=bid)
                bdata.mpayment_date=date.today()
                bdata.booking_status=1
                bdata.save()
        # print(quncount)
        user=tbl_cus_reg.objects.get(id=request.session["customer_id"])
        email=user.cus_email
        name=user.cus_name
        send_mail(
                'Respected '+ str(name),#subject
                "\rYou ordered "+ str(quncount) +" items. Your payment type is online payment"
                "\rThank you for choosing us for your shopping needs! We truly appreciate your visit and hope you had a wonderful experience exploring our products."
                "\rWe value your patronage and want to express our gratitude for your support." 
                "\rOur team is committed to providing exceptional service, and we hope we met or even exceeded your expectations during your shopping trip."
                "\rIf you have any feedback or suggestions, we would love to hear from you. "
                "\rYour input helps us improve our services and ensure we continue to deliver a fantastic shopping experience."
                "\rOnce again, thank you for shopping with us. We look forward to serving you again in the future. Have a fantastic day!"
                "\rBest regards,"
                "\rD MARKET"
                "\r <<<<  WARNNING : BOOKING VALIDITY ONLY FOR 24 HOHURS  >>>>",#body
                settings.EMAIL_HOST_USER,
                [email],
            )
        return redirect("webcustomer:loader")
    else:
        return render(request,"Customer/Mpayment.html",{'total':mamt})

def fpaymentoffline(request):
    quantity=tbl_farmer_cart.objects.filter(bookingid__booking_status=0,bookingid__user=request.session["customer_id"])
    for a in quantity:
        if a.fquantity<=0:
            tbl_farmer_cart.objects.get(id=a.id).delete()
    quncount=tbl_farmer_cart.objects.filter(bookingid__booking_status=0,bookingid__user=request.session["customer_id"]).count()
    qun=tbl_farmer_cart.objects.filter(bookingid__booking_status=0,bookingid__user=request.session["customer_id"])
    for i in qun:
        prdata=tbl_farmer_product.objects.get(id=i.productid.id)
        stock=prdata.pdt_stock
        st=stock*1000
        fqun=i.fquantity
        fq=fqun*1000
        bal=st-fq
        tbal=bal/1000
        if fq>st:
            out=1
            return render(request,"Customer/My_cart.html",{'sout':out})
        else:
            prdatas=tbl_farmer_product.objects.get(id=i.productid.id)
            prdatas.pdt_stock=tbal
            prdatas.save()
            bkid=i.bookingid.id
            bookdata=tbl_farmer_booking.objects.get(id=bkid)
            bookdata.date_time=timezone.now()
            bookdata.save()
            if tbal==0:
                use=tbl_cus_reg.objects.get(id=request.session["customer_id"])
                da=tbl_farmer_cart.objects.filter(bookingid__booking_status=0,productid=prdatas)
                for j in da:
                    if j.bookingid.user!=use:
                        j.mquantity=0
                        j.save()
                bid=qun[0].bookingid.id
                bdata=tbl_farmer_booking.objects.get(id=bid)
                # bdata.fpayment_date=date.today()
                bdata.booking_status=2
                bdata.save()
                bk=1
                #return render(request,"Customer/Home.html",{'book':bk})
            else:
                bid=qun[0].bookingid.id
                bdata=tbl_farmer_booking.objects.get(id=bid)
                # bdata.fpayment_date=date.today()
                bdata.booking_status=2
                bdata.save()
                bk=1
                #return render(request,"Customer/Home.html",{'book':bk})
    # print(quncount)
    user=tbl_cus_reg.objects.get(id=request.session["customer_id"])
    email=user.cus_email
    name=user.cus_name
    send_mail(
            'Respected ' + str(name),#subject
            "\rYou ordered "+str(quncount)+" items. Your payment type is cash on delivery."
            "\rThank you for choosing us for your shopping needs! We truly appreciate your visit and hope you had a wonderful experience exploring our products."
            "\rWe value your patronage and want to express our gratitude for your support." 
            "\rOur team is committed to providing exceptional service, and we hope we met or even exceeded your expectations during your shopping trip."
            "\rIf you have any feedback or suggestions, we would love to hear from you. "
            "\rYour input helps us improve our services and ensure we continue to deliver a fantastic shopping experience."
            "\rOnce again, thank you for shopping with us. We look forward to serving you again in the future. Have a fantastic day!"
            "\rBest regards,"
            "\rD MARKET"
            "\r <<<<  WARNNING : BOOKING VALIDITY ONLY FOR 24 HOHURS  >>>>",#body
            settings.EMAIL_HOST_USER,
            [email],
        )
    return redirect("webcustomer:home") 

def fpayment(request,famt):
    quantity=tbl_farmer_cart.objects.filter(bookingid__booking_status=0,bookingid__user=request.session["customer_id"])
    for a in quantity:
        if a.fquantity<=0:
            tbl_farmer_cart.objects.get(id=a.id).delete()

    if request.method=="POST":
        qun=tbl_farmer_cart.objects.filter(bookingid__booking_status=0,bookingid__user=request.session["customer_id"])

        quncount=tbl_farmer_cart.objects.filter(bookingid__booking_status=0,bookingid__user=request.session["customer_id"]).count()
        for i in qun:
            pdata=tbl_farmer_product.objects.get(id=i.productid.id)
            stock=pdata.pdt_stock
            st=stock*1000
            fqun=i.fquantity
            fq=fqun*1000
            bal=st-fq
            tbal=bal/1000
            pdata.pdt_stock=tbal
            pdata.save()
            if fq>st:
                out=1
                return render(request,"Customer/Fpayment.html",{'out':out})
            else:
                prdatas=tbl_farmer_product.objects.get(id=i.productid.id)
                prdatas.pdt_stock=tbal
                prdatas.save()
                bkid=i.bookingid.id
                bookdata=tbl_farmer_booking.objects.get(id=bkid)
                bookdata.date_time=timezone.now()
                bookdata.save()
                if tbal==0:
                    use=tbl_cus_reg.objects.get(id=request.session["customer_id"])
                    dms=tbl_farmer_cart.objects.filter(bookingid__booking_status=0,productid=pdata)
                    for j in dms:
                        if j.bookingid.user!=use:
                            j.fquantity=0
                            j.save()
                    fdataid=qun[0].bookingid.id
                    fdata=tbl_farmer_booking.objects.get(id=fdataid)
                    fdata.fpayment_date=date.today()
                    fdata.booking_status=1
                    fdata.save()
                    # return redirect("webcustomer:loader")
                else:
                    fdataid=qun[0].bookingid.id
                    fdata=tbl_farmer_booking.objects.get(id=fdataid)
                    fdata.fpayment_date=date.today()
                    fdata.booking_status=1
                    fdata.save()
        # print(quncount)
        user=tbl_cus_reg.objects.get(id=request.session["customer_id"])
        email=user.cus_email
        name=user.cus_name
        send_mail(
                'Respected ' + str(name),#subject
                "\rYou ordered "+str(quncount)+" items. Your payment type is online payment"
                "\rThank you for choosing us for your shopping needs! We truly appreciate your visit and hope you had a wonderful experience exploring our products."
                "\rWe value your patronage and want to express our gratitude for your support." 
                "\rOur team is committed to providing exceptional service, and we hope we met or even exceeded your expectations during your shopping trip."
                "\rIf you have any feedback or suggestions, we would love to hear from you. "
                "\rYour input helps us improve our services and ensure we continue to deliver a fantastic shopping experience."
                "\rOnce again, thank you for shopping with us. We look forward to serving you again in the future. Have a fantastic day!"
                "\rBest regards,"
                "\rD MARKET"
                "\r <<<<  WARNNING : BOOKING VALIDITY ONLY FOR 24 HOHURS  >>>>",#body
                settings.EMAIL_HOST_USER,
                [email],
            )
        return redirect("webcustomer:loader")
    else:
        return render(request,"Customer/Fpayment.html",{'total':famt})

def loader(request):
    return render(request,"Customer/Loader.html")

def paymentsuc(request):
    return render(request,"Customer/Payment_suc.html")

def mybooking(request):
    if 'customer_id' in request.session:
        customer=tbl_cus_reg.objects.get(id=request.session["customer_id"])
        ###################################################################################################
        counts=tbl_market_cart.objects.filter(bookingid__user=request.session["customer_id"],mcart_status__lt=1).count()
        parray=[0 for i in range(1,counts+1)]
        j=0 
        mpdtdata=tbl_market_cart.objects.filter(bookingid__user=request.session["customer_id"],mcart_status__lt=1)
        for i in mpdtdata:
            parray[j]=i.bookingid.id
            j=j+1

        ###################################################################################################
        ###################################################################################################
        marbookdata=tbl_market_booking.objects.filter(user=customer,booking_status__gt=0,booking_status__lt=3,id__in=parray)
        mcartda=tbl_market_cart.objects.filter(bookingid__in=parray)
        mtotals=[]
        m2=1
        for m1 in marbookdata:
            marcartdata=tbl_market_cart.objects.filter(bookingid=m1.id,mcart_status=0)
            mtotal=0
            for m2 in marcartdata:
                mtotal=mtotal+(float(m2.mquantity)*float(m2.productid.pdt_rate))
            mtotals.append(mtotal)
        ###################################################################################################
        ###################################################################################################
        farcounts=tbl_farmer_cart.objects.filter(bookingid__user=request.session["customer_id"],fcart_status__lt=1).count()
        fparray=[0 for i in range(1,farcounts+1)]
        p=0 
        fpdtdata=tbl_farmer_cart.objects.filter(bookingid__user=request.session["customer_id"],fcart_status__lt=1)
        for i in fpdtdata:
            fparray[p]=i.bookingid.id
            p=p+1

        ###################################################################################################
        ###################################################################################################
        farbookdata=tbl_farmer_booking.objects.filter(user=customer,booking_status__gt=0,booking_status__lt=3,id__in=fparray)
        fcartda=tbl_farmer_cart.objects.filter(bookingid__in=fparray)
        ftotals=[]
        f2=0
        for f1 in farbookdata:
            farcartdata=tbl_farmer_cart.objects.filter(bookingid=f1.id,fcart_status=0)
            ftotal=0
            for f2 in farcartdata:
                ftotal=ftotal+(float(f2.fquantity)*float(f2.productid.pdt_rate))
            ftotals.append(ftotal)
        ###################################################################################################
        mbookdatacount=tbl_market_booking.objects.filter(user=customer,booking_status__gt=0,booking_status__lt=3,id__in=parray).count()
        fbookdatacount=tbl_farmer_booking.objects.filter(user=customer,booking_status__gt=0,booking_status__lt=3,id__in=fparray).count()
        if mbookdatacount > 0 and fbookdatacount>0 :
            mbookdata=tbl_market_booking.objects.filter(user=customer,booking_status__gt=0,booking_status__lt=3,id__in=parray)
            mbookdatas=zip(mbookdata,mtotals,mcartda)
            mbookid=mbookdata[0]
            mcartdata=tbl_market_cart.objects.filter(bookingid=mbookid,mcart_status=0)

            fbookdata=tbl_farmer_booking.objects.filter(user=customer,booking_status__gt=0,booking_status__lt=3,id__in=fparray)
            fbookdatas=zip(fbookdata,ftotals,fcartda)
            fbookid=fbookdata[0]
            fcartdata=tbl_farmer_cart.objects.filter(bookingid=fbookid,fcart_status=0)

            return render(request,"Customer/My_booking.html",{'mardata':mbookdatas,'fardata':fbookdatas})
        elif mbookdatacount > 0:
            mbookdata=tbl_market_booking.objects.filter(user=customer,booking_status__gt=0,booking_status__lt=3,id__in=parray)
            mbookdatas=zip(mbookdata,mtotals,mcartda)
            mbookid=mbookdata[0]
            mcartdata=tbl_market_cart.objects.filter(bookingid=mbookid,mcart_status=0)
            return render(request,"Customer/My_booking.html",{'mardata':mbookdatas})
        
        elif fbookdatacount>0 :
            fbookdata=tbl_farmer_booking.objects.filter(user=customer,booking_status__gt=0,booking_status__lt=3,id__in=fparray)
            fbookdatas=zip(fbookdata,ftotals,fcartda)
            fbookid=fbookdata[0]
            fcartdata=tbl_farmer_cart.objects.filter(bookingid=fbookid,fcart_status=0)
            return render(request,"Customer/My_booking.html",{'fardata':fbookdatas})
        else:
            return render(request,"Customer/My_booking.html",{'mess':1})
    else:
        return redirect("webguest:login")

def mymarketproduct(request,pdid):
    if 'customer_id' in request.session:
        mpdtdata=tbl_market_cart.objects.filter(bookingid__booking_status__gt=0,bookingid__user=request.session["customer_id"],bookingid=pdid,mcart_status=0)
        return render(request,"Customer/My_market_product.html",{'market':mpdtdata,'bkid':pdid})
    else:
        return redirect("webguest:login")

def mymarketdeliveredpdt(request,delpid):
    if 'customer_id' in request.session:
        mpdtdata=tbl_market_cart.objects.filter(bookingid__booking_status__gt=0,bookingid__user=request.session["customer_id"],bookingid=delpid,mcart_status=2)
        return render(request,"Customer/My_market_delivered_pdt.html",{'market':mpdtdata,'bkid':delpid})
    else:
        return redirect("webguest:login")

def deletemitembooking(request,itemid):
    market=tbl_market_cart.objects.get(id=itemid)
    itemquantity=market.mquantity
    itemqun=itemquantity*1000
    product=market.productid.id
    pdt=tbl_market_product.objects.get(id=product)
    stock=pdt.pdt_stock
    st=stock*1000
    total=itemqun+st
    tot=total/1000
    pdt.pdt_stock=tot
    pdt.save()
    market.mcart_status=1
    market.save()
    stup=1
    user=tbl_cus_reg.objects.get(id=request.session["customer_id"])
    email=user.cus_email
    send_mail(
                'Respected Sir/Madam ',#subject
                "\rOne item order is cancelled." ,#body
                settings.EMAIL_HOST_USER,
                [email],
            )
    return render(request,"Customer/Home.html",{'st':stup})

def myfarmerproduct(request,fpdid):
    if 'customer_id' in request.session:
        fpdtdata=tbl_farmer_cart.objects.filter(bookingid__booking_status__gt=0,bookingid__user=request.session["customer_id"],bookingid=fpdid,fcart_status=0)
        return render(request,"Customer/My_farmer_product.html",{'farmer':fpdtdata,'fbkid':fpdid})
    else:
        return redirect("webguest:login")

def myfarmerdeliveredpdt(request,fdelpid):
    if 'customer_id' in request.session:
        fpdtdata=tbl_farmer_cart.objects.filter(bookingid__booking_status__gt=0,bookingid__user=request.session["customer_id"],bookingid=fdelpid,fcart_status=2)
        return render(request,"Customer/My_farmer_product.html",{'farmer':fpdtdata,'fbkid':fdelpid})
    else:
        return redirect("webguest:login")

def deletefitembooking(request,fitemid):
    farmer=tbl_farmer_cart.objects.get(id=fitemid)
    itemquantity=farmer.fquantity
    itemqun=itemquantity*1000
    product=farmer.productid.id
    pdt=tbl_farmer_product.objects.get(id=product)
    stock=pdt.pdt_stock
    st=stock*1000
    total=itemqun+st
    tot=total/1000
    pdt.pdt_stock=tot
    pdt.save()
    farmer.fcart_status=1
    farmer.save()
    stup=1
    user=tbl_cus_reg.objects.get(id=request.session["customer_id"])
    email=user.cus_email
    send_mail(
                'Respected Sir/Madam ',#subject
                "\rOne item order is cancelled." ,#body
                settings.EMAIL_HOST_USER,
                [email],
            )
    return render(request,"Customer/Home.html",{'st':stup})

def complaint(request):
    if 'customer_id' in request.session:
        comtype=tbl_complainttype.objects.all()
        cudata=tbl_cus_reg.objects.get(id=request.session["customer_id"])
        if request.method=="POST":
            comtype=tbl_complainttype.objects.get(id=request.POST.get("txtcomtype"))
            tbl_complaint.objects.create(complaint_con=request.POST.get("txtcomcon"),customer=cudata,com_type=comtype)
            ins=1
            return render(request,"Customer/Complaint.html",{'ins':ins})
        else:
            return render(request,"Customer/Complaint.html",{'type':comtype})
    else:
        return redirect("webguest:login")

def feedback(request):
    if 'customer_id' in request.session:
        cudata=tbl_cus_reg.objects.get(id=request.session["customer_id"])
        if request.method=="POST":
            tbl_feedback.objects.create(feedback_con=request.POST.get("txtfeedback"),customer=cudata)
            ins1=1
            return render(request,"Customer/Feedback.html",{'ins1':ins1})
        else:
            return render(request,"Customer/Feedback.html")
    else:
        return redirect("webguest:login")

def reply(request):
    if 'customer_id' in request.session:
        reply=tbl_complaint.objects.filter(customer=request.session["customer_id"])
        return render(request,"Customer/View_reply.html",{'customer':reply})
    else:
        return redirect("webguest:login")

def marketbills(request,bkid):
    if 'customer_id' in request.session:
        total=0.0
        # dates=date.today()
        rand=random.randint(111111,999999)
        cusdata=tbl_cus_reg.objects.get(id=request.session["customer_id"])
        bk=tbl_market_booking.objects.get(id=bkid,user=cusdata)
        bkcount=tbl_market_booking.objects.filter(id=bkid,user=cusdata).count()
        if bkcount>0:
            bill=tbl_market_cart.objects.filter(bookingid__user=cusdata,bookingid=bkid,mcart_status=0)
            status=bill[0].bookingid.booking_status
            for i in bill:
                total=total+(float(i.mquantity)*float(i.productid.pdt_rate))
            marketid=bill[0].productid.market.id
            marketdata=tbl_market_reg.objects.get(id=marketid)
            return render(request,"Customer/Market_bills.html",{'bill':bill,'market':marketdata,'customer':cusdata,'status':status,'tot':total,'day':bk,'ran':rand})
        else:
            return render(request,"Customer/Market_bills.html")
    else:
        return redirect("webguest:login")

def marketdeliveredbills(request,mdelid):
    if 'customer_id' in request.session:
        total=0.0
        # dates=date.today()
        rand=random.randint(111111,999999)
        cusdata=tbl_cus_reg.objects.get(id=request.session["customer_id"])
        bk=tbl_market_booking.objects.get(id=mdelid,user=cusdata)
        bkcount=tbl_market_booking.objects.filter(id=mdelid,user=cusdata).count()
        if bkcount>0:
            bill=tbl_market_cart.objects.filter(bookingid__user=cusdata,bookingid=mdelid,mcart_status=2)
            status=bill[0].bookingid.booking_status
            for i in bill:
                total=total+(float(i.mquantity)*float(i.productid.pdt_rate))
            marketid=bill[0].productid.market.id
            marketdata=tbl_market_reg.objects.get(id=marketid)
            return render(request,"Customer/Market_bills.html",{'bill':bill,'market':marketdata,'customer':cusdata,'status':status,'tot':total,'day':bk,'ran':rand})
        else:
            return render(request,"Customer/Market_bills.html")
    else:
        return redirect("webguest:login")

def farmerbills(request,fbkid):
    if 'customer_id' in request.session:
        total=0.0
        dates=date.today()
        rand=random.randint(111111,999999)
        cusdata=tbl_cus_reg.objects.get(id=request.session["customer_id"])
        fbkcount=tbl_farmer_booking.objects.filter(user=cusdata,id=fbkid).count()
        if fbkcount>0:
            bill=tbl_farmer_cart.objects.filter(bookingid__user=cusdata,bookingid=fbkid,fcart_status=0)
            status=bill[0].bookingid.booking_status
            for i in bill:
                total=total+(float(i.fquantity)*float(i.productid.pdt_rate))
            farmerid=bill[0].productid.farmer.id
            farmerdata=tbl_farmer_reg.objects.get(id=farmerid)
            return render(request,"Customer/farmer_bills.html",{'bill':bill,'farmer':farmerdata,'customer':cusdata,'status':status,'tot':total,'day':dates,'ran':rand})
        else:
            return render(request,"Customer/Farmer_bills.html")
    else:
        return redirect("webguest:login")

def farmerdeliveredbills(request,fdelid):
    if 'customer_id' in request.session:
        total=0.0
        dates=date.today()
        rand=random.randint(111111,999999)
        cusdata=tbl_cus_reg.objects.get(id=request.session["customer_id"])
        fbkcount=tbl_farmer_booking.objects.filter(user=cusdata,id=fdelid).count()
        if fbkcount>0:
            bill=tbl_farmer_cart.objects.filter(bookingid__user=cusdata,bookingid=fdelid,fcart_status=2)
            status=bill[0].bookingid.booking_status
            for i in bill:
                total=total+(float(i.fquantity)*float(i.productid.pdt_rate))
            farmerid=bill[0].productid.farmer.id
            farmerdata=tbl_farmer_reg.objects.get(id=farmerid)
            return render(request,"Customer/farmer_bills.html",{'bill':bill,'farmer':farmerdata,'customer':cusdata,'status':status,'tot':total,'day':dates,'ran':rand})
        else:
            return render(request,"Customer/Farmer_bills.html")
    else:
        return redirect("webguest:login")

def viewevents(request,eventid):
    if 'customer_id' in request.session:
        event=tbl_events.objects.get(id=eventid)
        return render(request,"Customer/View_events.html",{'edata':event})
    else:
        return redirect("webguest:login")

def applysevent(request,eventid):
    request.session["ev"]=eventid
    event=tbl_events.objects.get(id=eventid)
    return render(request,"Customer/View_events.html",{'edata':event,'mes':1})

def applied(request):
    events=tbl_events.objects.get(id=request.session["ev"])
    customerdata=tbl_cus_reg.objects.get(id=request.session["customer_id"])
    applyevent.objects.create(customer=customerdata,event=events)
    return redirect("webcustomer:home")

def viewapplicationrequest(request):
    if 'customer_id' in request.session:
        cus=tbl_cus_reg.objects.get(id=request.session["customer_id"])
        eventdata=applyevent.objects.filter(customer=cus)
        return render(request,"Customer/View_application_request.html",{'datas':eventdata})
    else:
        return redirect("webguest:login")

def history(request):
    if 'customer_id' in request.session:
        customer=tbl_cus_reg.objects.get(id=request.session["customer_id"])
        ###################################################################################################
        counts=tbl_market_cart.objects.filter(bookingid__user=request.session["customer_id"],mcart_status=2).count()
        parray=[0 for i in range(1,counts+1)]
        j=0 
        mpdtdata=tbl_market_cart.objects.filter(bookingid__user=request.session["customer_id"],mcart_status=2)
        for i in mpdtdata:
            parray[j]=i.bookingid.id
            j=j+1

        ###################################################################################################
        ###################################################################################################
        marbookdata=tbl_market_booking.objects.filter(user=customer,booking_status__gte=3,id__in=parray)
        mcartda=tbl_market_cart.objects.filter(bookingid__in=parray)
        mtotals=[]
        m2=1
        for m1 in marbookdata:
            marcartdata=tbl_market_cart.objects.filter(bookingid=m1.id,mcart_status=2)
            mtotal=0
            for m2 in marcartdata:
                mtotal=mtotal+(float(m2.mquantity)*float(m2.productid.pdt_rate))
            mtotals.append(mtotal)
        ###################################################################################################
        ###################################################################################################
        farcounts=tbl_farmer_cart.objects.filter(bookingid__user=request.session["customer_id"],fcart_status=2).count()
        fparray=[0 for i in range(1,farcounts+1)]
        p=0 
        fpdtdata=tbl_farmer_cart.objects.filter(bookingid__user=request.session["customer_id"],fcart_status=2)
        for i in fpdtdata:
            fparray[p]=i.bookingid.id
            p=p+1

        ###################################################################################################
        ###################################################################################################
        farbookdata=tbl_farmer_booking.objects.filter(user=customer,booking_status__gte=3,id__in=fparray)
        fcartda=tbl_farmer_cart.objects.filter(bookingid__in=fparray)
        ftotals=[]
        f2=0
        for f1 in farbookdata:
            farcartdata=tbl_farmer_cart.objects.filter(bookingid=f1.id,fcart_status=2)
            ftotal=0
            for f2 in farcartdata:
                ftotal=ftotal+(float(f2.fquantity)*float(f2.productid.pdt_rate))
            ftotals.append(ftotal)
        ###################################################################################################
        mbookdatacount=tbl_market_booking.objects.filter(user=customer,booking_status__gte=3,id__in=parray).count()
        fbookdatacount=tbl_farmer_booking.objects.filter(user=customer,booking_status__gte=3,id__in=fparray).count()
        if mbookdatacount > 0 and fbookdatacount>0 :
            mbookdata=tbl_market_booking.objects.filter(user=customer,booking_status__gte=3,id__in=parray)
            mbookdatas=zip(mbookdata,mtotals,mcartda)
            mbookid=mbookdata[0]
            mcartdata=tbl_market_cart.objects.filter(bookingid=mbookid,mcart_status=2)

            fbookdata=tbl_farmer_booking.objects.filter(user=customer,booking_status__gte=3,id__in=fparray)
            fbookdatas=zip(fbookdata,ftotals,fcartda)
            fbookid=fbookdata[0]
            fcartdata=tbl_farmer_cart.objects.filter(bookingid=fbookid,fcart_status=2)

            return render(request,"Customer/History.html",{'mardata':mbookdatas,'fardata':fbookdatas})
        elif mbookdatacount > 0:
            mbookdata=tbl_market_booking.objects.filter(user=customer,booking_status__gte=3,id__in=parray)
            mbookdatas=zip(mbookdata,mtotals,mcartda)
            mbookid=mbookdata[0]
            mcartdata=tbl_market_cart.objects.filter(bookingid=mbookid,mcart_status=2)
            return render(request,"Customer/History.html",{'mardata':mbookdatas})
        
        elif fbookdatacount>0 :
            fbookdata=tbl_farmer_booking.objects.filter(user=customer,booking_status__gte=3,id__in=fparray)
            fbookdatas=zip(fbookdata,ftotals,fcartda)
            fbookid=fbookdata[0]
            fcartdata=tbl_farmer_cart.objects.filter(bookingid=fbookid,fcart_status=2)
            return render(request,"Customer/History.html",{'fardata':fbookdatas})
        else:
            return render(request,"Customer/History.html",{'mess':1})
    else:
        return redirect("webguest:login")

def report(request):
    if 'customer_id' in request.session:
        customer=tbl_cus_reg.objects.get(id=request.session["customer_id"])
        ###################################################################################################
        counts=tbl_market_cart.objects.filter(bookingid__user=request.session["customer_id"],mcart_status=2).count()
        parray=[0 for i in range(1,counts+1)]
        j=0 
        mpdtdata=tbl_market_cart.objects.filter(bookingid__user=request.session["customer_id"],mcart_status=2)
        for i in mpdtdata:
            parray[j]=i.bookingid.id
            j=j+1

        ###################################################################################################
        ###################################################################################################
        marbookdata=tbl_market_booking.objects.filter(user=customer,booking_status__gte=3,id__in=parray)
        mcartda=tbl_market_cart.objects.filter(bookingid__in=parray)
        mtotals=[]
        m2=1
        for m1 in marbookdata:
            marcartdata=tbl_market_cart.objects.filter(bookingid=m1.id,mcart_status=2)
            mtotal=0
            for m2 in marcartdata:
                mtotal=mtotal+(float(m2.mquantity)*float(m2.productid.pdt_rate))
            mtotals.append(mtotal)
        ###################################################################################################
        ###################################################################################################
        farcounts=tbl_farmer_cart.objects.filter(bookingid__user=request.session["customer_id"],fcart_status=2).count()
        fparray=[0 for i in range(1,farcounts+1)]
        p=0 
        fpdtdata=tbl_farmer_cart.objects.filter(bookingid__user=request.session["customer_id"],fcart_status=2)
        for i in fpdtdata:
            fparray[p]=i.bookingid.id
            p=p+1

        ###################################################################################################
        ###################################################################################################
        farbookdata=tbl_farmer_booking.objects.filter(user=customer,booking_status__gte=3,id__in=fparray)
        fcartda=tbl_farmer_cart.objects.filter(bookingid__in=fparray)
        ftotals=[]
        f2=0
        for f1 in farbookdata:
            farcartdata=tbl_farmer_cart.objects.filter(bookingid=f1.id,fcart_status=2)
            ftotal=0
            for f2 in farcartdata:
                ftotal=ftotal+(float(f2.fquantity)*float(f2.productid.pdt_rate))
            ftotals.append(ftotal)
        ###################################################################################################
        mbookdatacount=tbl_market_booking.objects.filter(user=customer,booking_status__gte=3,id__in=parray).count()
        fbookdatacount=tbl_farmer_booking.objects.filter(user=customer,booking_status__gte=3,id__in=fparray).count()
        if mbookdatacount > 0 and fbookdatacount>0 :
            mbookdata=tbl_market_booking.objects.filter(user=customer,booking_status__gte=3,id__in=parray)
            mbookdatas=zip(mbookdata,mtotals,mcartda)
            mbookid=mbookdata[0]
            mcartdata=tbl_market_cart.objects.filter(bookingid=mbookid,mcart_status=2)

            fbookdata=tbl_farmer_booking.objects.filter(user=customer,booking_status__gte=3,id__in=fparray)
            fbookdatas=zip(fbookdata,ftotals,fcartda)
            fbookid=fbookdata[0]
            fcartdata=tbl_farmer_cart.objects.filter(bookingid=fbookid,fcart_status=2)

            return render(request,"Customer/Report.html",{'mardata':mbookdatas,'fardata':fbookdatas})
        elif mbookdatacount > 0:
            mbookdata=tbl_market_booking.objects.filter(user=customer,booking_status__gte=3,id__in=parray)
            mbookdatas=zip(mbookdata,mtotals,mcartda)
            mbookid=mbookdata[0]
            mcartdata=tbl_market_cart.objects.filter(bookingid=mbookid,mcart_status=2)
            return render(request,"Customer/Report.html",{'mardata':mbookdatas})
        
        elif fbookdatacount>0 :
            fbookdata=tbl_farmer_booking.objects.filter(user=customer,booking_status__gte=3,id__in=fparray)
            fbookdatas=zip(fbookdata,ftotals,fcartda)
            fbookid=fbookdata[0]
            fcartdata=tbl_farmer_cart.objects.filter(bookingid=fbookid,fcart_status=2)
            return render(request,"Customer/Report.html",{'fardata':fbookdatas})
        else:
            return render(request,"Customer/Report.html",{'mess':1})
    else:
        return redirect("webguest:login")

def ajaxreport(request):
    customer=tbl_cus_reg.objects.get(id=request.session["customer_id"])
    if request.GET.get('fdate')!="" and request.GET.get('edate')!="":
        
    ###################################################################################################
        counts=tbl_market_cart.objects.filter(bookingid__user=request.session["customer_id"],mcart_status=2).count()
        parray=[0 for i in range(1,counts+1)]
        j=0 
        mpdtdata=tbl_market_cart.objects.filter(bookingid__user=request.session["customer_id"],mcart_status=2)
        for i in mpdtdata:
            parray[j]=i.bookingid.id
            j=j+1

    ###################################################################################################
    ###################################################################################################
        marbookdata=tbl_market_booking.objects.filter(user=customer,booking_status__gte=3,id__in=parray,booking_date__gte=request.GET.get('fdate'),booking_date__lte=request.GET.get('edate'))
        mcartda=tbl_market_cart.objects.filter(bookingid__in=parray)
        mtotals=[]
        m2=1
        for m1 in marbookdata:
            marcartdata=tbl_market_cart.objects.filter(bookingid=m1.id,mcart_status=2)
            mtotal=0
            for m2 in marcartdata:
                mtotal=mtotal+(float(m2.mquantity)*float(m2.productid.pdt_rate))
            mtotals.append(mtotal)
    ###################################################################################################
    ###################################################################################################
        farcounts=tbl_farmer_cart.objects.filter(bookingid__user=request.session["customer_id"],fcart_status=2).count()
        fparray=[0 for i in range(1,farcounts+1)]
        p=0 
        fpdtdata=tbl_farmer_cart.objects.filter(bookingid__user=request.session["customer_id"],fcart_status=2)
        for i in fpdtdata:
            fparray[p]=i.bookingid.id
            p=p+1

    ###################################################################################################
    ###################################################################################################
        farbookdata=tbl_farmer_booking.objects.filter(user=customer,booking_status__gte=3,id__in=fparray,booking_date__gte=request.GET.get('fdate'),booking_date__lte=request.GET.get('edate'))
        fcartda=tbl_farmer_cart.objects.filter(bookingid__in=fparray)
        ftotals=[]
        f2=0
        for f1 in farbookdata:
            farcartdata=tbl_farmer_cart.objects.filter(bookingid=f1.id,fcart_status=2)
            ftotal=0
            for f2 in farcartdata:
                ftotal=ftotal+(float(f2.fquantity)*float(f2.productid.pdt_rate))
            ftotals.append(ftotal)
    ###################################################################################################
        mbookdatacount=tbl_market_booking.objects.filter(user=customer,booking_status__gte=3,id__in=parray,booking_date__gte=request.GET.get('fdate'),booking_date__lte=request.GET.get('edate')).count()
        fbookdatacount=tbl_farmer_booking.objects.filter(user=customer,booking_status__gte=3,id__in=fparray,booking_date__gte=request.GET.get('fdate'),booking_date__lte=request.GET.get('edate')).count()
        if mbookdatacount > 0 and fbookdatacount>0 :
            mbookdata=tbl_market_booking.objects.filter(user=customer,booking_status__gte=3,id__in=parray,booking_date__gte=request.GET.get('fdate'),booking_date__lte=request.GET.get('edate'))
            mbookdatas=zip(mbookdata,mtotals,mcartda)
            mbookid=mbookdata[0]
            mcartdata=tbl_market_cart.objects.filter(bookingid=mbookid,mcart_status=2)

            fbookdata=tbl_farmer_booking.objects.filter(user=customer,booking_status__gte=3,id__in=fparray,booking_date__gte=request.GET.get('fdate'),booking_date__lte=request.GET.get('edate'))
            fbookdatas=zip(fbookdata,ftotals,fcartda)
            fbookid=fbookdata[0]
            fcartdata=tbl_farmer_cart.objects.filter(bookingid=fbookid,fcart_status=2)

            return render(request,"Customer/AjaxReport.html",{'mardata':mbookdatas,'fardata':fbookdatas})
        elif mbookdatacount > 0:
            mbookdata=tbl_market_booking.objects.filter(user=customer,booking_status__gte=3,id__in=parray,booking_date__gte=request.GET.get('fdate'),booking_date__lte=request.GET.get('edate'))
            mbookdatas=zip(mbookdata,mtotals,mcartda)
            mbookid=mbookdata[0]
            mcartdata=tbl_market_cart.objects.filter(bookingid=mbookid,mcart_status=2)
            return render(request,"Customer/AjaxReport.html",{'mardata':mbookdatas})
    
        elif fbookdatacount>0 :
            fbookdata=tbl_farmer_booking.objects.filter(user=customer,booking_status__gte=3,id__in=fparray,booking_date__gte=request.GET.get('fdate'),booking_date__lte=request.GET.get('edate'))
            fbookdatas=zip(fbookdata,ftotals,fcartda)
            fbookid=fbookdata[0]
            fcartdata=tbl_farmer_cart.objects.filter(bookingid=fbookid,fcart_status=2)
            return render(request,"Customer/AjaxReport.html",{'fardata':fbookdatas})
        else:
            return render(request,"Customer/AjaxReport.html",{'mess':1})
    elif request.GET.get('fdate')!="":
        ###################################################################################################
        counts=tbl_market_cart.objects.filter(bookingid__user=request.session["customer_id"],mcart_status=2).count()
        parray=[0 for i in range(1,counts+1)]
        j=0 
        mpdtdata=tbl_market_cart.objects.filter(bookingid__user=request.session["customer_id"],mcart_status=2)
        for i in mpdtdata:
            parray[j]=i.bookingid.id
            j=j+1

    ###################################################################################################
    ###################################################################################################
        marbookdata=tbl_market_booking.objects.filter(user=customer,booking_status__gte=3,id__in=parray,booking_date__gte=request.GET.get('fdate'))
        mcartda=tbl_market_cart.objects.filter(bookingid__in=parray)
        mtotals=[]
        m2=1
        for m1 in marbookdata:
            marcartdata=tbl_market_cart.objects.filter(bookingid=m1.id,mcart_status=2)
            mtotal=0
            for m2 in marcartdata:
                mtotal=mtotal+(float(m2.mquantity)*float(m2.productid.pdt_rate))
            mtotals.append(mtotal)
    ###################################################################################################
    ###################################################################################################
        farcounts=tbl_farmer_cart.objects.filter(bookingid__user=request.session["customer_id"],fcart_status=2).count()
        fparray=[0 for i in range(1,farcounts+1)]
        p=0 
        fpdtdata=tbl_farmer_cart.objects.filter(bookingid__user=request.session["customer_id"],fcart_status=2)
        for i in fpdtdata:
            fparray[p]=i.bookingid.id
            p=p+1

    ###################################################################################################
    ###################################################################################################
        farbookdata=tbl_farmer_booking.objects.filter(user=customer,booking_status__gte=3,id__in=fparray,booking_date__gte=request.GET.get('fdate'))
        fcartda=tbl_farmer_cart.objects.filter(bookingid__in=fparray)
        ftotals=[]
        f2=0
        for f1 in farbookdata:
            farcartdata=tbl_farmer_cart.objects.filter(bookingid=f1.id,fcart_status=2)
            ftotal=0
            for f2 in farcartdata:
                ftotal=ftotal+(float(f2.fquantity)*float(f2.productid.pdt_rate))
            ftotals.append(ftotal)
    ###################################################################################################
        mbookdatacount=tbl_market_booking.objects.filter(user=customer,booking_status__gte=3,id__in=parray,booking_date__gte=request.GET.get('fdate')).count()
        fbookdatacount=tbl_farmer_booking.objects.filter(user=customer,booking_status__gte=3,id__in=fparray,booking_date__gte=request.GET.get('fdate')).count()
        if mbookdatacount > 0 and fbookdatacount>0 :
            mbookdata=tbl_market_booking.objects.filter(user=customer,booking_status__gte=3,id__in=parray,booking_date__gte=request.GET.get('fdate'))
            mbookdatas=zip(mbookdata,mtotals,mcartda)
            mbookid=mbookdata[0]
            mcartdata=tbl_market_cart.objects.filter(bookingid=mbookid,mcart_status=2)

            fbookdata=tbl_farmer_booking.objects.filter(user=customer,booking_status__gte=3,id__in=fparray,booking_date__gte=request.GET.get('fdate'))
            fbookdatas=zip(fbookdata,ftotals,fcartda)
            fbookid=fbookdata[0]
            fcartdata=tbl_farmer_cart.objects.filter(bookingid=fbookid,fcart_status=2)

            return render(request,"Customer/AjaxReport.html",{'mardata':mbookdatas,'fardata':fbookdatas})
        elif mbookdatacount > 0:
            mbookdata=tbl_market_booking.objects.filter(user=customer,booking_status__gte=3,id__in=parray,booking_date__gte=request.GET.get('fdate'))
            mbookdatas=zip(mbookdata,mtotals,mcartda)
            mbookid=mbookdata[0]
            mcartdata=tbl_market_cart.objects.filter(bookingid=mbookid,mcart_status=2)
            return render(request,"Customer/AjaxReport.html",{'mardata':mbookdatas})
    
        elif fbookdatacount>0 :
            fbookdata=tbl_farmer_booking.objects.filter(user=customer,booking_status__gte=3,id__in=fparray,booking_date__gte=request.GET.get('fdate'))
            fbookdatas=zip(fbookdata,ftotals,fcartda)
            fbookid=fbookdata[0]
            fcartdata=tbl_farmer_cart.objects.filter(bookingid=fbookid,fcart_status=2)
            return render(request,"Customer/AjaxReport.html",{'fardata':fbookdatas})
        else:
            return render(request,"Customer/AjaxReport.html",{'mess':1})
    elif request.GET.get('edate')!="":
        ###################################################################################################
        counts=tbl_market_cart.objects.filter(bookingid__user=request.session["customer_id"],mcart_status=2).count()
        parray=[0 for i in range(1,counts+1)]
        j=0 
        mpdtdata=tbl_market_cart.objects.filter(bookingid__user=request.session["customer_id"],mcart_status=2)
        for i in mpdtdata:
            parray[j]=i.bookingid.id
            j=j+1

    ###################################################################################################
    ###################################################################################################
        marbookdata=tbl_market_booking.objects.filter(user=customer,booking_status__gte=3,id__in=parray,booking_date__lte=request.GET.get('edate'))
        mcartda=tbl_market_cart.objects.filter(bookingid__in=parray)
        mtotals=[]
        m2=1
        for m1 in marbookdata:
            marcartdata=tbl_market_cart.objects.filter(bookingid=m1.id,mcart_status=2)
            mtotal=0
            for m2 in marcartdata:
                mtotal=mtotal+(float(m2.mquantity)*float(m2.productid.pdt_rate))
            mtotals.append(mtotal)
    ###################################################################################################
    ###################################################################################################
        farcounts=tbl_farmer_cart.objects.filter(bookingid__user=request.session["customer_id"],fcart_status=2).count()
        fparray=[0 for i in range(1,farcounts+1)]
        p=0 
        fpdtdata=tbl_farmer_cart.objects.filter(bookingid__user=request.session["customer_id"],fcart_status=2)
        for i in fpdtdata:
            fparray[p]=i.bookingid.id
            p=p+1

    ###################################################################################################
    ###################################################################################################
        farbookdata=tbl_farmer_booking.objects.filter(user=customer,booking_status__gte=3,id__in=fparray,booking_date__lte=request.GET.get('edate'))
        fcartda=tbl_farmer_cart.objects.filter(bookingid__in=fparray)
        ftotals=[]
        f2=0
        for f1 in farbookdata:
            farcartdata=tbl_farmer_cart.objects.filter(bookingid=f1.id,fcart_status=2)
            ftotal=0
            for f2 in farcartdata:
                ftotal=ftotal+(float(f2.fquantity)*float(f2.productid.pdt_rate))
            ftotals.append(ftotal)
    ###################################################################################################
        mbookdatacount=tbl_market_booking.objects.filter(user=customer,booking_status__gte=3,id__in=parray,booking_date__lte=request.GET.get('edate')).count()
        fbookdatacount=tbl_farmer_booking.objects.filter(user=customer,booking_status__gte=3,id__in=fparray,booking_date__lte=request.GET.get('edate')).count()
        if mbookdatacount > 0 and fbookdatacount>0 :
            mbookdata=tbl_market_booking.objects.filter(user=customer,booking_status__gte=3,id__in=parray,booking_date__lte=request.GET.get('edate'))
            mbookdatas=zip(mbookdata,mtotals,mcartda)
            mbookid=mbookdata[0]
            mcartdata=tbl_market_cart.objects.filter(bookingid=mbookid,mcart_status=2)

            fbookdata=tbl_farmer_booking.objects.filter(user=customer,booking_status__gte=3,id__in=fparray,booking_date__lte=request.GET.get('edate'))
            fbookdatas=zip(fbookdata,ftotals,fcartda)
            fbookid=fbookdata[0]
            fcartdata=tbl_farmer_cart.objects.filter(bookingid=fbookid,fcart_status=2)

            return render(request,"Customer/AjaxReport.html",{'mardata':mbookdatas,'fardata':fbookdatas})
        elif mbookdatacount > 0:
            mbookdata=tbl_market_booking.objects.filter(user=customer,booking_status__gte=3,id__in=parray,booking_date__lte=request.GET.get('edate'))
            mbookdatas=zip(mbookdata,mtotals,mcartda)
            mbookid=mbookdata[0]
            mcartdata=tbl_market_cart.objects.filter(bookingid=mbookid,mcart_status=2)
            return render(request,"Customer/AjaxReport.html",{'mardata':mbookdatas})
    
        elif fbookdatacount>0 :
            fbookdata=tbl_farmer_booking.objects.filter(user=customer,booking_status__gte=3,id__in=fparray,booking_date__lte=request.GET.get('edate'))
            fbookdatas=zip(fbookdata,ftotals,fcartda)
            fbookid=fbookdata[0]
            fcartdata=tbl_farmer_cart.objects.filter(bookingid=fbookid,fcart_status=2)
            return render(request,"Customer/AjaxReport.html",{'fardata':fbookdatas})
        else:
            return render(request,"Customer/AjaxReport.html",{'mess':1})
    else:
        return render(request,"Customer/AjaxReport.html",{'mess':1})

def trialpage(request):
    userdata=tbl_cus_reg.objects.get(id=request.session['customer_id'])
    market=tbl_market_reg.objects.filter(mar_status=1)
    return render(request,"Customer/trial_page.html",{'user':userdata,'mar':market})