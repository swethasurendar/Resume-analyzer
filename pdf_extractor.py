import pdfplumber
import os
from pathlib import Path


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF file using pdfplumber.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text from all pages
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = '\n'.join([page.extract_text() or '' for page in pdf.pages])
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""


def extract_text_with_metadata(pdf_path: str) -> dict:
    """
    Extract text and metadata from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary containing text and metadata
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            result = {
                'filename': os.path.basename(pdf_path),
                'num_pages': len(pdf.pages),
                'text': '',
                'tables': []
            }
            
            # Extract text from all pages
            all_text = []
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text() or ''
                all_text.append(page_text)
                
                # Extract tables from each page
                tables = page.extract_tables()
                if tables:
                    result['tables'].append({
                        'page': page_num,
                        'tables': tables
                    })
            
            result['text'] = '\n'.join(all_text)
            return result
            
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None


def extract_from_multiple_pdfs(directory: str) -> dict:
    """
    Extract text from all PDF files in a directory.
    
    Args:
        directory: Path to directory containing PDFs
        
    Returns:
        Dictionary with filenames as keys and extracted text as values
    """
    results = {}
    pdf_files = Path(directory).glob('*.pdf')
    
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file.name}...")
        text = extract_text_from_pdf(str(pdf_file))
        results[pdf_file.name] = text
    
    return results


if __name__ == "__main__":
    # Example usage
    pdf_path = "sample_resume.pdf"
    
    if os.path.exists(pdf_path):
        # Extract simple text
        text = extract_text_from_pdf(pdf_path)
        print("Extracted Text:")
        print(text)
        print("\n" + "="*50 + "\n")
        
        # Extract with metadata
        data = extract_text_with_metadata(pdf_path)
        if data:
            print(f"File: {data['filename']}")
            print(f"Pages: {data['num_pages']}")
            if data['tables']:
                print(f"Tables found: {len(data['tables'])}")
    else:
        print(f"PDF file not found: {pdf_path}")
