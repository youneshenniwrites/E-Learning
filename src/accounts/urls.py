from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^register/$', views.UserRegistrationView.as_view(), name='user-registration'),
    url(r'^enroll-course/$', views.UserEnrollCourseView.as_view(), name='user-enroll-course'),
    url(r'^course/(?P<pk>\d+)/(?P<module_id>\d+)/$', views.UserCourseDetailView.as_view(), name='user-course-detail-module'),
    url(r'^course/(?P<pk>\d+)/$', views.UserCourseDetailView.as_view(), name='user-course-detail'),
    url(r'^courses/$', views.UserCourseListView.as_view(), name='user-course-list'),
]
