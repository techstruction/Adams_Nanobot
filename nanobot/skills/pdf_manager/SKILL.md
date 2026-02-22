# PDF Manager Skill

Complete PDF management for nanobot - Read and create PDF files.

## Features

- **Read PDF**: Extract text from PDF files
- **Create PDF**: Generate new PDF files from text
- **List PDFs**: Find PDF files in workspace
- **PDF Info**: Get metadata (page count, etc.)
- **Search PDF**: Search text within PDFs
- **Merge PDFs**: Combine multiple PDFs (future feature)
- **PDF to Text**: Extract all text to .txt file

## Requirements

- Python 3.12+
- PyPDF2 (PDF reading)
- reportlab (PDF creation)
- Access to workspace directory

## Installation

Dependencies are automatically installed:

```bash
pip install PyPDF2 reportlab
# or
uv pip install PyPDF2 reportlab
```

## Usage

### Read PDF

```bash
# Extract text from PDF
nanobot agent -m "Read PDF file roadmap.pdf"

# Read specific pages
nanobot agent -m "Read pages 5-10 of somedoc.pdf"

# Extract to text file
nanobot agent -m "Extract text from report.pdf and save as report.txt"
```

### Create PDF

```bash
# Create PDF from text
nanobot agent -m "Create PDF file summary.pdf with content 'Project summary Q1'"

# Create from multiple text sections
nanobot agent -m "Create PDF with title 'Meeting Notes', body 'Discussed: 1. Dashboard release 2. Skill development'"

# Create with formatting
nanobot agent -m "Create formatted PDF 'presentation.pdf' with headings and bullet points"
```

### List PDFs

```bash
# List all PDFs in workspace
nanobot agent -m "List all PDF files"

# Find PDFs in subdirectory
nanobot agent -m "Find all PDFs in the docs folder"
```

### PDF Info

```bash
# Get PDF metadata
nanobot agent -m "Get info about presentation.pdf"

# Count pages
nanobot agent -m "How many pages in report.pdf"
```

### Search PDF

```bash
# Search for keyword across all PDFs
nanobot agent -m "Find PDFs containing 'budget'"

# Search specific PDF
nanobot agent -m "Search nanobot.pdf for 'API'
```

## API

### Functions

#### read_pdf(filepath, pages=None)
Extract text from PDF file
- `filepath`: Path to PDF file
- `pages`: Optional page range (e.g., "1-5")

#### create_pdf(filepath, content, title=None)
Create new PDF file
- `filepath`: Output PDF path
- `content`: Text content
- `title`: Optional title in PDF

#### list_pdfs(directory)
Find all PDFs in directory
- Returns list of PDF file paths

#### get_pdf_info(filepath)
Get PDF metadata
- Returns dict with page_count, file_size, etc.

#### search_pdf_files(directory, keyword)
Search for keyword in all PDFs
- Returns list of matching PDFs and lines

#### pdf_to_text(pdf_path, txt_path)
Extract all text to .txt file

## Technical Details

### PDF Reading (PyPDF2)

```python
import PyPDF2

# Read entire PDF
with open('file.pdf', 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
```

### PDF Creation (reportlab)

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

c = canvas.Canvas("output.pdf", pagesize=letter)
c.drawString(100, 750, "Title")
c.drawString(100, 730, "Content")
c.save()
```

### Supported Formats

**Input:**
- .pdf (PyPDF2 compatible)
- Text files for PDF creation
- UTF-8 encoding for multi-language support

**Output:**
- .pdf files (reportlab)
- .txt extracted text
- UTF-8 encoding

## File Locations

**Workspace PDFs:**
- Default: ~/.nanobot/workspace/
- Subdirectories supported
- Valid extensions: .pdf, .PDF

**Created PDFs:**
- Saved to workspace directory
- Overwrite protection (renames if duplicate)

## Limitations

- PDF reading: May lose complex formatting (tables, images)
- OCR not supported (scanned PDFs won't work)
- Maximum file size: 50MB (configurable)
- Encrypted PDFs: Must provide password

## Security

- Only accesses workspace directory
- Cannot read files outside workspace (sandboxed)
- New files get standard user permissions
- Encrypted PDFs: password required

## Troubleshooting

**"PDF not found"**
- File must be in workspace directory
- Check file extension (.pdf)
- Use relative path from workspace

**"Unsupported PDF"**
- PDF may be encrypted
- PDF may be scanned/image-based
- File may be corrupted

**"Permission denied"**
- Check workspace permissions
- Ensure PDF is readable by current user

## Performance

- Read small PDF (< 1MB): < 1 second
- Read large PDF (10MB): < 5 seconds
- Create PDF from text: < 1 second

## Future Features (v2.1+)

- [ ] PDF merging/splitting
- [ ] Add images to PDF
- [ ] PDF encryption/password protection
- [ ] Table support in generated PDFs
- [ ] Links and annotations
- [ ] Form field creation

---

**Version:** 1.0.0  
**Status:** Production Ready  
**PDF Standard:** PDF 1.7 compatible
