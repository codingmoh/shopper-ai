from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Shopper AI Administration"
admin.site.site_title = "Shopper AI Administration"


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("orders.urls")),
]


