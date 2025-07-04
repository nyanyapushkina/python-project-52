# Generated by Django 5.2.1 on 2025-06-26 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0002_alter_status_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={'ordering': ['name'], 'verbose_name': 'Status', 'verbose_name_plural': 'Statuses'},
        ),
        migrations.AlterField(
            model_name='status',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(error_messages={'unique': 'A status with this name already exists.'}, max_length=255, unique=True, verbose_name='Name'),
        ),
    ]
