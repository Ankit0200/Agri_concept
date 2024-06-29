from django.urls import path,include
from . import views
urlpatterns = [
    path("", views.home_page, name="publish_home"),
    path("published_news/", views.published_news, name="news_list")
]
