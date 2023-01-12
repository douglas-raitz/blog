# Generated by Django 4.1.4 on 2023-01-12 19:36

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_post_date_create'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.categoria'),
        ),
        migrations.AlterField(
            model_name='post',
            name='date_create',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]