from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.views.generic import FormView
from django.contrib.auth import login as auth_login
from django.core.urlresolvers import reverse
from django.conf import settings


class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    form_class = AuthenticationForm
    template_name = 'accounts/login.jinja2'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('index')

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        return reverse('index')
