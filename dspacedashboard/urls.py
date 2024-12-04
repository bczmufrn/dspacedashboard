"""dspacedashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('', include('dspacedashboard.core.urls', namespace='core')),
    path('import/', include('dspacedashboard.imports.urls', namespace='import')),
    path('scylax/', include('dspacedashboard.scylax.urls', namespace='scylax')),
    path('conta/', include('dspacedashboard.accounts.urls', namespace='accounts')),
    path('autopermission/', include('dspacedashboard.autopermission.urls', namespace='autopermission')),
    path('admin/', admin.site.urls),
]
