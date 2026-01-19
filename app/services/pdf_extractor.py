"""
PDF Extraction Service
Extract text from PDF files with OCR fallback
"""

import re
from pathlib import Path
from typing import List
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from app.utils.text_utils import clean_text
from app.utils.exceptions import PDFExtractionError


class PDFExtractor:
    """Service for extracting text from PDF documents"""
    
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        """
        Extract text from a PDF file with OCR fallback.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted and cleaned text from all pages
            
        Raises:
            PDFExtractionError: If extraction fails
        """
        try:
            path = Path(pdf_path)
            if not path.exists():
                raise PDFExtractionError(f"PDF file not found: {pdf_path}")
            
            if not path.suffix.lower() == '.pdf':
                raise PDFExtractionError(f"File is not a PDF: {pdf_path}")
            
            report_text: List[str] = []
            
            # Open the PDF file using PyMuPDF
            doc = fitz.open(pdf_path)
            
            # Loop through each page in the PDF
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Attempt to extract text directly from the page
                text = page.get_text("text")
                
                # If no text is found, use OCR as a fallback
                if not text.strip():
                    text = PDFExtractor._ocr_page(page)
                
                # Clean the extracted text
                text = clean_text(text)
                report_text.append(text)
            
            doc.close()
            
            # Join all pages with double newline
            return "\n\n".join(report_text)
            
        except fitz.FileDataError as e:
            raise PDFExtractionError(f"Invalid PDF file: {str(e)}")
        except Exception as e:
            if isinstance(e, PDFExtractionError):
                raise
            raise PDFExtractionError(f"PDF extraction failed: {str(e)}")
    
    @staticmethod
    def _ocr_page(page) -> str:
        """
        Perform OCR on a PDF page.
        
        Args:
            page: PyMuPDF page object
            
        Returns:
            OCR extracted text
        """
        try:
            # Render page as an image (pixmap)
            pix = page.get_pixmap()
            
            # Convert pixmap to a PIL Image
            img = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )
            
            # Perform OCR on the image
            text = pytesseract.image_to_string(img, lang="eng")
            return text
            
        except Exception as e:
            # Return empty string if OCR fails
            return ""
    
    @staticmethod
    def extract_text_from_bytes(pdf_bytes: bytes) -> str:
        """
        Extract text from PDF bytes (for file uploads).
        
        Args:
            pdf_bytes: PDF file content as bytes
            
        Returns:
            Extracted and cleaned text from all pages
        """
        try:
            report_text: List[str] = []
            
            # Open PDF from bytes
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text("text")
                
                if not text.strip():
                    text = PDFExtractor._ocr_page(page)
                
                text = clean_text(text)
                report_text.append(text)
            
            doc.close()
            
            return "\n\n".join(report_text)
            
        except Exception as e:
            raise PDFExtractionError(f"PDF extraction from bytes failed: {str(e)}")


# Singleton instance
pdf_extractor = PDFExtractor()
