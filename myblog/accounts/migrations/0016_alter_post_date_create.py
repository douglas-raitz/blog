# Generated by Django 4.1.4 on 2023-01-12 18:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_post_date_create'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_create',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
