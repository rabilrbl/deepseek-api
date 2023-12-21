import requests
import json
from deepseek_api.constants import API_URL
from deepseek_api.errors import EmptyEmailOrPasswordError, NotLoggedInError

class DeepseekAPI:
    """A class to interact with the Deepseek API."""
    
    def __init__(self, email: str, password: str, model_class: str = "deepseek_code", save_login: bool = False):
        self.email = email
        self.password = password
        self.session = requests.Session()
        self.cookies = self.session.get('https://coder.deepseek.com/').cookies
        self.headers = {
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
            'x-app-version': '20231220.2',
        }
        self.credentials = {}
        self.model_class = model_class
        self.save_login = save_login
        self._login()
        
    def __repr__(self):
        return f"DeepseekAPI(email={self.email}, password={self.password}, model_class={self.model_class}, save_login={self.save_login})"
    
    def __del__(self):
        self.session.close()
        
    def _login(self):
        if self.save_login:
            try:
                with open("login.json", "r") as file:
                    self.credentials = json.load(file)
                    self.headers["authorization"] = "Bearer " + self.get_token()
                    return self.credentials
                
            except FileNotFoundError:
                pass
            
        if self.email == "" or self.password == "":
            raise EmptyEmailOrPasswordError
        
        json_data = {
            'email': self.email,
            'mobile': '',
            'password': self.password,
            'area_code': '',
        }
        
        response = self.session.post(API_URL.LOGIN, cookies=self.cookies, headers=self.headers, json=json_data)
        self.credentials = response.json()
        self.headers["authorization"] = "Bearer " + self.get_token()
        
        if self.save_login:
            with open("login.json", "w") as file:
                json.dump(self.credentials, file)
                
        return response.json()
    
    def is_logged_in(self):
        if self.credentials:
            return True
        else:
            return False
        
    def raise_for_not_logged_in(self):
        if not self.is_logged_in():
            raise NotLoggedInError
    
    def get_credentials(self):
        self.raise_for_not_logged_in()
        return self.credentials
    
    def get_token(self):
        self.raise_for_not_logged_in()
        return self.get_credentials()["data"]["user"]["token"]
        
    def new_chat(self):
        self.raise_for_not_logged_in()
        
        params = {
            "session_id": "1",
        }
        
        json_data = {
            'model_class': self.model_class,
            'append_welcome_message': False,
        }
        
        response = self.session.post(
            API_URL.CLEAR_CONTEXT,
            params=params,
            cookies=self.cookies,
            headers=self.headers,
            json=json_data,
        )

        return response.json()
    
    def chat(self, message: str, chunk_size: int = 512):
        self.raise_for_not_logged_in()
        
        json_data = {
            "message": message,
            "stream": True,
            "model_class": self.model_class,
            "model_preference": None,
            "temperature": 0,
        }
        
        with self.session.post(API_URL.CHAT, cookies=self.cookies, headers=self.headers, json=json_data, stream=True) as response:
            # Check if the request was successful (status code 200)
            response.raise_for_status()

            # Iterate over the content in chunks
            for line in response.iter_lines(chunk_size=chunk_size, decode_unicode=True):
                if line:
                    line = line.strip().replace("data: ", "")
                    line = json.loads(line)
                    if line["payload"] is None:  # Hack to fix initial empty payload
                        line["choices"][0]["delta"]["content"] = ""
                    yield line