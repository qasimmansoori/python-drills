from pydantic import BaseModel, Field

class UserModel(BaseModel):
    username: str = Field(alias="login")
    id: int
    public_repos: int
    followers: int
    bio: str | None = None


