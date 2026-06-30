import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

@api_view(['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def forward(request, service, path=''):
    # get base URL and the prefix that service uses in its own urls.py
    base_url, prefix = settings.SERVICE_URLS[service]
    # build full URL — base + /api/ + service prefix + rest of the path
    url = f'{base_url}/api/{prefix}/{path}' if prefix else f'{base_url}/api/{path}'

    # forward request to the target service using the same HTTP method
    if request.method == 'GET':
        response = requests.get(url)
    elif request.method == 'POST':
        response = requests.post(url, json=request.data)
    elif request.method == 'PUT':
        response = requests.put(url, json=request.data)
    elif request.method == 'DELETE':
        response = requests.delete(url)
    elif request.method == 'PATCH':
        response = requests.patch(url, json=request.data)

    # return the service response with its original status code
    return Response(response.json(), status=response.status_code)