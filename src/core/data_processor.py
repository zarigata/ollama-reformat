"""
Data processing for PDF, text, and image files
"""

import os
import PyPDF2
from PIL import Image
import pytesseract
import json
from typing import List, Dict, Any
import io
import base64

class DataProcessor:
    """Processes various file types for fine-tuning"""
    
    def __init__(self):
        self.supported_formats = {
            'text': ['.txt', '.md', '.json', '.csv'],
            'pdf': ['.pdf'],
            'image': ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        }
    
    def process_files(self, files: List[str]) -> Dict[str, Any]:
        """Process uploaded files and return structured data"""
        results = {
            "total_files": len(files),
            "processed_files": [],
            "errors": [],
            "summary": {
                "text_files": 0,
                "pdf_files": 0,
                "image_files": 0,
                "total_chars": 0,
                "total_tokens": 0
            }
        }
        
        for file_path in files:
            try:
                file_ext = os.path.splitext(file_path)[1].lower()
                
                if file_ext in self.supported_formats['text']:
                    processed = self._process_text_file(file_path)
                    results["summary"]["text_files"] += 1
                elif file_ext in self.supported_formats['pdf']:
                    processed = self._process_pdf_file(file_path)
                    results["summary"]["pdf_files"] += 1
                elif file_ext in self.supported_formats['image']:
                    processed = self._process_image_file(file_path)
                    results["summary"]["image_files"] += 1
                else:
                    results["errors"].append(f"Unsupported format: {file_path}")
                    continue
                
                results["processed_files"].append(processed)
                results["summary"]["total_chars"] += processed.get("char_count", 0)
                results["summary"]["total_tokens"] += processed.get("token_count", 0)
                
            except Exception as e:
                results["errors"].append(f"Error processing {file_path}: {str(e)}")
        
        return results
    
    def _process_text_file(self, file_path: str) -> Dict[str, Any]:
        """Process text-based files"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        return {
            "filename": os.path.basename(file_path),
            "type": "text",
            "content": content,
            "char_count": len(content),
            "token_count": self._estimate_tokens(content),
            "preview": content[:500] + "..." if len(content) > 500 else content
        }
    
    def _process_pdf_file(self, file_path: str) -> Dict[str, Any]:
        """Process PDF files"""
        content = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                content += page.extract_text() + "\n\n"
        
        return {
            "filename": os.path.basename(file_path),
            "type": "pdf",
            "content": content.strip(),
            "char_count": len(content),
            "token_count": self._estimate_tokens(content),
            "pages": len(reader.pages),
            "preview": content[:500] + "..." if len(content) > 500 else content
        }
    
    def _process_image_file(self, file_path: str) -> Dict[str, Any]:
        """Process image files with OCR"""
        try:
            image = Image.open(file_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Extract text with OCR
            text = pytesseract.image_to_string(image)
            
            # Get image metadata
            width, height = image.size
            
            return {
                "filename": os.path.basename(file_path),
                "type": "image",
                "content": text.strip(),
                "char_count": len(text),
                "token_count": self._estimate_tokens(text),
                "dimensions": f"{width}x{height}",
                "preview": text[:500] + "..." if len(text) > 500 else text
            }
            
        except Exception as e:
            return {
                "filename": os.path.basename(file_path),
                "type": "image",
                "content": "",
                "char_count": 0,
                "token_count": 0,
                "error": str(e),
                "preview": "Failed to extract text"
            }
    
    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimation (4 chars per token average)"""
        return max(1, len(text) // 4)
    
    def chunk_data(self, data: List[Dict[str, Any]], chunk_size: int = 512) -> List[Dict[str, Any]]:
        """Chunk processed data for training"""
        chunks = []
        
        for item in data:
            content = item.get("content", "")
            if not content:
                continue
            
            # Split into chunks
            words = content.split()
            current_chunk = []
            current_length = 0
            
            for word in words:
                word_length = len(word) + 1  # +1 for space
                
                if current_length + word_length > chunk_size and current_chunk:
                    chunk_text = " ".join(current_chunk)
                    chunks.append({
                        "text": chunk_text,
                        "source": item["filename"],
                        "type": item["type"],
                        "tokens": self._estimate_tokens(chunk_text)
                    })
                    current_chunk = [word]
                    current_length = word_length
                else:
                    current_chunk.append(word)
                    current_length += word_length
            
            # Add remaining chunk
            if current_chunk:
                chunk_text = " ".join(current_chunk)
                chunks.append({
                    "text": chunk_text,
                    "source": item["filename"],
                    "type": item["type"],
                    "tokens": self._estimate_tokens(chunk_text)
                })
        
        return chunks
    
    def prepare_training_data(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Prepare data for fine-tuning"""
        total_tokens = sum(chunk["tokens"] for chunk in chunks)
        
        return {
            "chunks": chunks,
            "total_chunks": len(chunks),
            "total_tokens": total_tokens,
            "estimated_training_time": self._estimate_training_time(total_tokens),
            "format": "instruction",
            "sample": chunks[:3] if chunks else []
        }
    
    def _estimate_training_time(self, total_tokens: int) -> str:
        """Estimate training time based on token count"""
        # Rough estimates for different hardware
        hardware = HardwareDetector()
        
        if hardware.device == "cuda":
            tokens_per_minute = 10000  # GPU
        else:
            tokens_per_minute = 1000   # CPU
        
        minutes = total_tokens / tokens_per_minute
        
        if minutes < 60:
            return f"{minutes:.1f} minutes"
        elif minutes < 1440:
            return f"{minutes/60:.1f} hours"
        else:
            return f"{minutes/1440:.1f} days"
