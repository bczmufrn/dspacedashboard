from django.urls import path

from dspacedashboard.imports import views

app_name = 'imports'
urlpatterns = [
	path('', views.ImportFileView.as_view(), name='file'),
	path('history/', views.ImportFileListView.as_view(), name='history'),
]
