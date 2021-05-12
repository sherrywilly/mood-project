from django.db import models
from django.http import request
from django.contrib.sessions.models import Session
from mood.models import CustomUser
from uuid import uuid4

# Create your models here.


class Friend(models.Model):
    u1 = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="From User", related_name='fromuser')
    u2 = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="To User", related_name='touser')
    date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        unique_together = ['u1', 'u2']

    def __str__(self):
        return str(self.u1.username + "    "+self.u2.username)


class Follow(models.Model):
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                  null=True, blank=True, verbose_name="who following", related_name="to")
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                 null=True, blank=True, verbose_name="followed by", related_name="by")
    follow_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["follow_time", ]

    @property
    def friends(self):

        x = Follow.objects.get(following=self.follower,
                               follower=self.following)
        if x is not None:
            return True

        return False


class Post(models.Model):

    PRIVACY_CHOICE = (('1', 'Public'), ('2', 'Friends'), ('3', 'Private'),)
    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    caption = models.CharField(max_length=500, null=True)
    date = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=1000, null=True)
    file = models.FileField(upload_to='media', null=True)
    privacy = models.CharField(
        choices=PRIVACY_CHOICE, max_length=20, default='1')
    # likes = models.IntegerField(default = 0)
    # comments =models.IntegerField(default = 0)

    class Meta:
        get_latest_by = ['date']
        ordering = ['-date', ]

    def __str__(self):
        return str(self.id)

    @ property
    def likeset(self):
        likes = self.like_set.all()
        return likes

    @ property
    def cmtset(self):
        commentss = self.comment_set.all()
        # print(commentss)
        return commentss

    @ property
    def cmtcount(self):
        try:
            commentss = self.comment_set.count()
        except:
            commentss = 0
        return commentss

    @ property
    def likecount(self):
        try:
            likes = self.like_set.count()
        except:
            likes = 0
        return likes


class Like(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, blank=True, null=True,)

    class Meta:
        unique_together = ('user', 'post',)


class Comment(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(auto_now=True)


class Notification(models.Model):
    NOTIFICATION_TYPES = (('1', 'Like'), ('2', 'Comment'),
                          ('3', 'follow'), ('4', 'Friend'))
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='noti_post', blank=True, null=True)
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='noti_from_user')
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='noti_to_user')
    notification_type = models.CharField(
        choices=NOTIFICATION_TYPES, max_length=50)
    text_preview = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return str(self.notification_type)
