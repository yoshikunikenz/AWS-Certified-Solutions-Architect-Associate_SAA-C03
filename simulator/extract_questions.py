import pdfplumber
import json
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text

def parse_questions(text):
    questions = []
    # Split by "Question X" pattern
    parts = re.split(r'Question\s+(\d+)\s+Not Attempted\s+\w+', text)
    
    # parts[0] is header, then alternating: question_number, question_content
    for i in range(1, len(parts)-1, 2):
        q_num = int(parts[i])
        q_content = parts[i+1].strip()
        
        # Remove page headers/footers
        q_content = re.sub(r'https://itcertifications\.io/\S+', '', q_content)
        q_content = re.sub(r'\d{2}/\d{2}/\d{2},\s+\d{2}:\d{2}\s+Aws Certified Solutions Architect.*?Real Updated Questions', '', q_content)
        q_content = re.sub(r'View Discussions\s+Ask AI', '', q_content)
        q_content = q_content.strip()
        
        # Try to find the question text (before the first answer option)
        # The question text ends where the first answer option begins
        # Answer options don't have a clear marker, so we use "Overall Explanation:" to find the end
        
        overall_match = re.search(r'Overall Explanation:', q_content)
        if overall_match:
            before_explanation = q_content[:overall_match.start()].strip()
            explanation = q_content[overall_match.end():].strip()
        else:
            before_explanation = q_content
            explanation = ""
        
        # Parse question and answers from before_explanation
        # The question text is the first paragraph, answers follow
        # Each answer has its text followed by an explanation paragraph
        # We need to identify the question text and the answer blocks
        
        questions.append({
            'number': q_num,
            'raw': before_explanation,
            'explanation': explanation
        })
    
    return questions

# Test with first PDF
text = extract_text_from_pdf("eser-1.pdf")
questions = parse_questions(text)
print(f"Found {len(questions)} questions")
if questions:
    print("\n--- Question 1 raw ---")
    print(questions[0]['raw'][:1500])
    print("\n--- Question 2 raw ---")
    if len(questions) > 1:
        print(questions[1]['raw'][:1500])
