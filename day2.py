import httpx
from pydantic import BaseModel, Field




class userModel(BaseModel):
    id: int
    username: str = Field(alias="login")
    followers: int
    bio: str | None = None

response = httpx.get("https://api.github.com/users/qasimmansoori")

if response.status_code == 200:
    data = response.json()
    clean_user = userModel(**data)
    print(f"id: {clean_user.id}, \nusername: {clean_user.username}, \nfollowers: {clean_user.followers}, \nBio: {clean_user.bio}")
else:
    print(f"User dont exists")