import requests, json, subprocess, logging, os
import shutil 


from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.core.files.storage import FileSystemStorage
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.shortcuts import render

from dspacedashboard.imports.forms import ImportFileForm
from dspacedashboard.imports.models import FileImport, Collection
from dspacedashboard.core.dspace_utils import get_collections


def import_file(request):
    template_name = 'imports/import_file.html'
    success_message = 'Importação realizada com sucesso'

    collections = get_collections()
    collections_form = ()
    for collection in collections:               
        if collection.get('dc.title', None):
            collections_form += ((collection['handle'], collection['dc.title'][0]),)
    
    form = ImportFileForm(request.POST or None, request.FILES or None, collections=collections_form)
    context = {}

    if form.is_valid():
        #Getting/save target collection and file data
        handle = form.cleaned_data.get('collection')        
        collection_name = next(item for item in collections if item["handle"] == handle)
        collection, created = Collection.objects.get_or_create(handle=handle, name=collection_name.get('dc.title', [['']])[0])
        file_import = FileImport.objects.create(user=request.user, collection=collection)
        
        #Saving temporary file
        fs = FileSystemStorage()
        upload_file = form.files.get('dspace_simple_archive', None)
        filename = fs.save(upload_file.name, upload_file)

        unziped_dir = os.path.join(settings.MEDIA_ROOT, str(file_import.id))
        output = subprocess.check_output(['unzip', fs.path(filename), '-d', unziped_dir])         
        
        import_dir = os.path.join(settings.MEDIA_ROOT, unziped_dir, os.listdir(unziped_dir)[0])
        import_dir = os.path.join(import_dir, os.listdir(import_dir)[0])

        #COMANDO DE IMPORTAÇÃO AQUI   
        output += subprocess.check_output(['ping', '-c', '10', '127.0.0.1'])

        fs.delete(filename)
        shutil.rmtree(unziped_dir)     
        
        logger = open(f'log/{str(file_import.id)}.log', 'w+')
        for line in output.splitlines():            
            logger.write(line.decode('utf-8'))
            logger.write('\n')
                    
        context['import_output'] = output.decode('utf-8').splitlines()

        messages.info(request, success_message)
        logger.close()

    context['form'] = form
    return render(request, template_name, context)


class ImportFileListView(ListView):
    template_name = 'imports/import_list.html'
    model = FileImport


class ImportLogDetailView(DetailView):
    template_name = 'imports/import_log.html'
    model = FileImport

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