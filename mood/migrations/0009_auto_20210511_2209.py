# Generated by Django 3.2.2 on 2021-05-11 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mood', '0008_privacy'),
    ]

    operations = [
        migrations.AddField(
            model_name='privacy',
            name='about_privacy',
            field=models.CharField(choices=[('1', 'Public'), ('2', 'Friends'), ('3', 'Only Me')], default='1', max_length=25),
        ),
        migrations.AddField(
            model_name='privacy',
            name='email_privacy',
            field=models.CharField(choices=[('1', 'Public'), ('2', 'Friends'), ('3', 'Only Me')], default='1', max_length=25),
        ),
        migrations.AddField(
            model_name='privacy',
            name='phone_privacy',
            field=models.CharField(choices=[('1', 'Public'), ('2', 'Friends'), ('3', 'Only Me')], default='1', max_length=25),
        ),
        migrations.AddField(
            model_name='privacy',
            name='search_privacy',
            field=models.CharField(choices=[('1', 'Public'), ('2', 'Friends'), ('3', 'Only Me')], default='1', max_length=25),
        ),
    ]
