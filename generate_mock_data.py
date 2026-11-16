import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import json

def generate_pdf(filename, title, content_blocks):
    os.makedirs("data/raw_pdfs", exist_ok=True)
    filepath = os.path.join("data/raw_pdfs", filename)
    doc = SimpleDocTemplate(filepath, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=16, leading=20, spaceAfter=12)
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=12, leading=16, spaceAfter=8)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=10)

    story = [Paragraph(title, title_style), Spacer(1, 12)]
    
    for heading, text in content_blocks:
        story.append(Paragraph(heading, heading_style))
        story.append(Paragraph(text, body_style))
        story.append(Spacer(1, 8))
        
    doc.build(story)
    print(f"Generated: {filepath}")

# 1. Generate v1 of Regulatory Act
v1_content = [
    ("Section 101: Algorithmic Transparency in Lending", 
     "All automated credit scoring models utilized by financial institutions must maintain an explainability index of at least 85%. Risk weights assigned via machine learning models (e.g., XGBoost, Neural Networks) must be disclosed to borrowers upon request within 30 business days. Effective date: January 1, 2025."),
    ("Section 102: Data Retention & Proxy Variables", 
     "Institutions are strictly prohibited from using postal code prefix or demographic proxies as direct inputs in credit decisioning algorithms unless explicitly audited and approved by the Federal Reserve board.")
]
generate_pdf("Digital_Lending_Act_v1.pdf", "Federal Digital Lending Act (v1.0)", v1_content)

# 2. Generate v2 (Drifted/Updated version simulating regulatory change)
v2_content = [
    ("Section 101: Algorithmic Transparency in Lending", 
     "All automated credit scoring models utilized by financial institutions must maintain an explainability index of at least 92% (upgraded from 85%). Risk weights assigned via machine learning models must be disclosed to borrowers within 14 business days (shortened from 30 days). Effective date: November 1, 2026."),
    ("Section 102: Data Retention & Proxy Variables", 
     "Institutions are strictly prohibited from using postal code prefix, geographic coordinates, or alternative consumer data proxies as direct inputs in credit decisioning algorithms.")
]
generate_pdf("Digital_Lending_Act_v2.pdf", "Federal Digital Lending Act (v2.0 - Current)", v2_content)

# 3. Generate Golden Test Set for Drift Auditor
test_cases = [
    {
        "test_id": "TC-001",
        "query": "What is the minimum explainability index required for automated credit scoring models?",
        "expected_citation": "Section 101",
        "expected_keywords": ["92%", "explainability index"]
    },
    {
        "test_id": "TC-002",
        "query": "Within how many days must risk weights be disclosed to borrowers under the current regulation?",
        "expected_citation": "Section 101",
        "expected_keywords": ["14 business days"]
    }
]

os.makedirs("tests", exist_ok=True)
with open("tests/golden_dataset.json", "w") as f:
    json.dump(test_cases, f, indent=2)
print("Generated golden test dataset: tests/golden_dataset.json")