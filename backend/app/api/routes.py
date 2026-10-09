"""REST API 路由。"""

from datetime import date
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from fastapi.responses import JSONResponse

from app.core.db import UPLOAD_DIR, get_db
from app.crud.diary import (
    add_photo as add_diary_photo,
    create_diary,
    delete_diary,
    get_diary,
    list_diaries,
    update_diary,
)
from app.crud.place import (
    add_photo as add_place_photo,
    create_place,
    delete_place,
    get_place,
    list_places,
    update_place,
)
from app.schemas.models import (
    Couple,
    CouplePayload,
    Diary,
    DiaryCreate,
    DiaryUpdate,
    Place,
    PlaceCreate,
    PlaceUpdate,
    Photo,
    Stats,
)
from app.service.stats import get_stats

router = APIRouter(prefix="/api")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_UPLOAD_BYTES = 10 * 1024 * 1024


def db_dependency():
    with get_db() as connection:
        yield connection


def _row_dict(row):
    return dict(row) if row else None


async def _save_upload(upload: UploadFile, category: str, record_id: int) -> str:
    suffix = Path(upload.filename or "").suffix.lower() or ".jpg"
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="只支持 JPG、PNG、GIF 和 WebP 图片。")
    content = await upload.read()
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="单张图片不能超过 10 MB。")

    folder = UPLOAD_DIR / category / str(record_id)
    folder.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid4().hex}{suffix}"
    destination = folder / filename
    destination.write_bytes(content)
    return f"/uploads/{category}/{record_id}/{filename}"


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/couple", response_model=Couple | None)
def read_couple(connection=Depends(db_dependency)):
    row = connection.execute(
        """
        SELECT id, nickname_a, nickname_b, anniversary, created_at, updated_at
        FROM couple_info WHERE id = 1
        """
    ).fetchone()
    return _row_dict(row)


@router.post("/couple", response_model=Couple)
def save_couple(payload: CouplePayload, connection=Depends(db_dependency)):
    connection.execute(
        """
        INSERT INTO couple_info (id, nickname_a, nickname_b, anniversary)
        VALUES (1, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
          nickname_a = excluded.nickname_a,
          nickname_b = excluded.nickname_b,
          anniversary = excluded.anniversary,
          updated_at = CURRENT_TIMESTAMP
        """,
        (payload.nickname_a.strip(), payload.nickname_b.strip(), payload.anniversary.isoformat()),
    )
    row = connection.execute(
        "SELECT id, nickname_a, nickname_b, anniversary, created_at, updated_at "
        "FROM couple_info WHERE id = 1"
    ).fetchone()
    return _row_dict(row)


@router.get("/diary", response_model=list[Diary])
def read_diaries(
    mood: str | None = Query(default=None),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    connection=Depends(db_dependency),
):
    return list_diaries(connection, mood, start_date, end_date)


@router.post("/diary", response_model=Diary)
def create_diary_route(payload: DiaryCreate, connection=Depends(db_dependency)):
    return create_diary(
        connection,
        {
            "diary_date": payload.diary_date.isoformat(),
            "title": payload.title,
            "content": payload.content,
            "mood": payload.mood,
        },
    )


@router.get("/diary/{diary_id}", response_model=Diary)
def read_diary(diary_id: int, connection=Depends(db_dependency)):
    diary = get_diary(connection, diary_id)
    if not diary:
        raise HTTPException(status_code=404, detail="日记不存在。")
    return diary


@router.put("/diary/{diary_id}", response_model=Diary)
def edit_diary(
    diary_id: int, payload: DiaryUpdate, connection=Depends(db_dependency)
):
    changes = payload.model_dump(exclude_unset=True)
    if "diary_date" in changes:
        changes["diary_date"] = changes["diary_date"].isoformat()
    diary = update_diary(connection, diary_id, changes)
    if not diary:
        raise HTTPException(status_code=404, detail="日记不存在。")
    return diary


@router.delete("/diary/{diary_id}")
def remove_diary(diary_id: int, connection=Depends(db_dependency)):
    paths = delete_diary(connection, diary_id)
    if paths is None:
        raise HTTPException(status_code=404, detail="日记不存在。")
    return JSONResponse({"deleted": diary_id})


@router.post("/diary/{diary_id}/photo", response_model=Photo)
async def upload_diary_photo(
    diary_id: int,
    file: UploadFile = File(...),
    connection=Depends(db_dependency),
):
    if not get_diary(connection, diary_id):
        raise HTTPException(status_code=404, detail="日记不存在。")
    path = await _save_upload(file, "diary", diary_id)
    return add_diary_photo(connection, diary_id, path)


@router.get("/place", response_model=list[Place])
def read_places(connection=Depends(db_dependency)):
    return list_places(connection)


@router.post("/place", response_model=Place)
def create_place_route(payload: PlaceCreate, connection=Depends(db_dependency)):
    if payload.diary_id and not get_diary(connection, payload.diary_id):
        raise HTTPException(status_code=400, detail="关联的日记不存在。")
    return create_place(
        connection,
        {
            "name": payload.name,
            "latitude": payload.latitude,
            "longitude": payload.longitude,
            "visited_date": payload.visited_date.isoformat(),
            "diary_id": payload.diary_id,
        },
    )


@router.put("/place/{place_id}", response_model=Place)
def edit_place(
    place_id: int, payload: PlaceUpdate, connection=Depends(db_dependency)
):
    changes = payload.model_dump(exclude_unset=True)
    if "visited_date" in changes:
        changes["visited_date"] = changes["visited_date"].isoformat()
    if changes.get("diary_id") and not get_diary(connection, changes["diary_id"]):
        raise HTTPException(status_code=400, detail="关联的日记不存在。")
    place = update_place(connection, place_id, changes)
    if not place:
        raise HTTPException(status_code=404, detail="地点不存在。")
    return place


@router.delete("/place/{place_id}")
def remove_place(place_id: int, connection=Depends(db_dependency)):
    paths = delete_place(connection, place_id)
    if paths is None:
        raise HTTPException(status_code=404, detail="地点不存在。")
    return JSONResponse({"deleted": place_id})


@router.post("/place/{place_id}/photo", response_model=Photo)
async def upload_place_photo(
    place_id: int,
    file: UploadFile = File(...),
    connection=Depends(db_dependency),
):
    if not get_place(connection, place_id):
        raise HTTPException(status_code=404, detail="地点不存在。")
    path = await _save_upload(file, "place", place_id)
    return add_place_photo(connection, place_id, path)


@router.get("/stats", response_model=Stats)
def read_stats(connection=Depends(db_dependency)):
    return get_stats(connection)
