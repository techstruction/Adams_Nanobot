"""PDF Manager skill module"""

from .pdf_manager import (
    read_pdf,
    create_pdf,
    list_pdfs,
    get_pdf_info,
    search_pdfs,
    pdf_to_text,
    pdf_manager
)

# Convenience exports
__all__ = [
    'read_pdf',
    'create_pdf',
    'list_pdfs',
    'get_pdf_info',
    'search_pdfs',
    'pdf_to_text',
    'pdf_manager'
]
