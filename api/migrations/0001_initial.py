# Generated by Django 3.0.5 on 2021-05-03 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advisor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advisor_name', models.CharField(blank=True, max_length=32)),
                ('advisor_photo_url', models.URLField(blank=True)),
            ],
        ),
    ]
