from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from pycep_correios import get_address_from_cep
from pycep_correios.exceptions import CEPNotFound, ConnectionError, InvalidCEP
import re
import requests
# Banner
class Banner(models.Model): 
    img=models.ImageField(upload_to="banner_imgs/")
    alt_text=models.CharField(max_length=300)

    class Meta:
        verbose_name_plural='0. Banners'

    def image_tag(self):
        return mark_safe('<img src="%s" width="100" />' % (self.img.url))

    def __str__(self):
        return self.alt_text

 # Promoção
class Promocao(models.Model):
    img=models.ImageField(upload_to="promocao_imgs/")
    alt_text=models.CharField(max_length=300)

    class Meta:
        verbose_name_plural='1. Promoção'

    def image_tag(self):
        return mark_safe('<img src="%s" width="100" />' % (self.img.url))

    def __str__(self):
        return self.alt_text

# Categoria
class Categoria(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="cat_imgs/")

    class Meta:
        verbose_name_plural='2. Categorias'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

# Marca
class Marca(models.Model):
    titulo=models.CharField(max_length=100)
    imagemarca=models.ImageField(upload_to="brand_imgs/")

    class Meta:
        verbose_name_plural='3. Marcas'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.imagemarca.url))

    def __str__(self):
        return self.titulo

# Cores
class Color(models.Model):
    title=models.CharField(max_length=100)
    color_code=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='4. Cores'

    def color_bg(self):
        return mark_safe('<div style="width:30px; height:30px; background-color:%s"></div>' % (self.color_code))

    def __str__(self):
        return self.title

# Cidades
class Size(models.Model):
    title=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='5. Cidades'

    def __str__(self):
        return self.title


# Modelo do Produto
class Produto(models.Model):
    titulo=models.CharField(max_length=200)
    image=models.ImageField(upload_to="product_imgs/",null=True)
    slug=models.CharField(max_length=400)
    detalhes=models.TextField()
    especificacoes=models.TextField()
    categoria=models.ForeignKey(Categoria,on_delete=models.CASCADE)
    marca=models.ForeignKey(Marca,on_delete=models.CASCADE)
    status=models.BooleanField(default=True)
    is_featured=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural='6. Produtos'

    def __str__(self):
        return self.titulo

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

# Atribuições do Produto
class ProdutoAtributo(models.Model):
    product=models.ForeignKey(Produto,on_delete=models.CASCADE)
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    size=models.ForeignKey(Size,on_delete=models.CASCADE)
    price=models.PositiveIntegerField(default=0)
    image=models.ImageField(upload_to="product_imgs/",null=True)

    class Meta:
        verbose_name_plural='7. Produtos Atributos'

    def __str__(self):
        return self.product.title

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

# Pedido
status_choice=(
        ('processo','In Processo'),
        ('enviado','Enviado'),
        ('entregue','Entregue'),
    )
class CarrinhoPedido(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)    
    total_amt=models.FloatField()
    paid_status=models.BooleanField(default=False)
    order_dt=models.DateTimeField(auto_now_add=True)
    order_status=models.CharField(choices=status_choice,default='processo',max_length=150)    

    class Meta:
        verbose_name_plural='8. Pedidos'
        

# Pedido itens
class CarrinhoPedidoItems(models.Model): 
    order=models.ForeignKey(CarrinhoPedido,on_delete=models.CASCADE)
    invoice_no=models.CharField(max_length=150)
    item=models.CharField(max_length=150)
    image=models.CharField(max_length=200)
    qty=models.IntegerField()
    price=models.FloatField()
    total=models.FloatField()

    class Meta:
        verbose_name_plural='9. Items Pedidos '

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))

# Avaliações dos Produtos
RATING=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)
class ProdutoFeedback(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Produto,on_delete=models.CASCADE)
    review_text=models.TextField()
    review_rating=models.CharField(choices=RATING,max_length=150)

    class Meta:
        verbose_name_plural='Avaliações'

    def get_review_rating(self):
        return self.review_rating

# Lista Desejo
class ListaDesejo(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Produto,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='Lista de Desejo'

# Livro Endereço
class UserEnderecoLista(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    telefone=models.CharField(max_length=50,null=False)
    whathsapp=models.CharField(max_length=50,null=False)
    cep=models.CharField(max_length=9, null=False)
    endereco=models.CharField(max_length=90, null=False)
    bairro=models.CharField(max_length=90, null=False)
    cidade=models.CharField(max_length=90, null=False)
    estado=models.CharField(max_length=90, null=False)
    status=models.BooleanField(default=False)


    @classmethod
    def buscarCepCliente(self):
        cep = self.tx_Cep.text()
        try:
            busca = get_address_from_cep(cep)
            self.tx_Endereco.setText(busca['logradouro'])
            self.tx_Bairro.setText(busca['bairro'])
            self.tx_Cidade.setText(busca['cidade'])
            self.tx_Estado.setText(busca['uf'])
            self.tx_Numero.setFocus()
        except ConnectionError:
            self.tx_Endereco.setText('Sem conexão com serviço dos Correios')
        except InvalidCEP:
            self.tx_Endereco.setText('CEP inválido')
        except CEPNotFound:
            self.tx_Endereco.setText('CEP não encontrado')
        except:
            self.tx_Endereco.setText('Erro desconhecido')

