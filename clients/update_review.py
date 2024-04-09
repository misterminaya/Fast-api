import requests

REVIEW_ID = 10
URL = f'http://127.0.0.1:8000/api/v1/reviews{REVIEW_ID}'


REVIEW = {
    'review': 'Great movie Update! 1',
    'score': 5
}
response = requests.put(URL, json= REVIEW)

if response.status_code == 200:
    print('Success!')
    print(response.json())

