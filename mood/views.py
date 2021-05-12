from mood.helpers import *
from django.shortcuts import render, redirect
from mood.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from social.models import *
from itertools import groupby
from django.contrib.auth.models import User
from django.urls import reverse
# Create your views here.


#! registration page
def register(request):
    Email = request.POST.get('email')
    Username = request.POST.get('username')
    fname = request.POST.get('first_name')
    lname = request.POST.get('last_name')
    phone = request.POST.get('phone')
    Password = request.POST.get('password1')
    Cat = request.POST.get('inlineRadioOptions')
    Gender = request.POST.get('inlineRadioOptions1')
    #password = make_password(Password)
    if request.method == "POST":
        user = CustomUser()
        user.first_name = fname
        user.last_name = lname
        user.email = Email
        user.username = Username
        user.phone = phone
        user.set_password(Password)
        user.is_active = True
        user.save()
        bio = Bio()
        bio.user = user
        bio.category = Cat
        bio.gender = Gender
        bio.save()
        login(request, user)
        return HttpResponseRedirect('timeline')
        # return redirect('register_as')
    return render(request, 'registration/registration.html')


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get('email')
    print(request.user.id)

    user_obj = CustomUser.objects.filter(
        Q(email=email)).exists()
    print(user_obj)
    print("user")
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_phone_exist(request):
    phone = request.POST.get('phoneno')
    user_obj = CustomUser.objects.filter(username=phone).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


#! LOGIN VIEW
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # user = authenticate(request, email=username, password=password)
        try:
            user = CustomUser.objects.get(
                Q(username=username) | Q(email=username))

            if user.check_password(password):

                print('username')
                login(request, user)
                print(user)
                return redirect('timeline')
        except CustomUser.DoesNotExist:
            messages.info(request, 'Username OR Password is incorrect')
            try:
                user = CustomUser.objects.get(email=username)
                if user.check_password(password):
                    login(request, user)
                    return redirect('timeline')
            except:
                messages.info(request, 'Username OR Password is incorrect')
                # return redirect('dashboard')

        # if user is not None:
        #
        #
        #     login(request, user)
        #     return redirect('dashboard')
        # else:
        #     messages.info(request, 'None user')
    return render(request, 'registration/login.html')


def my_profile(request, pk=None):
    if pk is not None:
        current_user = CustomUser.objects.get(id=pk)
    else:
        current_user = request.user
    posts = Post.objects.filter(user=current_user)
    try:
        friends = [i for i in Follow.objects.filter(
            follower=current_user) if i.friends == True]
    except:
        friends = []
    _y = [i.following.pk for i in request.user.by.all()]
    print(_y)
    p = groupby(posts, 4)

    context = {
        'posts': posts,
        'gposts': p,
        'friends': friends,
        'r_user': _y,
        'current_user': current_user
    }
    return render(request, 'profile/profile.html', context)


def notification(request):
    notifications = Notification.objects.filter(
        user=request.user).order_by('-date')
    notifications.update(is_seen=True)
    x = request.user.noti_to_user.filter(is_seen=False)
    print(x)

    context = {
        'notifications': notifications,
    }
    return render(request, 'notification/notification.html', context)


def explore_users(request):

    search = request.GET.get('tags')
    searching = CustomUser.objects.filter(Q(first_name__icontains=search) | Q(
        username__icontains=search) | Q(email__icontains=search)).exclude(id=request.user.id)
    a = len(searching)
    print(a)
    print(searching)
    _y = [i.following.pk for i in request.user.by.all()]
    _n = get_active_friends(user=request.user)
    _m = get_inactive_friends(user=request.user)

    context = {
        'searching': searching,
        'count': a,
        'r_user': _y,
        'friends': _n,
        'nonaccepted': _m,
    }
    return render(request, 'search/search.html', context)


def user_setting(request):
    context = {

    }
    return render(request, "profile/edit.html", context)


@csrf_exempt
def email_privacy_update(request):
    Privacy.objects.get_or_create(user=request.user)

    _x = Privacy.objects.get(user=request.user)
    print(_x)
    _x.email_privacy = request.POST.get('email-id')
    _x.save()

    return HttpResponse(True)


@csrf_exempt
def phone_privacy_update(request):
    Privacy.objects.get_or_create(user=request.user)
    try:
        _x = Privacy.objects.get(user=request.user)
        _x.phone_privacy = request.POST.get('phone-id')
        _x.save()
    except:
        pass
    return HttpResponse(True)


@csrf_exempt
def about_privacy_update(request):
    Privacy.objects.get_or_create(user=request.user)
    try:
        _x = Privacy.objects.get(user=request.user)
        _x.about_privacy = request.POST.get('about-id')
        _x.save()
    except:
        pass
    return HttpResponse(True)


@csrf_exempt
def search_privacy_update(request):
    Privacy.objects.get_or_create(user=request.user)
    try:
        _x = Privacy.objects.get(user=request.user)
        _x.search_privacy = request.POST.get('search-id')
        _x.save()
    except:
        pass
    return HttpResponse(True)


def setting_update(request):
    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        phone = request.POST.get('phone')
        gender = request.POST.get('inlineRadioOptions')
        category = request.POST.get('inlineRadioOptions1')
        partner = request.POST.get('partner')
        user = CustomUser.objects.get(id=request.user.id)
        user.first_name = fname
        user.last_name = lname
        user.email = email
        user.phone = phone
        user.save()
        user2 = Bio.objects.get(user=request.user)
        user2.gender = gender
        user2.category = category
        if partner is not None:
            user2.partner = partner
        user2.dob = dob
        user2.save()

        # lname= request.POST.get('')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse(True)
