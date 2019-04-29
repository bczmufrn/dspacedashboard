from django.urls import path

from dspacedashboard.imports import views

app_name = 'imports'
urlpatterns = [
	path('', views.import_file, name='file'),
	path('history/', views.ImportFileListView.as_view(), name='history'),
	path('history/<uuid:pk>/', views.ImportLogDetailView.as_view(), name='log'),
]
