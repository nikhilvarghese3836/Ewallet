from django.db import models
import uuid

# Create your models here.
from django.contrib.auth.base_user import AbstractBaseUser


class Wallet(AbstractBaseUser, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    owned_by = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=10, default='disabled')
    enabled_at = models.DateTimeField(blank=True, null=True,)
    disabled_at = models.DateTimeField(blank=True, null=True,)
    balance = models.FloatField(default=0.0)

    USERNAME_FIELD = 'owned_by'

    def serialize(self):
        return_data = {
            'id': self.id,
            'owned_by': self.owned_by,
            'status': self.status,
            'balance': self.balance
        }
        if self.status == 'enabled':
            return_data['enabled_at'] = self.enabled_at
        else:
            return_data['disabled_at'] = self.disabled_at
        return return_data
