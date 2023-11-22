import datetime
import pandas as pd

from django.core.management.base import BaseCommand

from dspacedashboard.scylax.models import AcademicCenter, Department, Author, Article


class Command(BaseCommand):
    help = 'Importa dados do CSV para database do dspacedashboard'

    # def add_arguments(self, parser):
    #     parser.add_argument('filename', nargs=1, type=str)

    def handle(self, *args, **kwargs):
        df = pd.read_csv('import/data-scylax.csv', converters={'nome_normalizado': str.strip})

        print("# Criando centros acadêmicos")
        academic_centers_df = df[['id_centro', 'nome_centro']].dropna()
        academic_centers_df = academic_centers_df.astype({'id_centro': int})
        academic_centers_df = academic_centers_df.drop_duplicates()

        for _, row in academic_centers_df.iterrows():
            academic_center, created = AcademicCenter.objects.update_or_create(
                id_scylax=row['id_centro'], 
                defaults={'name': row['nome_centro']}
            )
            print(f'{"Criado" if created else "Atualizado"} centro {academic_center.name}')

        print("# Criando departamentos")
        departments_df = df[['id_departamento', 'nome_departamento', 'id_centro']].dropna()
        departments_df = departments_df.astype({'id_departamento': int})
        departments_df = departments_df.drop_duplicates(subset=['id_departamento', 'nome_departamento'])

        for _, row in departments_df.iterrows():
            academic_center = AcademicCenter.objects.get(id_scylax=row['id_centro'])
            department, created = Department.objects.update_or_create(
                id_scylax=row['id_departamento'],
                academic_center=academic_center,
                defaults={'name':row['nome_departamento']}
            )
            print(f'{"Criado" if created else "Atualizado"} departamento {department.name}')

        print("# Criando autores")
        authors_df = df[['id_producao', 'nome_normalizado', 'id_lattes', 'id_departamento']].fillna(0)
        #authors_df['nome_normalizado'] = authors_df['nome_normalizado'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        authors_df = authors_df.astype({'id_lattes': 'Int64', 'id_departamento': int})
        authors_df = authors_df.drop_duplicates().reset_index(drop=True)

        for _, row in authors_df.iterrows():
            author, created = Author.objects.get_or_create(
                name=row['nome_normalizado'], 
                defaults={'id_lattes': 0}
            )

            if row['id_lattes'] > 0 and author.id_lattes == 0:
                author.id_lattes=row['id_lattes']
                author.save()

            if row['id_departamento']:
                department = Department.objects.get(id_scylax=row['id_departamento'])
                author.departments.add(department)

            print(f'{"Criado" if created else "Atualizado"} autor {author.name}. Departamentos: {list(author.departments.all().values_list("name"))}')


        print("# Criando artigos")
        articles_df = df[['id_producao', 'titulo_normalizado', 'ano', 'issn']].fillna(0)
        articles_df = articles_df.drop_duplicates().reset_index(drop=True)
        articles_df = articles_df.astype({'titulo_normalizado': str})

        for _, row in articles_df.iterrows():
            article, created = Article.objects.get_or_create(
                id_scylax=row['id_producao'],
                defaults={
                    'title': row['titulo_normalizado'][:2048],
                    'year': datetime.date(row['ano'], 1, 1),
                    'issn': row['issn'],
                }
            )

            article_authors_df = df[df['id_producao'] == article.id_scylax]
            article_authors_df = article_authors_df[['nome_normalizado', 'id_lattes']].drop_duplicates().fillna(0)
            article_authors_df = article_authors_df.astype({'id_lattes': 'Int64'})

            for _, author_row in article_authors_df.iterrows():
                authors = Author.objects.filter(
                    name=author_row['nome_normalizado'],
                )
                
                if authors.count() == 1:
                    article.authors.add(authors.first())
                elif authors.count() > 1:
                    article.authors.add(authors.filter(id_lattes=author_row['id_lattes']).first())

            print(f'{"Criado" if created else "Atualizado"} artigo de ID {article.id_scylax}. Número de autores: {article.authors.count()}')