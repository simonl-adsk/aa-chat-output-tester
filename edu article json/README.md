# RAG Processor for Autodesk Education Content

Convert Autodesk support HTML content into clean JSON optimized for RAG (Retrieval-Augmented Generation) systems.

## Features

✅ **Clean Content Extraction** - Removes HTML noise, preserves structure  
✅ **Links Preserved** - Keeps clickable links in text for user actions  
✅ **RAG Optimized** - Perfect for vector embeddings and semantic search  
✅ **Rich Metadata** - Keywords, categories, token estimates  
✅ **Structured Output** - Consistent JSON schema for easy ingestion  

## Quick Start

```python
from rag_processor import process_html_simple

# Process your HTML content
result = process_html_simple(
    html_content="<your_autodesk_html_here>",
    source_url="https://www.autodesk.com/support/...",
    filename="output.json"
)
```

## Output Format

```json
{
  "document_id": "autodesk_1234567890",
  "source_url": "https://www.autodesk.com/...",
  "title": "Renewing access to Education software",
  "category": "Account management for education",
  "content": {
    "text": "Clean text with preserved links (https://...)",
    "summary": "Auto-generated summary...",
    "word_count": 372,
    "estimated_tokens": 483
  },
  "metadata": {
    "keywords": ["education", "access", "renewal"],
    "audience": "education"
  }
}
```

## Content Processing

The processor:
- Extracts title and category from Autodesk page structure
- Preserves links in format: `link_text (full_URL)`
- Removes UI elements (dividers, share buttons, feedback forms)
- Maintains paragraph structure and numbered/bulleted lists
- Converts relative URLs to absolute URLs
- Generates relevant keywords for better retrieval

## Perfect for RAG Systems

- **Vector Embeddings**: Clean text produces better semantic embeddings
- **User Experience**: Preserved links allow users to take action
- **Content Search**: Rich metadata enables filtering and ranking
- **Token Efficiency**: Optimized content fits in model context windows

## Workflow

1. Copy HTML content from Autodesk education support pages
2. Run through processor 
3. Get clean JSON ready for your RAG pipeline
4. Embed content in vector database (Pinecone, Weaviate, etc.)
5. Use for semantic search and question answering

## Dependencies

- BeautifulSoup4
- Standard Python libraries (json, re, datetime, typing)

Clean, production-ready processor for converting Autodesk education content into RAG-optimized JSON. 