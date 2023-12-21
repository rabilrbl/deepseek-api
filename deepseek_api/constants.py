class API_URL:
    """Deepseek API URL constants
    """
    BASE_URL = "https://coder.deepseek.com/api/v0"
    LOGIN = BASE_URL + "/users/login"
    CLEAR_CONTEXT = BASE_URL + "/chat/clear_context"
    CHAT = BASE_URL + "/chat/completions"