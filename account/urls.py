from django.urls import path
from . import views

app_name = 'account'


urlpatterns = [
    path("registration", views.register, name="register"),
    path("home",views.home, name="Home"),
    path("logout",views.logout,name="logout"),
    path("",views.home, name= "home"),

    # path('password_reset/', views.password_reset_request, name='password_reset'),
    # path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    # path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
    #
    # path('reset-password/', views.send_password_reset_email, name='send_password_reset_email'),
    # path('reset-password/<str:uidb64>/<str:token>/', views.reset_password, name='reset_password'),
    #
    # # path('password_reset/', views.password_reset_request_cus, name='password_resetmmm')
    #
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:uidb64>/<str:token>/', views.reset_password, name='reset-password'),


    # path('reset-password/<str:uidb64>/<str:token>/', views.ResetPasswordView.as_view(), name='reset_password'),






]



