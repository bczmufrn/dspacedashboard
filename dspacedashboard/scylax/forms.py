from django import forms

from dspacedashboard.scylax.models import Department

class ScylaxSearchForm(forms.Form):
    title = forms.CharField(label='Título da produção', required=False)
    author = forms.CharField(label='Nome do autor', required=False)
    year = forms.IntegerField(label='Ano de publicação', required=False)
    include_exported = forms.BooleanField(label='Apenas artigos já exportados', required=False)

    department = forms.ModelChoiceField(
        queryset=Department.objects.all().order_by('name'),
        label='Departamento*', 
        required=True, 
        empty_label='Selecione o departamento...'
    )