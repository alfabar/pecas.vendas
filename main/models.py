from cProfile import label
from attr import attr
from django.db import models
from django.forms import TextInput
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from pycep_correios import get_address_from_cep, WebService, exceptions
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
    titulo=models.CharField(max_length=100)
    image=models.ImageField(upload_to="cat_imgs/")

    class Meta:
        verbose_name_plural='2. Categorias'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.titulo

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
class Cores(models.Model):
    titulo=models.CharField(max_length=100)
    cor_code=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='4. Cores'

    def cor_bg(self):
        return mark_safe('<div style="width:30px; height:30px; background-color:%s"></div>' % (self.cor_code))

    def __str__(self):
        return self.titulo

# Cidades
class Tamanhos(models.Model):
    titulo=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='5. Cidades' 

    def __str__(self):
        return self.titulo


# Modelo do Produto
class Produto(models.Model):
    titulo=models.CharField(max_length=200)
    imagem=models.ImageField(upload_to="product_imgs/",null=True)
    imagem1=models.ImageField(upload_to="product_imgs/",null=True)
    imagem2=models.ImageField(upload_to="product_imgs/",null=True)
    imagem3=models.ImageField(upload_to="product_imgs/",null=True)
    slug=models.CharField(max_length=400)
    cor=models.CharField(max_length=6)
    tamanho=models.CharField(max_length=6)
    preco=models.PositiveIntegerField(default=0)
    detalhes=models.TextField()
    especificacoes=models.TextField()
    categoria=models.ForeignKey(Categoria,on_delete=models.CASCADE)
    marca=models.ForeignKey(Marca,on_delete=models.CASCADE)
    status=models.BooleanField(default=True)
    e_apresentado=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural='6. Produtos'

    def __str__(self):
        return self.titulo

    def imagem_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.imagem.url))

    def imagem1_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.imagem1.url))

    def imagem2_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.imagem2.url))    

    def imagem3_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.imagem3.url))
# Atribuições do Produto
class ProdutoAtributo(models.Model):
    produto=models.ForeignKey(Produto,on_delete=models.CASCADE)
    cor=models.ForeignKey(Cores,on_delete=models.CASCADE)
    tamanho=models.ForeignKey(Tamanhos,on_delete=models.CASCADE)
    preco=models.PositiveIntegerField(default=0)
    

    class Meta:
        verbose_name_plural='7. Produtos Atributos'

    def __str__(self):
        return self.produto.titulo

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

# Pedido
status_escolha=(
        ('pedido recebido','Pedido Recebido'),
        ('enviado','Enviado'),
        ('entregue','Entregue'),
    )
class CarrinhoPedido(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)    
    pedido_total=models.FloatField()
    status_pago=models.BooleanField(default=False)
    pedido_dt=models.DateTimeField(auto_now_add=True)
    pedido_status=models.CharField(choices=status_escolha,default='Pedido Recebido',max_length=150)    

    class Meta:
        verbose_name_plural='8. Pedidos'
        

# Pedido itens
class CarrinhoPedidoItems(models.Model): 
    pedido=models.ForeignKey(CarrinhoPedido,on_delete=models.CASCADE)
    fatura_no=models.CharField(max_length=150)
    item=models.ForeignKey(Produto, on_delete=models.CASCADE)
    imagem=models.CharField(max_length=200)
    qty=models.IntegerField()
    preco=models.FloatField()
    total=models.FloatField()

    class Meta:
        verbose_name_plural='9. Items Pedidos '

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.imagem))

# Avaliações dos Produtos
AVALIACAO=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)
class ProdutoFeedback(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    produto=models.ForeignKey(Produto,on_delete=models.CASCADE)
    texto_avaliacao=models.TextField()
    nota_avaliacao=models.CharField(choices=AVALIACAO,max_length=150)

    class Meta:
        verbose_name_plural='Avaliações'

    def get_nota_avaliacao(self):
        return self.nota_avaliacao

# Lista Desejo
class ListaDesejo(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    produto=models.ForeignKey(Produto,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='Lista de Desejo'

# Livro Endereço
class UserEnderecoLista(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    telefone=models.CharField(max_length=50,null=False)
    whathsapp=models.CharField(max_length=50,null=False)
    cep=models.CharField(max_length=9,null=False)   
    endereco=models.CharField(max_length=90, null=False)
    bairro=models.CharField(max_length=90, null=False)
    cidade=models.CharField(max_length=90, null=False)
    estado=models.CharField(max_length=90, null=False)
    status=models.BooleanField(default=False)
    
    
class Entregar(models.Model):
    pedido=models.ForeignKey(CarrinhoPedidoItems, on_delete=models.CASCADE)
    cliente=models.ForeignKey(User, on_delete=models.CASCADE)    
    
    class Meta:
        verbose_name_plural='Entregar '