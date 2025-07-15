from typing import Annotated, Optional
from pydantic import BaseModel, Field

StringStrip500 = Annotated[str, Field(strip_whitespace=True, min_length=1, max_length=500)]
StringStrip255 = Annotated[str, Field(strip_whitespace=True, max_length=255)]
StringContent3000 = Annotated[str, Field(strip_whitespace=True)]

class PostModel(BaseModel):
    id: Optional[StringStrip500] = None
    doc_type: int = Field(default=1)
    crawl_source: int
    crawl_source_code: Optional[str] = None #crawl_source: int = Field(default=1
    pub_time: int = Field(..., gt=0)
    crawl_time: int = Field(..., gt=0)
    org_id: int
    subject_id: Optional[StringStrip255] = None
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[StringContent3000] = None
    url: Annotated[str, Field(strip_whitespace=True, max_length=3000)]
    media_urls: Optional[Annotated[str, Field(strip_whitespace=True)]] = '[]'
    comments: int = Field(default=0, ge=0)
    shares: int = Field(default=0, ge=0)
    reactions: int = Field(default=0, ge=0)
    favors: int = Field(default=0, ge=0)
    views: int = Field(default=0, ge=0)
    web_tags: Optional[Annotated[str, Field(strip_whitespace=True)]] = '[]'
    web_keywords: Optional[Annotated[str, Field(strip_whitespace=True)]] = '[]'
    auth_id: Annotated[str, Field(strip_whitespace=True, max_length=3000)]
    auth_name: Annotated[str, Field(strip_whitespace=True, max_length=3000)]
    auth_type: Optional[int] = None
    auth_url: Annotated[str, Field(strip_whitespace=True, max_length=3000)]
    source_id: Annotated[str, Field(strip_whitespace=True, max_length=3000)]
    source_type: int
    source_name: Annotated[str, Field(strip_whitespace=True, max_length=3000)]
    source_url: Annotated[str, Field(strip_whitespace=True, max_length=3000)]
    reply_to: Optional[str] = None
    level: Optional[int] = None
    sentiment: int = Field(default=0)
    isPriority: bool
    crawl_bot: str