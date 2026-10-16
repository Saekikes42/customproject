from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base


class Role(Base):
    __tablename__ = "Roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("Roles.id"), nullable=False)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    display_name = Column(String(60), nullable=False)
    is_blocked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Genre(Base):
    __tablename__ = "Genres"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)


class Lobby(Base):
    __tablename__ = "Lobbies"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    genre_id = Column(Integer, ForeignKey("Genres.id"), nullable=False)
    name = Column(String(100), nullable=False)
    invite_code = Column(String(20), unique=True, nullable=False)
    status = Column(String(25), default="collecting")
    created_at = Column(DateTime, default=datetime.utcnow)


class LobbyMember(Base):
    __tablename__ = "Lobby_Members"

    lobby_id = Column(Integer, ForeignKey("Lobbies.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"), primary_key=True)
    joined_at = Column(DateTime, default=datetime.utcnow)


class Idea(Base):
    __tablename__ = "Ideas"

    id = Column(Integer, primary_key=True)
    lobby_id = Column(Integer, ForeignKey("Lobbies.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    body = Column(Text, nullable=False)
    status = Column(String(25), default="proposed")
    created_at = Column(DateTime, default=datetime.utcnow)


class Generation(Base):
    __tablename__ = "Generations"

    id = Column(Integer, primary_key=True)
    lobby_id = Column(Integer, ForeignKey("Lobbies.id"), nullable=False)
    requester_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    ai_model = Column(String(60), nullable=False)
    cost_credits = Column(Integer, default=1)
    status = Column(String(25), default="succeeded")
    created_at = Column(DateTime, default=datetime.utcnow)

    lobby = relationship("Lobby")


class Game(Base):
    __tablename__ = "Games"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    genre_id = Column(Integer, ForeignKey("Genres.id"), nullable=False)
    lobby_id = Column(Integer, ForeignKey("Lobbies.id"), nullable=True)
    name = Column(String(120), nullable=False)
    description = Column(String(1000), nullable=False)
    publication_status = Column(String(25), default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)


class GameVersion(Base):
    __tablename__ = "Game_Versions"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("Games.id"), nullable=False)
    generation_id = Column(Integer, ForeignKey("Generations.id"), nullable=True)
    version_number = Column(Integer, default=1)
    html_file = Column(String(255), nullable=False)
    source_type = Column(String(20), default="ai")
    created_at = Column(DateTime, default=datetime.utcnow)
