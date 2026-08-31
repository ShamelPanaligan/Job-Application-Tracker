from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum

class Status(str, Enum):
    APPLIED = "applied"
    SCREENING = "screening"
    INTERVIEWING = "interviewing"
    OFFER = "offer"
    REJECTED = "rejected"
    GHOSTED = "ghosted"
    WITHDRAWN = "withdrawn"

@dataclass
class Application:
    company : str
    role : str
    status : Status
    date_applied : date
    id : int| None = None
    source : str | None = None
    link : str | None = None
    created_at : datetime = field(default_factory=datetime.now)
    updated_at : datetime = field(default_factory=datetime.now)
    archived : bool = False

@dataclass
class Note:
    application_id : int
    body : str
    created_at : datetime = field(default_factory=datetime.now)
    id : int| None = None


@dataclass
class Tag:
    application_id : int
    tag : str