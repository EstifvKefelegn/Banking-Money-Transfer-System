from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import Account
from .models import Transaction

@login_required
def searchUserRequest(request):
    account = Account.objects.all()
    query =  request.POST.get('account_number')

    if query:
        account = account.get(
            Q(account_number = query)|
            Q(account_id = query)
        )
    context = {
        "account":account,
        "query":query
    }

    return render(request, 'payment-request/searchuserrequest.html', context)    


def amountRequest(request, accountNumber):
    account = Account.objects.get(account_number = accountNumber)
    
    context = {
        "account":account
    }

    return render(request, "payment-request/paymentrequest.html", context)


def amountRequestProcess(request, accountNumber):
    account = Account.objects.get(account_number = accountNumber)
    sender = request.user
    reciver = account.user

    sender_account = request.user.account
    reciver_account = account

    if request.method == "POST":
        amount = request.POST.get("amount-send")
        description = request.POST.get('description')

        new_request = Transaction.objects.create(
            user = request.user,
            amount = amount,
            description = description,
            reciver = reciver,
            sender = sender,
            sender_account = sender_account,
            reciver_account = reciver_account,
            status = "request_processing",
            transaction_type = "request"
        )

        new_request.save()
        transaction_id = new_request.transaction_id
        return  redirect("core:requestconfirmation", accountNumber, transaction_id)
    else:
        messages.warning(request, "Error occured try agin later")
        return redirect("account:dashboard")
    
def requestConfirmation(request, accountNumber, transaction_id):
    account = Account.objects.get(account_number=accountNumber)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    context = {
        "account":account,
        "transaction":transaction
    }   

    return render(request, "payment-request/request_confirmation.html", context)

def amoutnRequestFinalProcess(request, accountNumber, transaction_id):
    account = Account.objects.get(account_number=accountNumber)
    transaction = Transaction.objects.get(transaction_id=transaction_id)


    if request.method ==  "POST":
        pin_number = request.POST.get('pin_number')
        if pin_number == request.user.account.pin_number:
            transaction.status = "request_sent"
            print(transaction.status)
            transaction.save()
            messages.success(request, "You sent a request successfully")    
            return redirect("core:requestcompleted", account.account_number, transaction.transaction_id)

        else:
            messages.warning(request, "Error occured")
            return redirect('account:dashboard')
        
def requestComplted(request, accountNumber, transaction_id):
    account = Account.objects.get(account_number=accountNumber)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    context = {
        "account":account,
        "transaction":transaction
    }   

    return render(request, "payment-request/request_completed.html", context)        


def settlement_confirmation(request, accountNumber, transaction_id):
    account = Account.objects.get(account_number=accountNumber)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    context = {
        "account": account,
        'transaction':transaction
    }
    return render(request, 'payment-request/settlement_confirmation.html', context)


def settlement_processing(request, accountNumber, transaction_id):
    account = Account.objects.get(account_number=accountNumber)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    sender = request.user
    sender_account = request.user.account

    if request.method == "POST":
        pin_number = request.POST.get('pin_number')
        if pin_number == sender_account.pin_number:
            if sender_account.account_balance < transaction.amount:
               messages.warning(request, "Insufficient balance")
            else: 
                sender_account.account_balance -= transaction.amount
                sender_account.save()

                account.account_balance += transaction.amount
                account.save()
                
                transaction.status = "request_settled"
                transaction.save() 

                messages.success(request, "The rqeuest accepted successfuly")  
                return redirect("account:dashboard")
        else:
            messages.warning(request, "Incorrect Pin") 
            return redirect("core:settlementconfirmation", account.account_number, transaction.transaction_id)       
    else:
            print("The post requets is not excuting")

            messages.warning(request, "Error Occured") 
            return redirect("core:settlementconfirmation", account.account_number, transaction.transaction_id)

def settlement_completed(request, accountNumber, transaction_id):
    account = Account.objects.get(account_number=accountNumber)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    context ={
        "account":account,
        'transaction':transaction
    }    

    return render(request, "payment-request/settlement_completed.html", context)

def request_delete(request, accountNumber, transaction_id):
    transaction = Transaction.objects.get(transaction_id=transaction_id)    
    # if request.user == transaction.user:
    transaction.delete()
    messages.success(request, "Successfully deleted")
    return redirect("core:transaction-list")

    