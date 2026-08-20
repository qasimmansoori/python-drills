import asyncio
import time
import httpx
from pydantic import BaseModel, Field

# 1. Pydantic Schema for GitHub API User
class UserModel(BaseModel):
    username: str = Field(alias="login")
    id: int
    public_repos: int
    followers: int
    bio: str | None = None


USERS = ["qasimmansoori", "torvalds", "tiangolo", "psf", "python"]


# Helper function to print clean user profile cards
def print_user_card(user: UserModel):
    bio_clean = user.bio.strip().replace("\r\n", " ") if user.bio else "No bio provided"
    print(f"👤 {user.username} (ID: {user.id})")
    print(f"   📦 Repos: {user.public_repos} | 👥 Followers: {user.followers}")
    print(f"   📝 Bio: {bio_clean}")
    print("-" * 55)


# 2. Synchronous Fetch (One by One)
def fetch_user_sync(user: str) -> UserModel:
    raw_data = httpx.get(f"https://api.github.com/users/{user}").json()
    return UserModel(**raw_data)


def run_sync_benchmark():
    print("\n--- 🐢 Synchronous Fetching ---")
    start = time.perf_counter()
    for user in USERS:
        user_model = fetch_user_sync(user)
        print_user_card(user_model)
    end = time.perf_counter()
    sync_duration = end - start
    print(f"Sync Total Time: {sync_duration:.2f}s\n")
    return sync_duration


# 3. Asynchronous Fetch (Concurrent with HTTP Connection Pooling)
async def fetch_user_async(client: httpx.AsyncClient, user: str) -> UserModel:
    response = await client.get(f"https://api.github.com/users/{user}")
    return UserModel(**response.json())


async def run_async_benchmark():
    print("--- ⚡ Asynchronous Fetching ---")
    start = time.perf_counter()
    
    # Reuse 1 HTTP client session for all concurrent requests
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            *[fetch_user_async(client, user) for user in USERS]
        )
        
    for user_model in results:
        print_user_card(user_model)
        
    end = time.perf_counter()
    async_duration = end - start
    print(f"Async Total Time: {async_duration:.2f}s\n")
    return async_duration



# 4. Main Execution & Comparison
if __name__ == "__main__":
    sync_time = run_sync_benchmark()
    async_time = asyncio.run(run_async_benchmark())
    
    speedup = sync_time / async_time if async_time > 0 else 0
    print("=" * 45)
    print(f"⚡ BENCHMARK RESULT: Async was {speedup:.1f}x faster!")
    print("=" * 45)