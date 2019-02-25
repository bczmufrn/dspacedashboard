from django.urls import path

from dspacedashboard.core import views

app_name = 'core'
urlpatterns = [
	path('', views.HomePageView.as_view(), name='home'),
]
