import asyncio
import os
from deepseek_api import DeepseekAPI
from dotenv import load_dotenv

load_dotenv()


async def main():
    email = os.environ.get("DEEPSEEK_EMAIL")
    password = os.environ.get("DEEPSEEK_PASSWORD")

    app = await DeepseekAPI.create(email=email, password=password, model_class="deepseek_code", save_login=True)
    
    async for chunk in app.chat("hi"):
        print(chunk["choices"][0]["delta"]["content"], end="")
        
    print()
    await app.close()


if __name__ == "__main__":
    asyncio.run(main())
