from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.create_transaction, name='create_transaction'),
    path('transactions/history/', views.transaction_history, name='transaction_history'),
]
