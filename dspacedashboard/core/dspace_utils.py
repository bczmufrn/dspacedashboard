import requests, json

from django.conf import settings
from django.core.cache import cache

def get_collections():  
    if collections := cache.get('collections', []):
        return collections
    
    try:
        response = requests.get(f'{settings.SOLR_URL}/server/api/core/collections?size=1000')
        collections = json.loads(response.text)['_embedded']['collections'] if response.status_code == 200 else []
        cache.set('collections', collections, 6 * 3600)
    except Exception as e:
        print("Error: ", e)
    return collections