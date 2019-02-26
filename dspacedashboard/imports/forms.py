from django import forms

from dspacedashboard.imports.models import FileImport

class ImportFileForm(forms.Form):

    collection = forms.ChoiceField(label='Coleção de destino')
    dspace_simple_archive = forms.FileField(label='Arquivo', allow_empty_file=False)

    def __init__(self, collections=(), *args, **kwargs):
        super(ImportFileForm, self).__init__(*args, **kwargs)

        self.fields['collection'] = forms.ChoiceField(label='Coleção', required=True, choices=collections)
        self.fields['dspace_simple_archive'].required = True