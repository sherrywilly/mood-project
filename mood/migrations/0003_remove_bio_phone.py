# Generated by Django 3.2.2 on 2021-05-09 02:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mood', '0002_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bio',
            name='phone',
        ),
    ]
