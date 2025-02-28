# Generated by Django 5.1.6 on 2025-02-28 02:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('businesses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(choices=[('instagram', 'Instagram'), ('facebook', 'Facebook'), ('twitter', 'Twitter / X'), ('threads', 'Threads')], max_length=20)),
                ('link', models.URLField()),
                ('username', models.CharField(max_length=255)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_media_links', to='businesses.business')),
            ],
            options={
                'unique_together': {('business', 'platform')},
            },
        ),
    ]
