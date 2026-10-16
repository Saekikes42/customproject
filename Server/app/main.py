from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from .database import get_db
from . import models, schemas

app = FastAPI(title="GameForge")


@app.get("/")
def root():
    return {"message": "Сервер работает"}


@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok"}


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    result = []
    for u in users:
        result.append({
            "id": u.id,
            "role_id": u.role_id,
            "telegram_id": u.telegram_id,
            "display_name": u.display_name,
            "is_blocked": u.is_blocked,
            "created_at": u.created_at
        })
    return result


@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return {
        "id": user.id,
        "role_id": user.role_id,
        "telegram_id": user.telegram_id,
        "display_name": user.display_name,
        "is_blocked": user.is_blocked,
        "created_at": user.created_at
    }


@app.post("/users")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(
        role_id=user.role_id,
        telegram_id=user.telegram_id,
        display_name=user.display_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "id": new_user.id,
        "role_id": new_user.role_id,
        "telegram_id": new_user.telegram_id,
        "display_name": new_user.display_name,
        "created_at": new_user.created_at
    }


@app.get("/games")
def get_games(db: Session = Depends(get_db)):
    games = db.query(models.Game).all()
    result = []
    for g in games:
        result.append({
            "id": g.id,
            "name": g.name,
            "description": g.description,
            "genre_id": g.genre_id,
            "author_id": g.author_id,
            "publication_status": g.publication_status,
            "created_at": g.created_at
        })
    return result


@app.get("/games/{game_id}")
def get_game(game_id: int, db: Session = Depends(get_db)):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    return {
        "id": game.id,
        "name": game.name,
        "description": game.description,
        "genre_id": game.genre_id,
        "author_id": game.author_id,
        "publication_status": game.publication_status,
        "created_at": game.created_at
    }


@app.post("/games")
def create_game(game: schemas.GameCreate, db: Session = Depends(get_db)):
    new_game = models.Game(
        name=game.name,
        description=game.description,
        genre_id=game.genre_id,
        author_id=game.author_id,
        publication_status=game.publication_status or "draft"
    )
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return {
        "id": new_game.id,
        "name": new_game.name,
        "description": new_game.description,
        "created_at": new_game.created_at
    }


@app.get("/genres")
def get_genres(db: Session = Depends(get_db)):
    genres = db.query(models.Genre).all()
    result = []
    for g in genres:
        result.append({
            "id": g.id,
            "name": g.name
        })
    return result


@app.post("/genres")
def create_genre(genre: schemas.GenreCreate, db: Session = Depends(get_db)):
    new_genre = models.Genre(name=genre.name)
    db.add(new_genre)
    db.commit()
    db.refresh(new_genre)
    return {
        "id": new_genre.id,
        "name": new_genre.name
    }


@app.get("/lobbies")
def get_lobbies(db: Session = Depends(get_db)):
    lobbies = db.query(models.Lobby).all()
    result = []
    for lob in lobbies:
        result.append({
            "id": lob.id,
            "owner_id": lob.owner_id,
            "genre_id": lob.genre_id,
            "name": lob.name,
            "invite_code": lob.invite_code,
            "status": lob.status,
            "created_at": lob.created_at
        })
    return result


@app.post("/lobbies")
def create_lobby(lobby: schemas.LobbyCreate, db: Session = Depends(get_db)):
    new_lobby = models.Lobby(
        owner_id=lobby.owner_id,
        genre_id=lobby.genre_id,
        name=lobby.name,
        invite_code=lobby.invite_code,
        status=lobby.status or "collecting"
    )
    db.add(new_lobby)
    db.commit()
    db.refresh(new_lobby)

    member = models.LobbyMember(lobby_id=new_lobby.id, user_id=new_lobby.owner_id)
    db.add(member)
    db.commit()

    return {
        "id": new_lobby.id,
        "name": new_lobby.name,
        "invite_code": new_lobby.invite_code,
        "owner_id": new_lobby.owner_id,
        "genre_id": new_lobby.genre_id,
        "status": new_lobby.status
    }


@app.get("/lobbies/{lobby_id}")
def get_lobby(lobby_id: int, db: Session = Depends(get_db)):
    lobby = db.query(models.Lobby).filter(models.Lobby.id == lobby_id).first()
    if not lobby:
        raise HTTPException(status_code=404, detail="Лобби не найдено")
    return {
        "id": lobby.id,
        "name": lobby.name,
        "invite_code": lobby.invite_code,
        "owner_id": lobby.owner_id,
        "genre_id": lobby.genre_id,
        "status": lobby.status,
        "created_at": lobby.created_at
    }


@app.get("/lobbies/{lobby_id}/members")
def get_lobby_members(lobby_id: int, db: Session = Depends(get_db)):
    lobby = db.query(models.Lobby).filter(models.Lobby.id == lobby_id).first()
    if not lobby:
        raise HTTPException(status_code=404, detail="Лобби не найдено")

    members = db.query(models.LobbyMember).filter(models.LobbyMember.lobby_id == lobby_id).all()
    result = []
    for m in members:
        result.append({
            "lobby_id": m.lobby_id,
            "user_id": m.user_id,
            "joined_at": m.joined_at
        })
    return result


@app.post("/lobbies/{lobby_id}/members")
def add_member(lobby_id: int, member: schemas.LobbyMemberAdd, db: Session = Depends(get_db)):
    lobby = db.query(models.Lobby).filter(models.Lobby.id == lobby_id).first()
    if not lobby:
        raise HTTPException(status_code=404, detail="Лобби не найдено")

    user = db.query(models.User).filter(models.User.id == member.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    already_in = db.query(models.LobbyMember).filter(
        models.LobbyMember.lobby_id == lobby_id,
        models.LobbyMember.user_id == member.user_id
    ).first()
    if already_in:
        raise HTTPException(status_code=400, detail="Пользователь уже в лобби")

    new_member = models.LobbyMember(lobby_id=lobby_id, user_id=member.user_id)
    db.add(new_member)
    db.commit()
    return {"message": "Участник добавлен", "lobby_id": lobby_id, "user_id": member.user_id}


@app.get("/lobbies/{lobby_id}/ideas")
def get_ideas(lobby_id: int, db: Session = Depends(get_db)):
    lobby = db.query(models.Lobby).filter(models.Lobby.id == lobby_id).first()
    if not lobby:
        raise HTTPException(status_code=404, detail="Лобби не найдено")

    ideas = db.query(models.Idea).filter(models.Idea.lobby_id == lobby_id).all()
    result = []
    for i in ideas:
        result.append({
            "id": i.id,
            "lobby_id": i.lobby_id,
            "author_id": i.author_id,
            "body": i.body,
            "status": i.status,
            "created_at": i.created_at
        })
    return result


@app.post("/lobbies/{lobby_id}/ideas")
def add_idea(lobby_id: int, idea: schemas.IdeaCreate, db: Session = Depends(get_db)):
    lobby = db.query(models.Lobby).filter(models.Lobby.id == lobby_id).first()
    if not lobby:
        raise HTTPException(status_code=404, detail="Лобби не найдено")

    is_member = db.query(models.LobbyMember).filter(
        models.LobbyMember.lobby_id == lobby_id,
        models.LobbyMember.user_id == idea.author_id
    ).first()
    if not is_member:
        raise HTTPException(status_code=400, detail="Автор должен быть участником лобби")

    new_idea = models.Idea(
        lobby_id=lobby_id,
        author_id=idea.author_id,
        body=idea.body,
        status="proposed"
    )
    db.add(new_idea)
    db.commit()
    db.refresh(new_idea)
    return {
        "id": new_idea.id,
        "lobby_id": new_idea.lobby_id,
        "author_id": new_idea.author_id,
        "body": new_idea.body,
        "status": new_idea.status
    }


@app.post("/ideas/{idea_id}/generate")
def generate_game(idea_id: int, request: schemas.GameGenerateRequest, db: Session = Depends(get_db)):
    idea = db.query(models.Idea).filter(models.Idea.id == idea_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Идея не найдена")

    user = db.query(models.User).filter(models.User.id == request.requester_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    gen = models.Generation(
        lobby_id=idea.lobby_id,
        requester_id=request.requester_id,
        ai_model=request.ai_model,
        cost_credits=request.cost_credits,
        status="succeeded"
    )
    idea.status = "accepted"

    db.add(gen)
    db.commit()
    db.refresh(gen)

    return {
        "generation_id": gen.id,
        "status": gen.status,
        "suggested_game": {
            "name": f"Игра: {idea.body[:30]}",
            "description": f"Сгенерировано по идее: {idea.body}",
            "html_file": f"game_{gen.id}.html"
        }
    }


@app.post("/generations/{generation_id}/save-game")
def save_game(generation_id: int, payload: schemas.GameSaveFromGeneration, db: Session = Depends(get_db)):
    gen = db.query(models.Generation).filter(models.Generation.id == generation_id).first()
    if not gen:
        raise HTTPException(status_code=404, detail="Генерация не найдена")

    game = models.Game(
        author_id=payload.author_id,
        genre_id=gen.lobby.genre_id,
        lobby_id=gen.lobby_id,
        name=payload.name or f"Игра #{gen.id}",
        description=payload.description or "Создано",
        publication_status=payload.publication_status or "draft"
    )
    db.add(game)
    db.commit()
    db.refresh(game)

    ver = models.GameVersion(
        game_id=game.id,
        generation_id=gen.id,
        version_number=1,
        html_file=payload.html_file or f"game_{gen.id}.html",
        source_type="ai"
    )
    db.add(ver)
    db.commit()

    return {
        "id": game.id,
        "name": game.name,
        "description": game.description,
        "author_id": game.author_id,
        "genre_id": game.genre_id,
        "created_at": game.created_at
    }
