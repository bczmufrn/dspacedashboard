import re
import requests, json, subprocess, logging, os
import shutil


from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.core.files.storage import FileSystemStorage
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.shortcuts import render

from dspacedashboard.imports.forms import ImportFileForm
from dspacedashboard.imports.models import FileImport, Collection
from dspacedashboard.core.dspace_utils import get_collections

@login_required
def import_file(request):
    template_name = 'imports/import_file.html'
    success_message = 'Importação realizada com sucesso!'

    collections = get_collections()
    collections_form = ()
    for collection in collections:
        if collection.get('name', None):
            collections_form += ((collection['handle'], collection['name']),)
    
    form = ImportFileForm(request.POST or None, request.FILES or None, collections=collections_form)
    context = {}

    if form.is_valid():
        #Getting/saving target collection and file data
        handle = form.cleaned_data.get('collection')        
        collection_name = next(item for item in collections if item["handle"] == handle)
        collection, _ = Collection.objects.get_or_create(handle=handle, 
            name=collection_name.get('name', [['']])[0])
        file_import = FileImport.objects.create(user=request.user, collection=collection)
        
        #Saving temporary file
        fs = FileSystemStorage()
        upload_file = form.files.get('dspace_simple_archive', None)
        filename = fs.save(upload_file.name, upload_file)

        unziped_dir = os.path.join(settings.MEDIA_ROOT, str(file_import.id))
        output = subprocess.check_output(['unzip', fs.path(filename), '-d', unziped_dir])
        
        import_dir = os.path.join(settings.MEDIA_ROOT, unziped_dir, os.listdir(unziped_dir)[0])
        import_dir = os.path.join(import_dir, os.listdir(import_dir)[0])

        dspace_binary_dir = os.path.join(settings.DSPACE_PATH, 'bin', 'dspace')
        mapfile = os.path.join(settings.MAPFILES_ROOT, f'{file_import.pk}.mapfile')

        try:
            output += subprocess.check_output([
                dspace_binary_dir, 'import', '-a', '-w', '-c', handle, '-m', mapfile,
                '-e', settings.DSPACE_IMPORT_USER_MAIL, '-s', import_dir
            ])
        except subprocess.CalledProcessError as e:
            output += e.output

        #Removing uploaded files
        fs.delete(filename)
        shutil.rmtree(unziped_dir)
        
        output = output.decode('utf-8').splitlines()
        context['import_output'] = output

        logger = open(f'log/{str(file_import.id)}.log', 'w+')
        for line in output:
            logger.write(line)
            logger.write('\n')

        messages.info(request, success_message)
        logger.close()

    context['form'] = form
    return render(request, template_name, context)


class ImportFileListView(LoginRequiredMixin, ListView):
    template_name = 'imports/import_list.html'
    model = FileImport
    paginate_by = 100

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        file_imports = FileImport.objects
        file_imports = file_imports.search(query) if query else file_imports.all()
        if not self.request.user.is_staff:
            file_imports = file_imports.filter(user=self.request.user)

        return file_imports.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super(ImportFileListView, self).get_context_data(**kwargs)
        context['enable_search'] = True
        return context


class ImportLogDetailView(UserPassesTestMixin, DetailView):
    template_name = 'imports/import_log.html'
    model = FileImport

    def test_func(self):
        user = self.request.user
        return user.is_staff or self.get_object().user == user

    def get_context_data(self, **kwargs):
        context = super(ImportLogDetailView, self).get_context_data(**kwargs)
        try:
            with open(f'log/{str(self.object.id)}.log', 'r') as log:  
                lines = []
                for line in log:
                    lines.append(line)
            context['log_content'] = lines
            log.close()
        except Exception as e:
            context['log_content'] = [e]
        return context