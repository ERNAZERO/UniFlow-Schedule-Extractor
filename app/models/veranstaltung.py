from dataclasses import dataclass
from typing import Optional


@dataclass
class ScheduleItemModel:
    veranstaltung: str
    zeit: str
    wochen_typ: Optional[str]
    start_kw: Optional[int]
    end_kw: Optional[int]