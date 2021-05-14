from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
# from .models import *
from django.db.models import Q
import json
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Prefetch
from django.db.models import Q
from mood.models import *
from social.models import *
from chat.models import *



# Create your views here.
@login_required
def chatroom(request,pk:int):
    current_user = request.user.id
    other_user = get_object_or_404(CustomUser, pk=pk)
    messages = Message.objects.filter(Q(receiver=request.user, sender=other_user,receiver_delete=False))
    messages.update(seen=True)
    messages = messages | Message.objects.filter(Q(receiver=other_user, sender=request.user,sender_delete=False) )
    connected1 = Friend.objects.filter(u1_id = request.user.id, active=1).values_list('u2_id')
    connected2 = Friend.objects.filter(u2_id = request.user.id, active=1).values_list('u1_id')
    connecteduser1 = CustomUser.objects.filter(id__in = connected1)
    connecteduser2 = CustomUser.objects.filter(id__in = connected2)
    connecteduser = connecteduser1 | connecteduser2
    context = {
        "other_user": other_user,
        "messages": messages,
        "current_user":current_user,
        "connecteduser":connecteduser
    }
    return render(request, "chat/onetoonechat.html",context)
def chatroombase(request):
    connected1 = Friend.objects.filter(u1_id = request.user.id, active=1).values_list('u2_id')
    connected2 = Friend.objects.filter(u2_id = request.user.id, active=1).values_list('u1_id')
    connecteduser1 = CustomUser.objects.filter(id__in = connected1)
    connecteduser2 = CustomUser.objects.filter(id__in = connected2)
    connecteduser = connecteduser1 | connecteduser2
    context = {
        "connecteduser":connecteduser
    }
    return render(request, "chat/onetoonechat_base.html",context)
@login_required
def ajax_load_messages(request,pk):
    message_list = []
    other_user = get_object_or_404(CustomUser, pk=pk)
    messages = Message.objects.filter(seen=False).filter(Q(receiver=request.user, sender=other_user))
    for message in messages:
        if message.files == '':
            message_list = [{
                "id":message.id,
                "sender": message.sender.id,
                "message": message.message,
                "sent": message.sender == request.user,
                "file": ''
                
            } ]
        else:
            message_list = [{
                "id":message.id,
                "sender": message.sender.id,
                "message": message.message,
                "sent": message.sender == request.user,
                "file":message.files.url
            } ]
        messages.update(seen=True)
    if request.method == "POST":
        a = request.POST.get('message')
        b = request.FILES.get('upload')
        if a == '' and b == None:
            message_list.append({
                    "id":'',
                    "sender": '',
                    "message": '',
                    "sent": '',
                    "file":''
                })
        else:
            m = Message.objects.create(receiver=other_user, sender=request.user, message=a, files=b)
            if m.files == None:
                message_list.append({
                    "id":m.id,
                    "sender": request.user.id,
                    "message": m.message,
                    "sent": True,
                    "file":''
                })
            else:
                message_list.append({
                    "id":m.id,
                    "sender": request.user.id,
                    "message": m.message,
                    "sent": True,
                    "file":m.files.url
                })
    return JsonResponse(message_list, safe=False)
def messageDelete(request):
    a = request.POST.get('id')
    d = Message.objects.get(pk=a)
    if d.receiver_id == request.user.id:
        d.receiver_delete=True
        d.save()
    elif d.sender_id == request.user.id:
        d.sender_delete=True
        d.save()
    else:
        pass
    return HttpResponse('')
# @login_required
# def switchUser(request):
#     current_user = request.user
#     connecteduser = CustomUser.objects.all()
#     last_seen = cache.get('seen_%s' % connecteduser)
#     return HttpResponse('')
# Group chat.
