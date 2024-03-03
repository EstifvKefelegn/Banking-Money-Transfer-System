from django.urls import path
from . import views
from . import transfer
from . import transaction
from . import payment_requst
from . import credit_card

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
    path('transaction-detail/<transaction_id>/', transaction.transaction_detail, name="transaction-detail"),
    path('searchuserrequest/', payment_requst.searchUserRequest, name="searchuserrequest"),
    path("payment-request/<accountNumber>/", payment_requst.amountRequest, name="paymentrequest"),
    path('amount-request-process/<accountNumber>/', payment_requst.amountRequestProcess, name='amountrequestprocess'),
    path('request_confirmation/<accountNumber>/<transaction_id>/', payment_requst.requestConfirmation, name="requestconfirmation"),
    path('request_final_confirmation/<accountNumber>/<transaction_id>/', payment_requst.amoutnRequestFinalProcess, name="requestfinalconfirmation"),
    path('request-completed/<accountNumber>/<transaction_id>/', payment_requst.requestComplted, name='requestcompleted'),
    path('settlement_confirmation/<accountNumber>/<transaction_id>/', payment_requst.settlement_confirmation, name="settlementconfirmation"),
    path('settlementprocessing/<accountNumber>/<transaction_id>/', payment_requst.settlement_processing, name="settlementprocessing"),
    path('settlement-completed/<accountNumber>/<transaction_id>/', payment_requst.settlement_completed, name="settlementcompletd"),
    path('delete-request/<accountNumber>/<transaction_id>/', payment_requst.request_delete, name="requestdelete"),
    path('card/<card_id>/', credit_card.card_detail, name="creditcarddetail"),
    path('fundingcard/<card_id>/', credit_card.fund_credit_card, name="fundcreditcard"),
    path('withdrawfund/<card_id>/', credit_card.withdraw_fund, name="withdrawfund"),
    path("delete-credit-card/<card_id>/", credit_card.delete_card, name="deletecreditcard"),
    path('recipients/', transaction.recipient_list, name="recipients")

]

