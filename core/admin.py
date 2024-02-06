from django.contrib import admin
from .models import Transaction, CreditCard

# Register your models here.
@admin.register(Transaction)
class TransactionModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'status', 'transaction_type', 'sender', 'reciver']
    list_editable = ['amount', 'status', 'transaction_type', 'sender', 'reciver']

@admin.register(CreditCard)
class CreditCardModelAdmin(admin.ModelAdmin):
    list_display = ["user", 'amount', 'card_type']
    list_editable = ['amount', 'card_type']
