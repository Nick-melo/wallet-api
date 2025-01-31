from rest_framework import serializers
from django.contrib.auth.models import User
from wallets.models import Wallet, Transaction

class UserSerializer(serializers.ModelSerializer):
    """Serializer para o modelo User"""
    
    password = serializers.CharField(write_only=True)  # Esconde a senha na resposta

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        """Criação do usuário com senha hash"""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        Wallet.objects.create(user=user)  # Criar carteira automaticamente
        return user

class WalletSerializer(serializers.ModelSerializer):
    """Serializer para a carteira digital"""
    
    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance']
        read_only_fields = ['id', 'user', 'balance']

class TransactionSerializer(serializers.ModelSerializer):
    """Serializer para as transações"""
    
    sender = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Transaction
        fields = ['id', 'sender', 'receiver', 'amount', 'date']
        read_only_fields = ['id', 'date']
