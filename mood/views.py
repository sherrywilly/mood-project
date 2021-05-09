from django.shortcuts import render, redirect
from mood.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from social.models import *
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
        Q(email=email) & ~Q(id=request.user.id)).exists()
    print(user_obj)
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
            user = CustomUser.objects.get(username=username)

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


def my_profile(request):
    posts = Post.objects.filter(user=request.user)
    context = {
        'posts': posts,
    }
    return render(request, 'profile/profile.html', context)
