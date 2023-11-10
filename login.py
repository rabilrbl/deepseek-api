import requests
import json


def _login(email, password, cookies=None):
    """
    Login to coder.deepseek.com

    Parameters
    ----------
    email : str
        Email address
    password : str
        Password
    cookies : dict, optional
        Cookies to be sent with the request

    Returns
    -------
    requests.Response
        Response object
    """
    headers = {
        'Accept-Language': 'en-IN,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://coder.deepseek.com',
        'Pragma': 'no-cache',
        'Referer': 'https://coder.deepseek.com/sign_in',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome',
        'accept': '*/*',
        'content-type': 'application/json',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'x-app-version': '20231109.0',
    }

    json_data = {
        'email': email,
        'mobile': '',
        'password': password,
        'area_code': '',
    }

    response = requests.post('https://coder.deepseek.com/api/v0/users/login', cookies=cookies, headers=headers, json=json_data)

    return response.json()

def get_user():
    import os
    # check if login.json exists
    if not os.path.isfile('login.json'):
        print("login.json not found. Please run login.py first")
        exit(1)
    # return json of login.json
    file = open('login.json', 'r')
    login_json = json.load(file)
    file.close()
    return login_json

def get_token():
    # return token from login.json
    login_json = get_user()
    return login_json["data"]["user"]["token"]

def do_login(email, password):
    cookies = requests.get('https://coder.deepseek.com/').cookies
    return _login(email, password, cookies=cookies)

if __name__ == '__main__':
    import sys
    import getpass

    if len(sys.argv) == 1:
        email = input('Email: ')
        password = getpass.getpass('Password: ')
    elif len(sys.argv) == 2:
        email = sys.argv[1]
        password = getpass.getpass('Password: ')
    elif len(sys.argv) == 3:
        email = sys.argv[1]
        password = sys.argv[2]
    else:
        print('Usage: python3 login.py [email] [password]')
        sys.exit(1)
        
    cookies = requests.get('https://coder.deepseek.com/').cookies

    response = _login(email, password, cookies=cookies)
    with open('login.json', 'w') as f:
        json.dump(response, f, indent=4)
        
    print("Successfully generated login.json. Now you can use login function")
