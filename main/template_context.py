from .models import Produto,ProdutoAtributo
from django.db.models import Min,Max
def get_filters(request):
	cats=Produto.objects.distinct().values('categoria__title','categoria__id')
	marcas=Produto.objects.distinct().values('marca__titulo','marca__id')
	colors=ProdutoAtributo.objects.distinct().values('color__title','color__id','color__color_code')
	sizes=ProdutoAtributo.objects.distinct().values('size__title','size__id')
	minMaxPrice=ProdutoAtributo.objects.aggregate(Min('price'),Max('price'))
	data={
		'cats':cats,
		'marcas':marcas,
		'colors':colors,
		'sizes':sizes,
		'minMaxPrice':minMaxPrice,
	}
	return data