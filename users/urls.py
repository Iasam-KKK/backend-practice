from django.urls import path
from .views import CreateUserView, LoginView, UpdateUserView, CurrentUserView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('users/', CreateUserView.as_view(), name='create-user'),
    path('users/update/', UpdateUserView.as_view(), name='update-user'),
    path('users/current/', CurrentUserView.as_view(), name='current-user'),
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('login/', LoginView.as_view(), name='login'),
]