# Generated by Django 4.1.5 on 2023-01-06 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='categoria',
        ),
    ]
