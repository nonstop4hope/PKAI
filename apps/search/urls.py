from django.urls import path

from apps.search import views

urlpatterns = [
    path('search', views.GeneralizedSearch.as_view()),
    path('get', views.OneHit.as_view()),
    path('get-file', views.GetFile.as_view()),
]
