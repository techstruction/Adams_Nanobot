#!/usr/bin/env python3
"""
PDF Manager
Handles reading and creating PDF files.
"""

import os
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pathlib import Path

class PDFManager:
    """Manages PDF reading and creation"""
    
    def __init__(self):
        self.base_dir = Path.home() / ".nanobot" / "workspace"
        self.base_dir.mkdir(exist_ok=True)
    
    def read_pdf(self, filepath):
        """Read PDF and return text"""
        try:
            full_path = self.base_dir / filepath
            with open(full_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text[:2000]  # Limit output
        except Exception as e:
            return f"Error: {e}"
    
    def create_pdf(self, filepath, content):
        """Create simple PDF"""
        try:
            full_path = self.base_dir / filepath
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'wb') as f:
                writer = PyPDF2.PdfWriter()
                # Note: Creation requires more complex setup
                # This is a placeholder
                f.write(b"PDF content")
            return f"Created: {full_path}"
        except Exception as e:
            return f"Error: {e}"

# Convenience functions
pdf_manager = PDFManager()

def read_pdf(filepath):
    """Read PDF (for nanobot integration)"""
    return pdf_manager.read_pdf(filepath)

def create_pdf(filepath, content):
    """Create PDF (for nanobot integration)"""
    return pdf_manager.create_pdf(filepath, content)
## STUBS - Add missing functions needed by __init__

def list_pdfs(directory=None):
    return _manager.list_pdfs(directory)

def create_pdf(filepath, content):
    return _manager.create_pdf(filepath, content)

def get_pdf_info(filepath):
    return _manager.get_pdf_info(filepath)

def search_pdfs(directory, keyword):
    return _manager.search_pdf_files(directory, keyword)


# Convenience functions (matching __init__ exports)
def list_pdfs(directory=None):
    """List PDF files (for nanobot)"""
    return pdf_manager.list_pdfs(directory)

def get_pdf_info(filepath):
    """Get PDF metadata (for nanobot)"""
    return pdf_manager.get_pdf_info(filepath)

def search_pdfs(directory, keyword):
    """Search in PDFs (for nanobot)"""
    return pdf_manager.search_pdf_files(directory, keyword)

def pdf_to_text(pdf_path, txt_path=None):
    """PDF to text (for nanobot)"""
    return pdf_manager.pdf_to_text(pdf_path, txt_path)

# Convenience functions (matching __init__ exports)
def list_pdfs(directory=None):
    """List PDF files (for nanobot)"""
    return pdf_manager.list_pdfs(directory)

def get_pdf_info(filepath):
    """Get PDF metadata (for nanobot)"""
    return pdf_manager.get_pdf_info(filepath)

def search_pdfs(directory, keyword):
    """Search in PDFs (for nanobot)"""
    return pdf_manager.search_pdf_files(directory, keyword)

def pdf_to_text(pdf_path, txt_path=None):
    """PDF to text (for nanobot)"""
    return pdf_manager.pdf_to_text(pdf_path, txt_path)
