"""
Resume parser - extracts clean text from PDFs.
Uses pdfplumber with layout-aware extraction + fallback to pypdf.
"""

import re
import pdfplumber


def _clean_text(text: str) -> str:
    """Normalize whitespace and fix common extraction artifacts."""
    # Remove non-printable chars except newlines/spaces
    text = re.sub(r'[^\x20-\x7E\n]', ' ', text)
    # Collapse multiple spaces to one
    text = re.sub(r'[ \t]+', ' ', text)
    # Collapse 3+ blank lines to 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract text from uploaded PDF using pdfplumber.
    Tries table-aware extraction first, then plain text fallback.
    Returns cleaned, normalized text string.
    """
    text_parts = []

    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                # Try to extract tables separately so they don't mangle text
                tables = page.extract_tables()
                table_bboxes = []
                if tables:
                    for table in tables:
                        # Flatten table cells into readable text
                        for row in table:
                            row_text = " | ".join(
                                cell.strip() if cell else ""
                                for cell in row
                                if cell
                            )
                            if row_text.strip():
                                text_parts.append(row_text)
                        # Note bboxes so we can exclude from main text
                        ts = page.find_tables()
                        for t in ts:
                            table_bboxes.append(t.bbox)

                # Extract main text excluding table regions
                if table_bboxes:
                    # Crop page excluding table areas
                    page_text = ""
                    for bbox in _get_non_table_regions(page, table_bboxes):
                        region = page.within_bbox(bbox)
                        t = region.extract_text()
                        if t:
                            page_text += t + "\n"
                else:
                    page_text = page.extract_text() or ""

                if page_text.strip():
                    text_parts.append(page_text)

    except Exception:
        # Fallback: try pypdf
        try:
            from pypdf import PdfReader
            reader = PdfReader(pdf_file)
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    text_parts.append(t)
        except Exception:
            return ""

    full_text = "\n".join(text_parts)
    return _clean_text(full_text)


def _get_non_table_regions(page, table_bboxes):
    """
    Return list of (x0, top, x1, bottom) bboxes on the page
    that don't overlap with any table.
    Simple vertical slicing by top/bottom of each table.
    """
    page_height = page.height
    page_width = page.width

    # Collect vertical spans occupied by tables
    occupied = sorted([(b[1], b[3]) for b in table_bboxes])

    regions = []
    prev_bottom = 0
    for top, bottom in occupied:
        if top > prev_bottom:
            regions.append((0, prev_bottom, page_width, top))
        prev_bottom = max(prev_bottom, bottom)
    if prev_bottom < page_height:
        regions.append((0, prev_bottom, page_width, page_height))

    return regions
