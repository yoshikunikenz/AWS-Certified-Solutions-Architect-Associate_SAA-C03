import json
import time
import os
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source='en', target='it')

# Load questions
with open('questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# Load progress if exists
output_file = 'questions_it.json'
if os.path.exists(output_file):
    with open(output_file, 'r', encoding='utf-8') as f:
        translated = json.load(f)
    start_idx = len(translated)
    print(f"Resuming from question {start_idx}")
else:
    translated = []
    start_idx = 0

def safe_translate(text, retries=3):
    if not text or not text.strip():
        return text
    for attempt in range(retries):
        try:
            # Google Translate has a ~5000 char limit per request
            if len(text) > 4500:
                # Split into chunks
                parts = []
                sentences = text.split('. ')
                chunk = ''
                for s in sentences:
                    if len(chunk) + len(s) > 4000:
                        parts.append(chunk)
                        chunk = s
                    else:
                        chunk = chunk + '. ' + s if chunk else s
                if chunk:
                    parts.append(chunk)
                result = '. '.join(translator.translate(p) for p in parts)
                return result
            else:
                return translator.translate(text)
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                print(f"  Translation failed: {str(e)[:80]}")
                return text  # Return original on failure

batch_size = 10  # Save every N questions

for i in range(start_idx, len(questions)):
    q = questions[i]
    print(f"[{i+1}/{len(questions)}] Translating {q.get('source','')} Q{q.get('number','')}...", end=' ', flush=True)
    
    tq = dict(q)  # Copy all fields
    
    # Translate question text
    tq['question_it'] = safe_translate(q['question'])
    
    # Translate answers
    tq['answers_it'] = []
    for a in q['answers']:
        ta = {
            'text': safe_translate(a['text']),
            'explanation': safe_translate(a.get('explanation', '')),
            'correct': a['correct']
        }
        tq['answers_it'].append(ta)
    
    # Translate overall explanation
    tq['overall_explanation_it'] = safe_translate(q.get('overall_explanation', ''))
    
    translated.append(tq)
    print("OK")
    
    # Save progress periodically
    if (i + 1) % batch_size == 0:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(translated, f, ensure_ascii=False, indent=2)
        print(f"  [Saved progress: {len(translated)} questions]")
    
    # Small delay to avoid rate limiting
    time.sleep(0.3)

# Final save
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(translated, f, ensure_ascii=False, indent=2)

print(f"\nDone! Translated {len(translated)} questions to {output_file}")
