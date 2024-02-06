from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import CreditCard
from account.models import Account

def card_detail(request, card_id):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(user=request.user, card_id=card_id)

    context = {
        "account":account,
        "credit_card":credit_card
    }

    return render(request, "payment-request/credit_card.html", context)