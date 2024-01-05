class API_URL:
    """Deepseek API URL constants"""

    BASE_URL = "https://coder.deepseek.com/api/v0"
    LOGIN = BASE_URL + "/users/login"
    CLEAR_CONTEXT = BASE_URL + "/chat/clear_context"
    CHAT = BASE_URL + "/chat/completions"


class DeepseekConstants:
    """Deepseek constants"""

    BASE_HEADERS = {
        "Accept-Language": "en-IN,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "DNT": "1",
        "Origin": "https://coder.deepseek.com",
        "Pragma": "no-cache",
        "Referer": "https://coder.deepseek.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome",
        "accept": "*/*",
        "content-type": "application/json",
        "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "x-app-version": "20240105.0",
    }
