from django.shortcuts import render,redirect
from Guest.models import *
from Admin.models import *
from Market.models import *
from Farmer.models import *
from Customer.models import *
from django.conf import settings
from django.core.mail import send_mail
from datetime import date
# Create your views here.
def home(request):
    if 'market_id' in request.session:
        market=tbl_market_reg.objects.get(id=request.session['market_id'])
        return render(request,"Market/Home.html",{'mark':market})
    else:
        return redirect("webguest:login") 

def my_pro(request):
    if 'market_id' in request.session:
        data=tbl_market_reg.objects.get(id=request.session["market_id"])
        return render(request,"Market/My_profile.html",{'data':data})
    else:
        return redirect("webguest:login")

def editpropic(request):
    if 'market_id' in request.session:
        marketpic=tbl_market_reg.objects.get(id=request.session['market_id'])
        if request.method=="POST":
            marketpic.marphoto=request.FILES.get('txtpropic')
            marketpic.save()
            up=1
            return render(request,"Market/Edit_pro_pic.html",{'update':up})
        else:
            return render(request,"Market/Edit_pro_pic.html",{'data':marketpic})
    else:
        return redirect("webguest:login")

def editprofile(request):
    if 'market_id' in request.session:
        prodata=tbl_market_reg.objects.get(id=request.session["market_id"])
        if request.method=="POST":
            prodata.mar_name=request.POST.get('txtname')
            prodata.mar_contact=request.POST.get('txtcon')
            prodata.mar_email=request.POST.get('txtemail')
            prodata.mar_address=request.POST.get('txtaddress')
            prodata.save()
            ed=1
            return render(request,"Market/Edit_profile.html",{'ed':ed})
        else:
            return render(request,"Market/Edit_profile.html",{'prodata':prodata})
    else:
        return redirect("webguest:login")

def changepassword(request):
    if 'market_id' in request.session:
        if request.method=="POST":
            ccount=tbl_market_reg.objects.filter(id=request.session["market_id"],marpassword=request.POST.get('txtcurpass')).count()
            if ccount>0:
                if request.POST.get('txtnewpass')==request.POST.get('txtconpass'):
                    marketdata=tbl_market_reg.objects.get(id=request.session["market_id"],marpassword=request.POST.get('txtcurpass'))
                    marketdata.marpassword=request.POST.get('txtnewpass')
                    marketdata.save()
                    er3=3
                    return render(request,"Market/Change_password.html",{'er':er3})
                else:
                    er1=1
                    return render(request,"Market/Change_password.html",{'er':er1})
            else:
                er2=2
                return render(request,"Market/Change_password.html",{'er':er2})
        else:
            return render(request,"Market/Change_password.html")
    else:
        return redirect("webguest:login")
        
def product(request):
    if 'market_id' in request.session:
        marketdata=tbl_market_reg.objects.get(id=request.session["market_id"])
        pdt=tbl_market_product.objects.filter(market=request.session['market_id'])
        cata=tbl_catageory.objects.filter(cat_status=1)
        if request.method=="POST":
            subcatdata=tbl_subcat.objects.get(id=request.POST.get('selsubcat'))
            tbl_market_product.objects.create(pdt_name=request.POST.get('txtname'),pdt_rate=request.POST.get('txtrate'),pdt_dis=request.POST.get('txtdes'),pdt_stock=request.POST.get('txtstock'),pdt_image=request.FILES.get('txtimage'),subcategory=subcatdata,market=marketdata)
            pro=1
            return render(request,"Market/Market_product.html",{'cata':cata,'pdt':pdt,'pro':pro})
        else:
            return render(request,"Market/Market_product.html",{'cata':cata,'pdt':pdt})
    else:
        return redirect("webguest:login")

def stock(request,stid):
    if 'market_id' in request.session:
        stock=tbl_market_product.objects.get(id=stid)
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
                return render(request,"Market/Stock_update.html",{'st':st})
            elif request.POST.get('txtstockno')!="":
                qun=stock.pdt_stock
                q=qun*1000
                te=float(request.POST.get('txtstockno'))
                s=q+(te*1000)
                newstock=s/1000
                stock.pdt_stock=newstock
                stock.save()
                st=1
                return render(request,"Market/Stock_update.html",{'st':st})
            elif request.POST.get('txtrate'):
                stock.pdt_rate=request.POST.get('txtrate')
                stock.save()
                st=1
                return render(request,"Market/Stock_update.html",{'st':st})
            else:
                return render(request,"Market/Stock_update.html")
        else:
            return render(request,"Market/Stock_update.html",{'stock':stock})
    else:
        return redirect("webguest:login")

def deleteitem(request,delid):
    itemdata=tbl_market_product.objects.get(id=delid).delete()
    de=1
    return render(request,"Market/Market_product.html",{'de':de})

def complaint(request):
    if 'market_id' in request.session:
        comtype=tbl_complainttype.objects.all()
        mardata=tbl_market_reg.objects.get(id=request.session["market_id"])
        if request.method=="POST":
            comtype=tbl_complainttype.objects.get(id=request.POST.get("txtcomtype"))
            tbl_complaint.objects.create(complaint_con=request.POST.get("txtcomcon"),market=mardata,com_type=comtype)
            ins=1
            return render(request,"Market/Complaint.html",{'ins':ins})
        else:
            return render(request,"Market/Complaint.html",{'type':comtype})
    else:
        return redirect("webguest:login")

def feedback(request):
    if 'market_id' in request.session:
        mardata=tbl_market_reg.objects.get(id=request.session["market_id"])
        if request.method=="POST":
            tbl_feedback.objects.create(feedback_con=request.POST.get("txtfeedback"),market=mardata)
            ins1=1
            return render(request,"Market/Feedback.html",{'ins1':ins1})
        else:
            return render(request,"Market/Feedback.html")
    else:
        return redirect("webguest:login")

def reply(request):
    if 'market_id' in request.session:
        reply=tbl_complaint.objects.filter(market=request.session["market_id"])
        return render(request,"Market/View_reply.html",{'market':reply})
    else:
        return redirect("webguest:login")

def viewbuyers(request):
    if 'market_id' in request.session:
        mardata = tbl_market_reg.objects.get(id=request.session["market_id"])
        fcart = tbl_m_cart.objects.filter(productid__market=mardata,bookingid__booking_status__gt=0,bookingid__booking_status__lt=3).count()
        ccart = tbl_market_cart.objects.filter(productid__market=mardata,bookingid__booking_status__gt=0,bookingid__booking_status__lt=3).count()

        if (fcart>0)&(ccart>0):
            # print("Jenin")
            fc = tbl_m_cart.objects.filter(productid__market=mardata,cart_status=0)
            bid_list = []  # Create an empty list to store all the bid values

            for item in fc:
                bid = item.bookingid.id
                bid_list.append(bid)  # Add each bid value to the list

            fbooking = tbl_m_booking.objects.filter(id__in=bid_list, booking_status__gt=0, booking_status__lt=3)
            t=[]
            for i in fbooking:
                total=0
                book=tbl_m_booking.objects.get(id=i.id)
                cart=tbl_m_cart.objects.filter(bookingid=book,productid__market=request.session['market_id'])
                for j in cart:
                    total=total+float(j.mquantity)*float(j.productid.pdt_rate)
                t.append(total)
            fadata=zip(fbooking,t)

            cc = tbl_market_cart.objects.filter(productid__market=mardata,mcart_status=0)
            cbid_list = []

            for citems in cc:
                cid=citems.bookingid.id
                cbid_list.append(cid)

            cbooking = tbl_market_booking.objects.filter(id__in=cbid_list, booking_status__gt=0, booking_status__lt=3)
            tot=[]
            for i in cbooking:
                t=0
                bookid=tbl_market_booking.objects.get(id=i.id)
                cartid=tbl_market_cart.objects.filter(bookingid=bookid,productid__market=request.session['market_id'])
                for j in cartid:
                    t=t+float(j.mquantity)*float(j.productid.pdt_rate)
                tot.append(t)
            cadata=zip(cbooking,tot)

            return render(request, "Market/View_Buyers.html", {'farmer': fadata,'customer':cadata})

        elif fcart > 0:
            print("Hai")
            fc = tbl_m_cart.objects.filter(productid__market=mardata,cart_status=0)
            bid_list = []  # Create an empty list to store all the bid values

            for item in fc:
                bid = item.bookingid.id
                bid_list.append(bid)  # Add each bid value to the list
            fbooking = tbl_m_booking.objects.filter(id__in=bid_list, booking_status__gt=0, booking_status__lt=3)
            t=[]
            for i in fbooking:
                total=0
                book=tbl_m_booking.objects.get(id=i.id)
                cart=tbl_m_cart.objects.filter(bookingid=book,productid__market=request.session['market_id'])
                for j in cart:
                    total=total+float(j.mquantity)*float(j.productid.pdt_rate)
                t.append(total)
            fadata=zip(fbooking,t)
            return render(request, "Market/View_Buyers.html", {'farmer': fadata})
        elif ccart > 0:
            print("Abin")
            cc = tbl_market_cart.objects.filter(productid__market=mardata,mcart_status=0)
            cbid_list = []

            for citems in cc:
                cid=citems.bookingid.id
                cbid_list.append(cid)

            cbooking = tbl_market_booking.objects.filter(id__in=cbid_list, booking_status__gt=0, booking_status__lt=3,)
            tot=[]
            for i in cbooking:
                t=0
                bookid=tbl_market_booking.objects.get(id=i.id)
                cartid=tbl_market_cart.objects.filter(bookingid=bookid,productid__market=request.session['market_id'])
                for j in cartid:
                    t=t+float(j.mquantity)*float(j.productid.pdt_rate)
                tot.append(t)
            cadata=zip(cbooking,tot)
            return render(request,"Market/View_Buyers.html",{'customer':cadata})

        else:
            return render(request, "Market/View_Buyers.html")
    else:
        return redirect("webguest:login") 

def viewbuyerspdt(request,pdtid):
    if 'market_id' in request.session:
        data=tbl_m_cart.objects.filter(bookingid=pdtid,cart_status=0,productid__market=request.session['market_id'])
        return render(request,"Market/Farmer_buy_pdt.html",{'pdtdata':data})
    else:
        return redirect("webguest:login")

def viewbuyersdeliverypdt(request,farmerproduct):
    if 'market_id' in request.session:
        data=tbl_m_cart.objects.filter(bookingid=farmerproduct,cart_status=2,productid__market=request.session['market_id'])
        return render(request,"Market/View_farmer_delivered_pdt.html",{'pdtdata':data})
    else:
        return redirect("webguest:login")

def viewcustomerpdt(request,cupdtid):
    if 'market_id' in request.session:
        cupdtdata=tbl_market_cart.objects.filter(bookingid=cupdtid,mcart_status=0,productid__market=request.session['market_id'])
        return render(request,"Market/Customer_buy_pdt.html",{'cuspdt':cupdtdata})
    else:
        return redirect("webguest:login")

def viewcustomerdeliveredpdt(request,customerproduct):
    if 'market_id' in request.session:
        cupdtdata=tbl_market_cart.objects.filter(bookingid=customerproduct,mcart_status=2,productid__market=request.session['market_id'])
        return render(request,"Market/Customer_buy_pdt.html",{'cuspdt':cupdtdata})
    else:
        return redirect("webguest:login")

def customeritemdelivered(request,cusitemid):
    itemdata=tbl_market_cart.objects.filter(bookingid=cusitemid,productid__market=request.session['market_id'])
    return render(request,"Market/Item_delivered.html",{'item':itemdata})

def farmeritemdelivered(request,farmeritem):
    itemdata=tbl_m_cart.objects.filter(bookingid=farmeritem,productid__market=request.session['market_id'])
    return render(request,"Market/Item_delivered_farmer.html",{'item':itemdata})

def itemdelivery(request,deid):
    # ddata=tbl_m_booking.objects.get(id=deid)
    # ddata.booking_status=3
    # ddata.payment_date=date.today()
    # ddata.save()
    # deli=1

    cdata=tbl_m_cart.objects.get(id=deid)
    bookdata=tbl_m_booking.objects.get(id=cdata.bookingid.id)
    if bookdata.booking_status == 1:
        cartdata=tbl_m_cart.objects.filter(bookingid=bookdata,cart_status=0).count()
        if cartdata == 1:
            cartitem=tbl_m_cart.objects.get(id=cdata.id)
            cartitem.cart_status=2
            cartitem.save()
            bookdata.booking_status=3
            bookdata.save()
        else:
            cartitem=tbl_m_cart.objects.get(id=cdata.id)
            cartitem.cart_status=2
            cartitem.save()
        deli=1
        return render(request,"Market/View_Buyers.html",{'stat':deli})
    else:
        cartdata=tbl_m_cart.objects.filter(bookingid=bookdata,cart_status=0).count()
        if cartdata == 1:
            cartitem=tbl_m_cart.objects.get(id=cdata.id)
            cartitem.cart_status=2
            cartitem.save()
            bookdata.booking_status=3
            bookdata.payment_date=date.today()
            bookdata.save()
        else:
            cartitem=tbl_m_cart.objects.get(id=cdata.id)
            cartitem.cart_status=2
            cartitem.save()
        deli=1
        return render(request,"Market/View_Buyers.html",{'stat':deli})

def cusdeliveryitem(request,cusid):
    # cusdata=tbl_market_booking.objects.get(id=cusid)
    # cusdata.booking_status=3
    # cusdata.mpayment_booking=date.today()
    # cusdata.save()
    # deli=1

    cdata=tbl_market_cart.objects.get(id=cusid)
    bookdata=tbl_market_booking.objects.get(id=cdata.bookingid.id)
    if bookdata.booking_status == 1:
        cartdata=tbl_market_cart.objects.filter(bookingid=bookdata,mcart_status=0).count()
        if cartdata == 1:
            cartitem=tbl_market_cart.objects.get(id=cdata.id)
            cartitem.mcart_status=2
            cartitem.save()
            bookdata.booking_status=3
            bookdata.save()
        else:
            cartitem=tbl_market_cart.objects.get(id=cdata.id)
            cartitem.mcart_status=2
            cartitem.save()
        deli=1
        return render(request,"Market/View_Buyers.html",{'stat':deli})
    else:
        cartdata=tbl_market_cart.objects.filter(bookingid=bookdata,mcart_status=0).count()
        if cartdata == 1:
            cartitem=tbl_market_cart.objects.get(id=cdata.id)
            cartitem.mcart_status=2
            cartitem.save()
            bookdata.booking_status=3
            bookdata.mpayment_date=date.today()
            bookdata.save()
        else:
            cartitem=tbl_market_cart.objects.get(id=cdata.id)
            cartitem.mcart_status=2
            cartitem.save()
        deli=1
        return render(request,"Market/View_Buyers.html",{'stat':deli})

def delivereditems(request):
    if 'market_id' in request.session:
        mardata = tbl_market_reg.objects.get(id=request.session["market_id"])
        fcart = tbl_m_cart.objects.filter(productid__market=mardata,bookingid__booking_status=3).count()
        ccart = tbl_market_cart.objects.filter(productid__market=mardata,bookingid__booking_status=3).count()

        if(fcart > 0)&(ccart > 0):
            fardata = tbl_m_cart.objects.filter(productid__market=mardata)
            bid_list = []  # Create an empty list to store all the bid values

            for item in fardata:
                bid = item.bookingid.id
                bid_list.append(bid)  # Add each bid value to the list

            fbooking = tbl_m_booking.objects.filter(id__in=bid_list, booking_status=3)
            totalf=[]
            for i in fbooking:
                total=0
                mbdata=tbl_m_booking.objects.get(id=i.id)
                mcdata=tbl_m_cart.objects.filter(bookingid=mbdata,productid__market=request.session['market_id'])
                for j in mcdata:
                    total=total+float(j.mquantity)*float(j.productid.pdt_rate)
                totalf.append(total)
            fdatas=zip(fbooking,totalf)
            cc = tbl_market_cart.objects.filter(productid__market=mardata)
            cbid_list = []

            for citems in cc:
                cid=citems.bookingid.id
                cbid_list.append(cid)

            cbooking = tbl_market_booking.objects.filter(id__in=cbid_list, booking_status=3)
            totals=[]
            for i in cbooking:
                total=0
                bmdata=tbl_market_booking.objects.get(id=i.id)
                cmdata=tbl_market_cart.objects.filter(bookingid=bmdata,productid__market=request.session['market_id'])
                for j in cmdata:
                    total=total+float(j.mquantity)*float(j.productid.pdt_rate)
                totals.append(total)
            cdatas=zip(cbooking,totals)
            return render(request, "Market/Delivered_items.html", {'farmer': fdatas,'customer':cdatas})

        elif fcart > 0:
            fardata = tbl_m_cart.objects.filter(productid__market=mardata)
            bid_list = []  # Create an empty list to store all the bid values

            for item in fardata:
                bid = item.bookingid.id
                bid_list.append(bid)  # Add each bid value to the list

            fbooking = tbl_m_booking.objects.filter(id__in=bid_list, booking_status=3)
            totalf=[]
            for i in fbooking:
                total=0
                mbdata=tbl_m_booking.objects.get(id=i.id)
                mcdata=tbl_m_cart.objects.filter(bookingid=mbdata,productid__market=request.session['market_id'])
                for j in mcdata:
                    total=total+float(j.mquantity)*float(j.productid.pdt_rate)
                totalf.append(total)
            fdatas=zip(fbooking,totalf)
            return render(request, "Market/Delivered_items.html", {'farmer': fdatas})

        elif ccart > 0:
            cc = tbl_market_cart.objects.filter(productid__market=mardata)
            cbid_list = []

            for citems in cc:
                cid=citems.bookingid.id
                cbid_list.append(cid)

            cbooking = tbl_market_booking.objects.filter(id__in=cbid_list, booking_status=3)
            cm=[]
            totals=[]
            for i in cbooking:
                total=0
                bmdata=tbl_market_booking.objects.get(id=i.id)
                cmdata=tbl_market_cart.objects.filter(bookingid=bmdata,productid__market=request.session['market_id'])
                for j in cmdata:
                    total=total+float(j.mquantity)*float(j.productid.pdt_rate)
                totals.append(total)
            cdatas=zip(cbooking,totals)
            
            return render(request,"Market/Delivered_items.html",{'customer':cdatas})
        else:
            return render(request, "Market/Delivered_items.html")
    else:
        return redirect("webguest:login") 

def event(request):
    if 'market_id' in request.session:
        event=tbl_events.objects.filter(market=request.session["market_id"])
        if request.method=="POST":
            market=tbl_market_reg.objects.get(id=request.session["market_id"])
            tbl_events.objects.create(event_name=request.POST.get("txteventname"),event_fdate=request.POST.get("txteventfdate"),event_tdate=request.POST.get("txteventtdate"),event_details=request.POST.get("txteventdetails"),event_photo=request.FILES.get("txteventphoto"),market=market)
            create=1
            return render(request,"MArket/Event_registration.html",{'status':create,'event':event})
        else:
            return render(request,"Market/Event_registration.html",{'event':event})
    else:
        return redirect("webguest:login")

def deleteevent(request,evid):
    tbl_events.objects.get(id=evid).delete()
    de=1
    return render(request,"Market/Home.html",{'de':de})

def viewapplication(request,appid):
    if 'market_id' in request.session:
        customer=tbl_cus_reg.objects.all()
        cusapp=applyevent.objects.filter(event__market=request.session["market_id"],event=appid,customer__in=customer,status__lt=2)
        farmer=tbl_farmer_reg.objects.all()
        farapp=applyevent.objects.filter(event__market=request.session["market_id"],event=appid,farmer__in=farmer,status__lt=2)
        return render(request,"Market/View_event_application.html",{'customerapp':cusapp,'farmerapp':farapp})
    else:
        return redirect("webguest:login")

def eventfarmerreply(request,apprpid):
    if 'market_id' in request.session:
        ev=applyevent.objects.get(id=apprpid)
        if request.method=="POST":
            ev.replay=request.POST.get("txtreply")
            ev.status=1
            ev.save()
            ac=1
            return render(request,"Market/Reply_to_application.html",{'data':ev,'ac':ac})
        else:
            return render(request,"Market/Reply_to_application.html",{'data':ev})
    else:
        return redirect("webguest:login")

def farmerapprove(request,farmerid):
    farevent=applyevent.objects.get(id=farmerid)
    farevent.status=2
    farevent.save()
    app=1
    return render(request,"Market/View_event_application.html",{'approve':app})

def farmerreject(request,farid):
    farmerevent=applyevent.objects.get(id=farid)
    farmerevent.status=3
    farmerevent.save()
    rjj=1
    return render(request,"Market/View_event_application.html",{'reject':rjj})

def farmerarrived(request,fararrid):
    fararrevent=applyevent.objects.get(id=fararrid)
    fararrevent.status=4
    fararrevent.save()
    arr=1
    return render(request,"Market/View_approve_application.html",{'arrived':arr})

def eventcustomerreply(request,cusappid):
    if 'market_id' in request.session:
        cusev=applyevent.objects.get(id=cusappid)
        if request.method=="POST":
            cusev.replay=request.POST.get("txtreply")
            cusev.status=1
            cusev.save()
            ac=1
            return render(request,"Market/Reply_to_application.html",{'data':ev,'ac':ac})
        else:
            return render(request,"Market/Reply_to_application.html",{'data':ev})
    else:
        return redirect("webguest:login")

def customerapprove(request,customerid):
    cusevent=applyevent.objects.get(id=customerid)
    cusevent.status=2
    cusevent.save()
    ac=1
    return render(request,"Market/View_event_application.html",{'approve':app})

def customerreject(request,custid):
    customerevent=applyevent.objects.get(id=custid)
    customerevent.status=3
    customerevent.save()
    rjj=1
    return render(request,"Market/View_event_application.html",{'reject':rjj})

def customerarrived(request,cusarrid):
    cusarrevent=applyevent.objects.get(id=cusarrid)
    cusarrevent.status=4
    cusarrevent.save()
    arr=1
    return render(request,"Market/View_approve_application.html",{'arrived':arr})

def viewapprovel(request,approvelid):
    if 'market_id' in request.session:
        customer=tbl_cus_reg.objects.all()
        cusapp=applyevent.objects.filter(event__market=request.session["market_id"],event=approvelid,customer__in=customer,status=2)
        farmer=tbl_farmer_reg.objects.all()
        farapp=applyevent.objects.filter(event__market=request.session["market_id"],event=approvelid,farmer__in=farmer,status=2)
        return render(request,"Market/View_approve_application.html",{'customerapp':cusapp,'farmerapp':farapp})
    else:
        return redirect("webguest:login")

def viewreject(request,rejectedid):
    if 'market_id' in request.session:
        customer=tbl_cus_reg.objects.all()
        cusapp=applyevent.objects.filter(event__market=request.session["market_id"],event=rejectedid,customer__in=customer,status=3)
        farmer=tbl_farmer_reg.objects.all()
        farapp=applyevent.objects.filter(event__market=request.session["market_id"],event=rejectedid,farmer__in=farmer,status=3)
        return render(request,"Market/View_reject_application.html",{'customerapp':cusapp,'farmerapp':farapp})
    else:
        return redirect("webguest:login")

def viewarrive(request,arrivelid):
    if 'market_id' in request.session:
        customer=tbl_cus_reg.objects.all()
        cusapp=applyevent.objects.filter(event__market=request.session["market_id"],event=arrivelid,customer__in=customer,status=4)
        farmer=tbl_farmer_reg.objects.all()
        farapp=applyevent.objects.filter(event__market=request.session["market_id"],event=arrivelid,farmer__in=farmer,status=4)
        return render(request,"Market/View_arrived_application.html",{'customerapp':cusapp,'farmerapp':farapp})
    else:
        return redirect("webguest:login")

def logout(request):
    del request.session["market_id"]
    return redirect("webguest:login")

def report(request):
    if 'market_id' in request.session:
        mardata = tbl_market_reg.objects.get(id=request.session["market_id"])
        fcart = tbl_m_cart.objects.filter(productid__market=mardata,bookingid__booking_status=3).count()
        ccart = tbl_market_cart.objects.filter(productid__market=mardata,bookingid__booking_status=3).count()

        if(fcart > 0)&(ccart > 0):
            fardata = tbl_m_cart.objects.filter(productid__market=mardata)
            bid_list = []  # Create an empty list to store all the bid values

            for item in fardata:
                bid = item.bookingid.id
                bid_list.append(bid)  # Add each bid value to the list

            fbooking = tbl_m_booking.objects.filter(id__in=bid_list, booking_status=3)
            totalf=[]
            for i in fbooking:
                total=0
                mbdata=tbl_m_booking.objects.get(id=i.id)
                mcdata=tbl_m_cart.objects.filter(bookingid=mbdata,productid__market=request.session['market_id'])
                for j in mcdata:
                    total=total+float(j.mquantity)*float(j.productid.pdt_rate)
                totalf.append(total)
            fdatas=zip(fbooking,totalf)
            cc = tbl_market_cart.objects.filter(productid__market=mardata)
            cbid_list = []

            for citems in cc:
                cid=citems.bookingid.id
                cbid_list.append(cid)

            cbooking = tbl_market_booking.objects.filter(id__in=cbid_list, booking_status=3)
            totals=[]
            for i in cbooking:
                total=0
                bmdata=tbl_market_booking.objects.get(id=i.id)
                cmdata=tbl_market_cart.objects.filter(bookingid=bmdata,productid__market=request.session['market_id'])
                for j in cmdata:
                    total=total+float(j.mquantity)*float(j.productid.pdt_rate)
                totals.append(total)
            cdatas=zip(cbooking,totals)
            return render(request,"Market/Report.html",{'farmer':fdatas,'customer':cdatas})
        elif fcart > 0:
            fardata = tbl_m_cart.objects.filter(productid__market=mardata)
            bid_list = []  # Create an empty list to store all the bid values

            for item in fardata:
                bid = item.bookingid.id
                bid_list.append(bid)  # Add each bid value to the list

            fbooking = tbl_m_booking.objects.filter(id__in=bid_list, booking_status=3)
            totalf=[]
            for i in fbooking:
                total=0
                mbdata=tbl_m_booking.objects.get(id=i.id)
                mcdata=tbl_m_cart.objects.filter(bookingid=mbdata,productid__market=request.session['market_id'])
                for j in mcdata:
                    total=total+float(j.mquantity)*float(j.productid.pdt_rate)
                totalf.append(total)
            fdatas=zip(fbooking,totalf)
            return render(request,"Market/Report.html",{'farmer':fdatas})
        elif ccart > 0:
            cc = tbl_market_cart.objects.filter(productid__market=mardata)
            cbid_list = []

            for citems in cc:
                cid=citems.bookingid.id
                cbid_list.append(cid)

            cbooking = tbl_market_booking.objects.filter(id__in=cbid_list, booking_status=3)
            cm=[]
            totals=[]
            for i in cbooking:
                total=0
                bmdata=tbl_market_booking.objects.get(id=i.id)
                cmdata=tbl_market_cart.objects.filter(bookingid=bmdata,productid__market=request.session['market_id'])
                for j in cmdata:
                    total=total+float(j.mquantity)*float(j.productid.pdt_rate)
                totals.append(total)
            cdatas=zip(cbooking,totals)
            return render(request,"Market/Report.html",{'customer':cdatas})
        
        else:
            return render(request,"Market/Report.html")
    else:
        return redirect("webguest:login")

def ajaxreport(request):
    mardata = tbl_market_reg.objects.get(id=request.session["market_id"])
    if request.GET.get('fdate')!="" and request.GET.get('edate')!="":
        print("first1")
        fcart = tbl_m_cart.objects.filter(productid__market=mardata,bookingid__booking_status=3).count()
        ccart = tbl_market_cart.objects.filter(productid__market=mardata,bookingid__booking_status=3).count()

        if(fcart > 0)&(ccart > 0):
            fardata = tbl_m_cart.objects.filter(productid__market=mardata)
            bid_list = []  # Create an empty list to store all the bid values

            for item in fardata:
                bid = item.bookingid.id
                bid_list.append(bid)  # Add each bid value to the list

            fbooking = tbl_m_booking.objects.filter(id__in=bid_list, booking_status=3,booking_date__gte=request.GET.get('fdate'),booking_date__lte=request.GET.get('edate'))
            totalf=[]
            for i in fbooking:
                total=0
                mbdata=tbl_m_booking.objects.get(id=i.id)
                mcdata=tbl_m_cart.objects.filter(bookingid=mbdata,productid__market=request.session['market_id'])
                for j in mcdata:
                    total=total+float(j.mquantity)*float(j.productid.pdt_rate)
                totalf.append(total)
            fdatas=zip(fbooking,totalf)
            cc = tbl_market_cart.objects.filter(productid__market=mardata)
            cbid_list = []

            for citems in cc:
                cid=citems.bookingid.id
                cbid_list.append(cid)

            cbooking = tbl_market_booking.objects.filter(id__in=cbid_list, booking_status=3,booking_date__gte=request.GET.get('fdate'),booking_date__lte=request.GET.get('edate'))
            totals=[]
            for i in cbooking:
                total=0
                bmdata=tbl_market_booking.objects.get(id=i.id)
                cmdata=tbl_market_cart.objects.filter(bookingid=bmdata,productid__market=request.session['market_id'])
                for j in cmdata:
                    total=total+float(j.mquantity)*float(j.productid.pdt_rate)
                totals.append(total)
            cdatas=zip(cbooking,totals)
            return render(request,"Market/AjaxReport.html",{'farmer':fdatas,'customer':cdatas})
        elif fcart > 0:
            fardata = tbl_m_cart.objects.filter(productid__market=mardata)
            bid_list = []  # Create an empty list to store all the bid values

            for item in fardata:
                bid = item.bookingid.id
                bid_list.append(bid)  # Add each bid value to the list

            fbooking = tbl_m_booking.objects.filter(id__in=bid_list, booking_status=3,booking_date__gte=request.GET.get('fdate'),booking_date__lte=request.GET.get('edate'))
            totalf=[]
            for i in fbooking:
                total=0
                mbdata=tbl_m_booking.objects.get(id=i.id)
                mcdata=tbl_m_cart.objects.filter(bookingid=mbdata,productid__market=request.session['market_id'])
                for j in mcdata:
                    total=total+float(j.mquantity)*float(j.productid.pdt_rate)
                totalf.append(total)
            fdatas=zip(fbooking,totalf)
            return render(request,"Market/AjaxReport.html",{'farmer':fdatas})
        elif ccart > 0:
            cc = tbl_market_cart.objects.filter(productid__market=mardata)
            cbid_list = []

            for citems in cc:
                cid=citems.bookingid.id
                cbid_list.append(cid)

            cbooking = tbl_market_booking.objects.filter(id__in=cbid_list, booking_status=3,booking_date__gte=request.GET.get('fdate'),booking_date__lte=request.GET.get('edate'))
            cm=[]
            totals=[]
            for i in cbooking:
                total=0
                bmdata=tbl_market_booking.objects.get(id=i.id)
                cmdata=tbl_market_cart.objects.filter(bookingid=bmdata,productid__market=request.session['market_id'])
                for j in cmdata:
                    total=total+float(j.mquantity)*float(j.productid.pdt_rate)
                totals.append(total)
            cdatas=zip(cbooking,totals)
            return render(request,"Market/AjaxReport.html",{'customer':cdatas})
    
        else:
            return render(request,"Market/AjaxReport.html")
    elif request.GET.get('edate')!="":
        print("first3")
        fcart = tbl_m_cart.objects.filter(productid__market=mardata,bookingid__booking_status=3).count()
        ccart = tbl_market_cart.objects.filter(productid__market=mardata,bookingid__booking_status=3).count()

        if(fcart > 0)&(ccart > 0):
            fardata = tbl_m_cart.objects.filter(productid__market=mardata)
            bid_list = []  # Create an empty list to store all the bid values

            for item in fardata:
                bid = item.bookingid.id
                bid_list.append(bid)  # Add each bid value to the list

            fbooking = tbl_m_booking.objects.filter(id__in=bid_list, booking_status=3,booking_date__lte=request.GET.get('edate'))
            totalf=[]
            for i in fbooking:
                total=0
                mbdata=tbl_m_booking.objects.get(id=i.id)
                mcdata=tbl_m_cart.objects.filter(bookingid=mbdata,productid__market=request.session['market_id'])
                for j in mcdata:
                    total=total+float(j.mquantity)*float(j.productid.pdt_rate)
                totalf.append(total)
            fdatas=zip(fbooking,totalf)
            cc = tbl_market_cart.objects.filter(productid__market=mardata)
            cbid_list = []

            for citems in cc:
                cid=citems.bookingid.id
                cbid_list.append(cid)

            cbooking = tbl_market_booking.objects.filter(id__in=cbid_list, booking_status=3,booking_date__lte=request.GET.get('edate'))
            totals=[]
            for i in cbooking:
                total=0
                bmdata=tbl_market_booking.objects.get(id=i.id)
                cmdata=tbl_market_cart.objects.filter(bookingid=bmdata,productid__market=request.session['market_id'])
                for j in cmdata:
                    total=total+float(j.mquantity)*float(j.productid.pdt_rate)
                totals.append(total)
            cdatas=zip(cbooking,totals)
            return render(request,"Market/AjaxReport.html",{'farmer':fdatas,'customer':cdatas})
        elif fcart > 0:
            fardata = tbl_m_cart.objects.filter(productid__market=mardata)
            bid_list = []  # Create an empty list to store all the bid values

            for item in fardata:
                bid = item.bookingid.id
                bid_list.append(bid)  # Add each bid value to the list

            fbooking = tbl_m_booking.objects.filter(id__in=bid_list, booking_status=3,booking_date__lte=request.GET.get('edate'))
            totalf=[]
            for i in fbooking:
                total=0
                mbdata=tbl_m_booking.objects.get(id=i.id)
                mcdata=tbl_m_cart.objects.filter(bookingid=mbdata,productid__market=request.session['market_id'])
                for j in mcdata:
                    total=total+float(j.mquantity)*float(j.productid.pdt_rate)
                totalf.append(total)
            fdatas=zip(fbooking,totalf)
            return render(request,"Market/AjaxReport.html",{'farmer':fdatas})
        elif ccart > 0:
            cc = tbl_market_cart.objects.filter(productid__market=mardata)
            cbid_list = []

            for citems in cc:
                cid=citems.bookingid.id
                cbid_list.append(cid)

            cbooking = tbl_market_booking.objects.filter(id__in=cbid_list, booking_status=3,booking_date__lte=request.GET.get('edate'))
            cm=[]
            totals=[]
            for i in cbooking:
                total=0
                bmdata=tbl_market_booking.objects.get(id=i.id)
                cmdata=tbl_market_cart.objects.filter(bookingid=bmdata,productid__market=request.session['market_id'])
                for j in cmdata:
                    total=total+float(j.mquantity)*float(j.productid.pdt_rate)
                totals.append(total)
            cdatas=zip(cbooking,totals)
            return render(request,"Market/AjaxReport.html",{'customer':cdatas})
    
        else:
            return render(request,"Market/AjaxReport.html")
    elif request.GET.get('fdate')!="":
        print("first2")
        fcart = tbl_m_cart.objects.filter(productid__market=mardata,bookingid__booking_status=3).count()
        ccart = tbl_market_cart.objects.filter(productid__market=mardata,bookingid__booking_status=3).count()

        if(fcart > 0)&(ccart > 0):
            fardata = tbl_m_cart.objects.filter(productid__market=mardata)
            bid_list = []  # Create an empty list to store all the bid values

            for item in fardata:
                bid = item.bookingid.id
                bid_list.append(bid)  # Add each bid value to the list

            fbooking = tbl_m_booking.objects.filter(id__in=bid_list, booking_status=3,booking_date__gte=request.GET.get('fdate'))
            totalf=[]
            for i in fbooking:
                total=0
                mbdata=tbl_m_booking.objects.get(id=i.id)
                mcdata=tbl_m_cart.objects.filter(bookingid=mbdata,productid__market=request.session['market_id'])
                for j in mcdata:
                    total=total+float(j.mquantity)*float(j.productid.pdt_rate)
                totalf.append(total)
            fdatas=zip(fbooking,totalf)
            cc = tbl_market_cart.objects.filter(productid__market=mardata)
            cbid_list = []

            for citems in cc:
                cid=citems.bookingid.id
                cbid_list.append(cid)

            cbooking = tbl_market_booking.objects.filter(id__in=cbid_list, booking_status=3,booking_date__gte=request.GET.get('fdate'))
            totals=[]
            for i in cbooking:
                total=0
                bmdata=tbl_market_booking.objects.get(id=i.id)
                cmdata=tbl_market_cart.objects.filter(bookingid=bmdata,productid__market=request.session['market_id'])
                for j in cmdata:
                    total=total+float(j.mquantity)*float(j.productid.pdt_rate)
                totals.append(total)
            cdatas=zip(cbooking,totals)
            return render(request,"Market/AjaxReport.html",{'farmer':fdatas,'customer':cdatas})
        elif fcart > 0:
            fardata = tbl_m_cart.objects.filter(productid__market=mardata)
            bid_list = []  # Create an empty list to store all the bid values

            for item in fardata:
                bid = item.bookingid.id
                bid_list.append(bid)  # Add each bid value to the list

            fbooking = tbl_m_booking.objects.filter(id__in=bid_list, booking_status=3,booking_date__gte=request.GET.get('fdate'))
            totalf=[]
            for i in fbooking:
                total=0
                mbdata=tbl_m_booking.objects.get(id=i.id)
                mcdata=tbl_m_cart.objects.filter(bookingid=mbdata,productid__market=request.session['market_id'])
                for j in mcdata:
                    total=total+float(j.mquantity)*float(j.productid.pdt_rate)
                totalf.append(total)
            fdatas=zip(fbooking,totalf)
            return render(request,"Market/AjaxReport.html",{'farmer':fdatas})
        elif ccart > 0:
            cc = tbl_market_cart.objects.filter(productid__market=mardata)
            cbid_list = []

            for citems in cc:
                cid=citems.bookingid.id
                cbid_list.append(cid)

            cbooking = tbl_market_booking.objects.filter(id__in=cbid_list, booking_status=3,booking_date__gte=request.GET.get('fdate'))
            cm=[]
            totals=[]
            for i in cbooking:
                total=0
                bmdata=tbl_market_booking.objects.get(id=i.id)
                cmdata=tbl_market_cart.objects.filter(bookingid=bmdata,productid__market=request.session['market_id'])
                for j in cmdata:
                    total=total+float(j.mquantity)*float(j.productid.pdt_rate)
                totals.append(total)
            cdatas=zip(cbooking,totals)
            return render(request,"Market/AjaxReport.html",{'customer':cdatas})
    
        else:
            return render(request,"Market/AjaxReport.html")
    
    else:
        return render(request,"Market/AjaxReport.html")