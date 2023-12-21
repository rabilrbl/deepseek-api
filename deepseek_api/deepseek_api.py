import requests
import json
import threading
import jwt
import datetime
from deepseek_api.constants import API_URL
from deepseek_api.errors import EmptyEmailOrPasswordError, NotLoggedInError

class DeepseekAPI:
    """
    A class to interact with the Deepseek API.
    """
    
    def __init__(self, email: str, password: str, model_class: str = "deepseek_code", save_login: bool = False):
        """Constructor method

        Args:
            email (str): Email of account from chat.deepseek.com
            password (str): Password of account from chat.deepseek.com
            model_class (str, optional): Deepseek model name "deepseek_chat" or "deepseek_code". Defaults to "deepseek_code".
            save_login (bool, optional): Save credentials to login.json. This will prevent login function from being called multiple times in constructor. Defaults to False.
        """
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
        self.login()
        
    def __repr__(self):
        """Representation method

        Returns:
            str: String representation of DeepseekAPI object
        """
        return f"DeepseekAPI(email={self.email}, password={self.password}, model_class={self.model_class}, save_login={self.save_login})"
    
    def __del__(self):
        """Destructor method
        """
        self.session.close()
        self._scheduled_token_object.cancel()
        
    def _login(self):
        """Login method

        Raises:
            EmptyEmailOrPasswordError: If email or password is empty

        Returns:
            dict: Login JSON response
        """
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
    
    def login(self):
        """Login method wrapper
        """
        if self.save_login:
            try:
                with open("login.json", "r") as file:
                    self.credentials = json.load(file)
                    self.headers["authorization"] = "Bearer " + self.get_token()
            except FileNotFoundError:
                self._login()
        else:
            self._login()
        # schedule the update token function
        self.__schedule_update_token()
    
    def __schedule_update_token(self) -> None:
        """Schedule the update token function as token expires every 7 days
        """
        # Decode the JWT token
        token = self.get_token()
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        
        # Fetch the 'exp' value and subtract 1 day
        exp_time = datetime.datetime.fromtimestamp(decoded_token['exp']) - datetime.timedelta(days=1)

        # Calculate the time difference in seconds
        time_diff = (exp_time - datetime.datetime.now()).total_seconds()

        # Schedule the execution
        thread_timer_obj = threading.Timer(time_diff, self._login)
        thread_timer_obj.start()
        self._scheduled_token_object = thread_timer_obj
    
    def is_logged_in(self):
        """Check if user is logged in

        Returns:
            bool: True if logged in, False otherwise
        """
        if self.credentials:
            return True
        else:
            return False
        
    def raise_for_not_logged_in(self):
        """Raise NotLoggedInError if user is not logged in

        Raises:
            NotLoggedInError: If user is not logged in
        """
        if not self.is_logged_in():
            raise NotLoggedInError
    
    def get_credentials(self):
        """Get credentials

        Returns:
            dict: Credentials JSON data from login response
        """
        self.raise_for_not_logged_in()
        return self.credentials
    
    def get_token(self):
        """Get token

        Returns:
            str: JWT Authorization token
        """
        self.raise_for_not_logged_in()
        return self.get_credentials()["data"]["user"]["token"]
        
    def new_chat(self):
        """Start a new chat

        Returns:
            dict: Clear context JSON response from deepseek API
        """
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
        """Chat with the deepseek API

        Args:
            message (str): Prompt message
            chunk_size (int, optional): Chunk size for streaming. Defaults to 512.

        Yields:
            dict: Response JSON data from deepseek API
        """
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
                    line: dict = json.loads(line)
                    if line.get("payload", None) is None:  # Hack to fix initial empty payload
                        line["choices"][0]["delta"]["content"] = ""
                    yield line