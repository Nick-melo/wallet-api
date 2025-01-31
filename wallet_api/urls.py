from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  


# Função simples de resposta para a raiz
def home(request):
    return HttpResponse("Bem-vindo à API! Use '/api/' para acessar as funcionalidades.")

urlpatterns = [
    path('', home, name='home'),  # Página inicial
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),  
    path('api/', include('wallets.urls')),
    path('api/', include('transactions.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('users.urls')),

]
