from typing import List
from app.schemas.veranstaltung import Veranstaltung
from app.services.pipeline import LCPipeline
from app.utils.text import kw_min_max_from_any
import json, re


PROMPT_OUTPUT_FORMAT = (
    'Gib NUR ein JSON-Array mit Objekten aus: '
    '"Wochentag", "Veranstaltung", "Zyklus", "Anfang", "Ende", "Raum", "Dozent". '
    'Nur Angaben aus dem PDF-Kontext; nichts erfinden. '
    'Fehlt etwas → null. '
    '"Anfang"/"Ende" nur HH:MM. '
    'Zyklus kurz (z.B. "wöch", "Z1", "Z2", "KWxx"). '
    'Kein Markdown/Code/Kommentar.'
    '"Raum" als Raumnummer/Kürzel wie GABxxx, PKBxxx, PBSxxx; wenn nicht eindeutig → null. '
    'Wochentag exakt: Montag/Dienstag/Mittwoch/Donnerstag/Freitag/Samstag/Sonntag.'
)

QUESTION = (
    'Extrahiere alle Lehrveranstaltungen aus dem Dokument. ' + PROMPT_OUTPUT_FORMAT
)


class VeranstaltungExtractor:
    def __init__(self):
        self.pipeline = LCPipeline()

    def parse(self, pdf_path: str) -> List[Veranstaltung]:
        docs = self.pipeline.extract_docs(pdf_path)
        vs = self.pipeline.build_vectorstore(docs)
        qa = self.pipeline.make_qa_chain(vs)

        raw = qa.invoke({"input": QUESTION})
        text = raw.get("answer") or raw.get("output_text") or "[]"

        m = re.search(r"\[.*\]", text, re.DOTALL)
        if m:
            text = m.group(0)

        try:
            data = json.loads(text)
        except Exception:
            data = []

        keys = ["Wochentag","Veranstaltung", "Zyklus", "Anfang", "Ende", "Raum", "Dozent"]
        items: List[Veranstaltung] = []
        for it in data if isinstance(data, list) else []:
            norm = {k: (it.get(k) if it.get(k) not in ("", "None") else None) for k in keys}
            items.append(Veranstaltung(**norm))
        return items