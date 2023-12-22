# Deepseek coder Reverse Engineered API Wrapper

Unofficial API Wrapper for Deepseek (chat.deepseek.com) in Python. This is a reverse-engineered API for the Deepseek coder and Deepseek code chatbots. This API is not affiliated with Deepseek in any way.

## Installation

```bash
pip install git+https://github.com/rabilrbl/deepseek-api.git
```

## Usage

### Asynchronous CLI Example

```python
import asyncio
import os
from deepseek_api import DeepseekAPI
from dotenv import load_dotenv

load_dotenv()


async def main():
    email = os.environ.get("DEEPSEEK_EMAIL")
    password = os.environ.get("DEEPSEEK_PASSWORD")

    async with DeepseekAPI(
        email=email,
        password=password,
        save_login=True,  # save login credentials to login.json
        model_class="deepseek_code",  # Choose from "deepseek_code" or "deepseek_code"
    ) as app:
        print(
            """
            Usage:
                - Type 'new' to start a new chat.
                - Type 'exit' to exit.
                
            Start chatting!
        """
        )

        while True:
            message = input("> ")

            if message == "exit":
                break
            elif message == "new":
                await app.new_chat()
                continue

            async for chunk in app.chat(message):
                try:
                    # keep printing in one line
                    print(chunk["choices"][0]["delta"]["content"], end="")
                except KeyError as ke:
                    print(ke)
            print()


if __name__ == "__main__":
    asyncio.run(main())
```

### Synchonous CLI Example

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

## License

[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Disclaimer

This project is not affiliated with Deepseek in any way. Use at your own risk. This project was created for educational purposes only.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
