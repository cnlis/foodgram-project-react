# Generated by Django 4.0.3 on 2022-03-31 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_rename_units_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]