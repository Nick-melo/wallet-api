from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from wallets.models import Transaction, Wallet
from .serializers import TransactionSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_transaction(request):
    """
    Cria uma transação entre usuários autenticados.
    - O usuário autenticado será sempre o remetente (`sender`).
    - O valor não pode ser maior que o saldo do remetente.
    """
    sender = request.user
    receiver_id = request.data.get("receiver")
    amount = request.data.get("amount")

    if not receiver_id or not amount:
        return Response({"error": "Receiver and amount are required"}, status=400)

    try:
        receiver = Wallet.objects.get(user_id=receiver_id).user
    except Wallet.DoesNotExist:
        return Response({"error": "Receiver not found"}, status=404)

    if sender == receiver:
        return Response({"error": "You cannot send money to yourself"}, status=400)

    sender_wallet = Wallet.objects.get(user=sender)
    receiver_wallet = Wallet.objects.get(user=receiver)

    if sender_wallet.balance < float(amount):
        return Response({"error": "Insufficient balance"}, status=400)

    # Realizando a transação de forma atômica
    with transaction.atomic():
        sender_wallet.balance -= float(amount)
        receiver_wallet.balance += float(amount)
        sender_wallet.save()
        receiver_wallet.save()

        trans = Transaction.objects.create(sender=sender, receiver=receiver, amount=amount)
        serializer = TransactionSerializer(trans)
        
    return Response(serializer.data, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Garantir que o usuário esteja autenticado
def transaction_history(request):
    """Retorna o histórico de transações do usuário autenticado."""
    user = request.user  # Acessa o usuário autenticado
    transactions = Transaction.objects.filter(sender=user) | Transaction.objects.filter(receiver=user)
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)
