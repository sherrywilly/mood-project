# Generated by Django 3.2.2 on 2021-05-14 04:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mood', '0010_customuser_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bio',
            old_name='patner',
            new_name='partner',
        ),
    ]
