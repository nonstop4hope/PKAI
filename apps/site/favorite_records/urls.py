from django.urls import path

from . import views

urlpatterns = [
    path('add', views.AddRecordToFavorites.as_view()),
    path('list', views.ListFavoriteRecords.as_view()),
    path('delete', views.DeleteFavoriteRecord.as_view()),
]
