# Generated by Django 5.1.1 on 2024-09-24 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_remove_profile_bio_profile_biography_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(blank=True, to='profiles.profile'),
        ),
    ]
