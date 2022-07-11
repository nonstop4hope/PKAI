from django.urls import path, include

urlpatterns = [
    path('search/', include('apps.search.urls')),
    path('news/', include('apps.site.news.urls')),
    path('auth/', include('apps.site.custom_auth.urls')),
]
