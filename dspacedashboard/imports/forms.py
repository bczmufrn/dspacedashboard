from django import forms

from dspacedashboard.imports.models import FileImport

class ImportFileForm(forms.ModelForm):

    def __init__(self, collections=(), *args, **kwargs):
        super(ImportFileForm, self).__init__(*args, **kwargs)

        self.fields['collection'] = forms.ChoiceField(label='Coleção', required=True, choices=collections)
        self.fields['dspace_simple_archive'].required = True

    def save(self, user, commit=True):
        import_file = super(ImportFileForm, self).save(commit=False)
        import_file.user = user    
        if commit:    
            import_file.save()

        return import_file
        
    class Meta:
        model = FileImport
        fields = ['collection', 'dspace_simple_archive']