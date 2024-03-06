# Generated by Django 4.2.7 on 2024-03-05 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("checkout", "0004_alter_order_address_1_alter_order_city_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="invoice",
            field=models.FileField(upload_to="media/invoices"),
        ),
        migrations.AlterField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="orders",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
