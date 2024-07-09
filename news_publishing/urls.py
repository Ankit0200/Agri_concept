from django.urls import path, include
from . import views



urlpatterns = [
    path("", views.home_page, name="publish_home"),
    path("published_news/", views.published_news, name="news_list"),
    path("approve_news/<int:id>", views.notice_approve, name="notice_approve"),
    path('personal_news/<int:id>', views.personal_news, name='personal_news'),
    path('blogs/', views.blogs_view, name='blogs'),
    path(
        'gallery/', views.gallery_view, name='gallery'
    ),
    path('recent_news/', views.recent_news_page, name='recent_news')

]

