# Generated by Django 4.2.7 on 2024-02-03 14:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("items", "0013_alter_item_different_sizes_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="item_category",
            field=models.ManyToManyField(
                help_text="Select more categories by CTRL + click", to="items.category"
            ),
        ),
    ]