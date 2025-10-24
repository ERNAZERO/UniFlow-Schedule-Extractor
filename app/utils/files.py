from fastapi import UploadFile, HTTPException
import tempfile, os

PDF_MIME = {"application/pdf", "application/x-pdf"}


def ensure_pdf(file: UploadFile):
    if file.content_type not in PDF_MIME and not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")


async def persist_upload_to_temp(file: UploadFile) -> str:
    """
    Сохраняет UploadFile в отдельный tmp-файл и возвращает путь.
    Файл НЕ удаляется автоматически — вызывающий код должен удалить его сам.
    """
    ensure_pdf(file)
    # создаём реальный файл, который не удаляется при закрытии
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        # читаем весь UploadFile и пишем в tmp
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            tmp.write(chunk)
        tmp.flush()
        path = tmp.name
    # сбросим курсор (если UploadFile будет ещё где-то использоваться)
    await file.seek(0)
    return path
