import zipfile
import io
import os

from django.http import HttpResponse
from django.views import View
from django.utils import timezone

from dspacedashboard.scylax.models import Article

class ExportArticles(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.filter()[:1]

        formated_data = timezone.localtime(timezone.now()).strftime('%d_%m_%Y_%H_%M')
        zip_filename = f'ArtigosScylax_{formated_data}.zip'
        base_zip_filepath = os.path.join('ProducoesAcademicas', 'ScylaxUFRN')

        in_memory_zip = io.BytesIO()

        with zipfile.ZipFile(in_memory_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for index, article in enumerate(articles, 1):
                zipf.writestr(os.path.join(base_zip_filepath, str(index), 'dublin_core.xml'), article.to_xml())

        response = HttpResponse(in_memory_zip.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
        return response
