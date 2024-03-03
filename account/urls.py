from django.urls import path
from . import views


app_name = "account"


urlpatterns = [
    path("", views.account, name="account"),
    path("kyc-reg/", views.KycRegistration, name="kyc-reg"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('deposit/', views.deposit, name="deposit"),
    path('withdraw/', views.withdraw, name="withdraw")
]

