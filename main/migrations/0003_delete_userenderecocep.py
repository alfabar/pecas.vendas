# Generated by Django 4.0.4 on 2022-04-29 22:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_userenderecolista_cep'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserEnderecoCep',
        ),
    ]
