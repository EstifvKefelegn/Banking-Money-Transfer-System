from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from account.models import Account
from .models import Transaction

@login_required
def search_user_with_account_number(request):
    account = Account.objects.all()
    query = request.POST.get("account_number")

    if query:
        account = account.filter(
            Q(account_number = query) |
            Q(account_id=query)
        ).distinct()

    
    context = {
        "account":account,
        "query":query
    }

    return render(request, 'transfer/search-by-account.html', context)


def AmonutTransfer(request, accountNumber):
    try:
        account = Account.objects.get(account_number=accountNumber)
    except:
        messages.warning(request, "Account Doesnot Exist")
        return redirect("core:search-user")
    context = {
        "account":account,
    }

    return render(request, 'transfer/transfer_amout.html', context)


def AmountTransferProcess(request, account_number):
    account = Account.objects.get(account_number=account_number)
    
    sender = request.user
    reciver = account.user

    sender_account = request.user.account
    reciver_account = account

    if request.method == "POST":
        ammount = request.POST.get('amount-send')
        description = request.POST.get('description')
        
        
        if sender_account.account_balance >  Decimal(ammount):  
            new_transaction = Transaction.objects.create(
                user= request.user,
                amount = ammount,
                description = description,
                reciver = reciver,
                sender = sender,
                sender_account = sender_account,
                reciver_account = reciver_account,
                status = "processing",
                transaction_type = "transfer"
            )
            new_transaction.save()

            transaction_id = new_transaction.transaction_id
            return redirect("core:transferconfirmation", account.account_number, transaction_id)
        else:
            messages.warning(request, "Insuficient Balance")
            return redirect("account:account")
    else:
        messages.warning(request, "Error occured try again latter")    
        return redirect("account:account")
    

def Transaction_confirmation(request, accountnumber, transaction_id):
    print("Account Number:", accountnumber)
    print("Transaction ID:", transaction_id)


    try:
        account = Account.objects.get(account_number=accountnumber)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request, "Transaction does not exist")
        return redirect("account:account")
    context = {
        "account":account,
        "transaction": transaction
    }

    return render(request, "transfer/transfer-confirmation.html", context)


def transfer_process(request, accountnumber, transaction_id):
    account = Account.objects.get(account_number=accountnumber)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    sender = request.user
    reciver = account.user

    sender_account = request.user.account
    reciver_account = account

    complete = False

    if request.method == "POST":
        pin_number = request.POST.get('pin_number')
        # print(pin_number)
        
        if pin_number == sender_account.pin_number:
            transaction.status = "complete"
            transaction.save()

            sender_account.account_balance -= transaction.amount
            sender_account.save()

            reciver_account.account_balance += transaction.amount
            reciver_account.save()
            messages.success(request, "Transfer succesful")   
            return redirect("core:transfer-completed", account.account_number, transaction_id)
        else:
            messages.warning(request, "Incorrect PIN")
            return redirect("core:transfer-process")   
    else:
        messages.warning(request, "an error occured try again later")
        return redirect("core:transfer-process")       

    return render(request, "transfer/transfer-confirmation.html")

def transfer_completed(request, accountnumber, transaction_id):
    try:
        account = Account.objects.get(account_number=accountnumber)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request, "Transaction does not exist")
        return redirect("account:account")
    context = {
        "account":account,
        "transaction": transaction
    }

    return render(request, 'transfer/transfer-completed.html', context)



def transaction_detail(request, transaction_id):
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    context = {
        "transaction":transaction
    }
    return render(request, "transfer/transaction-list.html")


