import calendar
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import Banner, Promocao, Categoria, Marca, Produto, ProdutoAtributo, CarrinhoPedido, CarrinhoPedidoItems, ProdutoFeedback, ListaDesejo, UserEnderecoLista
from django.db.models import Max, Min, Count, Avg
from django.db.models.functions import ExtractMonth
from django.template.loader import render_to_string
from .forms import SignupForm, ReviewAdd, FormListaEndereco, ProfileForm, EntrarFormulario
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.decorators import login_required
from pycep_correios import get_address_from_cep, WebService, exceptions
from selenium import webdriver
# paypal
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm

# Home Page


def home(request):
    banners = Banner.objects.all().order_by('-id')
    data = Produto.objects.filter(e_apresentado=True).order_by('-id')
    promocaos = Promocao.objects.all().order_by('-id')
    data1 = Produto.objects.filter(e_apresentado=True).order_by('-id')
    return render(request, 'index.html', {'data': data, 'banners': banners, 'data1': data1, 'promocaos': promocaos})

# Categoria


def lista_categoria(request):
    data = Categoria.objects.all().order_by('-id')
    return render(request, 'lista_categoria.html', {'data': data})

# Marca


def lista_marca(request):
    data = Marca.objects.all().order_by('-id')
    return render(request, 'lista_marca.html', {'data': data})

# Lista de Produtos


def lista_produto(request):
    total_data = Produto.objects.count()
    data = Produto.objects.all().order_by('-id')[:3]
    min_preco = ProdutoAtributo.objects.aggregate(Min('preco'))
    max_preco = ProdutoAtributo.objects.aggregate(Max('preco'))
    return render(request, 'lista-produto.html', {'data': data, 'total_data': total_data, 'min_preco': min_preco, 'max_preco': max_preco, })

# Lista de produtos de acordo com a categoria


def lista_produto_categoria(request, cat_id):
    categoria = Categoria.objects.get(id=cat_id)
    data = Produto.objects.filter(categoria=categoria).order_by('-id')
    return render(request, 'lista-produto-categoria.html', {'data': data, })

# Lista de produtos de acordo com a marca


def lista_produto_marca(request, marca_id):
    marca = Marca.objects.get(id=marca_id)
    data = Produto.objects.filter(marca=marca).order_by('-id')
    return render(request, 'lista-produto-categoria.html', {'data': data,})


@login_required
# Detalhe do produto
def detalhe_produto(request, slug, id):
    produto = Produto.objects.get(id=id)
    produtos_relacionado = Produto.objects.filter(categoria=produto.categoria).exclude(id=id)[:4]
    cores = ProdutoAtributo.objects.filter(produto=produto).values('cor__id', 'cor__titulo', 'cor__cor_code').distinct()
    tamanhos = ProdutoAtributo.objects.filter(produto=produto).values('tamanho__id', 'tamanho__titulo', 'preco', 'cor__id').distinct()
    reviewForm = ReviewAdd()

    # Verificar
    canAdd = True
    reviewCheck = ProdutoFeedback.objects.filter(
        user=request.user, produto=produto).count()
    if request.user.is_authenticated:
        if reviewCheck > 0:
            canAdd = False
    # End

    # Buscar avaliações
    reviews = ProdutoFeedback.objects.filter(produto=produto)
    # End

    # Buscar classificação avg para avaliações
    avg_reviews = ProdutoFeedback.objects.filter(
        produto=produto).aggregate(avg_rating=Avg('review_rating'))
    # End

    return render(request, 'detalhes-produtos.html', {'data': produto, 'related': produtos_relacionado, 'cores': cores, 'tamanhos': tamanhos, 'reviewForm': reviewForm, 'canAdd': canAdd, 'reviews': reviews, 'avg_reviews': avg_reviews})

# Procurar


def search(request):
    q = request.GET['q']
    data = Produto.objects.filter(titulo__icontains=q).order_by('-id')
    return render(request, 'procurar.html', {'data': data})

# Dados do filtro


def filtro_dados(request):
    cores = request.GET.getlist('cor[]')
    categorias = request.GET.getlist('categoria[]')
    marcas = request.GET.getlist('marca[]')
    tamanhos = request.GET.getlist('tamanho[]')
    precoMin = request.GET['precoMin']
    precoMax = request.GET['precoMax']
    todosProdutos = Produto.objects.all().order_by('-id').distinct()
    todosProdutos = todosProdutos.filter(ProdutoAtributo__preco__gte=precoMin)
    todosProdutos = todosProdutos.filter(ProdutoAtributo__preco__lte=precoMax)
    if len(cores) > 0:
        todosProdutos = todosProdutos.filter(
            ProdutoAtributo__cor__id__in=cores).distinct()
    if len(categorias) > 0:
        todosProdutos = todosProdutos.filter(
            categoria__id__in=categorias).distinct()
    if len(marcas) > 0:
        todosProdutos = todosProdutos.filter(marca__id__in=marcas).distinct()
    if len(tamanhos) > 0:
        todosProdutos = todosProdutos.filter(
            ProdutoAtributo__tamanho__id__in=tamanhos).distinct()
    t = render_to_string('ajax/lista-produtos.html', {'data': todosProdutos})
    return JsonResponse({'data': t})

# Carregar mais


def carregar_mais_dados(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    data = Produto.objects.all().order_by('-id')[offset:offset+limit]
    t = render_to_string('ajax/lista-produtos.html', {'data': data})
    return JsonResponse({'data':t})

# Adicione ao carrinho


def carrinho_add(request):
    carrinho_p = {}
    carrinho_p[str(request.GET['id'])] = {
        'imagem': request.GET['imagem'],
        'titulo': request.GET['titulo'],
        'qty': request.GET['qty'],
        'preco': request.GET['preco'],
    }
    if 'cartdata' in request.session:
        if str(request.GET['id']) in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = int(
                carrinho_p[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cartdata'] = cart_data
        else:
            cart_data = request.session['cartdata']
            cart_data.update(carrinho_p)
            request.session['cartdata'] = cart_data
    else:
        request.session['cartdata'] = carrinho_p
    return JsonResponse({'data': request.session['cartdata'], 'totalitems': len(request.session['cartdata'])})

# Página da lista de carrinhos


def lista_carrinho(request):
    pedido_total = 0
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            pedido_total += int(item['qty'])*float(item['preco'])
        return render(request, 'carrinho.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'pedido_total': pedido_total})
    else:
        return render(request, 'carrinho.html', {'cart_data': '', 'totalitems': 0, 'pedido_total': pedido_total})


# Excluir item do carrinho
def deletar_carrinho_item(request):
    p_id = str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata'] = cart_data
    pedido_total = 0
    for p_id, item in request.session['cartdata'].items():
        pedido_total += int(item['qty'])*float(item['price'])
    t = render_to_string('ajax/lista-carrinho.html', {'cart_data': request.session['cartdata'], 'totalitems': len(
        request.session['cartdata']), 'pedido_total': pedido_total})
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})

# Excluir item do carrinho


def atualizar_item_carrinho(request):
    p_id = str(request.GET['id'])
    p_qty = request.GET['qty']
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = p_qty
            request.session['cartdata'] = cart_data
    pedido_total = 0
    for p_id, item in request.session['cartdata'].items():
        pedido_total += int(item['qty'])*float(item['preco'])
    t = render_to_string('ajax/lista-carrinho.html', {'cart_data': request.session['cartdata'], 'totalitems': len(
        request.session['cartdata']), 'pedido_total': pedido_total})
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})

# Formulário de inscrição

#entrar se inscreva
def inscrever_se(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=pwd)
            login(request, user)
            return redirect('home')
    form = SignupForm
    return render(request, 'registration/registrar.html', {'form': form})


#entrar logar formulario de login
def entrar_login(request):
   
    form = EntrarFormulario
    return render(request, 'registration/login.html', {'form': form})

# Caixa
@login_required
def checkout(request):
    pedido_total = 0
    totalPedido = 0
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            totalPedido += int(item['qty'])*float(item['preco'])
        # Ordem
        pedido = CarrinhoPedido.objects.create(
            user=request.user,
            pedido_total=totalPedido
        )
        # Fim
        for p_id, item in request.session['cartdata'].items():
            pedido_total += int(item['qty'])*float(item['preco'])
            # Itens de pedidos
            items = CarrinhoPedidoItems.objects.create(
                pedido=pedido,
                fatura_no='PEDIDO Nº-'+str(pedido.id),
                item=item['titulo'],
                imagem=item['imagem'],
                qty=item['qty'],
                preco=item['preco'],
                total=float(item['qty'])*float(item['preco'])
            )
            # End
        # Pagamento de processos
        host = request.get_host()
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': pedido_total,
            'item_name': 'OrderNo-'+str(pedido.id),
            'invoice': 'PEDIDO Nº-'+str(pedido.id),
            'currency_code': 'BRL',
            'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(host, reverse('pagaento-efetuado')),
            'cancel_return': 'http://{}{}'.format(host, reverse('pagamento-cancelado')),
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        endereco = UserEnderecoLista.objects.filter(
            user=request.user, status=True).first()
        return render(request, 'checkout.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'pedido_total': pedido_total, 'form': form, 'endereco': endereco})


@csrf_exempt
def pagaento_efetuado(request):
    returnData = request.POST
    return render(request, 'pagamento-sucesso.html', {'data': returnData})


@csrf_exempt
def pagamento_cancelado(request):
    return render(request, 'pagamento-falhou.html')


# Salvar revisão
def salvar_avaliacao(request, pid):
    produto = Produto.objects.get(pk=pid)
    user = request.user
    review = ProdutoFeedback.objects.create(
        user=user,
        produto=produto,
        review_text=request.POST['review_text'],
        review_rating=request.POST['review_rating'],
    )
    data = {
        'user': user.username,
        'review_text': request.POST['review_text'],
        'review_rating': request.POST['review_rating']
    }

    # Buscar classificação avg para avaliações
    avg_reviews = ProdutoFeedback.objects.filter(
        produto=produto).aggregate(avg_rating=Avg('review_rating'))
    # End

    return JsonResponse({'bool': True, 'data': data, 'avg_reviews': avg_reviews})


# Painel do usuário


def meu_painel(request):
    orders = CarrinhoPedido.objects.annotate(month=ExtractMonth('pedido_dt')).values(
        'month').annotate(count=Count('id')).values('month', 'count')
    monthNumber = []
    totalOrders = []
    for d in orders:
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['count'])
    return render(request, 'user/painel.html', {'monthNumber': monthNumber, 'totalOrders': totalOrders})

# Minhas Ordens


def meus_pedidos(request):
    orders = CarrinhoPedido.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/pedidos.html', {'orders': orders})

# Detalhe do pedido


def meus_pedidos_items(request, id):
    order = CarrinhoPedido.objects.get(pk=id)
    orderitems = CarrinhoPedidoItems.objects.filter(
        order=order).order_by('-id')
    return render(request, 'user/pedido-items.html', {'orderitems': orderitems})

# Lista de desejos


def add_lista_desejo(request):
    pid = request.GET['produto']
    produto = Produto.objects.get(pk=pid)
    data = {}
    checkw = ListaDesejo.objects.filter(
        produto=produto, user=request.user).count()
    if checkw > 0:
        data = {
            'bool': False
        }
    else:
        lista_desejo = ListaDesejo.objects.create(
            produto=produto,
            user=request.user
        )
        data = {
            'bool': True
        }
    return JsonResponse(data)

# Minha lista de desejos


def minha_lista_desejo(request):
    wlist = ListaDesejo.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/lista_desejo.html', {'wlist': wlist})

# Minhas Avaliações


def meus_comentarios(request):
    reviews = ProdutoFeedback.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/avaliacao.html', {'reviews': reviews})

# Meu livro de endereços


def minha_lista_endereco(request):
    addEndereco = UserEnderecoLista.objects.filter(
        user=request.user).order_by('-id')
    return render(request, 'user/enderecolivro.html', {'addEndereco': addEndereco})


def salvar_endereco(request):
    msg = None
    if request.method == 'POST':
       form = FormListaEndereco(request.POST)
       cep = request.POST.get('cep')
       resulta_cep = get_address_from_cep(cep, webservice=WebService.VIACEP)
       endereco = request.POST.get('endereco')
       print(UserEnderecoLista)
       if form.is_valid():
           saveForm = form.save(commit=False)
           saveForm.user = request.user
           if 'status' in request.POST:
                UserEnderecoLista.objects.update(status=False)
                saveForm.save()
                msg = 'Os dados foram salvos'
    form = FormListaEndereco
    return render(request, 'user/add-endereco.html', {'form': form, 'msg': msg})


# Ativar endereço
def ativar_endereco(request):
    a_id = str(request.GET['id'])
    UserEnderecoLista.objects.update(status=False)
    UserEnderecoLista.objects.filter(id=a_id).update(status=True)
    return JsonResponse({'bool': True})

# Editar perfil


def editar_perfil(request):
    msg = None
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            msg = 'Os dados foram salvos'
    form = ProfileForm(instance=request.user)
    return render(request, 'user/editar-perfil.html', {'form': form, 'msg': msg})

# Atualizar endereços


def atualizar_endereco(request, id):
    endereco = UserEnderecoLista.objects.get(pk=id)
    msg = None
    if request.method == 'POST':
        form = FormListaEndereco(request.POST, instance=endereco)
        if form.is_valid():
            saveForm = form.save(commit=False)
            saveForm.user = request.user
            if 'status' in request.POST:
                UserEnderecoLista.objects.update(status=False)
            saveForm.save()
            msg = 'Os dados foram salvos'
    form = FormListaEndereco(instance=endereco)
    return render(request, 'user/atualizar-endereco.html', {'form': form,'msg': msg})

def sair_site(request):
    logout(request)
    return render(request, 'index.html')