import datetime
import zipfile
import io
import os
import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView
from django.urls import reverse

from dspacedashboard.scylax.models import Article
from dspacedashboard.scylax.forms import ScylaxSearchForm

class SearchArticlesView(FormView):
    template_name = 'scylax/search_articles.html'
    form_class = ScylaxSearchForm
    
    def form_valid(self, form):
        articles = Article.objects.filter(
            authors__departments__in=[form.cleaned_data['department']],
            exported=form.cleaned_data['include_exported'],
        ).distinct().order_by('-year')

        if form.cleaned_data.get('year', None):
            articles = articles.filter(
                year=datetime.datetime(form.cleaned_data['year'], 1, 1)
            )

        if form.cleaned_data.get('title', None):
            articles = articles.filter(title__icontains=form.cleaned_data['title'])

        if form.cleaned_data.get('author', None):
            articles = articles.filter(authors__name__icontains=form.cleaned_data['author'])

        return self.render_to_response(self.get_context_data(form=form, articles=articles, show_results=True))

    def get_success_url(self):
        return reverse('scylax:search')
    
class ArticleDetailAPIView(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        article_data = {
            'title': article.title,
            'year': article.year.year,
            'issn': article.issn,
            'exported': article.exported,
            'total_authors': article.authors.count(),
            'authors': [],
        }

        for author in article.authors.all().order_by('-departments__name', 'name'):
            author_data = {
                'name': author.name,
                'departments': []
            }
            for department in author.departments.all():
                author_data['departments'].append(department.name)

            article_data['authors'].append(author_data)

        jsondata = json.dumps(article_data)
        return HttpResponse(jsondata, content_type='application/json')

class ExportArticles(View):
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        article_pks = body.get('article_pks', None)
        mark_exported = body.get('mark_exported', False)

        if not article_pks:
            return HttpResponseBadRequest()

        articles = Article.objects.filter(pk__in=article_pks)

        if mark_exported:
            articles.update(exported=True)

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
