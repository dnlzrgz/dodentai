# Generated by Django 5.1.2 on 2024-10-10 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='meta_keywords',
        ),
    ]
