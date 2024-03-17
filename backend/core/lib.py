import requests
import json

from django.conf import settings

def cse_search(params):
    params.update(settings.CSE_PARAMS)
    response = requests.get(settings.CSE_URL, params=params)
    return response.json()

def get_search_results(context: dict) -> dict:
    if not context.get('q'):
        return {}

    try:  
        params = {
            **context,
            # 'q' : context.get('q'),  # Specify the search query
            # 'num' : context.get('num', 10),  # Specify the number of results to return (default: 10)
            # 'start' : context.get('start', 1),  # Specify the index of the first result to return (default: 1)
            # 'filter' : context.get('filter', 1),  # Specify whether to filter similar results (default: 1)
            # 'safe' : context.get('safe', 'off'),  # Specify the safe search level (default: 'off')
            # 'fields' : context.get('fields', 'items(title,link)'),  # Specify the fields to include in the response (default: 'items(title,link)')
            # 'sort' : context.get('sort', 'relevance'),  # Specify the sorting order of the results (default: 'relevance')
            # 'searchType' : context.get('searchType', 'image'),  # Specify the search type (default: 'image', options: 'image', 'video', 'news', 'froogle', 'local')
            
            # 'siteSearch' : context.get('siteSearch'),  # Restricts results to URLs from a specified site
            # 'siteSearchFilter' : context.get('siteSearchFilter'),  # Controls whether to include or exclude results from the site named in the siteSearch parameter (default: 'e')
        }

        json_response = cse_search(params)
        return json_response
    except Exception as e:
        return {
            'error': 'Something went wrong',
            'details': str(e)
        }

def get_page_content(link: str):
    try:
        response = requests.get(link)
        return response.text
    except Exception as e:
        return {
            'error': 'Something went wrong',
            'details': str(e)
        }
    
