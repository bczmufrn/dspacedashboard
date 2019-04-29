from django.urls import path

from dspacedashboard.accounts import views

app_name = 'accounts'

urlpatterns = [
	path('', views.user_list, name='user_list'),
	path('usuario/novo/', views.user_create, name='user_create'),
	path('usuario/editar/<uuid:pk>/', views.user_update, name='user_update'),
	path('usuario/redefinir-senha/<uuid:pk>/', views.reset_password, name='reset_password'),
]
