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

def positive_score(exp):
    if not exp: return -1
    lower = exp.lower()
    score = 0
    for w, p in [(3,r'this is the correct'),(3,r'correct solution'),(3,r'correct answer'),
        (2,r'this is the most appropriate'),(2,r'this is the best'),(2,r'this meets all'),
        (2,r'this solution meets'),(2,r'this approach meets'),(2,r'this is ideal'),
        (2,r'the right choice'),(2,r'this ensures'),(2,r'this is the recommended'),
        (2,r'this is the optimal'),(1,r'is designed for'),(1,r'minimizes.*complexity'),
        (1,r'ensures that'),(1,r'provides the fastest'),(1,r'most cost-effective'),
        (1,r'leverages'),(1,r'optimizes'),(1,r'improving speed'),
        (1,r'maintaining.*order'),(1,r'exact sequence')]:
        if re.search(p, lower): score += w
    for w, p in [(-3,r'does not guarantee'),(-3,r'does not maintain'),(-3,r'does not support'),
        (-3,r'is not designed'),(-3,r'is not suitable'),(-3,r'is not the best'),
        (-2,r'unnecessary'),(-2,r'adds.*complexity'),(-2,r'more complex'),
        (-2,r'overkill'),(-2,r'while this'),(-2,r'although this'),(-2,r'however,'),
        (-2,r'incorrect'),(-2,r'not the correct'),(-2,r'poor'),
        (-2,r'introduces.*complexity'),(-2,r'far more complex'),(-2,r'not guarantee'),
        (-2,r'not suited'),(-2,r'extra step'),(-2,r'extra cost'),
        (-1,r"doesn't"),(-1,r'would not'),(-1,r"wouldn't"),
        (-1,r'not efficient'),(-1,r'not recommended'),(-1,r'significant.*complexity')]:
        if re.search(p, lower): score += w
    return score

def classify_line(line):
    lower = line.lower().strip()
    exp_starts = ['this is','this option','this solution','this approach','this would',
        'this does',"this doesn't",'this method','while ','although ','however,','however ',
        'sns is','sqs ','api gateway authorizers','standard queues','fifo queues are',
        'cross-region replication adds','multipart uploads allow','s3 transfer acceleration is',
        'the solution','the approach','not suitable','not designed','not the best',
        'does not',"doesn't",'is not',"isn't",'unnecessary','overkill','adds complexity',
        'more complex','far more','significant','ensures that','designed for','provides the',
        'minimizes','leverages','optimizes','correctly','appropriate','ideal',
        'blocking requests','may occasionally','using snowball','snowball edge',
        'cross-region','replication adds','lambda@edge','cloudfront functions',
        'elastic beanstalk','ecs is','eks is','fargate is','aurora is','dynamodb is',
        'redshift is','elasticache is','kinesis is','glue is','athena is',
        'macie is','guardduty is','inspector is','waf is','shield is',
        'kms is','secrets manager is','parameter store is','systems manager is',
        'cloudwatch is','cloudtrail is','config is','trusted advisor is',
        'organizations is','control tower is','service catalog is',
        'direct connect is','vpn is','transit gateway is','vpc peering is',
        'nat gateway is','internet gateway is','load balancer is',
        'auto scaling is','launch template is','placement group is']
    for s in exp_starts:
        if lower.startswith(s): return 'explanation'
    ans_starts = ['use ','create ','configure ','set up','deploy ','turn on','enable ',
        'upload ','schedule ','store ','launch ','attach ','add ','implement ','migrate ',
        'move ','place ','run ','install ','build ','modify ','update ','change ',
        'replace ','remove ','delete ','provision ','establish ','register ',
        'associate ','assign ','grant ','allow ','deny ','restrict ','encrypt ',
        'publish ','subscribe ','send ','receive ','write ','read ','put ','get ',
        'host ','serve ','route ','forward ','replicate ','backup ','restore ',
        'scale ','resize ','optimize ','monitor ','invoke ','call ','trigger ',
        'set the','purchase ','select ','choose ','apply ','define ','specify ']
    for s in ans_starts:
        if lower.startswith(s): return 'answer'
    if re.search(r'(amazon|aws|s3|ec2|lambda|rds|dynamodb|cloudfront|route\s*53|ecs|eks|sqs|sns|kinesis)', lower):
        if re.search(r'(use|create|configure|deploy|set up|enable|with|to|for|in an|on the|from)', lower):
            return 'answer'
    return 'explanation'

def parse_question_block(q_content):
    overall_match = re.search(r'Overall Explanation:\s*', q_content)
    if overall_match:
        before = q_content[:overall_match.start()].strip()
        overall = q_content[overall_match.end():].strip()
    else:
        before = q_content
        overall = ""
    
    # Find question text
    q_match = re.search(r'^(.*?\?)\s*\n', before, re.DOTALL)
    if q_match:
        question_text = q_match.group(1).strip()
        answers_block = before[q_match.end():].strip()
    else:
        lines = before.split('\n')
        question_text = lines[0]
        answers_block = '\n'.join(lines[1:])
    
    question_text = re.sub(r'\s+', ' ', question_text).strip()
    
    # Parse answers
    lines = [l.strip() for l in answers_block.split('\n') if l.strip()]
    
    # Group lines into answer+explanation pairs
    groups = []
    current_type = None
    current_lines = []
    for line in lines:
        lt = classify_line(line)
        if lt != current_type and current_lines:
            groups.append((current_type, ' '.join(current_lines)))
            current_lines = [line]
            current_type = lt
        else:
            current_lines.append(line)
            current_type = lt
    if current_lines:
        groups.append((current_type, ' '.join(current_lines)))
    
    # Pair answer+explanation groups
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
            answers.append({'text': ans_text, 'explanation': exp_text, 'correct': positive_score(exp_text) > 0})
        else:
            if answers:
                answers[-1]['explanation'] += ' ' + groups[i][1]
                answers[-1]['correct'] = positive_score(answers[-1]['explanation']) > 0
            i += 1
    
    # If we have more than 6 answers, try to merge small fragments
    if len(answers) > 6:
        merged = []
        for a in answers:
            if len(a['text']) < 40 and merged:
                # Likely a fragment, merge with previous
                merged[-1]['text'] += ' ' + a['text']
                if a['explanation']:
                    merged[-1]['explanation'] += ' ' + a['explanation']
            else:
                merged.append(a)
        answers = merged
    
    # If still too many, keep only the 4 with longest text
    if len(answers) > 6:
        answers.sort(key=lambda a: len(a['text']), reverse=True)
        answers = answers[:4]
    
    # Recalculate correct
    for a in answers:
        a['correct'] = positive_score(a['explanation']) > 0
    
    # Ensure exactly one correct answer
    correct_count = sum(1 for a in answers if a['correct'])
    if correct_count == 0 and answers:
        best_idx = max(range(len(answers)), key=lambda i: positive_score(answers[i]['explanation']))
        answers[best_idx]['correct'] = True
    elif correct_count > 1:
        best_idx = max((i for i, a in enumerate(answers) if a['correct']),
                       key=lambda i: positive_score(answers[i]['explanation']))
        for i, a in enumerate(answers):
            a['correct'] = (i == best_idx)
    
    return {
        'question': question_text,
        'answers': answers,
        'overall_explanation': overall,
        'has_correct': any(a['correct'] for a in answers)
    }

def parse_questions(text):
    questions = []
    text = clean_text(text)
    parts = re.split(r'Question\s+(\d+)\s+Not Attempted\s+[\w\s,&]+?\n', text)
    for i in range(1, len(parts)-1, 2):
        q_num = int(parts[i])
        result = parse_question_block(parts[i+1].strip())
        result['number'] = q_num
        questions.append(result)
    return questions

all_questions = []
for i in range(1, 17):
    pdf_path = f"eser-{i}.pdf"
    print(f"Processing {pdf_path}...", end=" ")
    text = extract_text_from_pdf(pdf_path)
    questions = parse_questions(text)
    valid = [q for q in questions if len(q['answers']) >= 2 and q['has_correct']]
    print(f"{len(questions)} found, {len(valid)} valid")
    for q in questions:
        q['source'] = f"eser-{i}"
        if len(q['answers']) >= 2 and q['has_correct']:
            all_questions.append(q)

print(f"\nTotal valid questions: {len(all_questions)}")
ans_counts = {}
for q in all_questions:
    n = len(q['answers'])
    ans_counts[n] = ans_counts.get(n, 0) + 1
print(f"Answer distribution: {dict(sorted(ans_counts.items()))}")

with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(all_questions, f, ensure_ascii=False, indent=2)
print("Saved to questions.json")
