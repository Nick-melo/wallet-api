from rest_framework import serializers
from .models import Wallet, Transaction
from django.contrib.auth.models import User

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance']
        read_only_fields = ['id', 'user', 'balance']  # O saldo será atualizado automaticamente

class TransactionSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Transaction
        fields = ['id', 'sender', 'receiver', 'amount', 'date']
        read_only_fields = ['id', 'date']
