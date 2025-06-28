from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal

User = get_user_model()

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'wallet'
        
    def __str__(self):
        return f"{self.user.email} - Balance: {self.balance}"
    
    def can_debit(self, amount):
        \"\"\"Check if wallet has sufficient balance for debit\"\"\"
        return self.balance >= amount
    
    def credit(self, amount):
        \"\"\"Credit amount to wallet\"\"\"
        self.balance += amount
        self.save(update_fields=['balance', 'updated_at'])
    
    def debit(self, amount):
        \"\"\"Debit amount from wallet\"\"\"
        if not self.can_debit(amount):
            raise ValueError("Insufficient balance")
        self.balance -= amount
        self.save(update_fields=['balance', 'updated_at'])