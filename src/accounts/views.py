from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


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
