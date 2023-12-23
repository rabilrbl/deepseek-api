import os
from deepseek_api import SyncDeepseekAPI
from dotenv import load_dotenv

load_dotenv()


def main():
    email = os.environ.get("DEEPSEEK_EMAIL")
    password = os.environ.get("DEEPSEEK_PASSWORD")

    app = SyncDeepseekAPI(
        email=email,
        password=password,
        save_login=True,  # save login credentials to login.json
        model_class="deepseek_code",  # Choose from "deepseek_chat" or "deepseek_code"
    )

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
            # close the app
            app.close()
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
        print()


if __name__ == "__main__":
    main()
