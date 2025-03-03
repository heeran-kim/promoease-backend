# Generated by Django 5.1.6 on 2025-03-03 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50, unique=True)),
                ('label', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='Categories',
        ),
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(related_name='posts', to='posts.category'),
        ),
    ]
