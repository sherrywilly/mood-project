# Generated by Django 3.2.2 on 2021-05-14 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mood', '0011_rename_patner_bio_partner'),
    ]

    operations = [
        migrations.AddField(
            model_name='bio',
            name='cover',
            field=models.ImageField(null=True, upload_to='cover'),
        ),
    ]