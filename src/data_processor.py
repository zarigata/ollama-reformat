"""
Simple data processor for training data
Handles PDF, TXT, DOCX, CSV, JSON, MD files automatically
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any
import tempfile

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    import docx
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

class DataProcessor:
    """Simple data processing for training"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.supported_formats = {'.pdf', '.txt', '.docx', '.csv', '.json', '.md'}
    
    def process_files(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """Process uploaded files and extract text content"""
        processed_data = []
        
        for file_path in file_paths:
            try:
                content = self._extract_text(file_path)
                if content:
                    processed_data.append({
                        "filename": Path(file_path).name,
                        "content": content,
                        "format": Path(file_path).suffix.lower(),
                        "size": len(content)
                    })
            except Exception as e:
                self.logger.error(f"Failed to process {file_path}: {e}")
        
        return processed_data
    
    def _extract_text(self, file_path: str) -> str:
        """Extract text from various file formats"""
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        if extension == '.pdf' and PDF_AVAILABLE:
            return self._extract_pdf(file_path)
        elif extension == '.docx' and DOCX_AVAILABLE:
            return self._extract_docx(file_path)
        elif extension == '.txt' or extension == '.md':
            return self._extract_text_file(file_path)
        elif extension == '.csv':
            return self._extract_csv(file_path)
        elif extension == '.json':
            return self._extract_json(file_path)
        else:
            return self._extract_text_file(file_path)  # Fallback
    
    def _extract_pdf(self, file_path: Path) -> str:
        """Extract text from PDF"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n\n"
        except Exception as e:
            self.logger.error(f"PDF extraction failed: {e}")
        return text.strip()
    
    def _extract_docx(self, file_path: Path) -> str:
        """Extract text from DOCX"""
        try:
            doc = docx.Document(file_path)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            self.logger.error(f"DOCX extraction failed: {e}")
            return ""
    
    def _extract_text_file(self, file_path: Path) -> str:
        """Extract text from plain text files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            self.logger.error(f"Text file extraction failed: {e}")
            return ""
    
    def _extract_csv(self, file_path: Path) -> str:
        """Extract text from CSV"""
        try:
            import pandas as pd
            df = pd.read_csv(file_path)
            return df.to_string(index=False)
        except Exception as e:
            self.logger.error(f"CSV extraction failed: {e}")
            return self._extract_text_file(file_path)
    
    def _extract_json(self, file_path: Path) -> str:
        """Extract text from JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return json.dumps(data, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"JSON extraction failed: {e}")
            return self._extract_text_file(file_path)
    
    def prepare_training_data(self, processed_files: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Prepare data for training - simple format"""
        training_data = []
        
        for file_data in processed_files:
            content = file_data["content"]
            
            # Simple chunking - split by paragraphs
            paragraphs = content.split('\n\n')
            
            for para in paragraphs:
                if len(para.strip()) > 50:  # Skip very short paragraphs
                    training_data.append({
                        "text": para.strip(),
                        "source": file_data["filename"]
                    })
        
        return training_data
