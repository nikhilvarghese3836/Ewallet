from django.db import models
import uuid

from wallet.models import Wallet

# Create your models here.
from django.utils.timezone import now


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    transaction_by = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    transaction_at = models.DateTimeField(blank=True, null=True, default=now)
    transaction_type = models.CharField(max_length=10)
    amount = models.FloatField(default=0.0)
    reference_id = models.CharField(max_length=50, unique=True)

    def serialize(self,):
        return_data = {
            'id': self.id,
            'amount': self.amount,
            'reference_id': self.reference_id,
            'status': "success"
        }
        if self.transaction_type == 'deposit':
            return_data.update(
                {'deposited_by': self.transaction_by.id, 'deposited_at': self.transaction_at})
        else:
            return_data.update(
                {'withdrawn_by': self.transaction_by.id, 'withdrawn_at': self.transaction_at})
        return return_data
