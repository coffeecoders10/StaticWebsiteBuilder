# Generated by Django 3.0.8 on 2023-12-19 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('path', models.CharField(max_length=255)),
                ('render_path', models.CharField(max_length=255)),
            ],
        ),
    ]
