# Generated by Django 3.1.4 on 2021-07-28 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20210728_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='new_arrival',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='popular',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]