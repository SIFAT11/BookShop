# Generated by Django 5.0.4 on 2024-04-22 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sellbook', '0003_seller_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller_profile',
            name='additional_information',
            field=models.TextField(blank=True),
        ),
    ]