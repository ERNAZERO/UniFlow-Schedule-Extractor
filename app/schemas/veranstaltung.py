from pydantic import BaseModel, Field, conint
from typing import List, Optional, Literal


WEEKDAY = Literal["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"]


class Veranstaltung(BaseModel):
    Wochentag: Optional[WEEKDAY] = None
    Veranstaltung: Optional[str] = Field(None, description="Titel der Veranstaltung")
    Zyklus: Optional[str] = Field(None, description="z. B. wöchentlich, A/B, Block")
    Anfang: Optional[str] = Field(None, description="Start (Uhrzeit/Datum wörtlich aus PDF)")
    Ende: Optional[str] = Field(None, description="Ende (Uhrzeit/Datum wörtlich aus PDF)")
    Raum: Optional[str] = Field(None, description="Raum/Ort")
    Dozent: Optional[str] = Field(None, description="Dozent/Dozentin")


class ParseResponse(BaseModel):
    items: List[Veranstaltung]


class ParseRequest(BaseModel):
    language: Optional[str] = Field(default="de", description="Язык промпта/ответа")
