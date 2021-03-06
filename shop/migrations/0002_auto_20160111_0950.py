# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-11 09:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=8),
        ),
        migrations.AlterField(
            model_name='product',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.Department'),
        ),
    ]
