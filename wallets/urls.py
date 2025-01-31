from django.urls import path
from wallets.views import get_balance, deposit, transfer, list_transactions
from users.views import create_user


urlpatterns = [
    path('users/', create_user, name='create-user'),
    path('wallets/<int:user_id>/balance/', get_balance, name='get-balance'),
    path('wallets/<int:user_id>/deposit/', deposit, name='deposit'),
    path('wallets/transfer/', transfer, name='transfer'),
    path('wallets/<int:user_id>/transactions/', list_transactions, name='list-transactions'),
]
