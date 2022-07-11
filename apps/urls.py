from django.urls import path, include

urlpatterns = [
    path('search/', include('apps.search.urls')),
    path('news/', include('apps.news.urls')),
]
