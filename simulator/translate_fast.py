import json
import time
import os
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source='en', target='it')
SEP = ' ||| '

def batch_translate(texts, max_chars=4500):
    """Translate multiple texts in one API call using a separator"""
    if not texts:
        return texts
    results = []
    batch = []
    batch_len = 0
    
    for t in texts:
        t_clean = (t or '').strip()
        if not t_clean:
            results.append('')
            continue
        
        if batch_len + len(t_clean) + len(SEP) > max_chars and batch:
            # Translate current batch
            combined = SEP.join(batch)
            try:
                translated = translator.translate(combined)
                parts = translated.split('|||')
                for p in parts:
                    results.append(p.strip())
            except Exception as e:
                print(f"  Batch error: {str(e)[:60]}")
                results.extend(batch)  # fallback to originals
            batch = [t_clean]
            batch_len = len(t_clean)
            time.sleep(0.2)
        else:
            batch.append(t_clean)
            batch_len += len(t_clean) + len(SEP)
    
    # Translate remaining batch
    if batch:
        combined = SEP.join(batch)
        try:
            translated = translator.translate(combined)
            parts = translated.split('|||')
            for p in parts:
                results.append(p.strip())
        except Exception as e:
            print(f"  Final batch error: {str(e)[:60]}")
            results.extend(batch)
    
    return results

# Load questions
with open('questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

output_file = 'questions_it.json'

# Check for existing progress
if os.path.exists(output_file):
    with open(output_file, 'r', encoding='utf-8') as f:
        existing = json.load(f)
    done_count = len(existing)
    print(f"Found {done_count} already translated, resuming...")
else:
    existing = []
    done_count = 0

# Process in chunks of 5 questions at a time
CHUNK = 5
for chunk_start in range(done_count, len(questions), CHUNK):
    chunk_end = min(chunk_start + CHUNK, len(questions))
    chunk_qs = questions[chunk_start:chunk_end]
    
    print(f"[{chunk_start+1}-{chunk_end}/{len(questions)}] Translating...", end=' ', flush=True)
    
    # Collect all texts to translate for this chunk
    all_texts = []
    text_map = []  # (question_idx_in_chunk, field, answer_idx)
    
    for qi, q in enumerate(chunk_qs):
        all_texts.append(q['question'])
        text_map.append((qi, 'question', -1))
        
        for ai, a in enumerate(q['answers']):
            all_texts.append(a['text'])
            text_map.append((qi, 'answer_text', ai))
            all_texts.append(a.get('explanation', ''))
            text_map.append((qi, 'answer_exp', ai))
        
        all_texts.append(q.get('overall_explanation', ''))
        text_map.append((qi, 'overall', -1))
    
    # Translate all texts
    translated_texts = batch_translate(all_texts)
    
    # Pad if needed (separator splitting can sometimes merge/split)
    while len(translated_texts) < len(text_map):
        translated_texts.append('')
    
    # Reconstruct translated questions
    for qi, q in enumerate(chunk_qs):
        tq = dict(q)
        tq['answers_it'] = [None] * len(q['answers'])
        
        for ti, (tqi, field, ai) in enumerate(text_map):
            if tqi != qi:
                continue
            if ti < len(translated_texts):
                val = translated_texts[ti]
            else:
                val = ''
            
            if field == 'question':
                tq['question_it'] = val
            elif field == 'answer_text':
                if tq['answers_it'][ai] is None:
                    tq['answers_it'][ai] = {'text': val, 'explanation': '', 'correct': q['answers'][ai]['correct']}
                else:
                    tq['answers_it'][ai]['text'] = val
            elif field == 'answer_exp':
                if tq['answers_it'][ai] is None:
                    tq['answers_it'][ai] = {'text': '', 'explanation': val, 'correct': q['answers'][ai]['correct']}
                else:
                    tq['answers_it'][ai]['explanation'] = val
            elif field == 'overall':
                tq['overall_explanation_it'] = val
        
        # Fill any None answers
        for ai in range(len(tq['answers_it'])):
            if tq['answers_it'][ai] is None:
                tq['answers_it'][ai] = {
                    'text': q['answers'][ai]['text'],
                    'explanation': q['answers'][ai].get('explanation', ''),
                    'correct': q['answers'][ai]['correct']
                }
        
        existing.append(tq)
    
    print(f"OK ({len(existing)} total)")
    
    # Save progress
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
    
    time.sleep(0.3)

print(f"\nDone! {len(existing)} questions saved to {output_file}")
