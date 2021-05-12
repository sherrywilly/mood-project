from mood.helpers import *
from django.shortcuts import redirect, render
from social.models import *
from mood.models import *
from django.db.models.query_utils import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from social.forms import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def activity(request):
    try:
        posts = Post.objects.filter(user=request.user)
    except:
        posts = []
    # print(posts)
    liked_posts = [i.post.pk for i in Like.objects.filter(user=request.user)]
    print(liked_posts)
    context = {
        'posts': posts,
        'liked_posts': liked_posts
    }
    return render(request, 'timeline/timeline.html', context)


def timeline(request):
    try:
        _x = [i.following.pk for i in request.user.by.all()]
        _x.append(request.user.pk)
        # * fetching posts from the following users and the current user`
        posts = Post.objects.filter(Q(user__in=_x))
    except:
        posts = []
    # print(posts)
    liked_posts = [i.post.pk for i in Like.objects.filter(user=request.user)]
    print(liked_posts)
    context = {
        'posts': posts,
        'liked_posts': liked_posts
    }
    return render(request, 'timeline/timeline.html', context)


def PostView(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            a = form.cleaned_data['caption']
            b = form.cleaned_data['file']
            post.user_id = request.user.id
            c = request.user.id
            post.bio_id = c
            post.save()

        # Cmnt = request.POST.get('caption')
        # img = request.POST.get('image')
        # post = Post()
        # post.caption = Cmnt
        # post.image = img
        # post.save()
        # print(Cmnt,img)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def like(request, id):

    # if liked:
    #     dislike = Like.objects.filter(post_id = id)
    #     dislike.delete()
    #     liked = False
    #     return HttpResponse('true')
    # else:

    like = Like()
    like.user_id = request.user.id
    like.post_id = id
    like.save()

    post = Post.objects.get(id=id)
    current_like = post.likes
    post.likes = current_like + 1
    post.save()
    return redirect('index')


def dislike(request, id):
    dislike = Like.objects.filter(post_id=id)
    dislike.delete()

    post = Post.objects.get(id=id)
    current_like = post.likes
    post.likes = current_like - 1
    post.save()
    return redirect('index')


def postlike(request, id):
    print(request)
    liked = Like.objects.filter(user_id=request.user.id, post_id=id)
    lc = Like.objects.filter(post_id=id).count()
    print(lc)

    post = Post.objects.get(id=id)
    p = post.user.id
    print(p)
    is_liked = True if liked else False
    if is_liked:
        liked.delete()
        notify = Notification.objects.filter(
            post=post, sender=request.user.id, notification_type=1)
        notify.delete()
        is_liked = False
        lcn = Like.objects.filter(post_id=id).count()

    else:
        like = Like()
        like.user_id = request.user.id
        like.post_id = id
        like.save()
        notify = Notification()
        notify.post_id = id
        notify.sender_id = request.user.id
        notify.user_id = p
        notify.notification_type = 1
        notify.save()
        is_liked = True
        lcn = Like.objects.filter(post_id=id).count()

    resp = {
        "liked": is_liked,
        "post_id": str(id),
        "lcn": lcn,
    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")


def likecount(request, id):
    likescount = Like.objects.filter(post_id=id).count()

    return render(request, 'index.html', {'likescount': likescount})


def comment(request):
    if request.method == "POST":
        post = request.POST.get('commentid')
        commentfeed = request.POST.get('comments')

        postid = post
        print(postid)
        p = Post.objects.get(id=post)
        print(p)
        sender = p.user.id
        print(sender)
        comment = Comment()
        comment.post_id = post
        comment.user_id = request.user.id
        comment.bio_id = request.user.id
        comment.comment = commentfeed
        comment.save()

        # bio = Bio.objects.get(id = request.user.id)
        # profile = bio.image

        notify = Notification()
        notify.post_id = post
        notify.user_id = request.user.id
        notify.sender_id = sender
        notify.notification_type = 2
        notify.save()

        # comment_list = []

        comment_list = [{
            "sender": request.user.id,
            "comment": commentfeed,
        }]

        return JsonResponse(comment_list, safe=False)


def check_friends(id, id2):
    try:
        c = Follow.objects.get(following__id=id2, follower__id=id)
        x = Follow.objects.get(following__id=id, follower__id=id2)
        if c.to == x.by:
            pass

    except:
        pass
    return None


def friends(request):
    c = get_active_friends(user=request.user)
    # x = [i for i in Follow.objects.filter(
    #     follower=request.user) if i.friends == True]
    # print(x)
    # print([i.following.pk for i in request.user.by.all()])
    # print(request.user.bio.following)

    # _x = [i.following.pk for i in request.user.by.all()]
    # print(_x)
    # f = Follow.objects.filter(follower__in=_x)
    # print(f)
    return HttpResponse('text')


def post_detail(request, id):
    post = Post.objects.get(id=id)
    context = {
        'post': post
    }
    return render(request, 'post/post.html', context)


@ csrf_exempt
def follow(request):
    if request.method == 'POST':
        following = request.POST.get('f-id')
        try:
            x = Follow.objects.get(
                following_id=following, follower=request.user)
        except:
            x = None
        if x is None:
            try:
                Follow.objects.create(following_id=following,
                                      follower=request.user)

            except:
                pass
            print('followed')
        else:
            x.delete()
            print('unfollow')
        return HttpResponse(True)
    return HttpResponse(False)


def friend_request(request):
    if request.method == "POST":
        rid = request.POST.get('r-id')
        try:
            x = Friend.objects.get(
                Q(u1=request.user, u2_id=rid) | Q(u1_id=rid, u2=request.user)).exclude(active=True)
        except:
            x = None
        if x is None:
            Friend.objects.create(u1=request.user, u2_id=rid)
            print('friend request sent')
        else:
            x.delete()
            print('friend request canceled')
        return HttpResponse(True)
    return HttpResponse(False)
