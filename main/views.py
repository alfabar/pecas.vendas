from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from .models import Banner,Promocao,Categoria,Marca,Produto,ProdutoAtributo,CarrinhoPedido,CarrinhoPedidoItems,ProdutoFeedback,ListaDesejo,UserEnderecoLista
from django.db.models import Max,Min,Count,Avg
from django.db.models.functions import ExtractMonth
from django.template.loader import render_to_string
from .forms import SignupForm,ReviewAdd,FormListaEndereco,ProfileForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
#paypal
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm

# Home Page
def home(request):
	banners=Banner.objects.all().order_by('-id')
	data=Produto.objects.filter(is_featured=True).order_by('-id')
	promocaos=Promocao.objects.all().order_by('-id')
	data1=Produto.objects.filter(is_featured=True).order_by('-id')
	return render(request,'index.html',{'data':data,'banners':banners,'data1':data1,'promocaos':promocaos})

# Categoria
def lista_categoria(request):
    data=Categoria.objects.all().order_by('-id')
    return render(request,'category_list.html',{'data':data})

# Marca
def lista_marca(request):
    data=Marca.objects.all().order_by('-id')
    return render(request,'brand_list.html',{'data':data})

# Lista de Produtos
def lista_produto(request):
	total_data=Produto.objects.count()
	data=Produto.objects.all().order_by('-id')[:3]
	min_price=ProdutoAtributo.objects.aggregate(Min('price'))
	max_price=ProdutoAtributo.objects.aggregate(Max('price')) 
	return render(request,'product_list.html',{'data':data,'total_data':total_data,'min_price':min_price,'max_price':max_price,})

# Lista de produtos de acordo com a categoria
def lista_produto_categoria(request,cat_id):
	categoria=Categoria.objects.get(id=cat_id)
	data=Produto.objects.filter(categoria=categoria).order_by('-id')
	return render(request,'category_product_list.html',{'data':data,})

# Lista de produtos de acordo com a marca
def lista_produto_marca(request,brand_id):
	brand=Marca.objects.get(id=brand_id)
	data=Produto.objects.filter(brand=brand).order_by('-id')
	return render(request,'category_product_list.html',{
			'data':data,
			})
@login_required
# Detalhe do produto
def detalhe_produto(request,slug,id):
	product=Produto.objects.get(id=id)
	related_products=Produto.objects.filter(categoria=product.categoria).exclude(id=id)[:4]
	colors=ProdutoAtributo.objects.filter(product=product).values('color__id','color__title','color__color_code').distinct()
	sizes=ProdutoAtributo.objects.filter(product=product).values('size__id','size__title','price','color__id').distinct()
	reviewForm=ReviewAdd()

	# Verificar
	canAdd=True
	reviewCheck=ProdutoFeedback.objects.filter(user=request.user,product=product).count()
	if request.user.is_authenticated:
		if reviewCheck > 0:
			canAdd=False
	# End

	# Buscar avaliações
	reviews=ProdutoFeedback.objects.filter(product=product)
	# End

	# Buscar classificação avg para avaliações
	avg_reviews=ProdutoFeedback.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
	# End

	return render(request, 'product_detail.html',{'data':product,'related':related_products,'colors':colors,'sizes':sizes,'reviewForm':reviewForm,'canAdd':canAdd,'reviews':reviews,'avg_reviews':avg_reviews})

# Procurar
def search(request):
	q=request.GET['q']
	data=Produto.objects.filter(title__icontains=q).order_by('-id')
	return render(request,'search.html',{'data':data})

# Dados do filtro
def filtro_dados(request):
	colors=request.GET.getlist('color[]')
	categories=request.GET.getlist('categoria[]')
	brands=request.GET.getlist('brand[]')
	sizes=request.GET.getlist('size[]')
	minPrice=request.GET['minPrice']
	maxPrice=request.GET['maxPrice']
	allProducts=Produto.objects.all().order_by('-id').distinct()
	allProducts=allProducts.filter(ProdutoAtributo__price__gte=minPrice)
	allProducts=allProducts.filter(ProdutoAtributo__price__lte=maxPrice)
	if len(colors)>0:
		allProducts=allProducts.filter(ProdutoAtributo__color__id__in=colors).distinct()
	if len(categories)>0:
		allProducts=allProducts.filter(categoria__id__in=categories).distinct()
	if len(brands)>0:
		allProducts=allProducts.filter(brand__id__in=brands).distinct()
	if len(sizes)>0:
		allProducts=allProducts.filter(ProdutoAtributo__size__id__in=sizes).distinct()
	t=render_to_string('ajax/product-list.html',{'data':allProducts})
	return JsonResponse({'data':t})

# Carregar mais
def carregar_mais_dados(request):
	offset=int(request.GET['offset'])
	limit=int(request.GET['limit'])
	data=Produto.objects.all().order_by('-id')[offset:offset+limit]
	t=render_to_string('ajax/product-list.html',{'data':data})
	return JsonResponse({'data':t}
)

# Adicione ao carrinho
def carrinho_add(request):
	# del request.session['cartdata']
	cart_p={}
	cart_p[str(request.GET['id'])]={
		'image':request.GET['image'],
		'title':request.GET['title'],
		'qty':request.GET['qty'],
		'price':request.GET['price'],
	}
	if 'cartdata' in request.session:
		if str(request.GET['id']) in request.session['cartdata']:
			cart_data=request.session['cartdata']
			cart_data[str(request.GET['id'])]['qty']=int(cart_p[str(request.GET['id'])]['qty'])
			cart_data.update(cart_data)
			request.session['cartdata']=cart_data
		else:
			cart_data=request.session['cartdata']
			cart_data.update(cart_p)
			request.session['cartdata']=cart_data
	else:
		request.session['cartdata']=cart_p
	return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})

# Página da lista de carrinhos

def cart_list(request):
	total_amt=0
	if 'cartdata' in request.session:
		for p_id,item in request.session['cartdata'].items():
			total_amt+=int(item['qty'])*float(item['price'])
		return render(request, 'cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	else:
		return render(request, 'cart.html',{'cart_data':'','totalitems':0,'total_amt':total_amt})


# Excluir item do carrinho
def delete_cart_item(request):
	p_id=str(request.GET['id'])
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			del request.session['cartdata'][p_id]
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		total_amt+=int(item['qty'])*float(item['price'])
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

# Excluir item do carrinho
def update_cart_item(request):
	p_id=str(request.GET['id'])
	p_qty=request.GET['qty']
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			cart_data[str(request.GET['id'])]['qty']=p_qty
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		total_amt+=int(item['qty'])*float(item['price'])
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

# Formulário de inscrição
def signup(request):
	if request.method=='POST':
		form=SignupForm(request.POST)
		if form.is_valid():
			form.save()
			username=form.cleaned_data.get('username')
			pwd=form.cleaned_data.get('password1')
			user=authenticate(username=username,password=pwd)
			login(request, user)
			return redirect('home')
	form=SignupForm
	return render(request, 'registration/signup.html',{'form':form})


# Caixa
@login_required
def checkout(request):
	total_amt=0
	totalAmt=0
	if 'cartdata' in request.session:
		for p_id,item in request.session['cartdata'].items():
			totalAmt+=int(item['qty'])*float(item['price'])
		# Ordem
		order=CarrinhoPedido.objects.create(
				user=request.user,
				total_amt=totalAmt
			)
		# Fim
		for p_id,item in request.session['cartdata'].items():
			total_amt+=int(item['qty'])*float(item['price'])
			# Itens de pedidos
			items=CarrinhoPedidoItems.objects.create(
				order=order,
				invoice_no='INV-'+str(order.id),
				item=item['title'],
				image=item['image'],
				qty=item['qty'],
				price=item['price'],
				total=float(item['qty'])*float(item['price'])
				)
			# End
		# Pagamento de processos
		host = request.get_host()
		paypal_dict = {
		    'business': settings.PAYPAL_RECEIVER_EMAIL,
		    'amount': total_amt,
		    'item_name': 'OrderNo-'+str(order.id),
		    'invoice': 'INV-'+str(order.id),
		    'currency_code': 'BRL',
		    'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
		    'return_url': 'http://{}{}'.format(host,reverse('payment_done')),
		    'cancel_return': 'http://{}{}'.format(host,reverse('payment_cancelled')),
		}
		form = PayPalPaymentsForm(initial=paypal_dict)
		endereco=UserEnderecoLista.objects.filter(user=request.user,status=True).first()
		return render(request, 'checkout.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt,'form':form,'endereco':endereco})

@csrf_exempt
def payment_done(request):
	returnData=request.POST
	return render(request, 'payment-success.html',{'data':returnData})


@csrf_exempt
def payment_canceled(request):
	return render(request, 'payment-fail.html')


# Salvar revisão
def save_review(request,pid):
	product=Produto.objects.get(pk=pid)
	user=request.user
	review=ProdutoFeedback.objects.create(
		user=user,
		product=product,
		review_text=request.POST['review_text'],
		review_rating=request.POST['review_rating'],
		)
	data={
		'user':user.username,
		'review_text':request.POST['review_text'],
		'review_rating':request.POST['review_rating']
	}

	# Buscar classificação avg para avaliações
	avg_reviews=ProdutoFeedback.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
	# End

	return JsonResponse({'bool':True,'data':data,'avg_reviews':avg_reviews})

# Painel do usuário
import calendar
def my_dashboard(request):
	orders=CarrinhoPedido.objects.annotate(month=ExtractMonth('order_dt')).values('month').annotate(count=Count('id')).values('month','count')
	monthNumber=[]
	totalOrders=[]
	for d in orders:
		monthNumber.append(calendar.month_name[d['month']])
		totalOrders.append(d['count'])
	return render(request, 'user/dashboard.html',{'monthNumber':monthNumber,'totalOrders':totalOrders})

# Minhas Ordens
def my_orders(request):
	orders=CarrinhoPedido.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/orders.html',{'orders':orders})

# Detalhe do pedido
def my_order_items(request,id):
	order=CarrinhoPedido.objects.get(pk=id)
	orderitems=CarrinhoPedidoItems.objects.filter(order=order).order_by('-id')
	return render(request, 'user/order-items.html',{'orderitems':orderitems})

# Lista de desejos
def add_lista_desejo(request):
	pid=request.GET['product']
	product=Produto.objects.get(pk=pid)
	data={}
	checkw=ListaDesejo.objects.filter(product=product,user=request.user).count()
	if checkw > 0:
		data={
			'bool':False
		}
	else:
		lista_desejo=ListaDesejo.objects.create(
			product=product,
			user=request.user
		)
		data={
			'bool':True
		}
	return JsonResponse(data)

# Minha lista de desejos
def minha_lista_desejo(request):
	wlist=ListaDesejo.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/lista_desejo.html',{'wlist':wlist})

# Minhas Avaliações
def my_reviews(request):
	reviews=ProdutoFeedback.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/reviews.html',{'reviews':reviews})

# Meu livro de endereços
def minha_lista_endereco(request):
	addbook=UserEnderecoLista.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/enderecobook.html',{'addbook':addbook})

# Salvar o catálogo de endereços
def salvar_endereco(request):
	msg=None
	if request.method=='POST':
		form=FormListaEndereco(request.POST)
		if form.is_valid():
			saveForm=form.save(commit=False)
			saveForm.user=request.user
			if 'status' in request.POST:
				UserEnderecoLista.objects.update(status=False)
			saveForm.save()
			msg='Os dados foram salvos'
	form=FormListaEndereco
	return render(request, 'user/add-endereco.html',{'form':form,'msg':msg})

# Ativar endereço
def ativar_endereco(request):
	a_id=str(request.GET['id'])
	UserEnderecoLista.objects.update(status=False)
	UserEnderecoLista.objects.filter(id=a_id).update(status=True)
	return JsonResponse({'bool':True})

# Editar perfil
def edit_profile(request):
	msg=None
	if request.method=='POST':
		form=ProfileForm(request.POST,instance=request.user)
		if form.is_valid():
			form.save()
			msg='Os dados foram salvos'
	form=ProfileForm(instance=request.user)
	return render(request, 'user/edit-profile.html',{'form':form,'msg':msg})

# Atualizar endereços
def atualizar_endereco(request,id):
	endereco=UserEnderecoLista.objects.get(pk=id)
	msg=None
	if request.method=='POST':
		form=FormListaEndereco(request.POST,instance=endereco)
		if form.is_valid():
			saveForm=form.save(commit=False)
			saveForm.user=request.user
			if 'status' in request.POST:
				UserEnderecoLista.objects.update(status=False)
			saveForm.save()
			msg='Os dados foram salvos'
	form=FormListaEndereco(instance=endereco)
	return render(request, 'user/update-endereco.html',{'form':form,'msg':msg})