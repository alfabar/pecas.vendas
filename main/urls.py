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
    path('cart',views.cart_list,name='cart'),
    path('delete-from-cart',views.delete_cart_item,name='delete-from-cart'),
    path('update-cart',views.update_cart_item,name='update-cart'),
    path('accounts/signup',views.signup,name='signup'),
    path('checkout',views.checkout,name='checkout'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-done/', views.payment_done, name='payment_done'), 
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    path('save-review/<int:pid>',views.save_review, name='save-review'),
    # User Section Start
    path('my-dashboard',views.my_dashboard, name='my_dashboard'),
    path('my-orders',views.my_orders, name='my_orders'),
    path('my-orders-items/<int:id>',views.my_order_items, name='my_order_items'),
    # End

    # lista_desejo
    path('add-lista-desejo',views.minha_lista_desejo, name='minha_lista_desejo'),
    path('minha_lista_desejo',views.minha_lista_desejo, name='minha_lista_desejo'),
    # My Reviews
    path('my-reviews',views.my_reviews, name='my-reviews'),
    # My AddressBook
    path('minha_lista_endereco',views.minha_lista_endereco, name='minha_lista_endereco'),
    path('add-address',views.save_address, name='add-address'),
    path('activate-address',views.activate_address, name='activate-address'),
    path('update-address/<int:id>',views.update_address, name='update-address'),
    path('edit-profile',views.edit_profile, name='edit-profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    