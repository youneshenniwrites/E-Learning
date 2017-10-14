from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from braces.views import LoginRequiredMixin

from .forms import CourseEnrollForm

from courses.models import Course


class UserCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'accounts/course/list.html'

    def get_queryset(self):
        '''
        Lists only courses in which the user is enrolled
        '''

        qs = super(UserCourseListView, self).get_queryset()
        return qs.filter(users__in=[self.request.user])


class UserCourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'accounts/course/detail.html'

    def get_queryset(self):
        '''
        Lists only courses in which the user is enrolled
        '''

        qs = super(UserCourseDetailView, self).get_queryset()
        return qs.filter(users__in=[self.request.user])

    def get_context_data(self, **kwargs):
        '''
        Users are able to naviguate through modules inside a course
        '''

        context = super(UserCourseDetailView, self).get_context_data(**kwargs)
        # get course object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module if module_id URL parameter is given
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            # or get the first module of the course
            context['module'] = course.modules.all()[0]
        return context


class UserEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        '''
        Adds the current user to the list
        of enrollment in the course
        '''

        self.course = form.cleaned_data['course']
        self.course.users.add(self.request.user)
        return super(UserEnrollCourseView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('user-course-detail', args=[self.course.id])

    
class UserRegistrationView(CreateView):
    template_name = 'accounts/user/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('user-course-list')

    def form_valid(self, form):
        '''
        login the user after successfully signing up
        '''

        result = super(UserRegistrationView, self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(usrname=cd['username'], password=['password'])
        login(self.request, user)
        return result
