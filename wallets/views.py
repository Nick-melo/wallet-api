from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from wallets.models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer
from django.contrib.auth.models import User
from decimal import Decimal

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_balance(request, user_id):
    """Consulta saldo do usuário"""
    if request.user.id != user_id:
        return Response({"error": "Não autorizado"}, status=403)

    try:
        wallet = Wallet.objects.get(user_id=user_id)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)
    except Wallet.DoesNotExist:
        return Response({"error": "Carteira não encontrada"}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit(request, user_id):
    """Adiciona saldo à carteira do usuário"""
    if request.user.id != user_id:
        return Response({"error": "Não autorizado"}, status=403)

    amount = request.data.get("amount")

    if amount is None or amount <= 0:
        return Response({"error": "Valor inválido"}, status=400)
   
   # Converte o valor para Decimal
    amount = Decimal(str(amount))

    wallet, _ = Wallet.objects.get_or_create(user_id=user_id)
    wallet.balance += amount
    wallet.save()

    return Response({"message": "Depósito realizado", "new_balance": wallet.balance}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer(request):
    """Realiza transferência entre usuários"""
    sender = request.user
    receiver_id = request.data.get("receiver_id")
    amount = request.data.get("amount")

    if not receiver_id or amount is None or amount <= 0:
        return Response({"error": "Dados inválidos"}, status=400)

    try:
        amount = Decimal(str(amount))

        receiver = User.objects.get(id=receiver_id)
        sender_wallet = Wallet.objects.get(user=sender)
        receiver_wallet = Wallet.objects.get(user=receiver)

        if sender_wallet.balance < amount:
            return Response({"error": "Saldo insuficiente"}, status=400)

        sender_wallet.balance -= amount
        receiver_wallet.balance += amount
        sender_wallet.save()
        receiver_wallet.save()

        transaction = Transaction.objects.create(sender=sender, receiver=receiver, amount=amount)
        serializer = TransactionSerializer(transaction)

        return Response(serializer.data, status=201)
    except User.DoesNotExist:
        return Response({"error": "Usuário destinatário não encontrado"}, status=404)
    except Wallet.DoesNotExist:
        return Response({"error": "Carteira não encontrada"}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_transactions(request, user_id):
    """Lista as transações do usuário"""
    if request.user.id != user_id:
        return Response({"error": "Não autorizado"}, status=403)

    transactions = Transaction.objects.filter(sender_id=user_id) | Transaction.objects.filter(receiver_id=user_id)
    serializer = TransactionSerializer(transactions, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Apenas usuários autenticados podem acessar
def get_wallet(request):
    """Retorna os dados da carteira do usuário autenticado"""
    try:
        wallet = Wallet.objects.get(user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)
    except Wallet.DoesNotExist:
        return Response({"error": "Wallet not found"}, status=404)
