import re
from pypdf import PdfReader


def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text



def split_clauses(text):
    # 🔹 Step 1: Normalize spacing
    text = re.sub(r'\s+', ' ', text)

    # 🔹 Step 2: Remove header before first clause
    match = re.search(r'\d+\.', text)
    if match:
        text = text[match.start():]   # start from first clause

    # 🔹 Step 3: Add newline before clause numbers
    text = re.sub(r'(\d+)\.\s+', r'\n\1. ', text)

    # 🔹 Step 4: Split clauses
    raw_clauses = re.split(r'\n(?=\d+\.)', text)

    # 🔹 Step 5: Clean
    clauses = []
    for c in raw_clauses:
        c = c.strip()
        if len(c) > 50:
            clauses.append(c)

    return clauses