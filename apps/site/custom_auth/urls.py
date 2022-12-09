from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# from .views import MyObtainTokenPairView, RegisterView, user_login, user_logout, user_is_login
# from rest_framework_simplejwt.views import TokenRefreshView
#
#
from apps.site.custom_auth.views import RegisterView

urlpatterns = [
    # path('login/', user_login, name='login'),
    # path('logout/', user_logout, name='logout'),
    # path('is-login/', user_is_login, name='is_login'),
    # # path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    # path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name="sign_up"),
]
