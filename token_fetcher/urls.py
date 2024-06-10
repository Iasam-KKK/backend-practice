# token_fetcher/urls.py
from django.urls import path
from .views import TokenView

urlpatterns = [
    path('api/tokens/', TokenView.as_view(), name='tokens-list'),
    path('api/tokens/<str:symbol>/', TokenView.as_view(), name='token-detail'),
]