# Generated by Django 4.0.5 on 2023-03-17 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomeModule', '0011_remove_cart_user_remove_cartitem_cart_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='username',
            field=models.CharField(default='', max_length=255),
        ),
    ]
