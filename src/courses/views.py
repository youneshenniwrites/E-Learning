from django.db.models import Count
from django.apps import apps
from django.forms.models import modelform_factory
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView,
                                        UpdateView,
                                        DeleteView)
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)

from braces.views import (CsrfExemptMixin,
                            JsonRequestResponseMixin)

from .models import (Course, Module, Content, Subject)
from .forms import ModuleFormset

from accounts.forms import CourseEnrollForm


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        '''
        let users enroll in a given course
        '''
        
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course': self.object})
        return context


class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        # retrieves all subjects with their total number of courses
        subjects = Subject.objects.annotate(total_courses=Count('courses'))
        # retrieves all courses with their total number of modules
        courses = Course.objects.annotate(total_modules=Count('modules'))
        if subject:
            # subject slug is provided
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)

        context = {'subjects': subjects,
                    'subject': subject,
                    'courses': courses}
        return self.render_to_response(context)


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
    success_url = reverse_lazy('manage-course-list')
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
    success_url = reverse_lazy('manage-course-list')
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
            return redirect('manage-course-list')
        return self.render_to_response(context)


class ContentCreateUpdateView(TemplateResponseMixin, View):
    '''
    Handles creating and updating
    objects of any content model
    '''

    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        '''
        Returns the corresponding class
        for type of content model using
        the built in Django apps module
        '''

        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses',
                                    model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        '''
        Dynamic form for the given contents
        '''

        Form = modelform_factory(model, exclude=['owner',
                                                    'order',
                                                    'created',
                                                    'updated'])
        return Form(*args, **kwargs)

    def get(self, request, module_id, model_name, id=None):
        '''
        Builds the model form of the instance
        content when a GET request is received
        '''

        form = self.get_form(self.model, instance=self.obj)
        context = {'form': form, 'object': self.obj}
        return self.render_to_response(context)

    def post(self, request, module_id, model_name, id=None):
        '''
        Builds a model form passing
        any submitted data and files to it
        '''

        form = self.get_form(self.model,
                            instance=self.obj,
                            data=request.POST,
                            files=request.FILES)
        context = {'form': form, 'object': self.obj}
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # not an update, but a new content object for the given module
                Content.objects.create(module=self.module, item=obj)
            return redirect('module-content-list', self.module.id)
        return self.render_to_response(context)

    def dispatch(self, request, module_id, model_name, id=None):
        '''
        Receives a number of arguments and
        stores their corresponding module,
        model and content object as class attributes
        '''

        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                            id=id,
                                            owner=request.user)
        return super(ContentCreateUpdateView, self).dispatch(request,
                                                                module_id,
                                                                model_name, id)


class ContentDeleteView(View):

    def post(self, request, id):
        content = get_object_or_404(Content,
                                    id=id,
                                    module__course__owner=request.user)
        module = content.module
        content.item.delete() # deletes the related video, text, image, file
        content.delete()
        return redirect('module-content-list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                    id=module_id,
                                    course__owner=request.user)
        return self.render_to_response({'module': module})


class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id,
                    course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.object.filter(id=id,
                    module__course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})
