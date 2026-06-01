# ⬡ Invoicely.AI — Layout-Aware Invoice Extraction Engine

A fast, layout-aware extraction engine that converts unstructured PDF invoices into strict JSON data. Built with Python, FastAPI, and `pdfplumber`.

## How it works
Unlike standard OCR that reads left-to-right and destroys table formatting, this engine parses the exact X/Y coordinate geometry of the PDF. This preserves multi-column layouts, allowing our heuristics to extract data with high accuracy without needing per-vendor templates.

## Getting Started

**1. Clone the repository**
```bash
git clone [https://github.com/Dannywinson1/Invoice-Data-Extraction-System.git](https://github.com/Dannywinson1/Invoice-Data-Extraction-System.git)
cd Invoice-Data-Extraction-System