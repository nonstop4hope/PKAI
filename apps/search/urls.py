from django.urls import path

from apps.search import views

urlpatterns = [
    path('search', views.get_zenodo_records, name='zenodo_search'),
    path('status', views.get_celery_result_by_id),
    path('result', views.get_result),
]
