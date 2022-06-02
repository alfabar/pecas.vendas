from .models import Produto,ProdutoAtributo
from django.db.models import Min,Max
def get_filters(request):
	cats=Produto.objects.distinct().values('categoria__titulo','categoria__id')
	marcas=Produto.objects.distinct().values('marca__titulo','marca__id')
	cor=ProdutoAtributo.objects.distinct().values('cor__titulo','cor__id','cor__cor_code')
	tamanho=ProdutoAtributo.objects.distinct().values('tamanho__titulo','tamanho__id')
	minMaxPreco=ProdutoAtributo.objects.aggregate(Min('preco'),Max('preco'))
	data={
		'cats':cats,
		'marcas':marcas,
		'cor':cor,
		'tamanho':tamanho,
		'minMaxPreco':minMaxPreco,
	}
	return data