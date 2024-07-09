from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_page, name='index'),
    path('farmer_signup/', views.farmer_signup, name='farmer_signup'),
    path('officer_signup/', views.officer_signup, name='officer_signup'),
    path("check-requests/",views.check_requests,name='check-requests'),
    path("qualify/<int:id>", views.qualify_requests, name='qualify'),
    path('reject/<int:id>', views.reject_request,name='reject'),
    path('approved/', views.approved_officials, name='approved'),
    path('approved/suspend/', views.suspend_officials,name='suspend'),
    path('approved/remove/', views.remove_officials, name='remove'),
    path('login/', views.login_view, name='login'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('otp_enter/', views.otp_enter, name='otp_enter'),
    path('reset_password/', views.reset_password, name='reset_password_name'),
    path('homepage/',views.after_official_login,name='homepage_after_official_login'),
    path(

        'contact/',views.contact_view,name='contact_view'
    ),
    path('leaderboard/', views.leaderboard_view, name='leaderboard_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('services/', views.services_view, name='services_view'),
    path('admin_page/', views.admin_page, name='admin_page')



]

