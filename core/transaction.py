from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction
from account.models import Account
from django.contrib import messages
from django.core.paginator import Paginator




def transaction_list(request):
    sender_transaction = Transaction.objects.filter(sender=request.user, transaction_type="transfer").order_by('-id')
    reciver_transaction = Transaction.objects.filter(reciver=request.user, transaction_type="transfer").order_by('-id')


    sender_request_transaction = Transaction.objects.filter(sender=request.user, transaction_type="request").order_by('-id')
    reciver_request_transaction = Transaction.objects.filter(reciver=request.user, transaction_type="request").order_by('-id')

    # transactions = [sender_transaction, reciver_transaction, sender_request_transaction, reciver_request_transaction]
    # paginated_transactions = []

    # paginator = Paginator(sender_transaction, 4)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    context = {
        "sender_transaction":sender_transaction,
        "reciver_transaction":reciver_transaction,
        'sender_request_transaction': sender_request_transaction,
        "reciver_request_transaction":reciver_request_transaction
    }


    return render(request, "transaction/transaction-list.html", context)
    
def transaction_detail(request, transaction_id):
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    context = {
        'transaction':transaction
    }    

    return render(request, 'transaction/transaction-detail.html', context)

def recipient_list(request):
    reciver_transaction = Transaction.objects.filter(reciver=request.user, transaction_type="transfer").order_by('-id')

    reciver_request_transaction = Transaction.objects.filter(reciver=request.user, transaction_type="request").order_by('-id')

    context = {
        "reciver_transaction":reciver_transaction,
        "reciver_request_transaction":reciver_request_transaction
    }


    return render(request, "transaction/recipients.html", context)


def check_notification(request):
    reciver_transaction = Transaction.objects.filter(reciver=request.user, transaction_type="transfer").order_by('-id')
    reciver_request_transaction = Transaction.objects.filter(reciver=request.user, transaction_type="request").order_by('-id')

  
    context = {
        "reciver_transaction":reciver_transaction,

        "reciver_request_transaction":reciver_request_transaction
    }

    return render(request, "partials/dashboard-base.html", context) 