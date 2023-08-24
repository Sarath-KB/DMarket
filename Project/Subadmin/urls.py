from django.urls import path,include
from Subadmin import views
app_name="websubadmin"
urlpatterns = [
     path('home/',views.home,name="home"),
     path('My_profile/',views.my_pro,name="my_pro"),
     path('editprofile/',views.editprofile,name="editprofile"),
     path('editpropic/',views.editpropic,name="editpropic"),
     path('changepassword/',views.changepassword,name="changepassword"),
     path('new_market/',views.new_market,name="new_market"),
     path('approvemarket/<int:apid>',views.approvemarket,name="approvemarket"),
     path('rejectmarket/<int:rjid>',views.rejectmarket,name="rejectmarket"),
     path('accepted_market/',views.accepted_market,name="accepted_market"),
     path('rejected_market/',views.rejected_market,name="rejected_market"),
     path('new_farmer/',views.new_farmer,name="new_farmer"),
     path('approvefarmer/<int:apid>',views.approvefarmer,name="approvefarmer"),
     path('rejectfarmer/<int:rjid>',views.rejectfarmer,name="rejectfarmer"),
     path('accepted_farmer/',views.accepted_farmer,name="accepted_farmer"),
     path('rejected_farmer/',views.rejected_farmer,name="rejected_farmer"),
     path('complaint/',views.complaint,name="complaint"),
     path('feedback/',views.feedback,name="feedback"),   
     path('viewcomplaints/',views.viewcomplaints,name="viewcomplaints"),  
     path('sendreply/<int:comid>',views.sendreply,name="sendreply"),
     path('replyedcom/',views.replyedcom,name="replyedcom"),
     path('reply/',views.reply,name="reply"),
     path('logout/',views.logout,name="logout"),
     path('marketreport/',views.marketreport,name="marketreport"),
     path('farmerreport/',views.farmerreport,name="farmerreport"),
     path('customerreport/',views.customerreport,name="customerreport"),
    
] 