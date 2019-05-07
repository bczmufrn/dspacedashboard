from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views

from dspacedashboard.accounts import views

app_name = 'accounts'

urlpatterns = [
	path('entrar/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
	path('sair/', auth_views.LogoutView.as_view(next_page=settings.LOGOUT_URL), name='logout'),
	path('alterar-senha/', views.update_password, name='update_password'),

	path('', views.user_list, name='user_list'),
	path('usuario/novo/', views.user_create, name='user_create'),
	path('usuario/editar/<uuid:pk>/', views.user_update, name='user_update'),
	path('usuario/redefinir-senha/<uuid:pk>/', views.reset_password, name='reset_password'),
]
