"""Configuração de URL da lojaPecas

A lista `urlpatterns` encaminha URLs para visualizações. Para mais informações consulte:
     https://docs.djangoproject.com/en/3.1/topics/http/urls/
Exemplos:
Visualizações de funções
     1. Adicione uma importação: das visualizações de importação my_app
     2. Adicione um URL a urlpatterns: path('', views.home, name='home')
Visualizações baseadas em classe
     1. Adicione uma importação: from other_app.views import Home
     2. Adicione um URL a urlpatterns: path('', Home.as_view(), name='home')
Incluindo outro URLconf
     1. Importe a função include(): from django.urls import include, path
     2. Adicione um URL a urlpatterns: path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('jet/', include('jet.urls')),
    path('jet/dashboard/', include('jet.dashboard.urls','jet-dashboard')),
    path('admin/', admin.site.urls),
    path('',include('main.urls')),
    #contato
    path('contato/',include('contato.urls')),
    #contas-login
    path('contas/',include('django.contrib.auth.urls')),
    path('accounts/',include('django.contrib.auth.urls')),

]
