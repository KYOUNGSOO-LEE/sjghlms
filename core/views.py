from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.http import HttpResponse


class HomeView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'
    template_name = 'home.html'