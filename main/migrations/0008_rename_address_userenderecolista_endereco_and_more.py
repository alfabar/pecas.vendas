# Generated by Django 4.0.4 on 2022-04-25 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_rename_brand_marca'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userenderecolista',
            old_name='address',
            new_name='endereco',
        ),
        migrations.RenameField(
            model_name='userenderecolista',
            old_name='mobile',
            new_name='telefone',
        ),
    ]