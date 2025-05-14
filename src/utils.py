from PyPDF2 import PdfReader
from docx import Document

def parse_pdf(file):
    reader = PdfReader(file)
    text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    return text

def parse_docx(file):
    doc = Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def parse_txt(file):
    return file.read().decode("utf-8")

def parse_uploaded_file(file):
    if file.type == "application/pdf":
        return parse_pdf(file)
    elif file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
        return parse_docx(file)
    elif file.type == "text/plain":
        return parse_txt(file)
    else:
        return "Unsupported file type." 