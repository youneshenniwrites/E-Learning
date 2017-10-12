
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from django.views.generic.edit import (CreateView,
                                        UpdateView,
                                        DeleteView)
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)

from .models import Course
from .forms import ModuleFormset


class ManageCourseListView(ListView):
    model = Course
    template_name = 'courses/manage/course/list.html'

    def get_queryset(self):
        '''
        only retrieve courses created by the current user
        '''

        qs = super(ManageCourseListView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerMixin(object):

    def get_queryset(self):
        '''
        get the base queryset and override it to retrieve
        objects that belong to the current user only
        '''

        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):

    def form_valid(self, form):
        '''override the form_valid method of the
        CRUD views to automatically set the current
        user in the owner attribute when the object
        is beign saved'''

        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin):
    '''
    provides the model used for all querysets by the child views
    '''

    model = Course


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin, LoginRequiredMixin):
    '''
    giving raw materials for the child views to build
    the model form and redirect after submission
    '''

    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    '''
    Lists the courses created by the user
    '''

    template_name = 'courses/manage/course/list.html'


class CourseCreateView(PermissionRequiredMixin, OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(PermissionRequiredMixin, OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin, OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('manage_course_list')
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, View):
    '''
    formset handeling view for CRUD methods
    '''

    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        '''
        a method to build the formset
        for a given Course object
        '''

        return ModuleFormset(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(
                                        Course,
                                        id=pk,
                                        owner=request.user)
        return super(CourseModuleUpdateView,
                        self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        context = {'course': self.course, 'formset': formset}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        context = {'course': self.course, 'formset': formset}
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response(context)
