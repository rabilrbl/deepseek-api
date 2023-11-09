import requests


def new_chat(token: str, cookies: dict = None) -> requests.Response:
    """
    Create a new chat

    Args:
        token (str): Bearer token

    Returns:
        requests.Response: Response object
    """

    headers = {
        "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "DNT": "1",
        "Origin": "https://coder.deepseek.com",
        "Pragma": "no-cache",
        "Referer": "https://coder.deepseek.com/chat",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/",
        "accept": "*/*",
        "authorization": "Bearer " + token,
        "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "x-app-version": "20231109.0",
    }

    params = {
        "session_id": "1",
    }

    response = requests.post(
        "https://coder.deepseek.com/api/v0/chat/clear_context",
        params=params,
        cookies=cookies,
        headers=headers,
    )

    return response.json()


if __name__ == "__main__":
    from login import get_token
    
    token = get_token()
    
    response = new_chat(token, cookies=cookies)
    print(response)
    
