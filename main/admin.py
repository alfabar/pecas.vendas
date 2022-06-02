from django.contrib import admin
from .models import Banner,Promocao,Categoria,Marca,Cores,Tamanhos,Produto,ProdutoAtributo,CarrinhoPedido,CarrinhoPedidoItems,ProdutoFeedback,ListaDesejo,UserEnderecoLista,Entregar
from django.utils.html import mark_safe

# admin.site.register(Banner)

admin.site.register(Tamanhos)


class BannerAdmin(admin.ModelAdmin):
	list_display=('alt_text','image_tag')
admin.site.register(Banner,BannerAdmin)

class PromocaoAdmin(admin.ModelAdmin):
    list_display=('alt_text','image_tag')	
admin.site.register(Promocao,PromocaoAdmin)

class CategoriaAdmin(admin.ModelAdmin):
	list_display=('titulo','image_tag')
admin.site.register(Categoria,CategoriaAdmin)
class MarcaAdmin(admin.ModelAdmin):
	list_display=('titulo','image_tag')
admin.site.register(Marca,MarcaAdmin)
class CoresAdmin(admin.ModelAdmin):
	list_display=('titulo','cor_bg')
admin.site.register(Cores,CoresAdmin)

class ProdutoAdmin(admin.ModelAdmin):
    list_display=('id','titulo','imagem_tag','imagem1_tag','imagem2_tag','imagem3_tag','categoria','marca','status','e_apresentado')
    list_editable=('status','e_apresentado')
admin.site.register(Produto,ProdutoAdmin)

# Product Attribute
class ProdutoAtributoAdmin(admin.ModelAdmin):
    list_display=('id','image_tag','produto','preco','cor','tamanho')
admin.site.register(ProdutoAtributo,ProdutoAtributoAdmin)

# Order
class CarrinhoPedidoAdmin(admin.ModelAdmin):
	list_editable=('status_pago','pedido_status')
	list_display=('user','pedido_total','status_pago','pedido_dt','pedido_status')
admin.site.register(CarrinhoPedido,CarrinhoPedidoAdmin)

class CarrinhoPedidoItemsAdmin(admin.ModelAdmin):
	list_display=('pedido','fatura_no','item','image_tag','qty','preco','total')
admin.site.register(CarrinhoPedidoItems,CarrinhoPedidoItemsAdmin)



class ProdutoFeedbackAdmin(admin.ModelAdmin):
	list_display=('user','produto','texto_avaliacao','get_nota_avaliacao')
admin.site.register(ProdutoFeedback,ProdutoFeedbackAdmin)


admin.site.register(ListaDesejo)


class UserEnderecoListaAdmin(admin.ModelAdmin):
	list_display=('user','cep','whathsapp','telefone','endereco','bairro','cidade','estado','status')
admin.site.register(UserEnderecoLista,UserEnderecoListaAdmin)

class EntregarAdmin(admin.ModelAdmin):
    list_display=('pedido','cliente')
admin.site.register(Entregar,EntregarAdmin)
