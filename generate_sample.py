from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_invoice():
    # Create a white image
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font, fallback to basic
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    # Invoice content
    content = [
        "INVOICE",
        "",
        "Invoice Number: INV-12345",
        "Date: 2025-12-29",
        "",
        "From: ABC Company",
        "123 Business St, City, State 12345",
        "",
        "To: Customer Name",
        "456 Customer Ave, City, State 67890",
        "",
        "Description: Services Rendered",
        "Quantity: 1",
        "Unit Price: $1000.00",
        "",
        "Total Amount: $1000.00"
    ]
    
    y = 50
    for line in content:
        draw.text((50, y), line, fill='black', font=font)
        y += 30
    
    # Save the image
    img.save('sample_invoice.jpg')
    print("Sample invoice image created: sample_invoice.jpg")

if __name__ == "__main__":
    create_sample_invoice()