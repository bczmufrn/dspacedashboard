from django.urls import path

from dspacedashboard.autopermission import api, views

app_name = 'autopermission'

urlpatterns = [
	path('list/', views.AutopermissionUserListView.as_view(), name='list'),
	path('api/create/', api.autopermission_create, name='create'),
]
