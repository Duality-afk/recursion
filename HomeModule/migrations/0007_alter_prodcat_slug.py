# Generated by Django 4.0.5 on 2023-03-16 13:43

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HomeModule', '0006_prodcat_slug_useractivity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prodcat',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, null=True, populate_from='name'),
        ),
    ]
