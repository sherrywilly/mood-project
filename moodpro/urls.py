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
    path('profile/', views.my_profile, name='my_profile'),
    path('explore/user/<pk>/', views.my_profile, name="userprofile"),

    #!notifications
    path('notifications', views.notification, name="notification"),
    #!app includes
    path('social/', include('social.urls')),

    #!search or explore users
    path('explore/users/', views.explore_users, name="explore"),

    #!settings
    path('settings/', views.user_setting, name="user_settings"),
    path('p-email/', views.email_privacy_update, name="p_email"),
    path('p-phone/', views.phone_privacy_update, name="p_phone"),
    path('p-about/', views.about_privacy_update, name="p_about"),
    path('p-search/', views.search_privacy_update, name="p_search"),
    path('setting_update/', views.setting_update, name="setting_update"),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
