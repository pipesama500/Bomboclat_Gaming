# Generated by Django 5.0.7 on 2025-05-16 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_pedido_direccion_envio_pedido_metodo_envio_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='ciudad',
            field=models.CharField(blank=True, max_length=100, verbose_name='Ciudad'),
        ),
        migrations.AddField(
            model_name='profile',
            name='municipio',
            field=models.CharField(blank=True, max_length=100, verbose_name='Municipio'),
        ),
        migrations.AddField(
            model_name='profile',
            name='pais',
            field=models.CharField(blank=True, max_length=100, verbose_name='País'),
        ),
    ]
