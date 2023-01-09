# Generated by Django 4.1.5 on 2023-01-06 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_post_categoria'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='usuario',
            new_name='autor',
        ),
        migrations.AddField(
            model_name='post',
            name='categoria',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.categoria'),
            preserve_default=False,
        ),
    ]