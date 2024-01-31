from django.urls import path
from . import views
from . import transfer
app_name = "core"

urlpatterns = [
    path('', views.index, name="index"),
    path('transfer/', transfer.search_user_with_account_number, name="transfer")
]
