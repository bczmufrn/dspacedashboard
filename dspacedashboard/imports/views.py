import requests, json

from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic import ListView

from dspacedashboard.imports.forms import ImportFileForm
from dspacedashboard.imports.models import FileImport

class ImportFileView(FormView):
    template_name = 'imports/import_file.html'
    success_message = 'Importação concluída com sucesso'
    form_class = ImportFileForm

    def get_collections(self):
        try:
            response = requests.get('http://localhost:8080/solr/search/select?q=search.resourcetype:3&fl=dc.title,handle&wt=json&omitHeader=true&rows=5000')
            raw_collections = json.loads(response.text)['response']['docs'] if response.status_code == 200 else []
            collections = ()
            for collection in raw_collections:                
                if collection.get('dc.title', None):
                    collections = collections + ((collection['handle'], collection['dc.title'][0]),)
            return collections
        except Exception as e:
            print("Error: ", e)
            return ()

    def get_form_kwargs(self):
        kwargs = super(ImportFileView, self).get_form_kwargs()
        kwargs.update({
		     'collections' : self.get_collections()
		})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ImportFileView, self).get_context_data()
        context['collections'] = self.get_collections()
        return context

    def get_success_url(self):		
        return reverse('import:file')

    def form_valid(self, form):
        form.save(self.request.user)
        messages.info(self.request, self.success_message)		
        return HttpResponseRedirect(self.get_success_url())

class ImportFileListView(ListView):
    template_name = 'imports/import_list.html'
    model = FileImport
