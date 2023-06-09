# Generated by Django 4.0.5 on 2023-03-16 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomeModule', '0009_cart_cartitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=12)),
                ('address', models.CharField(max_length=255)),
                ('mode', models.CharField(max_length=255)),
                ('size', models.IntegerField(default=32, null=True)),
                ('payment_status', models.BooleanField(default=False)),
                ('delivered', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='Paymemnt',
        ),
        migrations.AlterField(
            model_name='useractivity',
            name='activity_details',
            field=models.CharField(max_length=1000),
        ),
    ]
