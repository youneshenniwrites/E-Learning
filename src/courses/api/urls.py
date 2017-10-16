from django.conf.urls import url, include

from rest_framework import routers

from . import views


# automatic generation of URLs for the viewset
router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)

urlpatterns = [url(r'^subjects/$',
                    views.SubjectListView.as_view(),
                    name='subject-list'),
                url(r'^subjects/(?P<pk>\d+)/$',
                    views.SubjectDetailView.as_view(),
                    name ='subject-detail'),
                url(r'', include(router.urls))
                ]
