from typing import List, Literal

from pydantic import BaseModel, Field


class Entity(BaseModel):
    people: List[str] = Field(default_factory=list)
    organizations: List[str] = Field(default_factory=list)
    locations: List[str] = Field(default_factory=list)


class AnalyzeRequest(BaseModel):
    input: str
    mode: Literal["auto", "url", "text"] = "auto"
    summary_length: Literal["short", "medium", "detailed"] = "medium"


class AnalyzeResponse(BaseModel):
    title: str
    source: str
    language: str
    article_text: str
    reading_time_minutes: int
    german_summary: str
    english_summary: str
    keywords: List[str]
    entities: Entity
    tone: str
