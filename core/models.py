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
    ("processing", "processing"),
    ("request_sent", "request sent"),
    ("request_processing", "request processing"),
    ("request_settled", "request settled")

)

CARD_TYPE = (
    ('master', 'master'),
    ('visa', 'visa'),
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
        

class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_id = ShortUUIDField(unique=True, length=5, max_length=20, prefix="CARD", alphabet="1234567890")

    name = models.CharField(max_length=100)
    number = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    cvv = models.IntegerField()

    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    card_type = models.CharField(choices=CARD_TYPE, max_length=20, default="master")
    card_status = models.BooleanField(default=True)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}" 
   



 