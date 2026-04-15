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

def clean_text(text):
    text = re.sub(r'https://itcertifications\.io/\S+', '', text)
    text = re.sub(r'\d{2}/\d{2}/\d{2},\s+\d{2}:\d{2}\s+Aws Certified Solutions Architect.*?Real Updated Questions', '', text)
    text = re.sub(r'View Discussions\s+Ask AI', '', text)
    text = re.sub(r'\d+/\d+\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def is_correct_answer(explanation):
    exp_lower = explanation.lower()
    
    # Strong positive indicators
    strong_positive = [
        r'this is the correct',
        r'correct solution',
        r'correct answer',
        r'this is the most appropriate',
        r'this is the best',
        r'this is the right',
        r'this meets all',
        r'this solution meets',
        r'this approach meets',
        r'this is ideal',
        r'the right choice',
        r'this ensures',
        r'this is the recommended',
        r'this option is correct',
        r'this is the optimal',
    ]
    
    # Strong negative indicators  
    strong_negative = [
        r'does not guarantee',
        r'does not maintain',
        r'does not support',
        r'does not provide',
        r'is not designed',
        r'is not suitable',
        r'is not the best',
        r'is unnecessary',
        r'adds.*complexity',
        r'more complex',
        r'would not',
        r'wouldn\'t',
        r'overkill',
        r'while this',
        r'although this',
        r'however,',
        r'incorrect',
        r'not the correct',
        r'poor user experience',
        r'introduces.*complexity',
        r'far more complex',
        r'not guarantee',
        r'not suited',
        r'not appropriate',
        r'doesn\'t guarantee',
        r'doesn\'t support',
        r'doesn\'t provide',
        r'not efficient',
        r'not cost-effective',
        r'not recommended',
        r'significant.*complexity',
        r'extra step',
        r'extra cost',
    ]
    
    # Moderate positive
    moderate_positive = [
        r'is designed for',
        r'minimizes operational complexity',
        r'ensures that',
        r'provides the fastest',
        r'most cost-effective',
        r'best approach',
        r'correctly',
        r'leverages',
        r'optimizes',
        r'efficient',
        r'appropriate',
        r'suitable',
        r'ideal for',
    ]
    
    sp = sum(2 for p in strong_positive if re.search(p, exp_lower))
    sn = sum(2 for p in strong_negative if re.search(p, exp_lower))
    mp = sum(1 for p in moderate_positive if re.search(p, exp_lower))
    
    return (sp + mp) > sn

def parse_answers_block(block):
    """
    Parse the answers block. Each answer consists of:
    - Answer text (the option itself, usually 1-3 lines)
    - Explanation text (why it's right or wrong, usually 1-3 lines)
    
    The key insight: answer text describes an action/solution,
    explanation text analyzes why it's good or bad.
    """
    lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
    if not lines:
        return []
    
    # Group lines into answer+explanation pairs
    # Strategy: accumulate lines, detect when a new answer starts
    # An explanation line typically starts with analysis words
    # A new answer typically starts with a verb or service name
    
    # Better strategy: split into chunks where each chunk is answer+explanation
    # We know there are typically 4 answers per question
    # Let's try to identify answer boundaries by looking for patterns
    
    # Join all lines back
    full_text = '\n'.join(lines)
    
    # Try to split by detecting answer option patterns
    # Answers typically start with action verbs or AWS service names
    # after an explanation paragraph
    
    # Alternative approach: use the fact that explanations contain evaluative language
    # and answers contain imperative/descriptive language
    
    answers = []
    current_answer = []
    current_explanation = []
    in_explanation = False
    
    for line in lines:
        line_lower = line.lower()
        
        # Heuristic: explanation lines contain evaluative words
        is_evaluative = any(w in line_lower for w in [
            'this is', 'this option', 'this solution', 'this approach',
            'while this', 'although', 'however', 'does not', "doesn't",
            'is not', "isn't", 'unnecessary', 'overkill', 'adds',
            'introduces', 'would not', "wouldn't", 'ensures',
            'designed for', 'suited for', 'appropriate', 'correct',
            'incorrect', 'provides', 'leverages', 'minimizes',
            'significant', 'complexity', 'extra', 'poor',
            'not guarantee', 'not maintain', 'not support',
            'far more', 'best', 'ideal', 'recommended',
            'sns is', 'sqs fifo', 'api gateway authorizers',
            'standard queues', 'fifo queues',
        ])
        
        if is_evaluative and current_answer:
            in_explanation = True
            current_explanation.append(line)
        elif in_explanation and not is_evaluative:
            # New answer starts
            # Save previous answer
            ans_text = ' '.join(current_answer)
            exp_text = ' '.join(current_explanation)
            answers.append({
                'text': ans_text,
                'explanation': exp_text,
                'correct': is_correct_answer(exp_text)
            })
            current_answer = [line]
            current_explanation = []
            in_explanation = False
        elif in_explanation:
            current_explanation.append(line)
        else:
            current_answer.append(line)
    
    # Save last answer
    if current_answer:
        ans_text = ' '.join(current_answer)
        exp_text = ' '.join(current_explanation)
        answers.append({
            'text': ans_text,
            'explanation': exp_text,
            'correct': is_correct_answer(exp_text)
        })
    
    return answers

def parse_questions(text):
    questions = []
    text = clean_text(text)
    
    parts = re.split(r'Question\s+(\d+)\s+Not Attempted\s+[\w\s,&]+?\n', text)
    
    for i in range(1, len(parts)-1, 2):
        q_num = int(parts[i])
        q_content = parts[i+1].strip()
        
        overall_match = re.search(r'Overall Explanation:\s*', q_content)
        if overall_match:
            before_explanation = q_content[:overall_match.start()].strip()
            overall_explanation = q_content[overall_match.end():].strip()
        else:
            before_explanation = q_content
            overall_explanation = ""
        
        # Find question text (ends with ?)
        # Some questions have multiple ? - find the last ? before answers start
        # Usually the question is the first paragraph
        q_match = re.search(r'^(.*?\?)\s*\n', before_explanation, re.DOTALL)
        if q_match:
            question_text = q_match.group(1).strip()
            answers_block = before_explanation[q_match.end():].strip()
        else:
            lines = before_explanation.split('\n')
            question_text = lines[0]
            answers_block = '\n'.join(lines[1:])
        
        # Clean question text - rejoin wrapped lines
        question_text = re.sub(r'\s+', ' ', question_text).strip()
        
        answers = parse_answers_block(answers_block)
        
        has_correct = any(a['correct'] for a in answers)
        
        questions.append({
            'number': q_num,
            'question': question_text,
            'answers': answers,
            'overall_explanation': overall_explanation,
            'has_correct': has_correct
        })
    
    return questions

# Process all PDFs
all_questions = []
for i in range(1, 17):
    pdf_path = f"eser-{i}.pdf"
    print(f"Processing {pdf_path}...")
    try:
        text = extract_text_from_pdf(pdf_path)
        questions = parse_questions(text)
        print(f"  Found {len(questions)} questions")
        
        # Stats for this PDF
        with_correct = sum(1 for q in questions if q['has_correct'])
        avg_ans = sum(len(q['answers']) for q in questions) / len(questions) if questions else 0
        print(f"  With correct answer: {with_correct}, Avg answers: {avg_ans:.1f}")
        
        for q in questions:
            q['source'] = f"eser-{i}"
            all_questions.append(q)
    except Exception as e:
        print(f"  Error: {e}")
        import traceback
        traceback.print_exc()

print(f"\nTotal questions extracted: {len(all_questions)}")
correct_count = sum(1 for q in all_questions if q['has_correct'])
print(f"Questions with identified correct answer: {correct_count}")
avg_answers = sum(len(q['answers']) for q in all_questions) / len(all_questions) if all_questions else 0
print(f"Average answers per question: {avg_answers:.1f}")

# Show samples
for q in all_questions[:2]:
    print(f"\n--- {q['source']} Q{q['number']} ---")
    print(f"Q: {q['question'][:200]}")
    print(f"Answers: {len(q['answers'])}")
    for j, a in enumerate(q['answers']):
        marker = '✓' if a['correct'] else '✗'
        print(f"  {marker} [{a['text'][:120]}]")
        print(f"    Exp: [{a['explanation'][:120]}]")

with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(all_questions, f, ensure_ascii=False, indent=2)
print(f"\nSaved to questions.json")
