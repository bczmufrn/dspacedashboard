from django.contrib import admin
from django.db.models import Count

from dspacedashboard.scylax.models import AcademicCenter, Department, Author, Article

admin.site.register([AcademicCenter])

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
	list_display = ('name', 'academic_center')
	list_filter = ('academic_center', )
	search_fields = ('name', )

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	search_fields = ('name', 'id_lattes')
	list_display = ('name', 'id_lattes', 'department_list', )
	
	def department_list(self, obj):
		return "\n".join([d.name for d in obj.departments.all()])

class AuthorInline(admin.TabularInline):
	model = Article.authors.through
	readonly_fields = ('author', 'author_lattes', 'department_list', )
	extra = 0
	can_delete = False

	def author_lattes(self, obj):
		return obj.author.id_lattes

	def department_list(self, obj):
		return "\n".join([d.name for d in obj.author.departments.all()])
	
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	search_fields = ('title', 'issn', 'id_scylax')
	readonly_fields = ('id_scylax', 'issn', 'authors', 'title', 'year')
	list_display = ('title', 'authors_count', 'year', )
	inlines = [
		AuthorInline,
	]

	def get_queryset(self, request):
		qs = super(ArticleAdmin, self).get_queryset(request)
		return qs.annotate(authors_count=Count('authors'))

	def authors_count(self, obj):
		return obj.authors_count
	
	authors_count.admin_order_field = 'authors_count'