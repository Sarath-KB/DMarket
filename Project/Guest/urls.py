from django.urls import path,include
from Guest import views
app_name="webguest"
urlpatterns = [
    path('Login/',views.login,name="login"),
    path('Cus_reg/',views.cus_reg,name="cusreg"),
    path('ajaxlocplace/',views.ajaxlocplace,name="ajaxlocplace"),
    path('farmer_reg/',views.freg,name="freg"),
    path('marketreg/',views.marketreg,name="marketreg"),
    path('adminlogin/',views.adminlogin,name="adminlogin"),
    path('',views.index,name="index"),
    path('about/',views.about,name="about"),
    path('service/',views.service,name="service"),
    path('contact/',views.contact,name="contact"),
    path('fpass/', views.ForgetPassword,name="forpass"),
    path('otpver/', views.OtpVerification,name="verification"),
    path('create/', views.CreateNewPass,name="create"),
    path('ajaxemail/', views.ajaxemail,name="ajaxemail"),
 
]