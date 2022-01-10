# Generated by Django 4.0 on 2022-01-06 13:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_user_stripe_customer_id_alter_user_account_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_rotation_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
