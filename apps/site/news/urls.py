from django.urls import path

from . import views

urlpatterns = [
    path('list', views.NewsListApi.as_view()),
    path('get/<int:news_id>', views.NewsOneApi.as_view()),
    path('create', views.NewsCreateApi.as_view()),
    path('update/<int:pk>', views.NewsUpdateApi.as_view()),
    path('delete/<int:pk>', views.NewsDeleteApi.as_view()),
]
