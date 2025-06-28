from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/wallet/', include('apps.wallet.urls')),
    path('api/transactions/', include('apps.transactions.urls')),
]
