from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from dspacedashboard.imports.models import FileImport

class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        file_imports = FileImport.objects.all()
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['imports'] = file_imports[:10] if user.is_staff else file_imports.filter(user=user)
        return context
