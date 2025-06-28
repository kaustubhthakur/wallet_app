from rest_framework import serializers
from decimal import Decimal
from .models import Wallet

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('id', 'balance', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class WalletBalanceUpdateSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = serializers.ChoiceField(choices=['credit', 'debit'])
    description = serializers.CharField(max_length=255, required=False)
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive")
        return value
    
    def validate(self, attrs):
        wallet = self.context['wallet']
        if attrs['transaction_type'] == 'debit' and not wallet.can_debit(attrs['amount']):
            raise serializers.ValidationError("Insufficient balance")
        return attrs

class WalletEnableSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()