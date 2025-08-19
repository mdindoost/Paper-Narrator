"""Extract and clean text from research paper PDFs"""

import PyPDF2
import re
from pathlib import Path
from typing import Dict, List, Optional


class PDFProcessor:
    def __init__(self):
        self.common_headers = [
            "abstract", "introduction", "methodology", "methods", 
            "results", "discussion", "conclusion", "references",
            "acknowledgments", "appendix"
        ]
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract all text from a PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- Page {page_num + 1} ---\n"
                        text += page_text
                
                return self._clean_text(text)
                
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove page markers we added
        text = re.sub(r'\n--- Page \d+ ---\n', '\n', text)
        
        # Fix common PDF extraction issues
        text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single
        text = re.sub(r'\n\s*\n', '\n\n', text)  # Multiple newlines to double
        text = re.sub(r'-\s*\n\s*', '', text)  # Remove hyphenation breaks
        
        # Remove page numbers and headers/footers (common patterns)
        text = re.sub(r'\n\d+\n', '\n', text)  # Standalone page numbers
        text = re.sub(r'\n[A-Z\s]{10,}\n', '\n', text)  # ALL CAPS headers
        
        # Clean up spacing
        text = text.strip()
        
        return text
    
    def extract_sections(self, text: str) -> Dict[str, str]:
        """Try to identify and extract paper sections"""
        sections = {}
        text_lower = text.lower()
        
        # Find section boundaries
        section_positions = []
        
        for section in self.common_headers:
            # Look for section headers (various formats)
            patterns = [
                f"\n{section}\n",
                f"\n{section.upper()}\n", 
                f"\n{section.title()}\n",
                f"\n\d+\.?\s*{section}\n",
                f"\n\d+\.?\s*{section.title()}\n"
            ]
            
            for pattern in patterns:
                matches = list(re.finditer(pattern, text_lower))
                for match in matches:
                    section_positions.append((match.start(), section, match.group()))
        
        # Sort by position
        section_positions.sort(key=lambda x: x[0])
        
        # Extract sections
        for i, (start_pos, section_name, match_text) in enumerate(section_positions):
            start_idx = start_pos + len(match_text)
            
            # Find end position (next section or end of text)
            if i + 1 < len(section_positions):
                end_idx = section_positions[i + 1][0]
            else:
                end_idx = len(text)
            
            section_text = text[start_idx:end_idx].strip()
            if section_text and len(section_text) > 50:  # Ignore tiny sections
                sections[section_name] = section_text
        
        # If no sections found, return the whole text as "content"
        if not sections:
            sections["content"] = text
            
        return sections
    
    def chunk_text(self, text: str, max_size: int = 4000, 
                   overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks for processing"""
        if len(text) <= max_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + max_size
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence end within last 200 chars
                sentence_end = text.rfind('.', end - 200, end)
                if sentence_end > start:
                    end = sentence_end + 1
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position with overlap
            start = end - overlap
            if start >= len(text):
                break
                
        return chunks
    
    def process_paper(self, pdf_path: str) -> Dict:
        """Complete processing pipeline for a research paper"""
        print(f"Processing paper: {pdf_path}")
        
        # Extract text
        raw_text = self.extract_text_from_pdf(pdf_path)
        print(f"Extracted {len(raw_text):,} characters")
        
        # Extract sections
        sections = self.extract_sections(raw_text)
        print(f"Found sections: {list(sections.keys())}")
        
        # Create chunks if text is too long
        chunks = self.chunk_text(raw_text)
        print(f"Created {len(chunks)} chunks for processing")
        
        return {
            "raw_text": raw_text,
            "sections": sections,
            "chunks": chunks,
            "metadata": {
                "total_length": len(raw_text),
                "num_sections": len(sections),
                "num_chunks": len(chunks)
            }
        }
