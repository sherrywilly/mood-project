from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from mood import views
from moodpro import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    #! pages without  authentication
    path('', views.loginpage, name='login'),
    path('register/', views.register, name='register'),
    #! validations
    path('check_email_exist/', views.check_email_exist, name='check_email_exist'),
    path('check_phone_exist/', views.check_phone_exist, name='check_phone_exist'),
    # ! profile
    path('profile', views.my_profile, name='my_profile'),
    #!app includes
    path('social/', include('social.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
