from django.urls import path

from apps.translate.views import Translate

urlpatterns = [
    path('translate/', Translate.as_view(), name='translate')
]
