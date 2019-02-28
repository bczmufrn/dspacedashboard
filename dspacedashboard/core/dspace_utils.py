import requests, json

def get_collections():  
    collections = []   
    try:
        response = requests.get('http://localhost:8080/solr/search/select?q=search.resourcetype:3&fl=dc.title,handle&wt=json&omitHeader=true&rows=5000')
        collections = json.loads(response.text)['response']['docs'] if response.status_code == 200 else []
    except Exception as e:
        print("Error: ", e)        
    return collections