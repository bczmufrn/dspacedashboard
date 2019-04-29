from django.urls import reverse
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404


from dspacedashboard.accounts.models import User
from dspacedashboard.accounts.forms import CreateUserForm, UpdateUserForm

class UserListView(ListView):
    template_name = 'accounts/user_list.html'
    model = User

    def get_queryset(self):
        return super(UserListView, self).get_queryset()

class UserCreateView(SuccessMessageMixin,CreateView):
    model = User
    form_class = CreateUserForm
    template_name = 'accounts/user_create.html'
    success_message = "Usuário criado com sucesso"

    def get_success_url(self):
        return reverse('accounts:user_list')

class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'accounts/user_update.html'
    success_message = "Usuário atualizado com sucesso"

    def get_success_url(self):
        return reverse('accounts:user_list')

class ResetPasswordRedirectView(RedirectView):

    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        user.set_password('12345')
        user.save()

        messages.info(self.request, 'Senha do usuário redefinida para <b>12345</b>')
        return reverse('accounts:user_list')


user_list = UserListView.as_view()
user_create = UserCreateView.as_view()
user_update = UserUpdateView.as_view()
reset_password = ResetPasswordRedirectView.as_view()