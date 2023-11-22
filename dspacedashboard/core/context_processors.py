from django.conf import settings

def settings_variables(request):
    return {'ENABLE_SCYLAX': settings.ENABLE_SCYLAX}