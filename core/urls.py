from django.urls import path
from . import views
from . import transfer
from . import transaction


app_name = "core"

urlpatterns = [
    path('', views.index, name="index"),
    path('searchuser/', transfer.search_user_with_account_number, name="search-user"),
    path('amount-transfer/<accountNumber>/', transfer.AmonutTransfer, name="transfer"),
    path('amount-transfer-process/<account_number>/', transfer.AmountTransferProcess, name="transferprocess"),
    path('transfer-confirmation/<accountnumber>/<transaction_id>/', transfer.Transaction_confirmation, name="transferconfirmation"),
    path('transfer-completion-process/<accountnumber>/<transaction_id>/', transfer.transfer_process, name="transfer-process"),
    path("transfer-completed/<accountnumber>/<transaction_id>/", transfer.transfer_completed, name='transfer-completed'),
    path('transaction-list/', transaction.transaction_list, name="transaction-list"),
    path('transaction-detail/<transaction_id>/', transaction.transaction_detail, name="transaction-detail")
]
