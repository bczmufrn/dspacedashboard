from django.urls import path

from dspacedashboard.scylax import views

app_name = 'scylax'
urlpatterns = [
	path('exportar/', views.ExportArticles.as_view(), name='export'),
]
