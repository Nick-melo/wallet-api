from django.urls import path
from .views import (
    create_user,  # Criação de usuário
    LoginView,    # Login (obter tokens)
    RefreshTokenView,  # Refresh token
    logout,       # Logout
    get_user,     # Consultar usuário por ID
    update_user,  # Atualizar usuário
    delete_user,  # Excluir usuário
    get_user_info  # Consultar informações do usuário autenticado
)

urlpatterns = [
    # Criação de usuário
    path('users/', create_user, name='create-user'),

    # Autenticação
    path('login/', LoginView.as_view(), name='token_obtain_pair'),  # Login
    path('refresh/', RefreshTokenView.as_view(), name='token_refresh'),  # Refresh token
    path('logout/', logout, name='logout'),  # Logout

    # Consultar informações do usuário autenticado
    path('users/me/', get_user_info, name='get-user-info'),

    # CRUD de usuários
    path('users/<int:user_id>/', get_user, name='get-user'),  # Consultar usuário por ID
    path('users/<int:user_id>/update/', update_user, name='update-user'),  # Atualizar usuário
    path('users/<int:user_id>/delete/', delete_user, name='delete-user'),  # Excluir usuário
]