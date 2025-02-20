from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', UserProfileView.as_view(), name="user-profile"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("api/users/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
