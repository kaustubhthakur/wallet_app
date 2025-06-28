from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='wallet.user.email', read_only=True)
    
    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'transaction_type', 'description', 'created_at', 'user_email')
        read_only_fields = ('id', 'created_at', 'user_email')