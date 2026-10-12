from __future__ import annotations

import io
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


def _attempt_ocr_from_document(document: fitz.Document) -> str:
    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        return ""

    try:
        pytesseract.get_tesseract_version()
    except (FileNotFoundError, OSError, RuntimeError, ValueError):
        return ""

    pages: list[str] = []
    for page in document:
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        image_bytes = pix.tobytes("png")
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image, config="--psm 6")
        if text and text.strip():
            pages.append(text.strip())

    return "\n".join(pages)


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
            ocr_text = _attempt_ocr_from_document(document)
            if ocr_text.strip():
                return ocr_text
            raise ValueError(
                "No readable text could be extracted from the PDF. Scanned image-only PDFs require OCR support, which is not available in this environment."
            )

        return "\n".join(pages)
    finally:
        document.close()
