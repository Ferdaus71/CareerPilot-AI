from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

import fitz

MAX_PDF_SIZE_BYTES = 10 * 1024 * 1024


def _validate_pdf_bytes(file_bytes: bytes, file_name: str | None = None) -> None:
    if not file_bytes:
        raise ValueError("The uploaded PDF is empty.")

    if len(file_bytes) > MAX_PDF_SIZE_BYTES:
        raise ValueError("The uploaded PDF exceeds the maximum supported size of 10 MB.")

    pdf_name = (file_name or "resume.pdf").lower()
    if not pdf_name.endswith(".pdf"):
        raise ValueError("Only PDF files are supported.")


def extract_pdf_text(file_bytes: bytes | BinaryIO | str | Path, file_name: str | None = None) -> str:
    """Read a PDF document and return plain text from its pages.

    The function intentionally avoids writing files to disk and does not expose the
    original resume contents beyond the extracted text needed for matching.
    """
    if hasattr(file_bytes, "read"):
        content = file_bytes.read()
    elif isinstance(file_bytes, (str, Path)):
        candidate = Path(file_bytes)
        if not candidate.exists():
            raise ValueError("The uploaded PDF could not be found.")
        content = candidate.read_bytes()
    else:
        content = file_bytes

    if not isinstance(content, (bytes, bytearray)):
        raise TypeError("The uploaded file could not be read as PDF data.")

    file_bytes_clean = bytes(content)
    _validate_pdf_bytes(file_bytes_clean, file_name)

    try:
        document = fitz.open(stream=file_bytes_clean, filetype="pdf")
    except Exception as exc:  # pragma: no cover - exercised by tests with invalid bytes
        raise ValueError("The PDF could not be opened. The file may be corrupt or unreadable.") from exc

    try:
        pages: list[str] = []
        for page in document:
            text = page.get_text("text")
            if text and text.strip():
                pages.append(text)

        if not pages:
            raise ValueError(
                "No readable text could be extracted from the PDF. Scanned image-only PDFs require OCR, which is not included in this version."
            )

        return "\n".join(pages)
    finally:
        document.close()
