import json
import requests

def chat(
    message: str,
    token: str,
    cookies: dict = None,
) -> None:
    """
    Send a message to coder.deepseek.com

    Args:
        message (string): Message to send
        token (string): Bearer token
        cookies (dict, optional): Cookies to be sent with the request. Defaults to None.
    
    Returns:
        Stream of bytes
    """

    headers = {
        "Accept-Language": "en-IN,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "DNT": "1",
        "Origin": "https://coder.deepseek.com",
        "Pragma": "no-cache",
        "Referer": "https://coder.deepseek.com/chat",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome",
        "accept": "*/*",
        "authorization": "Bearer " + token,
        "content-type": "application/json",
        "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "x-app-version": "20231109.0",
    }

    json_data = {
        "message": message,
        "stream": True,
        "model_class": "deepseek_code",
        "model_preference": None,
        "temperature": 0,
    }
    
    try:
        with requests.post("https://coder.deepseek.com/api/v0/chat/completions",
        cookies=cookies,
        headers=headers,
        json=json_data, stream=True) as response:
            # Check if the request was successful (status code 200)
            response.raise_for_status()

            # Iterate over the content in chunks
            for line in response.iter_lines():
                if line:
                    yield line
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    from login import get_token
    from newchat import new_chat
    # Get the token from the user
    token = get_token()
    
    while True:
        message = input("Message: ")
        if message == "exit":
            break
        elif message == "/clear":
            print("\033[H\033[J")
            continue
        elif message == "/new":
            new_chat(token)
            print("New chat started...")
            continue
        print()
        # Send a message
        for chunk in chat(message, token):
            chunk = chunk.strip().decode("utf-8").replace("data: ", "")
            json_chunk = json.loads(chunk)
            try:
                # keep printing in one line
                print(json_chunk["choices"][0]["delta"]["content"], end="")
            except KeyError:
                pass
        print()
        print("-"*30,end="\n\n")
