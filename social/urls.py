from django.urls import path
from social import views
urlpatterns = [
    path('timeline/', views.timeline, name="timeline"),
    path('like/<int:id>', views.like, name="like"),
    path('dislike/<int:id>', views.dislike, name="dislike"),
    path('likecount/<int:id>', views.likecount, name="likecount"),
    path('postlike/<int:id>', views.postlike, name="postlike"),
    path('comment/', views.comment, name="comment"),
    path('post/', views.PostView, name="post"),
]
