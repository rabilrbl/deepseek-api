import os
from deepseek_api import DeepseekAPI
from dotenv import load_dotenv

load_dotenv()

def main():
    email = os.environ.get("DEEPSEEK_EMAIL")
    password = os.environ.get("DEEPSEEK_PASSWORD")
    
    app = DeepseekAPI(
        email=email,
        password=password,
        save_login=True, # save login credentials to login.json
    )
    
    print("""
          Usage:
            - Type 'new' to start a new chat.
            - Type 'exit' to exit.
            
          Start chatting!
          \n\n
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
                print(ke)


if __name__ == "__main__":
    main()
