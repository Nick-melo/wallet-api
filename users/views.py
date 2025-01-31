from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from wallets.models import Wallet
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Criação de Usuário
@api_view(['POST'])
@permission_classes([AllowAny])  # Permite criar usuários sem autenticação
def create_user(request):
    """Cria um novo usuário, uma carteira associada e gera um token JWT"""
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        # Cria o usuário
        user = serializer.save()

        # Verifica se o usuário já tem uma carteira associada
        if not Wallet.objects.filter(user=user).exists():
            # Cria a carteira associada ao usuário
            Wallet.objects.create(user=user)

        # Gera o token JWT para o novo usuário
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Retorna a resposta com os dados do usuário e o token
        return Response({
            'message': 'User and wallet created successfully!',
            'user': serializer.data,
            'access_token': access_token
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login (Obter Tokens)
class LoginView(TokenObtainPairView):
    """Gera um token JWT para autenticação do usuário"""
    pass

# Refresh Token
class RefreshTokenView(TokenRefreshView):
    """Gera um novo token de acesso usando um refresh token"""
    pass

# Logout (Invalidar Tokens)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Faz logout do usuário e invalida seu token"""
    try:
        refresh_token = request.data.get("refresh_token")
        token = OutstandingToken.objects.get(token=refresh_token)
        BlacklistedToken.objects.create(token=token)
        return Response({"message": "Successfully logged out."}, status=200)
    except Exception as e:
        return Response({"error": "Invalid token."}, status=400)

# Consultar Informações do Usuário Autenticado
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    """Retorna as informações do usuário autenticado"""
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

# Consultar Usuário por ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, user_id):
    """Consulta os dados de um usuário específico"""
    try:
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({"error": "Usuário não encontrado"}, status=status.HTTP_404_NOT_FOUND)

# Atualizar Usuário
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    """Atualiza os dados de um usuário específico"""
    try:
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"error": "Usuário não encontrado"}, status=status.HTTP_404_NOT_FOUND)

# Excluir Usuário
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    """Exclui um usuário específico"""
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({"error": "Usuário não encontrado"}, status=status.HTTP_404_NOT_FOUND)