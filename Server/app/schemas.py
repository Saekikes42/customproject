"""Input data for the small educational API."""

from pydantic import BaseModel, ConfigDict, Field


class RequestData(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


class UserCreate(RequestData):
    role_id: int = Field(gt=0)
    telegram_id: int = Field(gt=0)
    display_name: str = Field(min_length=2, max_length=60)


class GenreCreate(RequestData):
    name: str = Field(min_length=2, max_length=50)


class GameCreate(RequestData):
    name: str = Field(min_length=2, max_length=120)
    description: str = Field(min_length=2, max_length=1000)
    genre_id: int = Field(gt=0)
    author_id: int = Field(gt=0)


class LobbyCreate(RequestData):
    owner_id: int = Field(gt=0)
    genre_id: int = Field(gt=0)
    name: str = Field(min_length=2, max_length=100)
    invite_code: str = Field(min_length=4, max_length=20, pattern=r"^[A-Za-z0-9_-]+$")


class LobbyMemberAdd(RequestData):
    user_id: int = Field(gt=0)


class IdeaCreate(RequestData):
    author_id: int = Field(gt=0)
    body: str = Field(min_length=3, max_length=500)


class GameGenerateRequest(RequestData):
    requester_id: int = Field(gt=0)


class GameSaveFromGeneration(RequestData):
    author_id: int = Field(gt=0)
    name: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = Field(default=None, min_length=2, max_length=1000)


class UserUpdate(RequestData):
    display_name: str = Field(min_length=2, max_length=60)


class GenreUpdate(RequestData):
    name: str = Field(min_length=2, max_length=50)


class GameUpdate(RequestData):
    name: str = Field(min_length=2, max_length=120)
    description: str = Field(min_length=2, max_length=1000)


class LobbyUpdate(RequestData):
    name: str = Field(min_length=2, max_length=100)


class IdeaUpdate(RequestData):
    body: str = Field(min_length=3, max_length=500)
