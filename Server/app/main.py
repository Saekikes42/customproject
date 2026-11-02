import os
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import text

from .database import get_db
from . import models, schemas
from .demo_game import build_game

app = FastAPI(title="GameForge")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)
GAME_DIR = Path(os.getenv("GAME_FILES_DIR", str(Path(__file__).resolve().parents[1] / "game_files")))


def save_changes(db: Session):
    """Commit one action, or return a clear error for duplicate/invalid links."""
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Запись уже существует или связанный объект не найден")


def delete_record(db: Session, record, not_found: str):
    if not record:
        raise HTTPException(status_code=404, detail=not_found)
    db.delete(record)
    save_changes(db)
    return {"message": "Запись удалена"}


@app.get("/", tags=["Служебные"])
def root():
    return {"message": "Сервер работает"}


@app.get("/health", tags=["Служебные"])
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok"}


@app.get("/users", tags=["Пользователи"])
def get_users(limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.id).offset(offset).limit(limit).all()
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


@app.get("/users/{user_id}", tags=["Пользователи"])
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


@app.post("/users", tags=["Пользователи"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(
        role_id=user.role_id,
        telegram_id=user.telegram_id,
        display_name=user.display_name
    )
    db.add(new_user)
    save_changes(db)
    db.refresh(new_user)
    return {
        "id": new_user.id,
        "role_id": new_user.role_id,
        "telegram_id": new_user.telegram_id,
        "display_name": new_user.display_name,
        "created_at": new_user.created_at
    }


@app.put("/users/{user_id}", tags=["Пользователи"])
def update_user(user_id: int, payload: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    user.display_name = payload.display_name
    save_changes(db)
    return {"id": user.id, "display_name": user.display_name}


@app.delete("/users/{user_id}", tags=["Пользователи"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return delete_record(db, db.query(models.User).filter(models.User.id == user_id).first(), "Пользователь не найден")


@app.get("/games", tags=["Игры"])
def get_games(limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    games = db.query(models.Game).order_by(models.Game.id.desc()).offset(offset).limit(limit).all()
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


@app.get("/games/{game_id}", tags=["Игры"])
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


@app.post("/games", tags=["Игры"])
def create_game(game: schemas.GameCreate, db: Session = Depends(get_db)):
    new_game = models.Game(
        name=game.name,
        description=game.description,
        genre_id=game.genre_id,
        author_id=game.author_id,
        publication_status="draft"
    )
    db.add(new_game)
    save_changes(db)
    db.refresh(new_game)
    return {
        "id": new_game.id,
        "name": new_game.name,
        "description": new_game.description,
        "created_at": new_game.created_at
    }


@app.put("/games/{game_id}", tags=["Игры"])
def update_game(game_id: int, payload: schemas.GameUpdate, db: Session = Depends(get_db)):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    game.name, game.description = payload.name, payload.description
    save_changes(db)
    return {"id": game.id, "name": game.name, "description": game.description}


@app.delete("/games/{game_id}", tags=["Игры"])
def delete_game(game_id: int, db: Session = Depends(get_db)):
    return delete_record(db, db.query(models.Game).filter(models.Game.id == game_id).first(), "Игра не найдена")


@app.get("/genres", tags=["Жанры"])
def get_genres(db: Session = Depends(get_db)):
    genres = db.query(models.Genre).all()
    result = []
    for g in genres:
        result.append({
            "id": g.id,
            "name": g.name
        })
    return result


@app.post("/genres", tags=["Жанры"])
def create_genre(genre: schemas.GenreCreate, db: Session = Depends(get_db)):
    new_genre = models.Genre(name=genre.name)
    db.add(new_genre)
    save_changes(db)
    db.refresh(new_genre)
    return {
        "id": new_genre.id,
        "name": new_genre.name
    }


@app.put("/genres/{genre_id}", tags=["Жанры"])
def update_genre(genre_id: int, payload: schemas.GenreUpdate, db: Session = Depends(get_db)):
    genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Жанр не найден")
    genre.name = payload.name
    save_changes(db)
    return {"id": genre.id, "name": genre.name}


@app.delete("/genres/{genre_id}", tags=["Жанры"])
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    return delete_record(db, db.query(models.Genre).filter(models.Genre.id == genre_id).first(), "Жанр не найден")


@app.get("/lobbies", tags=["Лобби"])
def get_lobbies(limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    lobbies = db.query(models.Lobby).order_by(models.Lobby.id.desc()).offset(offset).limit(limit).all()
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


@app.post("/lobbies", tags=["Лобби"])
def create_lobby(lobby: schemas.LobbyCreate, db: Session = Depends(get_db)):
    new_lobby = models.Lobby(
        owner_id=lobby.owner_id,
        genre_id=lobby.genre_id,
        name=lobby.name,
        invite_code=lobby.invite_code,
        status="collecting"
    )
    db.add(new_lobby)
    try:
        db.flush()  # Obtain lobby ID without saving half of the action.
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Код приглашения уже занят или пользователь/жанр не найден")
    member = models.LobbyMember(lobby_id=new_lobby.id, user_id=new_lobby.owner_id)
    db.add(member)
    save_changes(db)
    db.refresh(new_lobby)

    return {
        "id": new_lobby.id,
        "name": new_lobby.name,
        "invite_code": new_lobby.invite_code,
        "owner_id": new_lobby.owner_id,
        "genre_id": new_lobby.genre_id,
        "status": new_lobby.status
    }


@app.get("/lobbies/{lobby_id}", tags=["Лобби"])
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


@app.put("/lobbies/{lobby_id}", tags=["Лобби"])
def update_lobby(lobby_id: int, payload: schemas.LobbyUpdate, db: Session = Depends(get_db)):
    lobby = db.query(models.Lobby).filter(models.Lobby.id == lobby_id).first()
    if not lobby:
        raise HTTPException(status_code=404, detail="Лобби не найдено")
    lobby.name = payload.name
    save_changes(db)
    return {"id": lobby.id, "name": lobby.name}


@app.delete("/lobbies/{lobby_id}", tags=["Лобби"])
def delete_lobby(lobby_id: int, db: Session = Depends(get_db)):
    return delete_record(db, db.query(models.Lobby).filter(models.Lobby.id == lobby_id).first(), "Лобби не найдено")


@app.get("/lobbies/{lobby_id}/members", tags=["Лобби"])
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


@app.post("/lobbies/{lobby_id}/members", tags=["Лобби"])
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
        raise HTTPException(status_code=409, detail="Пользователь уже в лобби")

    new_member = models.LobbyMember(lobby_id=lobby_id, user_id=member.user_id)
    db.add(new_member)
    save_changes(db)
    return {"message": "Участник добавлен", "lobby_id": lobby_id, "user_id": member.user_id}


@app.get("/lobbies/{lobby_id}/ideas", tags=["Идеи"])
def get_ideas(lobby_id: int, limit: int = Query(20, ge=1, le=100),
              offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    lobby = db.query(models.Lobby).filter(models.Lobby.id == lobby_id).first()
    if not lobby:
        raise HTTPException(status_code=404, detail="Лобби не найдено")

    ideas = (db.query(models.Idea).filter(models.Idea.lobby_id == lobby_id)
             .order_by(models.Idea.id.desc()).offset(offset).limit(limit).all())
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


@app.post("/lobbies/{lobby_id}/ideas", tags=["Идеи"])
def add_idea(lobby_id: int, idea: schemas.IdeaCreate, db: Session = Depends(get_db)):
    lobby = db.query(models.Lobby).filter(models.Lobby.id == lobby_id).first()
    if not lobby:
        raise HTTPException(status_code=404, detail="Лобби не найдено")

    is_member = db.query(models.LobbyMember).filter(
        models.LobbyMember.lobby_id == lobby_id,
        models.LobbyMember.user_id == idea.author_id
    ).first()
    if not is_member:
        raise HTTPException(status_code=403, detail="Автор должен быть участником лобби")

    new_idea = models.Idea(
        lobby_id=lobby_id,
        author_id=idea.author_id,
        body=idea.body,
        status="proposed"
    )
    db.add(new_idea)
    save_changes(db)
    db.refresh(new_idea)
    return {
        "id": new_idea.id,
        "lobby_id": new_idea.lobby_id,
        "author_id": new_idea.author_id,
        "body": new_idea.body,
        "status": new_idea.status
    }


@app.put("/ideas/{idea_id}", tags=["Идеи"])
def update_idea(idea_id: int, payload: schemas.IdeaUpdate, db: Session = Depends(get_db)):
    idea = db.query(models.Idea).filter(models.Idea.id == idea_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Идея не найдена")
    idea.body = payload.body
    save_changes(db)
    return {"id": idea.id, "body": idea.body, "status": idea.status}


@app.delete("/ideas/{idea_id}", tags=["Идеи"])
def delete_idea(idea_id: int, db: Session = Depends(get_db)):
    return delete_record(db, db.query(models.Idea).filter(models.Idea.id == idea_id).first(), "Идея не найдена")


@app.post("/ideas/{idea_id}/generate", tags=["Генерация"])
def generate_game(idea_id: int, request: schemas.GameGenerateRequest, db: Session = Depends(get_db)):
    idea = db.query(models.Idea).filter(models.Idea.id == idea_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Идея не найдена")

    lobby = db.query(models.Lobby).filter(models.Lobby.id == idea.lobby_id).first()
    if not lobby or lobby.owner_id != request.requester_id:
        raise HTTPException(status_code=403, detail="Создавать игру может только владелец лобби")
    if lobby.status == "closed":
        raise HTTPException(status_code=409, detail="Лобби закрыто")
    # This is a small playable template, not an AI-generated game.
    html = build_game(idea.body)
    gen = models.Generation(
        lobby_id=idea.lobby_id,
        requester_id=request.requester_id,
        ai_model="demo-template",
        cost_credits=0,
        status="succeeded"
    )
    idea.status = "accepted"
    db.add(gen)
    try:
        db.flush()
        GAME_DIR.mkdir(parents=True, exist_ok=True)
        filename = f"game_{gen.id}.html"
        path = GAME_DIR / filename
        path.write_text(html, encoding="utf-8")
        save_changes(db)
    except Exception:
        db.rollback()
        if "path" in locals():
            path.unlink(missing_ok=True)
        raise
    return {
        "generation_id": gen.id,
        "status": "succeeded",
        "mode": "demo-template",
        "play_url": f"/generations/{gen.id}/play",
        "suggested_game": {
            "name": f"Игра: {idea.body[:30]}",
            "description": f"Демо-игра по идее: {idea.body}",
            "html_file": filename
        }
    }


def show_game_file(filename: str):
    if Path(filename).name != filename:
        raise HTTPException(status_code=404, detail="Файл игры не найден")
    path = GAME_DIR / filename
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Файл игры не найден")
    return HTMLResponse(path.read_text(encoding="utf-8"), headers={
        "Content-Security-Policy": "sandbox allow-scripts; default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'",
        "X-Content-Type-Options": "nosniff"
    })


@app.get("/generations/{generation_id}/play", tags=["Генерация"])
def play_generation(generation_id: int, db: Session = Depends(get_db)):
    gen = db.query(models.Generation).filter(models.Generation.id == generation_id).first()
    if not gen or gen.status != "succeeded":
        raise HTTPException(status_code=404, detail="Игра не найдена")
    return show_game_file(f"game_{gen.id}.html")


@app.get("/games/{game_id}/play", tags=["Игры"])
def play_saved_game(game_id: int, db: Session = Depends(get_db)):
    version = (db.query(models.GameVersion).filter(models.GameVersion.game_id == game_id)
               .order_by(models.GameVersion.version_number.desc()).first())
    if not version:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    return show_game_file(version.html_file)


@app.post("/generations/{generation_id}/save-game", tags=["Генерация"])
def save_game(generation_id: int, payload: schemas.GameSaveFromGeneration, db: Session = Depends(get_db)):
    gen = db.query(models.Generation).filter(models.Generation.id == generation_id).first()
    if not gen or gen.status != "succeeded":
        raise HTTPException(status_code=404, detail="Генерация не найдена")
    if payload.author_id != gen.requester_id or payload.author_id != gen.lobby.owner_id:
        raise HTTPException(status_code=403, detail="Сохранить игру может только создатель")
    filename = f"game_{gen.id}.html"
    if not (GAME_DIR / filename).is_file():
        raise HTTPException(status_code=404, detail="Файл игры не найден")
    if db.query(models.GameVersion).filter(models.GameVersion.generation_id == gen.id).first():
        raise HTTPException(status_code=409, detail="Игра уже сохранена")
    game = models.Game(
        author_id=payload.author_id,
        genre_id=gen.lobby.genre_id,
        lobby_id=gen.lobby_id,
        name=payload.name or f"Игра #{gen.id}",
        description=payload.description or "Демо-игра",
        publication_status="draft"
    )
    db.add(game)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Не удалось сохранить игру")
    ver = models.GameVersion(
        game_id=game.id,
        generation_id=gen.id,
        version_number=1,
        html_file=filename,
        source_type="ai"
    )
    db.add(ver)
    save_changes(db)
    db.refresh(game)

    return {
        "id": game.id,
        "name": game.name,
        "description": game.description,
        "author_id": game.author_id,
        "genre_id": game.genre_id,
        "created_at": game.created_at
    }

