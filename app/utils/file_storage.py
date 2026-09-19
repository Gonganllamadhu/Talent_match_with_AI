
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status


UPLOAD_DIR = Path("uploads/resumes")

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
}

MAX_FILE_SIZE = 10 * 1024 * 1024


async def save_resume(
    file: UploadFile,
) -> tuple[str, str]:

    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume file name is missing",
        )

    extension = Path(
        file.filename
    ).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF, DOC and DOCX resumes are allowed",
        )

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Resume file cannot exceed 10 MB",
        )

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    stored_filename = (
        f"{uuid4().hex}{extension}"
    )

    file_path = (
        UPLOAD_DIR / stored_filename
    )

    file_path.write_bytes(content)

    return (
        file.filename,
        str(file_path),
    )

