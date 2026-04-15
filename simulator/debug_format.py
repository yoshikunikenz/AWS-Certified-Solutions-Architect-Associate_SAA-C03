import pdfplumber
import re
import json

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text

def clean_text(text):
    text = re.sub(r'https://itcertifications\.io/\S+', '', text)
    text = re.sub(r'\d{2}/\d{2}/\d{2},\s+\d{2}:\d{2}\s+Aws Certified Solutions Architect.*?Real Updated Questions', '', text)
    text = re.sub(r'View Discussions\s+Ask AI', '', text)
    text = re.sub(r'\d+/\d+\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

text = extract_text_from_pdf("eser-1.pdf")
text = clean_text(text)

# Get question 1 raw content
parts = re.split(r'Question\s+(\d+)\s+Not Attempted\s+[\w\s,&]+?\n', text)
print(f"Parts count: {len(parts)}")
print(f"Part indices: 0=header, 1=q1num, 2=q1content, 3=q2num, 4=q2content...")

# Show Q1 content with repr to see exact formatting
q1_content = parts[2]
# Find Overall Explanation
oe_match = re.search(r'Overall Explanation:\s*', q1_content)
if oe_match:
    before = q1_content[:oe_match.start()]
else:
    before = q1_content

# Find question mark
qm = re.search(r'^(.*?\?)\s*', before, re.DOTALL)
if qm:
    q_text = qm.group(1)
    answers_block = before[qm.end():]
    print("=== QUESTION TEXT ===")
    print(q_text)
    print("\n=== ANSWERS BLOCK (first 2000 chars) ===")
    print(repr(answers_block[:2000]))
