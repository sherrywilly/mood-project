from django.urls import path
from social import views
urlpatterns = [
    path('timeline/', views.timeline, name="timeline"),
    path('activities/', views.timeline, name="activity"),
    path('like/<uuid:id>', views.like, name="like"),
    path('dislike/<uuid:id>', views.dislike, name="dislike"),
    path('likecount/<uuid:id>', views.likecount, name="likecount"),
    path('postlike/<uuid:id>', views.postlike, name="postlike"),
    path('comment/', views.comment, name="comment"),
    path('post/', views.PostView, name="post"),
    path('test/', views.friends, name="test"),
    path('post-detail/<uuid:id>', views.post_detail, name="post_detail"),
    path('follow/', views.follow, name="follow"),
    path('friend_request/', views.friend_request, name="friend_request"),


]
