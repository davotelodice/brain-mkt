"""File parsers for .txt, .pdf, .docx documents."""
from pathlib import Path

import docx
import PyPDF2


async def parse_txt(file_path: Path) -> str:
    """Parse .txt file and return content.

    Args:
        file_path: Path to .txt file

    Returns:
        File content as string

    Raises:
        FileNotFoundError: If file doesn't exist
        UnicodeDecodeError: If file has encoding issues
    """
    with open(file_path, encoding='utf-8') as f:
        return f.read()


async def parse_pdf(file_path: Path) -> str:
    """Parse .pdf file and extract text.

    Args:
        file_path: Path to .pdf file

    Returns:
        Extracted text from all pages

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    text_parts = []
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text_parts.append(page.extract_text())
    return "\n".join(text_parts)


async def parse_docx(file_path: Path) -> str:
    """Parse .docx file and extract text.

    Args:
        file_path: Path to .docx file

    Returns:
        Extracted text from all paragraphs

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


async def parse_document(file_path: Path, file_type: str) -> str:
    """Route to appropriate parser based on file type.

    Args:
        file_path: Path to document
        file_type: File extension (.txt, .pdf, .docx)

    Returns:
        Extracted text content

    Raises:
        ValueError: If file type is not supported
    """
    parsers = {
        '.txt': parse_txt,
        '.pdf': parse_pdf,
        '.docx': parse_docx,
    }
    parser = parsers.get(file_type)
    if not parser:
        raise ValueError(f"Unsupported file type: {file_type}")
    return await parser(file_path)
