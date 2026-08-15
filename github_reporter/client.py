import httpx
import asyncio
from .models import UserModel

# client = httpx.AsyncClient()

async def fetch_user(client: httpx.AsyncClient, username: str) -> UserModel | None:
    try:
        response = await client.get(f"https://api.github.com/users/{username}")
        # response.raise_for_status()
        if response.status_code == 200:
            data = response.json()
            return UserModel(**data)
        elif response.status_code == 404:
            print(f"username: {username} not found")
        elif response.status_code == 403:
            print("rate limit exceeded")
        
        else:
            print(f"HTTP error: {response.status_code} for the {username}")

    except Exception as e:
        print(f"Error: {e}")


async def fetch_all_users(usernames: list[str]):
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            *[fetch_user(client, user) for user in usernames]
        )
        return results



