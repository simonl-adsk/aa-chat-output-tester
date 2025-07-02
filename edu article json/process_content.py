#!/usr/bin/env python3
"""
Script to process the HTML content and create fresh JSON
"""

from rag_processor import process_html_simple

def main():
    # Read the HTML content
    with open('temp_html.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print("🚀 Processing comprehensive HTML content...")
    print("=" * 50)
    
    # Process the content
    result = process_html_simple(
        html_content=html_content,
        source_url="https://www.autodesk.com/support/account/education/students-educators/renew",
        filename="autodesk_renewal_guide.json"
    )
    
    if result:
        print("\n🎉 Fresh JSON created successfully!")
        print(f"📄 Output file: autodesk_renewal_guide.json")
    else:
        print("\n❌ Processing failed")

if __name__ == "__main__":
    main() 