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

def find_correct_from_overall(overall_exp, answers):
    """Use the overall explanation to identify which answer is correct"""
    if not overall_exp:
        return
    
    exp_lower = overall_exp.lower()
    
    # Look for "Option A/B/C/D" or letter references
    option_match = re.search(r'option[s]?\s+([A-D])', exp_lower)
    if option_match:
        letter = option_match.group(1).upper()
        idx = ord(letter) - ord('A')
        if idx < len(answers):
            for a in answers:
                a['correct'] = False
            answers[idx]['correct'] = True
            return
    
    # Look for "Options B, C, and D are more complex" pattern (meaning A is correct)
    wrong_options = re.findall(r'option[s]?\s+([B-D](?:,\s*[B-D])*(?:\s*,?\s*and\s+[B-D])?)', exp_lower)
    if wrong_options:
        # If B, C, D are wrong, A is correct
        for a in answers:
            a['correct'] = False
        if len(answers) > 0:
            answers[0]['correct'] = True
        return

def parse_question_block(q_content):
    """Parse a single question block into question + answers"""
    # Separate overall explanation
    overall_match = re.search(r'Overall Explanation:\s*', q_content)
    if overall_match:
        before = q_content[:overall_match.start()].strip()
        overall = q_content[overall_match.end():].strip()
    else:
        before = q_content
        overall = ""
    
    # Find question text (ends with ?)
    # Handle multi-line questions - find the FIRST ? that makes sense as end of question
    q_match = re.search(r'^(.*?\?)\s*\n', before, re.DOTALL)
    if q_match:
        question_text = q_match.group(1).strip()
        answers_block = before[q_match.end():].strip()
    else:
        lines = before.split('\n')
        question_text = lines[0]
        answers_block = '\n'.join(lines[1:])
    
    question_text = re.sub(r'\s+', ' ', question_text).strip()
    
    # Parse answers using a smarter approach
    # Join all lines, then try to identify 4 answer blocks
    lines = [l.strip() for l in answers_block.split('\n') if l.strip()]
    full = ' '.join(lines)
    
    # Strategy: each answer option describes an AWS solution/action
    # Each explanation analyzes why it's right/wrong
    # We'll group consecutive lines and use heuristics
    
    # Build line groups - each line is either "answer-like" or "explanation-like"
    groups = []
    current_type = None
    current_lines = []
    
    for line in lines:
        line_type = classify_line(line)
        if line_type != current_type and current_lines:
            groups.append((current_type, ' '.join(current_lines)))
            current_lines = [line]
            current_type = line_type
        else:
            current_lines.append(line)
            current_type = line_type
    
    if current_lines:
        groups.append((current_type, ' '.join(current_lines)))
    
    # Now pair answer groups with explanation groups
    answers = []
    i = 0
    while i < len(groups):
        if groups[i][0] == 'answer':
            ans_text = groups[i][1]
            exp_text = ''
            if i + 1 < len(groups) and groups[i+1][0] == 'explanation':
                exp_text = groups[i+1][1]
                i += 2
            else:
                i += 1
            
            is_correct = is_positive_explanation(exp_text)
            answers.append({
                'text': ans_text,
                'explanation': exp_text,
                'correct': is_correct
            })
        else:
            # Orphan explanation - might belong to previous answer
            if answers:
                answers[-1]['explanation'] += ' ' + groups[i][1]
                answers[-1]['correct'] = is_positive_explanation(answers[-1]['explanation'])
            i += 1
    
    # Use overall explanation to validate/fix correct answer
    correct_count = sum(1 for a in answers if a['correct'])
    if correct_count != 1 and overall:
        find_correct_from_overall(overall, answers)
    
    # If still no correct answer, try to find the most positive one
    if not any(a['correct'] for a in answers) and answers:
        best_idx = 0
        best_score = -999
        for idx, a in enumerate(answers):
            score = positive_score(a['explanation'])
            if score > best_score:
                best_score = score
                best_idx = idx
        answers[best_idx]['correct'] = True
    
    # If multiple correct, keep only the most positive
    correct_indices = [i for i, a in enumerate(answers) if a['correct']]
    if len(correct_indices) > 1:
        best_idx = correct_indices[0]
        best_score = -999
        for idx in correct_indices:
            score = positive_score(answers[idx]['explanation'])
            if score > best_score:
                best_score = score
                best_idx = idx
        for i, a in enumerate(answers):
            a['correct'] = (i == best_idx)
    
    return {
        'question': question_text,
        'answers': answers,
        'overall_explanation': overall,
        'has_correct': any(a['correct'] for a in answers)
    }

def classify_line(line):
    """Classify a line as 'answer' (describes a solution) or 'explanation' (analyzes it)"""
    lower = line.lower()
    
    explanation_starters = [
        'this is', 'this option', 'this solution', 'this approach',
        'this would', 'this does', "this doesn't", 'this method',
        'while ', 'although ', 'however,', 'however ',
        'sns is', 'sqs ', 'api gateway authorizers',
        'using ', 'snowball', 'standard queues',
        'fifo queues are', 'cross-region replication adds',
        'multipart uploads allow', 's3 transfer acceleration is',
        'the solution', 'the approach',
        'not suitable', 'not designed', 'not the best',
        'does not', "doesn't", 'is not', "isn't",
        'unnecessary', 'overkill', 'adds complexity',
        'more complex', 'far more', 'significant',
        'ensures that', 'designed for', 'provides the',
        'minimizes', 'leverages', 'optimizes',
        'correctly', 'appropriate', 'ideal',
        'blocking requests', 'may occasionally',
    ]
    
    for starter in explanation_starters:
        if lower.startswith(starter) or (starter in lower and len(line) < 200):
            return 'explanation'
    
    # Lines starting with action verbs are likely answers
    answer_starters = [
        'use ', 'create ', 'configure ', 'set up', 'deploy ',
        'turn on', 'enable ', 'upload ', 'schedule ', 'store ',
        'launch ', 'attach ', 'add ', 'implement ', 'migrate ',
        'move ', 'place ', 'run ', 'install ', 'build ',
        'modify ', 'update ', 'change ', 'replace ', 'remove ',
        'delete ', 'provision ', 'establish ', 'register ',
        'associate ', 'assign ', 'grant ', 'allow ', 'deny ',
        'restrict ', 'encrypt ', 'decrypt ', 'sign ',
        'publish ', 'subscribe ', 'send ', 'receive ',
        'write ', 'read ', 'put ', 'get ', 'list ',
        'describe ', 'invoke ', 'call ', 'trigger ',
        'host ', 'serve ', 'route ', 'forward ',
        'replicate ', 'backup ', 'restore ', 'snapshot ',
        'scale ', 'resize ', 'optimize ', 'monitor ',
    ]
    
    for starter in answer_starters:
        if lower.startswith(starter):
            return 'answer'
    
    # Default: if it contains AWS service names and action words, likely answer
    if re.search(r'(amazon|aws|s3|ec2|lambda|rds|dynamodb|cloudfront|route\s*53|ecs|eks|sqs|sns|kinesis|redshift|elasticache|aurora)', lower):
        if re.search(r'(use|create|configure|deploy|set up|enable|with|to|for)', lower):
            return 'answer'
    
    return 'explanation'

def is_positive_explanation(exp):
    """Check if explanation indicates correct answer"""
    return positive_score(exp) > 0

def positive_score(exp):
    if not exp:
        return -1
    lower = exp.lower()
    
    score = 0
    positives = [
        (3, r'this is the correct'),
        (3, r'correct solution'),
        (3, r'correct answer'),
        (2, r'this is the most appropriate'),
        (2, r'this is the best'),
        (2, r'this meets all'),
        (2, r'this solution meets'),
        (2, r'this approach meets'),
        (2, r'this is ideal'),
        (2, r'the right choice'),
        (2, r'this ensures'),
        (2, r'this is the recommended'),
        (2, r'this is the optimal'),
        (1, r'is designed for'),
        (1, r'minimizes.*complexity'),
        (1, r'ensures that'),
        (1, r'provides the fastest'),
        (1, r'most cost-effective'),
        (1, r'leverages'),
        (1, r'optimizes'),
        (1, r'appropriate'),
        (1, r'improving speed'),
        (1, r'maintaining.*order'),
        (1, r'exact sequence'),
    ]
    
    negatives = [
        (-3, r'does not guarantee'),
        (-3, r'does not maintain'),
        (-3, r'does not support'),
        (-3, r'is not designed'),
        (-3, r'is not suitable'),
        (-3, r'is not the best'),
        (-2, r'unnecessary'),
        (-2, r'adds.*complexity'),
        (-2, r'more complex'),
        (-2, r'overkill'),
        (-2, r'while this'),
        (-2, r'although this'),
        (-2, r'however,'),
        (-2, r'incorrect'),
        (-2, r'not the correct'),
        (-2, r'poor'),
        (-2, r'introduces.*complexity'),
        (-2, r'far more complex'),
        (-2, r'not guarantee'),
        (-2, r'not suited'),
        (-2, r'extra step'),
        (-2, r'extra cost'),
        (-1, r"doesn't"),
        (-1, r'would not'),
        (-1, r"wouldn't"),
        (-1, r'not efficient'),
        (-1, r'not recommended'),
        (-1, r'significant.*complexity'),
    ]
    
    for weight, pattern in positives:
        if re.search(pattern, lower):
            score += weight
    
    for weight, pattern in negatives:
        if re.search(pattern, lower):
            score += weight
    
    return score

def parse_questions(text):
    questions = []
    text = clean_text(text)
    
    parts = re.split(r'Question\s+(\d+)\s+Not Attempted\s+[\w\s,&]+?\n', text)
    
    for i in range(1, len(parts)-1, 2):
        q_num = int(parts[i])
        q_content = parts[i+1].strip()
        
        result = parse_question_block(q_content)
        result['number'] = q_num
        questions.append(result)
    
    return questions

# Process all PDFs
all_questions = []
for i in range(1, 17):
    pdf_path = f"eser-{i}.pdf"
    print(f"Processing {pdf_path}...")
    try:
        text = extract_text_from_pdf(pdf_path)
        questions = parse_questions(text)
        
        with_correct = sum(1 for q in questions if q['has_correct'])
        avg_ans = sum(len(q['answers']) for q in questions) / len(questions) if questions else 0
        print(f"  {len(questions)} questions, {with_correct} with correct, avg {avg_ans:.1f} answers")
        
        for q in questions:
            q['source'] = f"eser-{i}"
            all_questions.append(q)
    except Exception as e:
        print(f"  Error: {e}")
        import traceback
        traceback.print_exc()

print(f"\nTotal: {len(all_questions)} questions")
correct_count = sum(1 for q in all_questions if q['has_correct'])
print(f"With correct answer: {correct_count}/{len(all_questions)}")

# Show first 3 samples
for q in all_questions[:3]:
    print(f"\n--- {q['source']} Q{q['number']} ---")
    print(f"Q: {q['question'][:200]}")
    for j, a in enumerate(q['answers']):
        marker = '✓' if a['correct'] else '✗'
        print(f"  {marker} {a['text'][:150]}")

with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(all_questions, f, ensure_ascii=False, indent=2)
print(f"\nSaved to questions.json")
