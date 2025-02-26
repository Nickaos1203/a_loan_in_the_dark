from django.urls import path
from news.views import get_all_news, news_detail, create_news

urlpatterns = [
    path("", get_all_news, name="all_news"),
    path("add/", create_news, name="create_news"),
    path("<int:id>/", news_detail, name="news_detail")
]