from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView

from dspacedashboard.autopermission.models import AutoPermissionUser

class AutopermissionUserListView(UserPassesTestMixin, ListView):
    template_name = 'autopermission/autopermission_user_list.html'
    model = AutoPermissionUser
    paginate_by = 100

    def test_func(self):
        return self.request.user.is_staff
    
    def get_queryset(self):
        query = self.request.GET.get('query', '')
        file_imports = AutoPermissionUser.objects
        file_imports = file_imports.search(query) if query else file_imports.all()
        return file_imports.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super(AutopermissionUserListView, self).get_context_data(**kwargs)
        context['enable_search'] = True
        return context