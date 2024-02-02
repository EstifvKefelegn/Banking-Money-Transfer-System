from django.db import models
from userauth.models import User
from account.models import Account
from shortuuid.django_fields import ShortUUIDField

# Create your models here.


TRANSACTION_TYPE = (
    ('transfer', 'transfer'),
    ('recived', 'recived'),
    ('withdraw', 'withdraw'),
    ('refund', 'refund'),
    ('request', 'request'),
    ('none', 'none')
)


TRANSACTION_STATUS = (
    ("failed", "failed"),
    ("complete", "complete"),
    ('pending', 'pending'),
    ("processing", "processing")
)


class Transaction(models.Model):
    transaction_id = ShortUUIDField(unique=True, length=15, max_length=20, prefix="TRN")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    description = models.TextField(max_length=1000, default="No Reason")

    reciver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reviver")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")

    sender_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="sender_account")
    reciver_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="reciver_account")
    
    status = models.CharField(choices=TRANSACTION_STATUS, max_length=100, default="pending")
    transaction_type = models.CharField(choices=TRANSACTION_TYPE, max_length=100, default="none")
    
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self) -> str:
        try:
            return f"{self.user}"
        except:
            return f"Transaction"