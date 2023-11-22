from django.urls import path

from dspacedashboard.scylax import views

app_name = 'scylax'
urlpatterns = [
	path('buscar/', views.SearchArticlesView.as_view(), name='search'),
	path('exportar/', views.ExportArticles.as_view(), name='export'),
	path('api/artigo/<uuid:pk>', views.ArticleDetailAPIView.as_view(), name='article_api'),
]
