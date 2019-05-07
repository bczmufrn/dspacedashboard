from django.urls import reverse
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404


from dspacedashboard.accounts.models import User
from dspacedashboard.accounts.forms import CreateUserForm, UpdateUserForm

class UserListView(UserPassesTestMixin, ListView):
    template_name = 'accounts/user_list.html'
    model = User

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        search = self.request.GET.get('query', '')
        users = User.objects
        users = users.search(search) if search else users.filter(is_active=True)
        return users.exclude(is_superuser=True)

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['enable_search'] = True
        return context

class UserCreateView(UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = CreateUserForm
    template_name = 'accounts/user_create.html'
    success_message = "Usuário criado com sucesso"

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse('accounts:user_list')

class UserUpdateView(UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'accounts/user_update.html'
    success_message = "Usuário atualizado com sucesso"

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse('accounts:user_list')

class ResetPasswordRedirectView(UserPassesTestMixin, RedirectView):

    permanent = False
    query_string = True

    def test_func(self):
        return self.request.user.is_staff

    def get_redirect_url(self, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        user.set_password('12345')
        user.save()

        messages.info(self.request, 'Senha do usuário redefinida para <b>12345</b>')
        return reverse('accounts:user_list')

@login_required
def update_password(request):
	template_name = 'accounts/update_password.html'
	
	form = PasswordChangeForm(data=request.POST or None, user=request.user)
	if form.is_valid():
		form.save()
		messages.info(request, 'Senha alterada com sucesso!')
		#Reautenticando usuário com nova senha		
		update_session_auth_hash(request, form.user)
		return redirect('core:home')
	
	return render(request, template_name, {'form': form})


user_list = UserListView.as_view()
user_create = UserCreateView.as_view()
user_update = UserUpdateView.as_view()
reset_password = ResetPasswordRedirectView.as_view()