import requests

URL = 'http://127.0.0.1:8000/api/v1/reviews'
REVIEW = {'user_id': 1, 'movie_id': 2, 'review': 'Great movie!', 'score': 5}

response = requests.post(URL, json=REVIEW)

if response.status_code == 200:
    print('Success!')
    print(response.json()['id'])
    
else:
    print('Error:', response.status_code)