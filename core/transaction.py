from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction
from account.models import Account
from django.contrib import messages



def transaction_list(request):
    sender_transaction = Transaction.objects.filter(sender=request.user, transaction_type="transfer").order_by('-id')
    reciver_transaction = Transaction.objects.filter(reciver=request.user, transaction_type="transfer").order_by('-id')


    sender_request_transaction = Transaction.objects.filter(sender=request.user, transaction_type="request").order_by('-id')
    reciver_request_transaction = Transaction.objects.filter(reciver=request.user, transaction_type="request").order_by('-id')


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
