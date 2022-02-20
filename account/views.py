from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse

from .models import MyUser
from .forms import SignUpForm


class UserCreationView(CreateView):
    template_name = 'registration/register.html'
    form_class = SignUpForm

    def get_context_data(self, *args, **kwargs):
        context = super(UserCreationView, self).get_context_data(*args, **kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        success_url = reverse('login')
        if next_url:
            success_url += '?next={}'.format(next_url)
        return success_url


class ProfileView(UpdateView):
    model = MyUser
    fields = ['email', 'name', ]
    template_name = 'registration/profile.html'

    def get_success_url(self):
        return reverse('home')

    def get_object(self):
        return self.request.user
