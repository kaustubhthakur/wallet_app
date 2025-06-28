from django.db import models
from django.utils import timezone
from apps.wallet.models import Wallet

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]
    
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'transaction'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.transaction_type.title()} - {self.amount} - {self.wallet.user.email}"