from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from account.models import Account

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