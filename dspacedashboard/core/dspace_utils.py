import requests, json

from django.conf import settings

def get_collections():  
    collections = []   
    try:        
        response = requests.get(f'{settings.SOLR_URL}/search/select?q=search.resourcetype:3&fl=dc.title,handle&wt=json&omitHeader=true&rows=5000')
        collections = json.loads(response.text)['response']['docs'] if response.status_code == 200 else []
    except Exception as e:
        print("Error: ", e)        
    return collections