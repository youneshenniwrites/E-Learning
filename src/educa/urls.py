from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, name='logout'),
    url(r'^admin/', admin.site.urls),
]
