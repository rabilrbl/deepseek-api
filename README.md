# Deepseek coder API

Unofficial API for Deepseek (chat.deepseek.com)

## Installation

```bash
pip install git+https://github.com/rabilrbl/deepseek-api.git
```

## Usage

### CLI Example

```python
import os
from deepseek_api import DeepseekAPI
from dotenv import load_dotenv

load_dotenv()

email = os.environ.get("DEEPSEEK_EMAIL") # or type your email here
password = os.environ.get("DEEPSEEK_PASSWORD") # or type your password here

app = DeepseekAPI(
    email=email,
    password=password,
    save_login=True, # save login credentials to login.json
    model_class="deepseek_code" # Choose from "deepseek_code" or "deepseek_code"
)

print("""
        Usage:
        - Type 'new' to start a new chat.
        - Type 'exit' to exit.
        
        Start chatting!
""")

while True:
    message = input("> ")
    
    if message == "exit":
        break
    elif message == "new":
        app.new_chat()
        continue

    response = app.chat(message)

    for chunk in response:
        try:
            # keep printing in one line
            print(chunk["choices"][0]["delta"]["content"], end="")
        except KeyError as ke:
            print("Error: ", ke)
    print()
```
