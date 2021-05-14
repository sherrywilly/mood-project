# Generated by Django 3.2.2 on 2021-05-11 07:33

from django.db import migrations, models
import shortuuid.main


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0011_auto_20210511_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.UUIDField(default=shortuuid.main.ShortUUID.uuid,
                                   editable=False, primary_key=True, serialize=False),

        ),
    ]
