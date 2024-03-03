from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import CreditCard
from account.models import Account
from decimal import Decimal


def card_detail(request, card_id):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(user=request.user, card_id=card_id)

    context = {
        "account":account,
        "credit_card":credit_card
    }

    return render(request, "payment-request/credit_card.html", context)

def fund_credit_card(request, card_id):
    account = request.user.account
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)

    if request.method == "POST":
        amount = request.POST.get('funding_amount')

        if Decimal(amount) <= account.account_balance:
             account.account_balance += Decimal(amount)
             account.save()

             credit_card.amount += Decimal(amount)
             credit_card.save()
             messages.success(request, "Funcing Sucessfully")
             return redirect("core:creditcarddetail", credit_card.card_id)
    
        else:
             messages.success(request, "Insufficient balance")
             return redirect("core:creditcarddetail", credit_card.card_id)
    

def withdraw_fund(request, card_id):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    
    if request.method =="POST":
        amount = request.POST.get("withdarwal_amount")
        
        if Decimal(amount) <= credit_card.amount:
            account.account_balance += Decimal(amount)
            account.save()
            
            credit_card.amount -= Decimal(amount)
            credit_card.save()
            messages.success(request, "refund succesfully transfered")  
            return redirect("core:creditcarddetail", credit_card.card_id )
        else:
            messages.success(request, "Insufficient credit amount")  
            return redirect("core:creditcarddetail", credit_card.card_id )


def delete_card(request, card_id):
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    credit_card.delete()
    messages.success(request, "Card succesfuly deleted")
    return redirect("account:dashboard")
