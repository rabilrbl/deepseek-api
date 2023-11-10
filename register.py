import requests


def register(email, email_verification_code, password):
    """
    Register a new user

    Parameters
    ----------
    email : str
        Email address
    email_verification_code : str
        Email verification code
    password : str
        Password
    cookies : dict, optional
        Cookies to be sent with the request

    Returns
    -------
    requests.Response
        Response object
    """
    cookies = requests.get('https://coder.deepseek.com/').cookies

    headers = {
        'Accept-Language': 'en-IN,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://coder.deepseek.com',
        'Pragma': 'no-cache',
        'Referer': 'https://coder.deepseek.com/sign_up',
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
        'locale': 'en_US',
        'region': 'IN',
        'payload': {
            'email': email,
            'email_verification_code': email_verification_code,
            'password': password,
        },
    }

    response = requests.post('https://coder.deepseek.com/api/v0/users/register', cookies=cookies, headers=headers, json=json_data)

    return response.json()


def create_email_verification_code(email: str) -> dict:
    """
    Create email verification code

    Parameters
    ----------
    email : str
        Email address
    cookies : dict, optional
        Cookies to be sent with the request

    Returns
    -------
    requests.Response
        Response object
    """
    cookies = requests.get('https://coder.deepseek.com/').cookies
    
    headers = {
        'Accept-Language': 'en-IN,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://coder.deepseek.com',
        'Pragma': 'no-cache',
        'Referer': 'https://coder.deepseek.com/sign_up',
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
        'locale': 'en_US',
    }

    response = requests.post(
        'https://coder.deepseek.com/api/v0/users/create_email_verification_code',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    return response.json()


if __name__ == '__main__':
    import json
    import getpass

    email = input('Email: ')
    password = getpass.getpass('Password: ')
    
    response = create_email_verification_code(email)
    print(json.dumps(response, indent=4))
    
    email_verification_code = input('Email verification code: ')
    
    response = register(email, email_verification_code, password)
    print(json.dumps(response, indent=4))
