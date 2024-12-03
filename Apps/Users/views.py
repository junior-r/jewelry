from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import UpdateView, DetailView

from Apps.Users.forms import UserUpdateForm
from Apps.Users.models import User


class UserProfileTemplateView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'Apps/Users/profile.html'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, username=self.kwargs['username'])


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'Apps/Users/profile.html'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, username=self.kwargs['username'])

    def get_success_url(self):
        return reverse('Users:profile', kwargs={'username': self.object.username})

    def form_valid(self, form):
        messages.success(self.request, 'Tu información ha sido actualizada correctamente.')
        return super().form_valid(form)
