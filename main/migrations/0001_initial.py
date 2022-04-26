# Generated by Django 4.0.4 on 2022-04-26 20:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='banner_imgs/')),
                ('alt_text', models.CharField(max_length=300)),
            ],
            options={
                'verbose_name_plural': '0. Banners',
            },
        ),
        migrations.CreateModel(
            name='CarrinhoPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amt', models.FloatField()),
                ('paid_status', models.BooleanField(default=False)),
                ('order_dt', models.DateTimeField(auto_now_add=True)),
                ('order_status', models.CharField(choices=[('processo', 'Processo'), ('enviado', 'Enviado'), ('entregue', 'Entregue')], default='processo', max_length=150)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '8. Pedidos',
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='cat_imgs/')),
            ],
            options={
                'verbose_name_plural': '2. Categorias',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('color_code', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': '4. Cores',
            },
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('imagemarca', models.ImageField(upload_to='brand_imgs/')),
            ],
            options={
                'verbose_name_plural': '3. Marcas',
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('imagem', models.ImageField(null=True, upload_to='product_imgs/')),
                ('imagem1', models.ImageField(null=True, upload_to='product_imgs/')),
                ('imagem2', models.ImageField(null=True, upload_to='product_imgs/')),
                ('imagem3', models.ImageField(null=True, upload_to='product_imgs/')),
                ('slug', models.CharField(max_length=400)),
                ('detalhes', models.TextField()),
                ('especificacoes', models.TextField()),
                ('status', models.BooleanField(default=True)),
                ('e_apresentado', models.BooleanField(default=False)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.categoria')),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.marca')),
            ],
            options={
                'verbose_name_plural': '6. Produtos',
            },
        ),
        migrations.CreateModel(
            name='Promocao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='promocao_imgs/')),
                ('alt_text', models.CharField(max_length=300)),
            ],
            options={
                'verbose_name_plural': '1. Promoção',
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': '5. Cidades',
            },
        ),
        migrations.CreateModel(
            name='UserEnderecoLista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefone', models.CharField(max_length=50)),
                ('whathsapp', models.CharField(max_length=50)),
                ('cep', models.CharField(max_length=9)),
                ('endereco', models.CharField(max_length=90)),
                ('bairro', models.CharField(max_length=90)),
                ('cidade', models.CharField(max_length=90)),
                ('estado', models.CharField(max_length=90)),
                ('status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProdutoFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', models.TextField()),
                ('review_rating', models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], max_length=150)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.produto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Avaliações',
            },
        ),
        migrations.CreateModel(
            name='ProdutoAtributo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField(default=0)),
                ('image', models.ImageField(null=True, upload_to='product_imgs/')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.color')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.produto')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.size')),
            ],
            options={
                'verbose_name_plural': '7. Produtos Atributos',
            },
        ),
        migrations.CreateModel(
            name='ListaDesejo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.produto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Lista de Desejo',
            },
        ),
        migrations.CreateModel(
            name='CarrinhoPedidoItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_no', models.CharField(max_length=150)),
                ('item', models.CharField(max_length=150)),
                ('image', models.CharField(max_length=200)),
                ('qty', models.IntegerField()),
                ('price', models.FloatField()),
                ('total', models.FloatField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.carrinhopedido')),
            ],
            options={
                'verbose_name_plural': '9. Items Pedidos ',
            },
        ),
    ]
