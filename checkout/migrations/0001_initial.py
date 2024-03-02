# Generated by Django 4.2.7 on 2024-03-02 10:47

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("profilemanager", "0006_alter_userprofile_profile_picture"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("order_number", models.CharField(editable=False, max_length=32)),
                ("first_name", models.CharField(blank=True, max_length=50, null=True)),
                ("last_name", models.CharField(blank=True, max_length=50, null=True)),
                ("email", models.EmailField(max_length=254)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("address_1", models.CharField(blank=True, max_length=100, null=True)),
                ("address_2", models.CharField(blank=True, max_length=100, null=True)),
                ("city", models.CharField(blank=True, max_length=50, null=True)),
                ("county", models.CharField(blank=True, max_length=50, null=True)),
                ("post_code", models.CharField(blank=True, max_length=15, null=True)),
                (
                    "country",
                    django_countries.fields.CountryField(
                        blank=True, max_length=2, null=True
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "delivery_cost",
                    models.DecimalField(decimal_places=2, default=0, max_digits=6),
                ),
                (
                    "sub_total",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "vat",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "total",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("original_vault", models.TextField(default="")),
                ("stripe_pid", models.CharField(default="", max_length=254)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="orders",
                        to="profilemanager.userprofile",
                    ),
                ),
            ],
        ),
    ]
