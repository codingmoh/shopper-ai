from django.urls import path
from .views import buy


urlpatterns = [
    path("buy/", buy, name="buy"),
]



