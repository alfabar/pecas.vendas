from django.urls import path,include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[ 
    path('',views.home,name='home'),
    path('search',views.search,name='search'),
    path('lista-categoria',views.lista_categoria,name='lista-categoria'),
    path('lista-marca',views.lista_marca,name='lista-marca'),
    path('lista-produtos',views.lista_produto,name='lista-produtos'),
    path('lista-produto-categoria/<int:cat_id>',views.lista_produto_categoria,name='lista-produto-categoria'),
    path('lista-produto-marca/<int:brand_id>',views.lista_produto_marca,name='lista-produto-marca'),
    path('produto/<str:slug>/<int:id>',views.detalhe_produto,name='detalhe_produto'),
    path('filtro-dados',views.filtro_dados,name='filtro_dados'),
    path('carregar-mais-dados',views.carregar_mais_dados,name='carregar_mais_dados'),
    path('adicionar-carrinho',views.carrinho_add,name='carrinho_add'),
    path('carrinho',views.lista_carrinho,name='carrinho'),
    path('deletar-item-carrinho',views.deletar_carrinho_item,name='deletar-item-carrinho'),
    path('atualizar-carrinho',views.atualizar_item_carrinho,name='atualizar-carrinho'),
    path('contas/inscricao',views.inscrever_se,name='inscrever-se'),
    path('checkout',views.checkout,name='checkout'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('pagaento-efetuado/', views.pagaento_efetuado, name='pagaento-efetuado'), 
    path('pagamento-cancelado/', views.pagamento_cancelado, name='pagamento-cancelado'),
    path('salvar-avaliacao/<int:pid>',views.salvar_avaliacao, name='salvar-avaliacao'),
    # Inicio Seção Usuario
    path('meu-painel',views.meu_painel, name='meu-painel'),
    path('my-orders',views.my_orders, name='my_orders'),
    path('my-orders-items/<int:id>',views.my_order_items, name='my_order_items'),
    # End

    # lista_desejo
    path('add-lista-desejo',views.minha_lista_desejo, name='minha_lista_desejo'),
    path('minha_lista_desejo',views.minha_lista_desejo, name='minha_lista_desejo'),
    # My Reviews
    path('my-reviews',views.my_reviews, name='my-reviews'),
    # My enderecoBook
    path('minha_lista_endereco',views.minha_lista_endereco, name='minha_lista_endereco'),
    path('adicionar-endereco',views.salvar_endereco, name='adicionar-endereco'),
    path('ativar-endereco',views.ativar_endereco, name='ativar-endereco'),
    path('atualizar-endereco/<int:id>',views.atualizar_endereco, name='atualizar-endereco'),
    path('editar-perfil',views.edit_profile, name='editar-perfil'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    