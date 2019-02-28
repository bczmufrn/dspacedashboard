from django import forms

from dspacedashboard.imports.models import FileImport

class ImportFileForm(forms.Form):

    collection = forms.ChoiceField(label='Coleção de destino')
    dspace_simple_archive = forms.FileField(label='Arquivo', allow_empty_file=False, required=True)

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('collections', ())
        super(ImportFileForm, self).__init__(*args, **kwargs)

        self.fields['collection'] = forms.ChoiceField(label='Coleção', required=True, choices=choices)