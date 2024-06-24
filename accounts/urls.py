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
    path('approved/suspend/<int:id>', views.suspend_officials,name='suspend'),
    path('approved/remove/<int:id>', views.remove_officials, name='remove'),
    path('login/', views.login_view, name='login')
]

