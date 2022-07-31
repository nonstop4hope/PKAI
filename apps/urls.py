from django.urls import path, include

urlpatterns = [
    path('search/', include('apps.search.urls')),
    path('news/', include('apps.site.news.urls')),
    path('auth/', include('apps.site.custom_auth.urls')),
    path('favorite_records/', include('apps.site.favorite_records.urls')),
    path('feedback/', include('apps.site.contact_form.urls')),
]
