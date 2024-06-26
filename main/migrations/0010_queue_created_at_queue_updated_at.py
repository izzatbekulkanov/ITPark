# Generated by Django 5.0.3 on 2024-04-22 14:10

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_services_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='Yaratilgan vaqti'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='queue',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text="O'zgartirilgan vaqti"),
        ),
    ]
