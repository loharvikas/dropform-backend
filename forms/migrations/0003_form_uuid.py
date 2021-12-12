# Generated by Django 4.0 on 2021-12-11 12:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
