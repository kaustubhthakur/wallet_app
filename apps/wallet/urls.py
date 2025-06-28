from django.urls import path
from . import views

urlpatterns = [
    path('enable/', views.enable_wallet, name='enable_wallet'),
    path('balance/', views.get_balance, name='get_balance'),
    path('update-balance/', views.update_balance, name='update_balance'),
]