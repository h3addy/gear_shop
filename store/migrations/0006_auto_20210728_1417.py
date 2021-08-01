# Generated by Django 3.1.4 on 2021-07-28 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20210728_1416'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productcategory',
            name='new_arrival',
        ),
        migrations.RemoveField(
            model_name='productcategory',
            name='popular',
        ),
        migrations.AddField(
            model_name='product',
            name='new_arrival',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='popular',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]