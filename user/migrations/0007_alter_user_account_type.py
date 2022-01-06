# Generated by Django 4.0 on 2022-01-04 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_user_account_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='account_type',
            field=models.CharField(choices=[('Free', 'Free'), ('Standard', 'Standard'), ('Professional', 'Professional'), ('Business', 'Business')], default='Free', max_length=255),
        ),
    ]
