import requests, json, subprocess, logging, os
import shutil 


from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.core.files.storage import FileSystemStorage
from django.views.generic.edit import FormView
from django.views.generic import ListView

from dspacedashboard.imports.forms import ImportFileForm
from dspacedashboard.imports.models import FileImport, Collection

class ImportFileView(FormView):
    template_name = 'imports/import_file.html'
    success_message = 'Importação concluída com sucesso'
    form_class = ImportFileForm

    def dispatch(self, *args, **kwargs):
        try:
            response = requests.get('http://localhost:8080/solr/search/select?q=search.resourcetype:3&fl=dc.title,handle&wt=json&omitHeader=true&rows=5000')
            self.collections = json.loads(response.text)['response']['docs'] if response.status_code == 200 else []
        except Exception as e:
            print("Error: ", e)
            self.collections = [] 
        return super(ImportFileView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ImportFileView, self).get_form_kwargs()

        collections = ()
        for collection in self.collections:                
            if collection.get('dc.title', None):
                collections = collections + ((collection['handle'], collection['dc.title'][0]),)

        kwargs.update({
		    'collections' : collections
		})
        return kwargs

    def get_success_url(self):		
        return reverse('import:file')

    def form_valid(self, form):
        #Getting/save target collection and file data
        handle = form.cleaned_data.get('collection')        
        collection_name = next(item for item in self.collections if item["handle"] == handle)
        collection, created = Collection.objects.get_or_create(handle=handle, name=collection_name.get('dc.title', [['']])[0])
        file_import = FileImport.objects.create(user=self.request.user, collection=collection)
        
        #Saving temporary file
        fs = FileSystemStorage()
        upload_file = form.files.get('dspace_simple_archive', None)
        filename = fs.save(upload_file.name, upload_file)
        
        #Setting logger up
        logging.basicConfig(filename=f'log/{str(file_import.id)}.log', level=logging.INFO)

        unziped_dir = os.path.join(settings.MEDIA_ROOT, str(file_import.id))
        output = subprocess.check_output(['unzip', fs.path(filename), '-d', unziped_dir])

        logging.info(output.decode("utf-8"))

        fs.delete(filename)
        shutil.rmtree(unziped_dir)

        messages.info(self.request, self.success_message)		
        return HttpResponseRedirect(self.get_success_url())


class ImportFileListView(ListView):
    template_name = 'imports/import_list.html'
    model = FileImport
