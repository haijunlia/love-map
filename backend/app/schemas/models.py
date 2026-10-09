"""API 请求和响应模型。"""

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Mood = Literal["happy", "calm", "sad", "angry"]


class CouplePayload(BaseModel):
    nickname_a: str = Field(min_length=1, max_length=30)
    nickname_b: str = Field(min_length=1, max_length=30)
    anniversary: date


class Couple(CouplePayload):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Photo(BaseModel):
    id: int
    file_path: str
    url: str
    sort_order: int


class DiaryPayload(BaseModel):
    diary_date: date
    title: str = Field(min_length=1, max_length=120)
    content: str = Field(min_length=1, max_length=10000)
    mood: Mood = "happy"


class DiaryCreate(DiaryPayload):
    pass


class DiaryUpdate(BaseModel):
    diary_date: date | None = None
    title: str | None = Field(default=None, min_length=1, max_length=120)
    content: str | None = Field(default=None, min_length=1, max_length=10000)
    mood: Mood | None = None


class Diary(DiaryPayload):
    id: int
    photos: list[Photo] = []
    created_at: datetime | None = None
    updated_at: datetime | None = None


class PlacePayload(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    visited_date: date
    diary_id: int | None = None


class PlaceCreate(PlacePayload):
    pass


class PlaceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    visited_date: date | None = None
    diary_id: int | None = None


class Place(PlacePayload):
    id: int
    diary_title: str | None = None
    photos: list[Photo] = []
    created_at: datetime | None = None


class MoodStat(BaseModel):
    mood: str
    count: int


class Stats(BaseModel):
    diary_count: int
    place_count: int
    mood_distribution: list[MoodStat]
    days_together: int | None = None
    next_anniversary_days: int | None = None
