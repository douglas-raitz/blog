# Generated by Django 4.1.5 on 2023-01-06 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_usuario_senha_usuario_senha2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='senha',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='senha2',
        ),
    ]