import os
import sys

# Suppress some noisy logs if desired, or ensure we fall back gracefully
# os.environ["OMP_NUM_THREADS"] = "1" 

from docling.document_converter import DocumentConverter
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_community.document_loaders import PyPDFLoader, UnstructuredImageLoader
import logging

# Set logging level to avoid too much noise from dependencies if needed
# logging.getLogger("docling").setLevel(logging.ERROR)

### 🔹 Docling Parsing
def parse_with_docling(file_path):
    """
    Parses a file (PDF, Image, etc.) using Docling, extracts markdown content.
    """
    try:
        # Ensure file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        print(f"\n🔍 [Docling] Processing: {file_path}")
        
        # Initialize Docling Converter
        converter = DocumentConverter()
        result = converter.convert(file_path)
        markdown_document = result.document.export_to_markdown()

        # Define headers to split on
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        
        # Initialize Markdown Splitter
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        docs_list = markdown_splitter.split_text(markdown_document)

        # Print full extracted sections
        print(f"✅ Extracted {len(docs_list)} sections with Docling.")
        for idx, doc in enumerate(docs_list[:3]): # Show first 3 for brevity
            print(f"\n🔹 Section {idx + 1}:\n{doc.page_content[:200]}..." if len(doc.page_content) > 200 else f"\n🔹 Section {idx + 1}:\n{doc.page_content}")
            print("-" * 40)
        
        if len(docs_list) > 3:
            print(f"... and {len(docs_list) - 3} more sections.")

        return docs_list

    except Exception as e:
        print(f"❌ Error during Docling processing: {e}")
        return []

### 🔹 LangChain Parsing
def parse_with_langchain(file_path):
    """
    Parses a file using LangChain's loaders. Handles PDF and Images separately.
    """
    try:
        # Ensure file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        print(f"\n🔍 [LangChain] Processing: {file_path}")
        
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == ".pdf":
            # Load PDF using PyPDFLoader
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            text = "\n\n".join([page.page_content for page in pages])
        elif ext in [".png", ".jpg", ".jpeg"]:
            # Load Image using UnstructuredImageLoader
            # Note: requires 'unstructured' and 'tesseract'
            try:
                loader = UnstructuredImageLoader(file_path)
                pages = loader.load()
                text = "\n\n".join([page.page_content for page in pages])
            except Exception as img_err:
                return f"❌ LangChain (Unstructured) failed for image: {img_err}"
        else:
            return f"⚠ Unsupported extension for LangChain in this test: {ext}"

        # Print summary
        if text.strip():
            print(f"✅ Extracted content with LangChain ({len(text)} chars).")
            print(f"Preview: {text[:200]}...")
        else:
            print("⚠ LangChain extracted NO text (might be a scanned file without OCR).")

        return text

    except Exception as e:
        print(f"❌ Error during LangChain processing: {e}")
        return ""

### 🔹 Main Execution
def main():
    # Detect the working directory to find files
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ocr_path = os.path.join(base_dir, "ocr_test.pdf")
    scanned_path = os.path.join(base_dir, "sample.png")
    
    # 1. OCR PDF
    parse_with_docling(ocr_path)
    parse_with_langchain(ocr_path)

    # 2. Scanned Image
    parse_with_docling(scanned_path)
    parse_with_langchain(scanned_path)

if __name__ == "__main__":
    main()
