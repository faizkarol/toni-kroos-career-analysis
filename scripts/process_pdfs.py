import os
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import pandas as pd
import re
from nltk.tokenize import sent_tokenize
import nltk

# Download NLTK data
nltk.download("punkt")

# Define folder containing PDFs and output CSV path
pdf_folder = r"H:\Toni_Kroos_Analysis\Raw_Data\Articles\Analysis_Pieces"
output_csv = os.path.join(pdf_folder, "summaries.csv")

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def clean_text(text):
    cleaned_text = re.sub(r"\s+", " ", text)  # Remove extra spaces
    cleaned_text = re.sub(r"Page \d+", "", cleaned_text)  # Remove page numbers
    return cleaned_text.strip() if cleaned_text.strip() else "No relevant text extracted"

def summarize_text(text, num_sentences=3):
    sentences = sent_tokenize(text)
    if len(sentences) < num_sentences:
        return " ".join(sentences) if sentences else "No content available to summarize"
    return " ".join(sentences[:num_sentences])

def extract_text_with_ocr_only(pdf_path):
    try:
        images = convert_from_path(pdf_path)
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"Error with OCR: {str(e)}"

# Process PDFs
summaries = []

for file in os.listdir(pdf_folder):
    if file.endswith(".pdf"):
        file_path = os.path.join(pdf_folder, file)
        try:
            raw_text = extract_text_with_ocr_only(file_path)
            with open(os.path.join(pdf_folder, f"{file}_raw.txt"), "w", encoding="utf-8") as txt_file:
                txt_file.write(raw_text)
            cleaned_text = clean_text(raw_text)
            summary = summarize_text(cleaned_text)
            summaries.append({
                "File Name": file,
                "Summary": summary,
                "Raw Text Length": len(raw_text),
                "Error": ""
            })
        except Exception as e:
            summaries.append({
                "File Name": file,
                "Summary": f"Error processing file: {str(e)}",
                "Raw Text Length": 0,
                "Error": f"Error: {str(e)}"
            })

# Save to CSV
df = pd.DataFrame(summaries)
df.to_csv(output_csv, index=False, encoding="utf-8")

print(f"Processing complete. Summaries saved to {output_csv}")
