from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Account, KYC
from .forms import KYCForms
from core.forms import CreditCardForms
from core.models import CreditCard, Transaction
from django.db.models import Q


# Create your views here.

@login_required
def account(request):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your kyc")
            return redirect("account:account")  
        account = Account.objects.get(user=request.user)

    else:
            messages.warning(request, "You need to login to access the dashboard")
            return redirect("userauth:signin")
    
    context = {
        'kyc':kyc,
        'account':account
    }  
    return render(request, 'account/account.html', context)


@login_required
def KycRegistration(request):
    user = request.user
    account = Account.objects.get(user=user)

    try:
        kyc = KYC.objects.get(user=user)
    except:
        kyc= None

    if request.method == "POST":
        form = KYCForms(request.POST,request.FILES, instance=kyc)
        if form.is_valid():
            kyc_form = form.save(commit=False)
            kyc_form.user = user
            kyc_form.account = account 
            kyc_form.save()
            messages.success(request, "KYC Form submitted successfully, In review now")            
            return redirect("account:kyc-reg")
    else:
        form=KYCForms(instance=kyc)

    context = {
        "account":account,
        "form":form,
        "kyc": kyc
    }

    return render(request, "account/kyc_form.html", context)


def dashboard(request):
    # form = CreditCardForms()
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your kyc")
            return redirect("account:kyc-reg")
        account = Account.objects.get(user=request.user)
        credit_card = CreditCard.objects.filter(user= request.user).order_by('-id')

        if request.method == "POST":
            form = CreditCardForms(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.save()

                card_id = new_form.card_id
                messages.success(request, "Card Sucessfully added")
                return redirect("account:dashboard")

        else:
            form = CreditCardForms()
        transaction_context = latest_transactions(request)
    else:
        messages.warning(request, 'You have to login first')
        return redirect("userauth:signin")    
    
    context = {
        "kyc":kyc,
        "account":account,
        "form":form,
        'credit_card':credit_card
    }
    
    context.update(transaction_context)

    return render(request, "account/dashboard.html", context)



def latest_transactions(request):
    sender_transaction = Transaction.objects.filter(sender=request.user, transaction_type="transfer").order_by('-id').prefetch_related("user", "sender")
    reciver_transaction = Transaction.objects.filter(reciver=request.user, transaction_type="transfer").order_by('-id').prefetch_related("user", "reciver")


    # sender_request_transaction = Transaction.objects.filter(sender=request.user, transaction_type="request").order_by('-id').prefetch_related("user", "sender")
    # reciver_request_transaction = Transaction.objects.filter(reciver=request.user, transaction_type="request").order_by('-id').prefetch_related("user", "reciver")


    context = {
        "sender_transaction":sender_transaction,
        "reciver_transaction":reciver_transaction,
        
    }
    return context

def deposit(request):
    kyc = KYC.objects.get(user=request.user)
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.filter(user= request.user).order_by('-id')

    
    context = {
        "kyc":kyc,
        "account":account,
        'credit_card':credit_card
    }
    return render(request, "account/deposit_money.html",context)


def withdraw(request):
    credit_card = CreditCard.objects.filter(user= request.user).order_by('-id')

    
    context = {
        'credit_card':credit_card
    }
    return render(request, "transaction/withdraw.html", context)