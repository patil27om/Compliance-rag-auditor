import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Anchor paths to project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DOCS_DIR = ROOT_DIR / "raw_docs"

def create_compliance_pdf(filename, title, sections):
    RAW_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    filepath = RAW_DOCS_DIR / filename
    
    doc = SimpleDocTemplate(str(filepath), pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=16, spaceAfter=12)
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=12, spaceAfter=8, textColor='navy')
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, spaceAfter=10, leading=14)

    story = [Paragraph(title, title_style), Spacer(1, 12)]
    
    for sec_num, sec_title, content in sections:
        story.append(Paragraph(f"Section {sec_num}: {sec_title}", heading_style))
        story.append(Paragraph(content, body_style))
        story.append(Spacer(1, 8))

    doc.build(story)
    print(f"Generated: {filepath}")

if __name__ == "__main__":
    aml_sections = [
        ("1.1", "Transaction Monitoring Thresholds", "All financial institutions must monitor wire transfers exceeding $10,000 USD for potential structuring. Automated alert flags must be reviewed by a compliance officer within 48 business hours."),
        ("1.2", "Sanctions Screening Mandate", "Real-time screening against OFAC SDN lists is mandatory for all cross-border transactions originating from high-risk jurisdictions. False positives must be logged with deterministic resolution codes."),
        ("1.3", "Record Retention Policy", "Audit logs, alert justifications, and customer identification program (CIP) records must be retained in an immutable state for a minimum duration of 5 years from the date of account closure.")
    ]
    create_compliance_pdf("AML_Directive_2026.pdf", "Enterprise Anti-Money Laundering Directive (Rev. 2026)", aml_sections)

    privacy_sections = [
        ("2.1", "Data Subject Access Requests (DSAR)", "Consumers have the right to request full disclosure of personal data stored within operational databases. Fulfillment must be completed within 30 calendar days of verified identity receipt."),
        ("2.2", "Cross-Border Data Transfer", "Personal identifiable information (PII) transferred outside regional boundaries must utilize standard contractual clauses (SCCs) and AES-256 encryption at rest and in transit.")
    ]
    create_compliance_pdf("Data_Privacy_Standard_2026.pdf", "Global Data Privacy & Security Standard 2026", privacy_sections)