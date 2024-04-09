import requests

URL = 'http://127.0.0.1:8000/api/v1/users/'
USER = {
    'username': 'carlitos',
    'password': 'DFG3495I'
}

response = requests.post(URL + 'login', json=USER)

if response.status_code == 200:
    print('Login Success!')

    user_id = response.cookies.get_dict().get('user_id')

    _cookies = {'user_id': user_id}
    response = requests.get(URL + 'reviews', cookies=_cookies)
    print(response.request.url)
    print(response.request.headers)
    print(response.request._cookies)
    
    try:
        data = response.json()
        print(data)
    except ValueError:
        print('No data', response.text)    

else:
    print('Error:', response.status_code)
    print(response.text)