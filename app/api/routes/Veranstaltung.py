from fastapi import APIRouter, UploadFile, File, Depends
from typing import List
from app.schemas.veranstaltung import ParseResponse, Veranstaltung, ParseRequest
from app.api.deps import get_extractor
from app.utils.files import persist_upload_to_temp
import os

router = APIRouter(prefix="/schedule", tags=["schedule"])


@router.post("/parse", response_model=ParseResponse)
async def parse_schedule(
        file: UploadFile = File(..., description="PDF с расписанием"),
        _: ParseRequest = Depends(),
        extractor = Depends(get_extractor),
    ):
    tmp_path = await persist_upload_to_temp(file)
    try:
        items: List[Veranstaltung] = extractor.parse(tmp_path)
        return ParseResponse(items=items)
    finally:
        try:
            os.remove(tmp_path)
        except FileNotFoundError:
            pass