# Generated by Django 5.0.4 on 2024-04-20 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_services_icon_alter_queue_done_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queue',
            name='order_number',
            field=models.PositiveIntegerField(editable=False, help_text='Buyurtma raqami'),
        ),
    ]
