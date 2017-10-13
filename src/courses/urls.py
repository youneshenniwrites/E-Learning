from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^mine/$', views.ManageCourseListView.as_view(), name='manage-course-list'),
    url(r'^create/$', views.CourseCreateView.as_view(), name='course-create'),
    url(r'^(?P<pk>\d+)/edit/$', views.CourseUpdateView.as_view(), name='course-edit'),
    url(r'^(?P<pk>\d+)/delete/$', views.CourseDeleteView.as_view(), name='course-delete'),
    url(r'^(?P<pk>\d+)/module/$', views.CourseModuleUpdateView.as_view(), name='course-module-update'),
    url(r'^module/(?P<module_id>\d+)/content/(?P<model_name>\w+)/create/$', views.ContentCreateUpdateView.as_view(), name='module-content-create'),
    url(r'^module/(?P<module_id>\d+)/content/(?P<model_name>\w+)/(?P<id>\d+)/$', views.ContentCreateUpdateView.as_view(), name='module-content-update'),
    url(r'^module/(?P<module_id>\d+)/$', views.ModuleContentListView.as_view(), name='module-content-list'),
    url(r'^content/(?P<id>\d+)/delete/$', views.ContentDeleteView.as_view(), name='module-content-delete'),

]
