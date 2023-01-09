# Generated by Django 4.1.5 on 2023-01-09 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_usuario_senha_remove_usuario_senha2'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='tipo',
            field=models.CharField(choices=[('AD', 'Administrador'), ('AU', 'Autor'), ('CO', 'Comum')], default='AD', max_length=30),
        ),
    ]
