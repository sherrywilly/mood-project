# Generated by Django 3.2.2 on 2021-05-24 08:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, null=True, unique=True, verbose_name='email address')),
                ('username', models.CharField(max_length=150, null=True, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=150, null=True)),
                ('last_name', models.CharField(blank=True, max_length=150, null=True)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('phone', models.CharField(blank=-1, max_length=12, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('1', 'Pending'), ('2', 'Approved'), ('3', 'Rejected')], default=1, max_length=50)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Privacy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_privacy', models.CharField(choices=[('1', 'Public'), ('2', 'Friends'), ('3', 'Only Me')], default='1', max_length=25)),
                ('email_privacy', models.CharField(choices=[('1', 'Public'), ('2', 'Friends'), ('3', 'Only Me')], default='1', max_length=25)),
                ('about_privacy', models.CharField(choices=[('1', 'Public'), ('2', 'Friends'), ('3', 'Only Me')], default='1', max_length=25)),
                ('search_privacy', models.CharField(choices=[('1', 'Public'), ('2', 'Friends'), ('3', 'Only Me')], default='1', max_length=25)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=500, null=True)),
                ('website', models.CharField(max_length=50, null=True)),
                ('image', models.ImageField(null=True, upload_to='media')),
                ('category', models.CharField(choices=[('1', 'Single'), ('2', 'Couple')], max_length=30, null=True)),
                ('gender', models.CharField(choices=[('1', 'Male'), ('2', 'Female')], max_length=50, null=True)),
                ('dob', models.DateField(null=True)),
                ('partner', models.CharField(blank=True, max_length=100, null=True)),
                ('cover', models.ImageField(null=True, upload_to='cover')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
