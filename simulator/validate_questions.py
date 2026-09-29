#!/usr/bin/env python3
"""Gate di qualita' per simulator/questions.json (e opzionalmente questions_it.json).

Nato perche' la corruzione precedente non e' mai stata rilevata: un singolo controllo
sulla distribuzione dell'indice della risposta corretta (gate 8) avrebbe rivelato
immediatamente il 68% di risposte finite sull'opzione A. Le soglie sono impostate
appena sopra i valori misurati sull'estrazione corretta, cosi' il gate resta
significativo senza essere fragile.

Uso:
    python3 validate_questions.py simulator/questions.json
    python3 validate_questions.py simulator/questions.json --it simulator/questions_it.json

Exit code 0 se tutti i gate passano, 1 altrimenti. Ogni violazione e' stampata con
il suo `source#number` per poterla controllare a mano contro il PDF.
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict

EXPECTED_COUNTS = {
    1: 65, 2: 65, 3: 65, 4: 65, 5: 64, 6: 65, 7: 65, 8: 65,
    9: 65, 10: 65, 11: 65, 12: 65, 13: 65, 14: 64, 15: 65, 16: 44,
}

NOISE_STRINGS = [
    "List of Updated IT Exams", "itcertifications.io", "View Discussions", "Ask AI",
    "Back to Exam", "Refund policy", "Shipping policy", "Whizlabs", "TutorialsDojo",
    "All rights reserved", "Final Score", "Answer Distribution", "Domain Performance",
    "19/03/26",
]
# Numero di pagina residuo del PDF, es. "29/73": denominatore a due cifre e >= 10,
# per non confondersi con contenuto legittimo come "Layer 3/4" (protocollo OSI).
NOISE_PAGE_NUM = re.compile(r"^\d{1,3}/\d{2,3}$")

DANGLING_WORDS = {
    "the", "a", "an", "to", "of", "in", "on", "for", "with", "and", "or",
    "from", "by", "at", "as", "that",
}

# Chiavi del CAT_MAP di simulator.html (le varianti sono normalizzate alla stessa categoria)
KNOWN_CATEGORIES = {
    "Storage", "Serverless", "Security", "Security, Identity, and Compliance",
    "Compute", "Databases", "Database", "Networking", "Automation",
    "Monitoring and Observability", "Monitoring and Logging",
    "Monitoring & Management", "Monitoring", "Cost Optimization",
    "Disaster Recovery", "Management & Governance", "Management and Governance",
    "Application Integration",
}


class Failure:
    def __init__(self, gate, msg, ref=None):
        self.gate = gate
        self.msg = msg
        self.ref = ref

    def __str__(self):
        loc = f" [{self.ref}]" if self.ref else ""
        return f"  GATE {self.gate}: {self.msg}{loc}"


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate(data, label="EN"):
    failures = []

    def fail(gate, msg, ref=None):
        failures.append(Failure(gate, msg, ref))

    # Gate 1: totale
    total = len(data)
    expected_total = sum(EXPECTED_COUNTS.values())
    if total != expected_total:
        fail(1, f"totale domande = {total}, atteso {expected_total}")

    by_source = defaultdict(list)
    for r in data:
        by_source[r.get("source")].append(r)

    # Gate 2/3: conteggi per set, numerazione senza buchi/duplicati
    for src, expected_n in sorted(EXPECTED_COUNTS.items(), key=lambda x: x[0]):
        key = f"eser-{src}"
        recs = by_source.get(key, [])
        if len(recs) != expected_n:
            fail(2, f"{key}: {len(recs)} domande, attese {expected_n}")
        nums = sorted(r["number"] for r in recs)
        expected_nums = list(range(1, expected_n + 1))
        if nums != expected_nums and recs:
            missing = sorted(set(expected_nums) - set(nums))
            dup = [n for n, c in Counter(nums).items() if c > 1]
            if missing:
                fail(3, f"{key}: numeri mancanti {missing}")
            if dup:
                fail(3, f"{key}: numeri duplicati {dup}")

    # Gate 4: id unico
    ids = [r.get("id") for r in data]
    id_counts = Counter(ids)
    dupes = [i for i, c in id_counts.items() if c > 1]
    if dupes:
        fail(4, f"id duplicati: {dupes[:10]}")
    bad_id_fmt = [i for i in ids if i and not re.match(r"^eser-\d+#\d+$", i)]
    if bad_id_fmt:
        fail(4, f"id con formato inatteso: {bad_id_fmt[:5]}")

    n_qs = len(data)
    correct_index_counter = Counter()
    n_single = 0
    lowercase_options = []
    no_punct_options = []
    dangling_options = []
    stem_prefix_options = []

    for r in data:
        ref = r.get("id", f"{r.get('source')}#{r.get('number')}")
        answers = r.get("answers", [])

        # Gate 5: 4-6 opzioni
        if not (4 <= len(answers) <= 6):
            fail(5, f"{len(answers)} opzioni (attese 4-6)", ref)

        # Gate 6/7: correttezza
        n_correct = sum(1 for a in answers if a.get("correct"))
        if not (1 <= n_correct <= 3):
            fail(6, f"{n_correct} opzioni corrette (attese 1-3)", ref)
        if r.get("correct_count") is not None and r["correct_count"] != n_correct:
            fail(6, f"correct_count={r['correct_count']} ma trovate {n_correct} corrette", ref)
        has_correct = r.get("has_correct")
        if has_correct != (n_correct > 0):
            fail(7, f"has_correct={has_correct} ma n_correct={n_correct}", ref)

        if n_correct == 1:
            n_single += 1
            for i, a in enumerate(answers):
                if a.get("correct"):
                    correct_index_counter[i] += 1

        # Gate 9: campi vuoti
        if not r.get("question", "").strip():
            fail(9, "question vuoto", ref)
        if not r.get("overall_explanation", "").strip():
            fail(9, "overall_explanation vuoto", ref)
        for i, a in enumerate(answers):
            if not a.get("text", "").strip():
                fail(9, f"answers[{i}].text vuoto", ref)
            if not a.get("explanation", "").strip():
                fail(9, f"answers[{i}].explanation vuoto", ref)

        # Gate 10: terminazione stem
        stem = r.get("question", "").strip()
        if stem and stem[-1] not in "?).":
            fail(10, f"stem non termina con ?)." + f" -> ...{stem[-20:]!r}", ref)

        # Gate 11/12/13: qualita' testo opzioni
        for i, a in enumerate(answers):
            text = a.get("text", "").strip()
            if not text:
                continue
            if text[0].islower():
                lowercase_options.append((ref, i, text[:50]))
            if len(text) >= 60 and text[-1] not in ".)?\"'":
                no_punct_options.append((ref, i, text[-40:]))
            last_word = re.sub(r"[^\w]", "", text.split()[-1]).lower() if text.split() else ""
            if last_word in DANGLING_WORDS:
                dangling_options.append((ref, i, text[-40:]))

            # Gate 15: opzione == prefisso dello stem (bug di sfasamento campi)
            if stem and (text == stem or (len(text) > 15 and stem.startswith(text))):
                stem_prefix_options.append((ref, i))

        # Gate 14: rumore PDF
        blob_parts = [r.get("question", ""), r.get("overall_explanation", "")]
        for a in answers:
            blob_parts.append(a.get("text", ""))
            blob_parts.append(a.get("explanation", ""))
        blob = " ".join(blob_parts)
        for noise in NOISE_STRINGS:
            if noise in blob:
                fail(14, f"rumore PDF trovato: {noise!r}", ref)
        for part in blob_parts:
            for tok in part.split():
                if NOISE_PAGE_NUM.match(tok):
                    fail(14, f"token numero di pagina trovato: {tok!r}", ref)
                    break

        # Gate 16: categoria nota
        cat = r.get("category", "")
        if cat and cat not in KNOWN_CATEGORIES:
            fail(16, f"categoria non riconosciuta: {cat!r}", ref)

    # Gate 8: skew indice risposta corretta (solo single-select)
    if n_single > 0:
        for idx, count in correct_index_counter.items():
            pct = count / n_single * 100
            if pct > 40:
                fail(8, f"indice {idx} detiene il {pct:.1f}% delle risposte single-select "
                        f"({count}/{n_single}), soglia 40%")

    if len(lowercase_options) > 10:
        fail(11, f"{len(lowercase_options)} opzioni iniziano in minuscolo (soglia 10): "
                 f"{[o[0] for o in lowercase_options[:5]]}")
    if len(no_punct_options) > 70:
        fail(12, f"{len(no_punct_options)} opzioni senza punteggiatura finale e >=60 char "
                 f"(soglia 70): {[o[0] for o in no_punct_options[:5]]}")
    if len(dangling_options) > 10:
        fail(13, f"{len(dangling_options)} opzioni finiscono con parola funzionale sospesa "
                 f"(soglia 10): {[o[0] for o in dangling_options[:5]]}")
    if stem_prefix_options:
        fail(15, f"{len(stem_prefix_options)} opzioni coincidono/prefissano lo stem "
                 f"(bug di sfasamento campi): {[o[0] for o in stem_prefix_options[:5]]}")

    return failures, correct_index_counter, n_single


def validate_it_pair(data_en, data_it):
    failures = []

    def fail(gate, msg, ref=None):
        failures.append(Failure(gate, msg, ref))

    if len(data_en) != len(data_it):
        fail(17, f"lunghezze diverse: EN={len(data_en)} IT={len(data_it)}")

    en_by_id = {r["id"]: r for r in data_en if r.get("id")}
    it_by_id = {r["id"]: r for r in data_it if r.get("id")}

    missing_in_it = set(en_by_id) - set(it_by_id)
    missing_in_en = set(it_by_id) - set(en_by_id)
    if missing_in_it:
        fail(17, f"{len(missing_in_it)} id presenti in EN ma non in IT: "
                 f"{sorted(missing_in_it)[:5]}")
    if missing_in_en:
        fail(17, f"{len(missing_in_en)} id presenti in IT ma non in EN: "
                 f"{sorted(missing_in_en)[:5]}")

    identical_question = []
    mismatched_correct = []
    for qid in sorted(set(en_by_id) & set(it_by_id)):
        en, it = en_by_id[qid], it_by_id[qid]
        en_correct = [a.get("correct") for a in en.get("answers", [])]
        it_correct = [a.get("correct") for a in it.get("answers", [])]
        if en_correct != it_correct:
            mismatched_correct.append(qid)
        if en.get("correct_count") != it.get("correct_count"):
            mismatched_correct.append(qid)
        if en.get("question", "") and en["question"] == it.get("question", ""):
            identical_question.append(qid)

    if mismatched_correct:
        fail(17, f"{len(mismatched_correct)} domande con vettore 'correct' diverso tra EN/IT: "
                 f"{mismatched_correct[:5]}")
    if identical_question:
        fail(17, f"{len(identical_question)} domande IT con 'question' identico all'EN "
                 f"(traduzione mancante?): {identical_question[:5]}")

    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="Percorso a questions.json")
    ap.add_argument("--it", metavar="PATH", help="Percorso a questions_it.json per il confronto EN/IT")
    args = ap.parse_args()

    data = load(args.path)
    failures, idx_counter, n_single = validate(data, label="EN")

    print(f"=== {args.path}: {len(data)} domande, {n_single} single-select ===")
    if n_single:
        dist = {i: idx_counter.get(i, 0) for i in range(6)}
        print(f"Distribuzione indice corretto (single-select): {dist}")

    if args.it:
        data_it = load(args.it)
        it_failures, _, _ = validate(data_it, label="IT")
        failures += it_failures
        failures += validate_it_pair(data, data_it)

    if failures:
        print(f"\n{len(failures)} violazioni:")
        for f in failures:
            print(f)
        sys.exit(1)
    else:
        print("\nTutti i gate superati.")
        sys.exit(0)


if __name__ == "__main__":
    main()
