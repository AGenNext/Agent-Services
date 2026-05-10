"""
Data Preparation Module

Tools for preparing data for AI/ML processing.
"""

from dataclasses import dataclass
from typing import Optional, Callable
from enum import Enum
import re
import json


class DataFormat(Enum):
    """Input data formats."""
    JSON = "json"
    MARKDOWN = "md"
    HTML = "html"
    PDF = "pdf"
    CSV = "csv"
    TXT = "txt"
    DOCX = "docx"
    RTF = "rtf"


class ChunkStrategy(Enum):
    """Text chunking strategies."""
    FIXED = "fixed"
    SENTENCE = "sentence"
    PARAGRAPH = "paragraph"
    RECURSIVE = "recursive"


@dataclass
class DataPrepConfig:
    """Data preparation configuration."""
    max_tokens: int = 2048
    overlap: int = 200
    strategy: ChunkStrategy = ChunkStrategy.SENTENCE
    preserve_formatting: bool = True
    strip_html: bool = True
    clean_whitespace: bool = True


class TextCleaner:
    """Clean and normalize text data."""
    
    @staticmethod
    def clean(text: str, remove_html: bool = True) -> str:
        """Clean text data."""
        result = text
        
        if remove_html:
            # Remove HTML tags
            result = re.sub(r'<[^>]+>', '', result)
            # Remove HTML entities
            result = re.sub(r'&[a-z]+;', ' ', result)
        
        # Normalize whitespace
        result = re.sub(r'\s+', ' ', result)
        
        # Remove control characters
        result = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', result)
        
        return result.strip()
    
    @staticmethod
    def remove_urls(text: str) -> str:
        """Remove URLs from text."""
        return re.sub(r'https?://\S+', '[URL]', text)
    
    @staticmethod
    def remove_emails(text: str) -> str:
        """Remove email addresses."""
        return re.sub(r'[\w.-]+@[\w.-]+', '[EMAIL]', text)
    
    @staticmethod
    def normalize_date(text: str) -> str:
        """Normalize date formats."""
        # Simple date normalization
        text = re.sub(r'\d{1,2}/\d{1,2}/\d{2,4}', '[DATE]', text)
        text = re.sub(r'\d{4}-\d{2}-\d{2}', '[DATE]', text)
        return text
    
    @staticmethod
    def truncate(text: str, max_length: int = 1000, suffix: str = "...") -> str:
        """Truncate text to max length."""
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix


class TextChunker:
    """Split text into chunks for processing."""
    
    def __init__(self, config: Optional[DataPrepConfig] = None):
        self.config = config or DataPrepConfig()
    
    def chunk(self, text: str) -> list[str]:
        """Split text into chunks."""
        if self.config.strategy == ChunkStrategy.FIXED:
            return self._chunk_fixed(text)
        elif self.config.strategy == ChunkStrategy.SENTENCE:
            return self._chunk_sentence(text)
        elif self.config.strategy == ChunkStrategy.PARAGRAPH:
            return self._chunk_paragraph(text)
        else:
            return self._chunk_recursive(text)
    
    def _chunk_fixed(self, text: str) -> list[str]:
        """Fixed-size chunks."""
        tokens_per_chunk = self.config.max_tokens
        overlap = self.config.overlap
        
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), tokens_per_chunk - overlap):
            chunk = ' '.join(words[i:i + tokens_per_chunk])
            if chunk:
                chunks.append(chunk)
        
        return chunks
    
    def _chunk_sentence(self, text: str) -> list[str]:
        """Split by sentences."""
        # Simple sentence splitting
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current = ""
        
        for sent in sentences:
            if len(current) + len(sent) > self.config.max_tokens and current:
                chunks.append(current)
                current = sent
            else:
                current += " " + sent if current else sent
        
        if current:
            chunks.append(current)
        
        return [c.strip() for c in chunks if c.strip()]
    
    def _chunk_paragraph(self, text: str) -> list[str]:
        """Split by paragraphs."""
        paragraphs = text.split('\n\n')
        
        chunks = []
        current = ""
        
        for para in paragraphs:
            if len(current) + len(para) > self.config.max_tokens and current:
                chunks.append(current)
                current = para
            else:
                current += "\n\n" + para if current else para
        
        if current:
            chunks.append(current)
        
        return [c.strip() for c in chunks if c.strip()]
    
    def _chunk_recursive(self, text: str) -> list[str]:
        """Recursive chunking with fallbacks."""
        # Try paragraphs first
        paragraphs = text.split('\n\n')
        if len(paragraphs) > 1:
            return self._chunk_paragraph(text)
        
        # Try sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        if len(sentences) > 1:
            return self._chunk_sentence(text)
        
        # Fall back to fixed
        return self._chunk_fixed(text)
    
    def estimate_tokens(self, text: str) -> int:
        """Estimate token count (simple approximation)."""
        return len(text.split()) * 4 // 3


class DataValidator:
    """Validate and transform input data."""
    
    @staticmethod
    def validate_json(data: str) -> tuple[bool, Optional[dict]]:
        """Validate JSON data."""
        try:
            return True, json.loads(data)
        except json.JSONDecodeError as e:
            return False, {"error": str(e)}
    
    @staticmethod
    def validate_length(
        text: str, 
        min_len: int = 10, 
        max_len: int = 100000
    ) -> tuple[bool, str]:
        """Validate text length."""
        if len(text) < min_len:
            return False, f"Text too short: {len(text)} < {min_len}"
        if len(text) > max_len:
            return False, f"Text too long: {len(text)} > {max_len}"
        return True, ""
    
    @staticmethod
    def validate_encoding(text: str) -> tuple[bool, str]:
        """Validate text encoding."""
        try:
            text.encode('utf-8')
            return True, ""
        except UnicodeEncodeError as e:
            return False, f"Encoding error: {e}"
    
    @staticmethod
    def detect_format(data: str) -> DataFormat:
        """Detect data format."""
        data = data.strip()
        
        if data.startswith('{') or data.startswith('['):
            return DataFormat.JSON
        
        if '<' in data and '</' in data:
            return DataFormat.HTML
        
        if '# ' in data or '* ' in data:
            return DataFormat.MARKDOWN
        
        if ',' in data and '\n' in data:
            return DataFormat.CSV
        
        return DataFormat.TXT


class DataTransformer:
    """Transform data between formats."""
    
    @staticmethod
    def json_to_markdown(data: dict, title: str = "") -> str:
        """Convert JSON to Markdown."""
        lines = []
        
        if title:
            lines.append(f"# {title}\n")
        
        def format_dict(d: dict, indent: int = 0):
            for key, value in d.items():
                prefix = "  " * indent
                if isinstance(value, dict):
                    lines.append(f"{prefix}{key}:")
                    format_dict(value, indent + 1)
                elif isinstance(value, list):
                    lines.append(f"{prefix}{key}:")
                    for item in value:
                        lines.append(f"{prefix}  - {item}")
                else:
                    lines.append(f"{prefix}{key}: {value}")
        
        format_dict(data)
        return '\n'.join(lines)
    
    @staticmethod
    def csv_to_json(csv: str) -> list[dict]:
        """Convert CSV to JSON."""
        lines = csv.strip().split('\n')
        
        if len(lines) < 2:
            return []
        
        headers = [h.strip() for h in lines[0].split(',')]
        result = []
        
        for line in lines[1:]:
            values = [v.strip() for v in line.split(',')]
            if len(values) == len(headers):
                result.append(dict(zip(headers, values)))
        
        return result
    
    @staticmethod
    def markdown_to_json(md: str) -> dict:
        """Convert Markdown to structured JSON."""
        result = {"sections": []}
        current_section = {"title": "", "content": []}
        
        for line in md.split('\n'):
            if line.startswith('# '):
                if current_section["title"]:
                    result["sections"].append(current_section)
                current_section = {"title": line[2:], "content": []}
            else:
                current_section["content"].append(line)
        
        if current_section["title"]:
            result["sections"].append(current_section)
        
        return result


@dataclass
class DataPrepResult:
    """Result of data preparation."""
    original_length: int
    cleaned_length: int
    chunks: int
    format: DataFormat
    valid: bool
    errors: list[str]


def prepare_data(
    data: str,
    config: Optional[DataPrepConfig] = None
) -> DataPrepResult:
    """Prepare data for AI processing."""
    config = config or DataPrepConfig()
    
    errors = []
    
    # Clean
    if config.clean_whitespace:
        data = TextCleaner.clean(data, remove_html=config.strip_html)
    
    # Validate
    valid, msg = DataValidator.validate_length(data)
    if not valid:
        errors.append(msg)
    
    # Detect format
    fmt = DataValidator.detect_format(data)
    
    # Chunk
    chunker = TextChunker(config)
    chunks = chunker.chunk(data)
    
    return DataPrepResult(
        original_length=len(data),
        cleaned_length=len(data),
        chunks=len(chunks),
        format=fmt,
        valid=len(errors) == 0,
        errors=errors
    )


# CLI for testing
if __name__ == "__main__":
    # Example: prepare data
    text = """
    # Sample Document
    
    This is a sample document for testing data preparation.
    It contains multiple paragraphs and some text.
    
    ## Section 1
    
    This is the first section with some content.
    
    ## Section 2
    
    This is the second section.
    """
    
    result = prepare_data(text)
    print(f"Chunks: {result.chunks}")
    print(f"Valid: {result.valid}")