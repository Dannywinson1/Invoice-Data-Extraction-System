import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image
import fitz  # pymupdf
from pdf2image import convert_from_path
import os
import re
import sqlite3
import argparse
import sys

def extract_text_from_file(file_path):
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        # Image: Direct OCR
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
    elif file_path.lower().endswith('.pdf'):
        # PDF: Try text extraction first
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        if text.strip():  # If text is present, use it
            return text
        # Otherwise, convert to images and OCR
        images = convert_from_path(file_path)
        for img in images:
            text += pytesseract.image_to_string(img) + "\n"
    else:
        raise ValueError("Unsupported file type")
    return text.strip()

def extract_entities(text):
    entities = {}
    
    # Invoice Number: Look for patterns like INV- followed by digits/alphanum
    inv_num_match = re.search(r'(?:Invoice\s*#?|INV-?|Bill\s*#?)\s*(?:Number\s*)?\s*:\s*([\w-]+)', text, re.IGNORECASE)
    entities['invoice_number'] = inv_num_match.group(1) if inv_num_match else None
    
    # Date: Simple YYYY-MM-DD or MM/DD/YYYY
    date_match = re.search(r'\b(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})\b', text)
    entities['date'] = date_match.group(1) if date_match else None
    
    # Total Amount: Look for "Total" followed by currency/amount
    amount_match = re.search(r'(?:Total|Amount Due|Total Amount)\s*[:$]?\s*\$?\s*([\d.,]+)', text, re.IGNORECASE)
    entities['total_amount'] = amount_match.group(1).replace(',', '') if amount_match else None  # Clean commas
    
    # Vendor Name: Assume it's near the top, after "From:" or company name pattern
    vendor_match = re.search(r'(?:From|Vendor|Supplier):\s*(.+)', text, re.IGNORECASE)
    entities['vendor_name'] = vendor_match.group(1).strip() if vendor_match else None
    
    return entities

def validate_entities(entities):
    errors = []
    if not entities['invoice_number']:
        errors.append("Missing invoice number")
    if entities['date']:
        # Basic date check (assumes YYYY-MM-DD)
        if not re.match(r'\d{4}-\d{2}-\d{2}', entities['date']):
            errors.append("Invalid date format")
    if entities['total_amount']:
        try:
            float(entities['total_amount'])
        except ValueError:
            errors.append("Invalid amount")
    if not entities['vendor_name']:
        errors.append("Missing vendor name")
    return errors, len(errors) == 0  # Return errors and validity flag

def init_db(db_path='invoices.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY,
            file_path TEXT,
            invoice_number TEXT,
            date TEXT,
            total_amount REAL,
            vendor_name TEXT,
            extraction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

def store_entities(conn, file_path, entities):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO invoices (file_path, invoice_number, date, total_amount, vendor_name)
        VALUES (?, ?, ?, ?, ?)
    ''', (file_path, entities['invoice_number'], entities['date'], 
          float(entities['total_amount']) if entities['total_amount'] else None, 
          entities['vendor_name']))
    conn.commit()

def main(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist. Please provide a valid path to an invoice file (PDF or image).")
        return
    
    conn = init_db()
    
    try:
        text = extract_text_from_file(file_path)
        entities = extract_entities(text)
        errors, is_valid = validate_entities(entities)
        
        if is_valid:
            store_entities(conn, file_path, entities)
            print("Extraction successful! Data stored.")
            print(entities)
        else:
            print("Validation errors:", errors)
    except Exception as e:
        print(f"Error processing file: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Invoice Data Extraction System")
    parser.add_argument('--file_path', type=str, default='sample_invoice.jpg', help="Path to the invoice file (PDF or image)")
    args = parser.parse_args()
    main(args.file_path)