# Generated by Django 4.2.2 on 2023-11-25 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_vendor_id_alter_vendor_average_response_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
