from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# from social.models import Notification

# from byhandpro.social.models import Post


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, first_name, password, **other_fields)

    def create_user(self, email, username, first_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, null=True)
    username = models.CharField(max_length=150, unique=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    start_date = models.DateTimeField(default=timezone.now)
    phone = models.CharField(max_length=12, null=True, blank=-True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    def __str__(self):
        return self.username


class Bio(models.Model):
    CATEGORY_CHOICES = (
        ('1', 'Single'),
        ('2', 'Couple'),
        ('3', 'Widower'),
        ('4', 'Divorced')
    )
    GENDER_CHOICES = (
        ('1', 'Male'),
        ('2', 'Female'),
        ('3', 'Transgenders'),
        ('4', 'Not To Say')
    )
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=500, null=True)
    website = models.CharField(max_length=50, null=True)
    image = models.ImageField(upload_to='media', null=True)
    category = models.CharField(
        choices=CATEGORY_CHOICES, max_length=30, null=True)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, null=True)
    dob = models.DateField(null=True)
    patner = models.CharField(max_length=100, null=True, blank=True)

    def profile_pic(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

    def __unicode__(self):
        return self.user

    def __str__(self):
        return self.user.username

    @property
    def notification_count(self):
        try:
            _x = self.user.noti_to_user.filter(is_seen=False)
            _x = _x.count()
        except:
            _x = 0
        return _x


class Privacy(models.Model):
    CHOICE = (
        ('1', 'Public'),
        ('2', 'Friends'),
        ('3', 'Only Me'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_privacy = models.CharField(
        choices=CHOICE, default='1', max_length=25)
    email_privacy = models.CharField(
        choices=CHOICE, default='1', max_length=25)
    about_privacy = models.CharField(
        choices=CHOICE, default='1', max_length=25)
    search_privacy = models.CharField(
        choices=CHOICE, default='1', max_length=25)
