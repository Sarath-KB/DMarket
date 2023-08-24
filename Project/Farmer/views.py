from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *
from Farmer.models import *
from Customer.models import *
import random
from django.utils import timezone
from datetime import date
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.
def home(request): 
    if 'farmer_id' in request.session:
        current_datetime = timezone.now()
        bookd=[]
        cartsdata=tbl_m_cart.objects.filter(cart_status=2)
        for k in cartsdata:
            if k.bookingid.id in bookd:
                continue
            else:
                bookd.append(k.bookingid.id)
        mbook=tbl_m_booking.objects.filter(booking_status__lt=3,booking_status__gt=0).exclude(id__in=bookd)

        
        for i in mbook:
            start_time=i.date_time
            email=i.farmer.far_email
            time_difference = current_datetime - start_time
            hours_difference = time_difference.total_seconds() //3600
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
                mcartdata=tbl_m_cart.objects.filter(bookingid=i.id)
                for j in mcartdata:
                    mpdt=j.productid.id
                    mpdtdata=tbl_market_product.objects.get(id=mpdt)
                    stock=mpdtdata.pdt_stock
                    s=stock*1000
                    qun=i.mquantity
                    q=qun*1000
                    t=s+q
                    total=t/1000
                    mpdtdata.pdt_stock=total
                    mpdtdata.save()
                tbl_m_booking.objects.get(id=i.id).delete()
        cdate=date.today()
        farmer=tbl_farmer_reg.objects.get(id=request.session["farmer_id"])
        place=tbl_place.objects.get(id=request.session["farmer_place"])
        eventdata=tbl_events.objects.filter(market__place=place,event_tdate__gte=cdate)
        return render(request,"Farmer/Home.html",{'eve':eventdata,'far':farmer})
    else:
        return redirect("webguest:login")

def my_pro(request): 
    if 'farmer_id' in request.session:
        data=tbl_farmer_reg.objects.get(id=request.session["farmer_id"])
        return render(request,"Farmer/My_profile.html",{'data':data})
    else:
        return redirect("webguest:login") 

def editprofile(request):
    if 'farmer_id' in request.session:
        prodata=tbl_farmer_reg.objects.get(id=request.session["farmer_id"])
        if request.method=="POST":
            prodata.far_name=request.POST.get('txtname')
            prodata.far_contact=request.POST.get('txtcon')
            prodata.far_email=request.POST.get('txtemail')
            prodata.far_address=request.POST.get("txtaddress")
            prodata.save()
            ed=1
            return render(request,"Farmer/Edit_profile.html",{'ed':ed})
        else:
            return render(request,"Farmer/Edit_profile.html",{'prodata':prodata})
    else:
        return redirect("webguest:login")

def editpropic(request):
    if 'farmer_id' in request.session:
        fa=tbl_farmer_reg.objects.get(id=request.session['farmer_id'])
        if request.method=="POST":
            fa.far_photo=request.FILES.get('txtphoto')
            fa.save()
            pic=1
            return render(request,"Farmer/Home.html",{'pic':pic})
        else:
            return render(request,"Farmer/Edit_pro_pic.html",{'farmer':fa})
    else:
        return redirect("webguest:login")

def logout(request):
    del request.session["farmer_id"]
    return redirect("webguest:login")

def changepass(request):
    if 'farmer_id' in request.session:
        if request.method=="POST":
            ccount=tbl_farmer_reg.objects.filter(id=request.session["farmer_id"],far_pass=request.POST.get('txtcurpass')).count()
            if ccount>0:
                if request.POST.get('txtnewpass')==request.POST.get('txtconpass'):
                    farmerdata=tbl_farmer_reg.objects.get(id=request.session["farmer_id"],far_pass=request.POST.get('txtcurpass'))
                    farmerdata.far_pass=request.POST.get('txtnewpass')
                    farmerdata.save()
                    er3=3
                    return render(request,"Farmer/Change_password.html",{'er':er3})
                else:
                    er1=1
                    return render(request,"Farmer/Change_password.html",{'er':er1})
            else:
                er2=2
                return render(request,"Farmer/Change_password.html",{'er':er2})
        else:
            return render(request,"Farmer/Change_password.html")
    else:
        return redirect("webguest:login")

def mycart(request):
    if 'farmer_id' in request.session:
        mcartdata=tbl_m_cart.objects.filter(bookingid__booking_status=0,bookingid__farmer=request.session["farmer_id"])
        mcartcount=tbl_m_cart.objects.filter(bookingid__booking_status=0,bookingid__farmer=request.session["farmer_id"]).count()
        mtotal=0
        if mcartcount>0:
            for i in mcartdata:
                mtotal=mtotal + (float(i.mquantity) * float(i.productid.pdt_rate))
                mtotal=int(mtotal)
            cart=1
            return render(request,"Farmer/My_cart.html",{'mdata':mcartdata,'mtot':mtotal,'cart':cart})
        else:
            cart=2
            return render(request,"Farmer/My_cart.html",{'cart':cart})
    else:
        return redirect("webguest:login")

def ajaxmarketpdtamt(request):
    madata=tbl_m_cart.objects.get(id=request.GET.get("cartid"))
    qdata=request.GET.get("qid")
    madata.mquantity=qdata
    madata.save()
    return redirect("webfarmer:mycart")

def mdeletecartitem(request,mcartid):
    tbl_m_cart.objects.get(id=mcartid).delete()
    dele=1
    return render(request,"Farmer/My_cart.html",{'de':dele})

def mpaymentoffline(request,am):
    quantity=tbl_m_cart.objects.filter(bookingid__booking_status=0,bookingid__farmer=request.session["farmer_id"])
    for a in quantity:
        if a.mquantity<=0:
            tbl_m_cart.objects.get(id=a.id).delete()

    
    qun=tbl_m_cart.objects.filter(bookingid__booking_status=0,bookingid__farmer=request.session["farmer_id"])
    quncount=tbl_m_cart.objects.filter(bookingid__booking_status=0,bookingid__farmer=request.session["farmer_id"]).count()
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
            return render(request,"Farmer/My_cart.html",{'out':out})
        else:
            prdatas=tbl_market_product.objects.get(id=i.productid.id)
            prdatas.pdt_stock=tbal
            prdatas.save()
            bkid=i.bookingid.id
            bookdata=tbl_m_booking.objects.get(id=bkid)
            bookdata.date_time=timezone.now()
            bookdata.save()
            if tbal==0:
                far=tbl_farmer_reg.objects.get(id=request.session["farmer_id"])
                da=tbl_m_cart.objects.filter(bookingid__booking_status=0,productid=prdatas)
                for j in da:
                    if j.bookingid.farmer!=far:
                        j.mquantity=0
                        j.save()
                da1=tbl_market_cart.objects.filter(bookingid__booking_status=0,productid=prdatas)
                for p in da1:
                    p.mquantity=0
                    p.save()
                bid=qun[0].bookingid.id
                bdata=tbl_m_booking.objects.get(id=bid)
                bdata.booking_status=2
                # bdata.payment_date=date.today()
                bdata.save()
                bk=1
                # return render(request,"Farmer/My_cart.html",{'book':bk})
            else:
                bid=qun[0].bookingid.id
                bdata=tbl_m_booking.objects.get(id=bid)
                bdata.booking_status=2
                # bdata.payment_date=date.today()
                bdata.save()
                bk=1
                # return render(request,"Farmer/My_cart.html",{'book':bk})
    farmer=tbl_farmer_reg.objects.get(id=request.session["farmer_id"])
    email=farmer.far_email
    send_mail(
            'Respected Sir/Madam ',#subject
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
    return redirect("webfarmer:home")

def mpayment(request,mamt):
    quantity=tbl_m_cart.objects.filter(bookingid__booking_status=0,bookingid__farmer=request.session["farmer_id"])
    for a in quantity:
        if a.mquantity<=0:
            tbl_m_cart.objects.get(id=a.id).delete()
            
    if request.method=="POST":
        qun=tbl_m_cart.objects.filter(bookingid__booking_status=0,bookingid__farmer=request.session["farmer_id"])
        quncount=tbl_m_cart.objects.filter(bookingid__booking_status=0,bookingid__farmer=request.session["farmer_id"]).count()
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
                return render(request,"Farmer/Mpayment.html",{'out':out})
            else:
                datas=tbl_market_product.objects.get(id=i.productid.id)
                datas.pdt_stock=tbal
                datas.save()
                bkid=i.bookingid.id
                bookdata=tbl_m_booking.objects.get(id=bkid)
                bookdata.date_time=timezone.now()
                bookdata.save()
            #########################
            
                if tbal==0:
                    far=tbl_farmer_reg.objects.get(id=request.session["farmer_id"])
                    dms=tbl_m_cart.objects.filter(bookingid__booking_status=0,productid=datas)
                    for j in dms:
                        if j.bookingid.farmer!=far:
                            j.mquantity=0
                            j.save()
                    bid=qun[0].bookingid.id
                    bdata=tbl_m_booking.objects.get(id=bid)
                    bdata.booking_status=1
                    bdata.payment_date=date.today()
                    bdata.save()
                    # return redirect("webfarmer:loader")
                else:
                    bid=qun[0].bookingid.id
                    bdata=tbl_m_booking.objects.get(id=bid)
                    bdata.booking_status=1
                    bdata.payment_date=date.today()
                    bdata.save()
        farmer=tbl_farmer_reg.objects.get(id=request.session["farmer_id"])
        email=farmer.far_email
        send_mail(
                'Respected Sir/Madam ',#subject
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
        return redirect("webfarmer:loader")
    else:
        return render(request,"Farmer/Mpayment.html",{'total':mamt})

def mdeletecartitem(request,mcartid):
    tbl_m_cart.objects.get(id=mcartid).delete()
    dele=1
    return render(request,"Farmer/My_cart.html",{'de':dele})

def loader(request):
    return render(request,"Customer/Loader.html")

def paymentsuc(request):
    return render(request,"Customer/Payment_suc.html")

def search_mar(request):
    if 'farmer_id' in request.session:
        disdata=tbl_district.objects.all()
        mardata=tbl_market_reg.objects.filter(mar_status=1)
        return render(request,"Farmer/Search_market.html",{'dis':disdata,'mar':mardata})
    else:
        return redirect("webguest:login")

def marketprofile(request,mproid):
    if 'farmer_id' in request.session:
        marketdata=tbl_market_reg.objects.get(id=mproid)
        return render(request,"Farmer/Market_pro.html",{'mardata':marketdata})
    else:
        return redirect("webguest:login")

def ajaxmarket(request):
    if request.GET.get("pid")!="":
        placedata=tbl_place.objects.get(id=request.GET.get("pid"))
        mardata=tbl_market_reg.objects.filter(mar_status=1,place=placedata)
        return render(request,"Farmer/ajaxmarket.html",{'mar':mardata})
    else:
        districtdata=tbl_district.objects.get(id=request.GET.get('did'))
        mardata=tbl_market_reg.objects.filter(mar_status=1,place__district=districtdata)
        return render(request,"Farmer/ajaxmarket.html",{'mar':mardata})

def marketproduct(request,marid):
    if 'farmer_id' in request.session:
        cat=tbl_catageory.objects.filter(cat_status=1)
        request.session["mdid"]=marid
        marketdata=tbl_market_product.objects.filter(market=marid)
        return render(request,"Farmer/Market_pdt.html",{'mdata':marketdata,'cat':cat})
    else:
        return redirect("webguest:login")

def ajaxmarketproduct(request):
    if request.GET.get("sub")!="":
        subdata=tbl_subcat.objects.get(id=request.GET.get("sub"))
        marpdt=tbl_market_product.objects.filter(subcategory=subdata,market=request.session["mdid"])
        return render(request,"Farmer/ajaxmarketpdt.html",{'mdata':marpdt})
    else:
        cat=tbl_catageory.objects.get(id=request.GET.get("cat"))
        marpdt=tbl_market_product.objects.filter(subcategory__cat=cat,market=request.session["mdid"])
        return render(request,"Farmer/ajaxmarketpdt.html",{'mdata':marpdt})

def marketcart(request,marketpdtid):
    if 'farmer_id' in request.session:
        mpdtdetails=tbl_market_product.objects.get(id=marketpdtid)
        cusdata=tbl_farmer_reg.objects.get(id=request.session["farmer_id"])
        mbookcount=tbl_m_booking.objects.filter(farmer=cusdata,booking_status=0).count()
        if mbookcount>0:
            mbookdata=tbl_m_booking.objects.get(farmer=cusdata,booking_status=0)
            cartcount=tbl_m_cart.objects.filter(bookingid=mbookdata,productid=mpdtdetails).count()
            if cartcount>0:
                er=1
                return render(request,"Farmer/Market_pdt.html",{'error':er})
            else:
                tbl_m_cart.objects.create(bookingid=mbookdata,productid=mpdtdetails)
                ins=1
                return render(request,"Farmer/Market_pdt.html",{'ins':ins})
        else:
            tbl_m_booking.objects.create(farmer=cusdata)
            mbookcount=tbl_m_booking.objects.filter(farmer=cusdata,booking_status=0).count()
            if mbookcount>0:
                mbookdata=tbl_m_booking.objects.get(farmer=cusdata,booking_status=0)
                cartcount=tbl_m_cart.objects.filter(bookingid=mbookdata,productid=mpdtdetails).count()
                if cartcount>0:
                    er=1
                    return render(request,"Farmer/Market_pdt.html",{'error':er})
                else:
                    tbl_m_cart.objects.create(bookingid=mbookdata,productid=mpdtdetails)
                    ins=1
                    return render(request,"Farmer/Market_pdt.html",{'ins':ins})
            else:
                return render(request,"Farmer/Market_pdt.html")
    else:
        return redirect("webguest:login")

def product(request):
    if 'farmer_id' in request.session:
        farmerdata=tbl_farmer_reg.objects.get(id=request.session["farmer_id"])
        cata=tbl_catageory.objects.filter(cat_status=1)
        pdt=tbl_farmer_product.objects.filter(farmer=farmerdata)
        if request.method=="POST":
            subcatdata=tbl_subcat.objects.get(id=request.POST.get('selsubcat'))
            tbl_farmer_product.objects.create(pdt_name=request.POST.get('txtname'),pdt_rate=request.POST.get('txtrate'),pdt_dis=request.POST.get('txtdes'),pdt_stock=request.POST.get('txtstock'),pdt_image=request.FILES.get('txtimage'),subcategory=subcatdata,farmer=farmerdata)
            pro=1
            return render(request,"Farmer/Farmer_product.html",{'cat':cata,'pdt':pdt,'pro':pro})
        else:
            return render(request,"Farmer/Farmer_product.html",{'cat':cata,'pdt':pdt})
    else:
        return redirect("webguest:login")

def ajaxsubcat(request):
    categorydata=tbl_catageory.objects.get(id=request.GET.get('disd'))
    subcatdata=tbl_subcat.objects.filter(cat=categorydata)
    return render(request,"Farmer/Ajaxsubcat.html",{'data':subcatdata})

def stock(request,stid):
    if 'farmer_id' in request.session:
        stock=tbl_farmer_product.objects.get(id=stid)
        if request.method=="POST":
            if request.POST.get('txtrate')!="" and request.POST.get('txtstockno')!="":
                qun=stock.pdt_stock
                q=qun*1000
                te=float(request.POST.get('txtstockno'))
                s=q+(te*1000)
                newstock=s/1000
                stock.pdt_stock=newstock
                stock.pdt_rate=request.POST.get('txtrate')
                stock.save()
                st=1
                return render(request,"Farmer/Stock_update.html",{'st':st})
            elif request.POST.get('txtstockno')!="":
                qun=stock.pdt_stock
                q=qun*1000
                te=float(request.POST.get('txtstockno'))
                s=q+(te*1000)
                newstock=s/1000
                stock.pdt_stock=newstock
                stock.save()
                st=1
                return render(request,"Farmer/Stock_update.html",{'st':st})
            elif request.POST.get('txtrate')!="":
                stock.pdt_rate=request.POST.get('txtrate')
                stock.save()
                st=1
                return render(request,"Farmer/Stock_update.html",{'st':st})
            else:
                return render(request,"Farmer/Stock_update.html")
        else:
            return render(request,"Farmer/Stock_update.html",{'stock':stock})
    else:
        return redirect("webguest:login")

def deleteitem(request,delit):
    itemdata=tbl_farmer_product.objects.get(id=delit).delete()
    de=1
    return render(request,"Farmer/Farmer_product.html",{'de':de})

def complaint(request):
    if 'farmer_id' in request.session:
        comtype=tbl_complainttype.objects.all()
        fdata=tbl_farmer_reg.objects.get(id=request.session["farmer_id"])
        if request.method=="POST":
            comtype=tbl_complainttype.objects.get(id=request.POST.get("txtcomtype"))
            tbl_complaint.objects.create(complaint_con=request.POST.get("txtcomcon"),farmer=fdata,com_type=comtype)
            ins=1
            return render(request,"Farmer/Complaint.html",{'ins':ins})
        else:
            return render(request,"Farmer/Complaint.html",{'type':comtype})
    else:
        return redirect("webguest:login")

def feedback(request):
    if 'farmer_id' in request.session:
        fdata=tbl_farmer_reg.objects.get(id=request.session["farmer_id"])
        if request.method=="POST":
            tbl_feedback.objects.create(feedback_con=request.POST.get("txtfeedback"),farmer=fdata)
            ins1=1
            return render(request,"Farmer/Feedback.html",{'ins1':ins1})
        else:
            return render(request,"Farmer/Feedback.html")
    else:
        return redirect("webguest:login")

def reply(request):
    if 'farmer_id' in request.session:
        reply=tbl_complaint.objects.filter(farmer=request.session["farmer_id"])
        return render(request,"Farmer/View_reply.html",{'farmer':reply})
    else:
        return redirect("webguest:login")

def mybookings(request):
    if 'farmer_id' in request.session:
        farmer = tbl_farmer_reg.objects.get(id=request.session["farmer_id"])
        ##################################################################################
        counts=tbl_m_cart.objects.filter(bookingid__farmer=farmer,cart_status__lt=1).count()
        array=[0 for i in range(1,counts+1)]
        p=0
        mprodata=tbl_m_cart.objects.filter(bookingid__farmer=farmer,cart_status__lt=1)
        for i in mprodata:
            array[p]=i.bookingid.id
            p=p+1
        ##################################################################################
        
        bcuount=tbl_m_booking.objects.filter(farmer=farmer,booking_status__gt=0,id__in=array).count()
        if bcuount>0:
            bookdata=tbl_m_booking.objects.filter(farmer=farmer,booking_status__gt=0,id__in=array)
            cart=tbl_m_cart.objects.filter(bookingid__in=array)
            totals=[]
            j=1
            for i in bookdata:
                cartdata=tbl_m_cart.objects.filter(bookingid=i.id,cart_status=0)
                total=0
                for j in cartdata:
                    total=total+(float(j.mquantity)*float(j.productid.pdt_rate))
                totals.append(total)
            bookid=bookdata[0].id
            cartdata= tbl_m_cart.objects.filter(bookingid=bookid)
            datas=zip(bookdata,totals,cart)
            return render(request,"Farmer/My_booking.html",{'book':datas,'totals':totals,'t':1})
        else:
            return render(request,"Farmer/My_booking.html")
    else:
        return redirect("webguest:login")

def myproduct(request,bkid):
    if 'farmer_id' in request.session:
        bdata=tbl_m_cart.objects.filter(bookingid__booking_status__gt=0,bookingid__farmer=request.session["farmer_id"],bookingid=bkid,cart_status=0)
        return render(request,"Farmer/My_product.html",{'bkdata':bdata,'bookid':bkid})
    else:
        return redirect("webguest:login")

def mydeliveredproduct(request,productid):
    if 'farmer_id' in request.session:
        bdata=tbl_m_cart.objects.filter(bookingid__booking_status__gt=0,bookingid__farmer=request.session["farmer_id"],bookingid=productid,cart_status=2)
        return render(request,"Farmer/My_delivered_pdt.html",{'bkdata':bdata,'bookid':productid})
    else:
        return redirect("webguest:login")

def deleteitemcart(request,delid):
    item=tbl_m_cart.objects.get(id=delid)
    itemqun=item.mquantity
    itqu=itemqun*1000
    product=item.productid.id
    pdtst=tbl_market_product.objects.get(id=product)
    st=pdtst.pdt_stock
    st1=st*1000
    tot=st1+itqu
    stock=tot/1000
    pdtst.pdt_stock=stock
    pdtst.save()
    item.cart_status=1
    item.save()
    stup=1
    farmer=tbl_farmer_reg.objects.get(id=request.session["farmer_id"])
    email=farmer.far_email
    send_mail(
                'Respected Sir/Madam ',#subject
                "\rOne item order is cancelled." ,#body
                settings.EMAIL_HOST_USER,
                [email],
            )
    return render(request,"Farmer/Home.html",{'stock':stup})

def bills(request,bookid):
    if 'farmer_id' in request.session:
        total=0.0
        # dates=date.today()
        rand=random.randint(1111111,9999999)
        fdata=tbl_farmer_reg.objects.get(id=request.session["farmer_id"])
        bk=tbl_m_booking.objects.get(farmer=fdata,id=bookid)
        bkcount=tbl_m_booking.objects.filter(farmer=fdata,id=bookid).count()
        
        if bkcount>0:
            bill=tbl_m_cart.objects.filter(bookingid__farmer=fdata,bookingid=bookid,cart_status=0)
            status=bill[0].bookingid.booking_status
            for i in bill:
                total=total+(float(i.mquantity)*float(i.productid.pdt_rate))
            marketid=bill[0].productid.market.id
            marketdata=tbl_market_reg.objects.get(id=marketid)
            return render(request,"Farmer/Bill.html",{'bill':bill,'market':marketdata,'far':fdata,'sta':status,'tot':total,'day':bk,'ran':rand})
        else:
            return render(request,"Farmer/Bill.html")
    else:
        return redirect("webguest:login")

def deliveredbills(request,billid):
    if 'farmer_id' in request.session:
        total=0.0
        # dates=date.today()
        rand=random.randint(1111111,9999999)
        fdata=tbl_farmer_reg.objects.get(id=request.session["farmer_id"])
        bk=tbl_m_booking.objects.get(farmer=fdata,id=billid)
        bkcount=tbl_m_booking.objects.filter(farmer=fdata,id=billid).count()
        
        if bkcount>0:
            bill=tbl_m_cart.objects.filter(bookingid__farmer=fdata,bookingid=billid,cart_status=2)
            status=bill[0].bookingid.booking_status
            for i in bill:
                total=total+(float(i.mquantity)*float(i.productid.pdt_rate))
            marketid=bill[0].productid.market.id
            marketdata=tbl_market_reg.objects.get(id=marketid)
            return render(request,"Farmer/Bill.html",{'bill':bill,'market':marketdata,'far':fdata,'sta':status,'tot':total,'day':bk,'ran':rand})
        else:
            return render(request,"Farmer/Bill.html")
    else:
        return redirect("webguest:login")

def viewevents(request,eventid):
    if 'farmer_id' in request.session:
        event=tbl_events.objects.get(id=eventid)
        return render(request,"Farmer/View_event.html",{'event':event})
    else:
        return redirect("webguest:login")

def applyevents(request,apid):
    request.session["evid"]=apid
    event=tbl_events.objects.get(id=apid)
    return render(request,"Farmer/View_event.html",{'event':event,'mes':1})

def applied(request):
    events=tbl_events.objects.get(id=request.session["evid"])
    farmerdata=tbl_farmer_reg.objects.get(id=request.session["farmer_id"])
    applyevn=applyevent.objects.filter(farmer=farmerdata,event=events).count()
    if applyevn > 0:
        msg=1
        return render(request,"Farmer/Home.html",{'msg':msg})
    else:
        applyevent.objects.create(farmer=farmerdata,event=events)
        return redirect("webfarmer:home")

def viewapplicationrequuest(request):
    if 'farmer_id' in request.session:
        far=tbl_farmer_reg.objects.get(id=request.session["farmer_id"])
        event=applyevent.objects.filter(farmer=far)
        return render(request,"Farmer/View_application_request.html",{'datas':event})
    else:
        return redirect("webguest:login")

def deleteeventapply(request,delev):
    applyevent.objects.get(id=delev).delete()
    delete=1
    return render(request,"Farmer/View_application_request.html",{'de':delete})

def buyers(request):
    if 'farmer_id' in request.session:
        farmer=tbl_farmer_reg.objects.get(id=request.session["farmer_id"])
        cdata=tbl_farmer_cart.objects.filter(productid__farmer=farmer,fcart_status=0)
        farbkid = []
        for i in cdata:
            farid=i.bookingid.id
            farbkid.append(farid)
        farbookcount=tbl_farmer_booking.objects.filter(id__in=farbkid,booking_status__gt=0,booking_status__lt=3).count()
        if farbookcount>0:
            farbook=tbl_farmer_booking.objects.filter(id__in=farbkid,booking_status__gt=0,booking_status__lt=3)
            tot=[]
            for i in farbook:
                dmcart=tbl_farmer_booking.objects.get(id=i.id)
                farcart=tbl_farmer_cart.objects.filter(bookingid=dmcart,productid__farmer=request.session['farmer_id'])
                total=0
                for j in farcart:
                    total=total+float(j.fquantity)*float(j.productid.pdt_rate)
                tot.append(total)
                fbooks=zip(farbook,tot)
            return render(request,"Farmer/My_buyers.html",{'buyers':fbooks})
        else:
            return render(request,"Farmer/My_buyers.html")
    else:
        return redirect("webguest:login")

def buyerspdt(request,bookid):
    if 'farmer_id' in request.session:
        pdt=tbl_farmer_cart.objects.filter(bookingid=bookid,productid__farmer=request.session['farmer_id'])
        return render(request,"Farmer/Buyer_pdt.html",{'product':pdt})
    else:
        return redirect("webguest:login")

def customerdelivereditem(request,custid):
    items=tbl_farmer_cart.objects.filter(bookingid=custid,productid__farmer=request.session['farmer_id'])
    return render(request,"Farmer/My_buyer_delivery_pdt.html",{'item':items})

def delivery(request,cartid):
    # bookid=tbl_farmer_booking.objects.get(id=cartid)
    # if bookid.booking_status == 1:
    #     book=tbl_farmer_booking.objects.get(id=cartid)
    #     book.booking_status=3
    #     book.save()
    #     de=1
    #     return render(request,"Farmer/My_buyers.html",{'deli':de})
    # else:
    #     book=tbl_farmer_booking.objects.get(id=cartid)
    #     book.booking_status=3
    #     book.fpayment_date=date.today()
    #     book.save()
    #     de=1
    #     return render(request,"Farmer/My_buyers.html",{'deli':de})


    cdata=tbl_farmer_cart.objects.get(id=cusid)
    bookdata=tbl_farmer_booking.objects.get(id=cdata.bookingid.id)
    if bookdata.booking_status == 1:
        cartdata=tbl_farmer_cart.objects.filter(bookingid=bookdata,fcart_status=0).count()
        if cartdata == 1:
            cartitem=tbl_farmer_cart.objects.get(id=cdata.id)
            cartitem.fcart_status=2
            cartitem.save()
            bookdata.booking_status=3
            bookdata.save()
        else:
            cartitem=tbl_farmer_cart.objects.get(id=cdata.id)
            cartitem.mcart_status=2
            cartitem.save()
        de=1
        return render(request,"Farmer/My_buyers.html",{'deli':de})
    else:
        cartdata=tbl_farmer_cart.objects.filter(bookingid=bookdata,mcart_status=0).count()
        if cartdata == 1:
            cartitem=tbl_farmer_cart.objects.get(id=cdata.id)
            cartitem.fcart_status=2
            cartitem.save()
            bookdata.booking_status=3
            bookdata.fpayment_date=date.today()
            bookdata.save()
        else:
            cartitem=tbl_farmer_cart.objects.get(id=cdata.id)
            cartitem.mcart_status=2
            cartitem.save()
        de=1
        return render(request,"Farmer/My_buyers.html",{'deli':de})

def delivereditem(request):
    if 'farmer_id' in request.session:
        fardata=tbl_farmer_reg.objects.get(id=request.session['farmer_id'])
        cartdata=tbl_farmer_cart.objects.filter(productid__farmer=fardata,fcart_status=0)
        cid=[]
        for i in cartdata:
            cart=i.bookingid.id
            cid.append(cart)
        bdatacount=tbl_farmer_booking.objects.filter(id__in=cid,booking_status=3).count()
        if bdatacount>0:
            bdata=tbl_farmer_booking.objects.filter(id__in=cid,booking_status=3)
            total=[]
            for i in bdata:
                tot=0
                bookdatas=tbl_farmer_booking.objects.get(id=i.id)
                cartdatas=tbl_farmer_cart.objects.filter(bookingid=bookdatas)
                for j in cartdatas:
                    tot=tot+float(j.fquantity)*float(j.productid.pdt_rate)
                total.append(tot)
                his=zip(bdata,total)
            return render(request,"Farmer/Delivered_history.html",{'history':his})
        else:
            return render(request,"Farmer/Delivered_history.html")
    else:
        return redirect("webguest:login")

def report(request):
    if 'farmer_id' in request.session:
        fardata=tbl_farmer_reg.objects.get(id=request.session['farmer_id'])
        cartdata=tbl_farmer_cart.objects.filter(productid__farmer=fardata,fcart_status=0)
        cid=[]
        for i in cartdata:
            cart=i.bookingid.id
            cid.append(cart)
        bdatacount=tbl_farmer_booking.objects.filter(id__in=cid,booking_status=3).count()
        if bdatacount>0:
            bdata=tbl_farmer_booking.objects.filter(id__in=cid,booking_status=3)
            total=[]
            for i in bdata:
                tot=0
                bookdatas=tbl_farmer_booking.objects.get(id=i.id)
                cartdatas=tbl_farmer_cart.objects.filter(bookingid=bookdatas)
                for j in cartdatas:
                    tot=tot+float(j.fquantity)*float(j.productid.pdt_rate)
                total.append(tot)
                his=zip(bdata,total)
            return render(request,"Farmer/Report.html",{'history':his})
        else:
            return render(request,"Farmer/Report.html")
    else:
        return redirect("webguest:login")

def ajaxfreport(request):
    fardata=tbl_farmer_reg.objects.get(id=request.session['farmer_id'])
    if request.GET.get('fdate')!="" and request.GET.get('edate')!="":
        cartdata=tbl_farmer_cart.objects.filter(productid__farmer=fardata,fcart_status=0)
        cid=[]
        for i in cartdata:
            cart=i.bookingid.id
            cid.append(cart)
        bdatacount=tbl_farmer_booking.objects.filter(id__in=cid,booking_status=3,booking_date__gte=request.GET.get('fdate'),booking_date__lte=request.GET.get('edate')).count()
        if bdatacount>0:
            bdata=tbl_farmer_booking.objects.filter(id__in=cid,booking_status=3,booking_date__gte=request.GET.get('fdate'),booking_date__lte=request.GET.get('edate'))
            total=[]
            for i in bdata:
                tot=0
                bookdatas=tbl_farmer_booking.objects.get(id=i.id)
                cartdatas=tbl_farmer_cart.objects.filter(bookingid=bookdatas)
                for j in cartdatas:
                    tot=tot+float(j.fquantity)*float(j.productid.pdt_rate)
                total.append(tot)
                his=zip(bdata,total)
            return render(request,"Farmer/AjaxfReport.html",{'history':his})
        else:
            return render(request,"Farmer/AjaxfReport.html")
    elif request.GET.get("fdate")!="":
        cartdata=tbl_farmer_cart.objects.filter(productid__farmer=fardata,fcart_status=0)
        cid=[]
        for i in cartdata:
            cart=i.bookingid.id
            cid.append(cart)
        bdatacount=tbl_farmer_booking.objects.filter(id__in=cid,booking_status=3,booking_date__gte=request.GET.get('fdate')).count()
        if bdatacount>0:
            bdata=tbl_farmer_booking.objects.filter(id__in=cid,booking_status=3,booking_date__gte=request.GET.get('fdate'))
            total=[]
            for i in bdata:
                tot=0
                bookdatas=tbl_farmer_booking.objects.get(id=i.id)
                cartdatas=tbl_farmer_cart.objects.filter(bookingid=bookdatas)
                for j in cartdatas:
                    tot=tot+float(j.fquantity)*float(j.productid.pdt_rate)
                total.append(tot)
                his=zip(bdata,total)
            return render(request,"Farmer/AjaxfReport.html",{'history':his})
        else:
            return render(request,"Farmer/AjaxfReport.html")
    elif request.GET.get("edate")!="":
        cartdata=tbl_farmer_cart.objects.filter(productid__farmer=fardata,fcart_status=0)
        cid=[]
        for i in cartdata:
            cart=i.bookingid.id
            cid.append(cart)
        bdatacount=tbl_farmer_booking.objects.filter(id__in=cid,booking_status=3,booking_date__lte=request.GET.get('edate')).count()
        if bdatacount>0:
            bdata=tbl_farmer_booking.objects.filter(id__in=cid,booking_status=3,booking_date__lte=request.GET.get('edate'))
            total=[]
            for i in bdata:
                tot=0
                bookdatas=tbl_farmer_booking.objects.get(id=i.id)
                cartdatas=tbl_farmer_cart.objects.filter(bookingid=bookdatas)
                for j in cartdatas:
                    tot=tot+float(j.fquantity)*float(j.productid.pdt_rate)
                total.append(tot)
                his=zip(bdata,total)
            return render(request,"Farmer/AjaxfReport.html",{'history':his})
        else:
            return render(request,"Farmer/AjaxfReport.html")
    else:
        return render(request,"Farmer/Report.html")

def buyreport(request):
    if 'farmer_id' in request.session:
        farmer = tbl_farmer_reg.objects.get(id=request.session["farmer_id"])
        ##################################################################################
        counts=tbl_m_cart.objects.filter(bookingid__farmer=farmer,cart_status=2).count()
        array=[0 for i in range(1,counts+1)]
        p=0
        mprodata=tbl_m_cart.objects.filter(bookingid__farmer=farmer,cart_status=2)
        for i in mprodata:
            array[p]=i.bookingid.id
            p=p+1
        ##################################################################################
        
        bcuount=tbl_m_booking.objects.filter(farmer=farmer,booking_status=3,id__in=array).count()
        if bcuount>0:
            bookdata=tbl_m_booking.objects.filter(farmer=farmer,booking_status=3,id__in=array)
            cart=tbl_m_cart.objects.filter(bookingid__in=array)
            totals=[]
            j=1
            for i in bookdata:
                cartdata=tbl_m_cart.objects.filter(bookingid=i.id,cart_status=2)
                total=0
                for j in cartdata:
                    total=total+(float(j.mquantity)*float(j.productid.pdt_rate))
                totals.append(total)
            bookid=bookdata[0].id
            cartdata= tbl_m_cart.objects.filter(bookingid=bookid)
            datas=zip(bookdata,totals,cart)
            return render(request,"Farmer/Buy_report.html",{'book':datas,'totals':totals,'t':1})
        else:
            return render(request,"Farmer/Buy_report.html")
    else:
        return redirect("webguest:login")

def ajaxbuyreport(request):
    farmer = tbl_farmer_reg.objects.get(id=request.session["farmer_id"])
    if request.GET.get('fdate')!="" and request.GET.get('edate')!="":
         
    ##################################################################################
        counts=tbl_m_cart.objects.filter(bookingid__farmer=farmer,cart_status=2).count()
        array=[0 for i in range(1,counts+1)]
        p=0
        mprodata=tbl_m_cart.objects.filter(bookingid__farmer=farmer,cart_status=2)
        for i in mprodata:
            array[p]=i.bookingid.id
            p=p+1
    ##################################################################################
    
        bcuount=tbl_m_booking.objects.filter(farmer=farmer,booking_status=3,id__in=array,booking_date__gte=request.GET.get('fdate'),booking_date__lte=request.GET.get('edate')).count()
        if bcuount>0:
            bookdata=tbl_m_booking.objects.filter(farmer=farmer,booking_status=3,id__in=array,booking_date__gte=request.GET.get('fdate'),booking_date__lte=request.GET.get('edate'))
            cart=tbl_m_cart.objects.filter(bookingid__in=array)
            totals=[]
            j=1
            for i in bookdata:
                cartdata=tbl_m_cart.objects.filter(bookingid=i.id,cart_status=2)
                total=0
                for j in cartdata:
                    total=total+(float(j.mquantity)*float(j.productid.pdt_rate))
                totals.append(total)
            bookid=bookdata[0].id
            cartdata= tbl_m_cart.objects.filter(bookingid=bookid)
            datas=zip(bookdata,totals,cart)
            return render(request,"Farmer/AjaxBuy_report.html",{'book':datas,'totals':totals,'t':1})
        else:
            return render(request,"Farmer/AjaxBuy_report.html")

    elif request.GET.get('fdate')!="":
             
    ##################################################################################
        counts=tbl_m_cart.objects.filter(bookingid__farmer=farmer,cart_status=2).count()
        array=[0 for i in range(1,counts+1)]
        p=0
        mprodata=tbl_m_cart.objects.filter(bookingid__farmer=farmer,cart_status=2)
        for i in mprodata:
            array[p]=i.bookingid.id
            p=p+1
    ##################################################################################
    
        bcuount=tbl_m_booking.objects.filter(farmer=farmer,booking_status=3,id__in=array,booking_date__gte=request.GET.get('fdate')).count()
        if bcuount>0:
            bookdata=tbl_m_booking.objects.filter(farmer=farmer,booking_status=3,id__in=array,booking_date__gte=request.GET.get('fdate'))
            cart=tbl_m_cart.objects.filter(bookingid__in=array)
            totals=[]
            j=1
            for i in bookdata:
                cartdata=tbl_m_cart.objects.filter(bookingid=i.id,cart_status=2)
                total=0
                for j in cartdata:
                    total=total+(float(j.mquantity)*float(j.productid.pdt_rate))
                totals.append(total)
            bookid=bookdata[0].id
            cartdata= tbl_m_cart.objects.filter(bookingid=bookid)
            datas=zip(bookdata,totals,cart)
            return render(request,"Farmer/AjaxBuy_report.html",{'book':datas,'totals':totals,'t':1})
        else:
            return render(request,"Farmer/AjaxBuy_report.html")
    elif request.GET.get('edate')!="":
             
    ##################################################################################
        counts=tbl_m_cart.objects.filter(bookingid__farmer=farmer,cart_status=2).count()
        array=[0 for i in range(1,counts+1)]
        p=0
        mprodata=tbl_m_cart.objects.filter(bookingid__farmer=farmer,cart_status=2)
        for i in mprodata:
            array[p]=i.bookingid.id
            p=p+1
    ##################################################################################
    
        bcuount=tbl_m_booking.objects.filter(farmer=farmer,booking_status=3,id__in=array,booking_date__lte=request.GET.get('edate')).count()
        if bcuount>0:
            bookdata=tbl_m_booking.objects.filter(farmer=farmer,booking_status=3,id__in=array,booking_date__lte=request.GET.get('edate'))
            cart=tbl_m_cart.objects.filter(bookingid__in=array)
            totals=[]
            j=1
            for i in bookdata:
                cartdata=tbl_m_cart.objects.filter(bookingid=i.id,cart_status=2)
                total=0
                for j in cartdata:
                    total=total+(float(j.mquantity)*float(j.productid.pdt_rate))
                totals.append(total)
            bookid=bookdata[0].id
            cartdata= tbl_m_cart.objects.filter(bookingid=bookid)
            datas=zip(bookdata,totals,cart)
            return render(request,"Farmer/AjaxBuy_report.html",{'book':datas,'totals':totals,'t':1})
        else:
            return render(request,"Farmer/AjaxBuy_report.html")
    else:
        pass