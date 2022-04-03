# Generated by Django 4.0.3 on 2022-04-03 14:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(max_length=1000, validators=[django.core.validators.MaxLengthValidator(1000)], verbose_name='Описание'),
        ),
    ]