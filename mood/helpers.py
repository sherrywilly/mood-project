from mood.models import *
from social.models import *


def get_active_friends(user):
    x = [i.u1.pk for i in Friend.objects.filter(u2=user, active=True)]
    y = [i.u2.pk for i in Friend.objects.filter(u1=user, active=True)]
    x.extend(y)
    return x


def get_inactive_friends(user):
    x = [i.u2.pk for i in Friend.objects.filter(u1=user, active=False)]
    return x
