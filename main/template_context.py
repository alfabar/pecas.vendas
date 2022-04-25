from .models import Produto,ProdutoAtributo
from django.db.models import Min,Max
def get_filters(request):
	cats=Produto.objects.distinct().values('categoria__title','categoria__id')
	brands=Produto.objects.distinct().values('brand__title','brand__id')
	colors=ProdutoAtributo.objects.distinct().values('color__title','color__id','color__color_code')
	sizes=ProdutoAtributo.objects.distinct().values('size__title','size__id')
	minMaxPrice=ProdutoAtributo.objects.aggregate(Min('price'),Max('price'))
	data={
		'cats':cats,
		'brands':brands,
		'colors':colors,
		'sizes':sizes,
		'minMaxPrice':minMaxPrice,
	}
	return data