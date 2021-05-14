from django.contrib.auth.decorators import login_required
from mood.helpers import *
from django.shortcuts import render, redirect
from mood.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from social.models import *
from itertools import groupby
from django.contrib.auth.models import User
from django.urls import reverse
# Create your views here.
from django.contrib.auth.decorators import login_required
#! registration page
from moodpro.decorators import unauth_user


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


@unauth_user
def register(request):
    Email = request.POST.get('email')
    Username = request.POST.get('username')
    fname = request.POST.get('first_name')
    lname = request.POST.get('last_name')
    phone = request.POST.get('phone')
    Password = request.POST.get('password1')
    Cat = request.POST.get('inlineRadioOptions')
    Gender = request.POST.get('inlineRadioOptions1')
    img = request.FILES.get('file')
    # password = make_password(Password)
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
        bio.image = img
        bio.category = Cat
        bio.gender = Gender
        bio.save()
        # login(request, user)
        # return HttpResponseRedirect('timeline')
        return redirect(reverse('login'))
    return render(request, 'registration/registration.html')


@ csrf_exempt
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


@ csrf_exempt
def check_phone_exist(request):
    phone = request.POST.get('phoneno')
    user_obj = CustomUser.objects.filter(username=phone).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


#! LOGIN VIEW
@ unauth_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # user = authenticate(request, email=username, password=password)
        try:
            user = CustomUser.objects.get(
                Q(username=username) | Q(email=username))
            if user is None:
                raise ValueError

            if user.status == '1':
                x = '1'
                context = {
                    'i': x
                }
                return render(request, 'registration/login.html', context)
            elif user.status == '3':
                x = '3'
                context = {
                    'i': x
                }
                return render(request, 'registration/login.html', context)
            else:
                if user.check_password(password):
                    if user.last_login is not None:
                        login(request, user)
                        return redirect(reverse('timeline'))
                    else:
                        login(request, user)
                        return redirect(reverse('timeline'))

                else:

                    messages.error(request, 'InValid Credentials')
        except:
            messages.error(request, 'InValid Credentials')
            # return redirect('dashboard')

        # if user is not None:
        #
        #
        #     login(request, user)
        #     return redirect('dashboard')
        # else:
        #     messages.info(request, 'None user')
    return render(request, 'registration/login.html')


@ login_required(login_url='login')
def my_profile(request, pk=None):
    if pk is not None:
        current_user, created = CustomUser.objects.get_or_create(id=pk)
    else:
        current_user = request.user
    posts = Post.objects.filter(user=current_user)

    _y = [i.following.pk for i in request.user.by.all()]

    # p = groupby(posts, 4)

    _n = get_active_friends(user=request.user)
    _nx = get_active_friends(user=current_user)
    print(_nx)
    friends = CustomUser.objects.filter(id__in=_nx)
    _m = get_inactive_friends(user=request.user)
    _f = get_inactive_friends(user=current_user)
    liked_posts = [i.post.pk for i in Like.objects.filter(user=request.user)]
    context = {
        'posts': posts,
        # 'gposts': p,
        'liked_posts': liked_posts,
        'friend': friends,
        'r_user': _y,
        'current_user': current_user,
        'friends': _nx,
        'nonaccepted': _m,
        'pending': _f
    }
    return render(request, 'profile/profile.html', context)


@ login_required(login_url='login')
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


@ login_required(login_url='login')
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


@ login_required(login_url='login')
def user_setting(request):
    context = {

    }
    return render(request, "profile/edit.html", context)


@login_required(login_url='login')
@csrf_exempt
def email_privacy_update(request):
    Privacy.objects.get_or_create(user=request.user)

    _x = Privacy.objects.get(user=request.user)
    print(_x)
    x = request.POST.get('email-id')
    print(x)
    _x.email_privacy = request.POST.get('email-id')
    _x.save()

    return HttpResponse(True)


@login_required(login_url='login')
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


@login_required(login_url='login')
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


@ login_required(login_url='login')
@ csrf_exempt
def search_privacy_update(request):
    Privacy.objects.get_or_create(user=request.user)
    try:
        _x = Privacy.objects.get(user=request.user)
        _x.search_privacy = request.POST.get('search-id')
        _x.save()
    except:
        pass
    return HttpResponse(True)


@ login_required(login_url='login')
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
        img = request.FILES.get('file')
        print(img)
        user, created = CustomUser.objects.get_or_create(id=request.user.id)
        user.first_name = fname
        user.last_name = lname
        user.email = email
        user.phone = phone
        user.save()
        user2, created = Bio.objects.get_or_create(user=request.user)
        user2.gender = gender
        user2.category = category
        if partner is not None:
            user2.partner = partner
        if img is not None:
            user2.image = img
        user2.dob = dob
        user2.save()

        # lname= request.POST.get('')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse(True)


def admin_area(request):
    context = {
        'users': CustomUser.objects.filter(status='1')
    }
    return render(request, 'admin-area/index.html', context)


@ login_required(login_url='login')
def u_accept(request, id):
    if request.method == "POST":
        x = CustomUser.objects.get(id=id)
        x.status = '2'
        x.save()
        return redirect(reverse('admin_area'))


@ login_required(login_url='login')
def u_reject(request, id):
    if request.method == "POST":
        x = CustomUser.objects.get(id=id)
        x.status = '3'
        x.save()
        return redirect(reverse('admin_area'))


def changeProfile(request):
    if request.method == "POST":
        img = request.FILES.get('file')
        _x, _ = Bio.objects.get_or_create(user=request.user)
        _x.image = img
        _x.save()
        return HttpResponseRedirect(reverse('my_profile'))
    else:
        return HttpResponse("un autherized request")


def changeCover(request):
    if request.method == "POST":
        img = request.FILES.get('file')
        _x, _ = Bio.objects.get_or_create(user=request.user)
        _x.cover = img
        _x.save()
        return HttpResponseRedirect(reverse('my_profile'))
    else:
        return HttpResponse("un autherized request")
