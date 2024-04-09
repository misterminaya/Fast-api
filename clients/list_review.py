import requests

URL = 'http://127.0.0.1:8000/api/v1/reviews'
HEADERS = {'Content-Type': 'application/json'}
QUERYSET = {'page': 1, 'limit': 10}

response = requests.get(URL,headers=HEADERS, params=QUERYSET)

if response.status_code == 200:
    print('Success!')
    
    if response.headers.get('content-type') == 'application/json':
        reviws = response.json()
        for review in reviws:
            print(f"> score: {review['score']} - {review['review']}")