from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    role_id: int
    telegram_id: int
    display_name: str


class GenreCreate(BaseModel):
    name: str


class GameCreate(BaseModel):
    name: str
    description: str
    genre_id: int
    author_id: int
    publication_status: Optional[str] = "draft"


class LobbyCreate(BaseModel):
    owner_id: int
    genre_id: int
    name: str
    invite_code: str
    status: Optional[str] = "collecting"


class LobbyMemberAdd(BaseModel):
    user_id: int


class IdeaCreate(BaseModel):
    author_id: int
    body: str


class GameGenerateRequest(BaseModel):
    requester_id: int
    ai_model: Optional[str] = "gpt-4o"
    cost_credits: Optional[int] = 50


class GameSaveFromGeneration(BaseModel):
    author_id: int
    name: Optional[str] = None
    description: Optional[str] = None
    publication_status: Optional[str] = "draft"
    html_file: Optional[str] = None
