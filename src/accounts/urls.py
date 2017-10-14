from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^register/$', views.UserRegistrationView.as_view(), name='user-registration'),
]
