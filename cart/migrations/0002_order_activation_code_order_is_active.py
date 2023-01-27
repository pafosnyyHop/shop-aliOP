# Generated by Django 4.1.5 on 2023-01-27 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='activation_code',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
