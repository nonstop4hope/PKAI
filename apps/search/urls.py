from django.urls import path

from apps.search import views

urlpatterns = [
    path('zenodo', views.get_zenodo_records, name='zenodo_search'),
    path('result', views.get_celery_result_by_id),
]
