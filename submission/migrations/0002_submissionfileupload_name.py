# Generated by Django 4.0 on 2022-01-18 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='submissionfileupload',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
