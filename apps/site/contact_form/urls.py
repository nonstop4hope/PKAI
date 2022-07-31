from django.urls import path

from apps.site.contact_form.views import FeedBackView

urlpatterns = [
    path('send/', FeedBackView.as_view(), name='send feedback'),
]
