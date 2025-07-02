#!/usr/bin/env python3
"""
RAG-Optimized HTML Processor for Autodesk Education Content
Extracts clean content optimized for vector embeddings and retrieval
"""

from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
from typing import Dict, List

def extract_content_simple(html_content: str) -> tuple[str, str, str]:
    """Simple content extraction that works"""
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract title
    title_element = soup.find('h1', class_='dhig-my-0 dhig-typography-headline-large')
    title = title_element.get_text().strip() if title_element else "Autodesk Support Article"
    
    # Extract category
    category_element = soup.find('div', class_='dhig-typography-eyebrow dhig-mb-2')
    category = category_element.get_text().strip() if category_element else ""
    
    # Remove unwanted elements
    for element in soup.select('.cmp-share, .cmp-divider, .MuiDivider-root, .cmp-feedback, .dhig-flex, .dhig-grid'):
        element.decompose()
    
    # Get clean text from paragraphs - PRESERVE LINKS
    content_parts = []
    
    # Get paragraphs with links preserved
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        # Process links within paragraphs first
        for a_tag in p.find_all('a'):
            if a_tag.get('href'):
                href = str(a_tag.get('href'))
                link_text = a_tag.get_text(strip=True)
                
                # Convert relative URLs to absolute
                if href.startswith('/'):
                    full_url = 'https://www.autodesk.com' + href
                elif href.startswith('http'):
                    full_url = href
                else:
                    full_url = 'https://www.autodesk.com/' + href.lstrip('/')
                
                # Replace the link with formatted text
                new_link = f"{link_text} ({full_url})"
                a_tag.replace_with(new_link)
        
        # Now get the text with preserved links
        text = p.get_text(strip=True)
        if text and len(text) > 10 and text != "":
            clean_text = re.sub(r'\s+', ' ', text)
            content_parts.append(clean_text)
    
    # Get lists
    lists = soup.find_all(['ol', 'ul'])
    for list_elem in lists:
        list_items = []
        for li in list_elem.find_all('li'):
            item_text = li.get_text(strip=True)
            if item_text:
                list_items.append(item_text)
        
        if list_items:
            if list_elem.name == 'ol':
                formatted_list = "\n".join([f"{i+1}. {item}" for i, item in enumerate(list_items)])
            else:
                formatted_list = "\n".join([f"• {item}" for item in list_items])
            content_parts.append(formatted_list)
    
    # Get headers
    headers = soup.find_all(['h2', 'h3'])
    for header in headers:
        header_text = header.get_text(strip=True)
        if header_text and header_text != title:
            content_parts.append(f"Section: {header_text}")
    
    # Combine content
    clean_content = "\n\n".join(content_parts)
    clean_content = re.sub(r'\n{3,}', '\n\n', clean_content)
    clean_content = clean_content.strip()
    
    print(f"DEBUG: Extracted {len(clean_content)} characters of content")
    print(f"DEBUG: First 200 chars: {clean_content[:200]}...")
    
    return clean_content, title, category

def create_rag_json_simple(html_content: str, source_url: str = "") -> Dict:
    """Create simplified RAG JSON"""
    
    # Extract content
    clean_content, title, category = extract_content_simple(html_content)
    
    if not clean_content or len(clean_content.strip()) < 50:
        print(f"DEBUG: Content too short: {len(clean_content)} chars")
        print(f"DEBUG: Content: '{clean_content}'")
        raise ValueError(f"Insufficient content extracted: {len(clean_content)} characters")
    
    # Basic metadata
    word_count = len(clean_content.split())
    token_estimate = int(word_count * 1.3)
    
    # Create summary (first 200 chars)
    summary = clean_content[:200] + "..." if len(clean_content) > 200 else clean_content
    
    # Simple keywords
    keywords = []
    content_lower = clean_content.lower()
    keyword_candidates = [
        'education', 'student', 'access', 'renewal', 'expiration', 
        'eligibility', 'account', 'autodesk', 'software', 'plan'
    ]
    
    for keyword in keyword_candidates:
        if keyword in content_lower:
            keywords.append(keyword)
    
    # Create JSON structure
    json_output = {
        "document_id": f"autodesk_{int(datetime.now().timestamp())}",
        "source_url": source_url,
        "source_name": "Autodesk",
        "title": title,
        "category": category,
        "document_type": "educational_resource",
        "date_retrieved": datetime.now().isoformat()[:10],
        
        "content": {
            "text": clean_content,
            "summary": summary,
            "word_count": word_count,
            "estimated_tokens": token_estimate
        },
        
        "metadata": {
            "keywords": keywords,
            "category": category,
            "audience": "education"
        }
    }
    
    return json_output

def process_html_simple(html_content: str, source_url: str = "", filename: str = "autodesk_simple_rag.json") -> Dict:
    """Process HTML content with simplified approach"""
    
    try:
        json_data = create_rag_json_simple(html_content, source_url)
        
        # Save to file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        # Print summary
        print("🎯 Simple RAG processing completed!")
        print(f"📄 File saved: {filename}")
        print(f"📝 Title: {json_data['title']}")
        print(f"📂 Category: {json_data['category']}")
        print(f"📊 Content: {json_data['content']['word_count']} words")
        print(f"🏷️  Keywords: {', '.join(json_data['metadata']['keywords'])}")
        
        return json_data
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {}

if __name__ == "__main__":
    print("RAG Processor for Autodesk Education Content")
    print("Usage: from rag_processor import process_html_simple")
    print("Example: process_html_simple(html_content, source_url, 'output.json')") 