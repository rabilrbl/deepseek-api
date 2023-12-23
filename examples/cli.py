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
        model_class="deepseek_code",  # Choose from "deepseek_chat" or "deepseek_code"
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
