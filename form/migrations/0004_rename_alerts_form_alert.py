# Generated by Django 4.0 on 2022-01-06 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0003_form_redirect_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='form',
            old_name='alerts',
            new_name='alert',
        ),
    ]