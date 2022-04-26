from django.contrib import admin
from .models import Banner,Promocao,Categoria,Marca,Color,Size,Produto,ProdutoAtributo,CarrinhoPedido,CarrinhoPedidoItems,ProdutoFeedback,ListaDesejo,UserEnderecoLista

# admin.site.register(Banner)
admin.site.register(Marca)
admin.site.register(Size)


class BannerAdmin(admin.ModelAdmin):
	list_display=('alt_text','image_tag')
admin.site.register(Banner,BannerAdmin)

class PromocaoAdmin(admin.ModelAdmin):
    list_display=('alt_text','image_tag')	
admin.site.register(Promocao,PromocaoAdmin)

class CategoriaAdmin(admin.ModelAdmin):
	list_display=('title','image_tag')
admin.site.register(Categoria,CategoriaAdmin)

class ColorAdmin(admin.ModelAdmin):
	list_display=('title','color_bg')
admin.site.register(Color,ColorAdmin)

class ProdutoAdmin(admin.ModelAdmin):
    list_display=('id','titulo','image','categoria','brand','status','is_featured')
    list_editable=('status','is_featured')
admin.site.register(Produto,ProdutoAdmin)

# Product Attribute
class ProdutoAtributoAdmin(admin.ModelAdmin):
    list_display=('id','image_tag','product','price','color','size')
admin.site.register(ProdutoAtributo,ProdutoAtributoAdmin)

# Order
class CarrinhoPedidoAdmin(admin.ModelAdmin):
	list_editable=('paid_status','order_status')
	list_display=('user','total_amt','paid_status','order_dt','order_status')
admin.site.register(CarrinhoPedido,CarrinhoPedidoAdmin)

class CarrinhoPedidoItemsAdmin(admin.ModelAdmin):
	list_display=('invoice_no','item','image_tag','qty','price','total')
admin.site.register(CarrinhoPedidoItems,CarrinhoPedidoItemsAdmin)


class ProdutoFeedbackAdmin(admin.ModelAdmin):
	list_display=('user','product','review_text','get_review_rating')
admin.site.register(ProdutoFeedback,ProdutoFeedbackAdmin)


admin.site.register(ListaDesejo)


class UserEnderecoListaAdmin(admin.ModelAdmin):
	list_display=('user','cep','whathsapp','telefone','endereco','bairro','cidade','estado','status')
admin.site.register(UserEnderecoLista,UserEnderecoListaAdmin)
