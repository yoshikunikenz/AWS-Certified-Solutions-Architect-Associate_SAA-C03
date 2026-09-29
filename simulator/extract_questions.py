#!/usr/bin/env python3
"""Estrae le domande del simulatore SAA-C03 dai PDF sorgente (eser-N.pdf).

I PDF sono export HTML->PDF di itcertifications.io. Non vivono nel repo (rimossi
in modo intenzionale nel commit 4625480 per la pubblicazione pubblica) ma restano
recuperabili dalla history di git.

## Provenienza dei dati: perché questo estrattore legge la struttura, non il testo

Gli estrattori precedenti (extract_all.py, extract_final.py, extract_final2.py,
extract_v2.py) chiamavano solo page.extract_text(), buttando via font e colori,
e poi INDOVINAVANO dove finisce un'opzione e quale sia corretta con euristiche a
regex sulla prosa delle spiegazioni. Il risultato: 73% delle opzioni troncate a
metà frase e il 68% delle risposte "corrette" finite sull'indice 0 per un
default di posizione in un max() su punteggi a pari merito.

Il PDF sorgente in realta' codifica tutto questo in modo deterministico, perche'
e' stato generato da un layout HTML con classi CSS fisse:

  - Risposta corretta = pallino radio VERDE, un cerchio (page.curves) 12x12pt con
    stroking_color == MARKER_GREEN. Non selezionato = stesso cerchio ma grigio
    (MARKER_GREY). Attenzione: esistono anche un punto interno verde 4x2pt e
    cerchi rossi/ambra/blu nei grafici di riepilogo della pagina 1-2: il filtro
    12x12pt esatto li esclude tutti.
  - Ruolo del testo = font size + indentazione x0 (colonna sinistra), non il
    contenuto delle parole:
      x0 ~53.2  size 12.0        -> testo della domanda (stem)
      x0 ~86.2  size 12.0        -> testo di un'opzione
      x0 ~86.2  size 10.5        -> spiegazione di quell'opzione
      x0 ~65.2  size 10.5 Semib. -> intestazione "Overall Explanation:"
      x0 ~65.2  size 12.0        -> corpo della spiegazione generale
      x0 ~61.5  size 9.0  Semib. -> intestazione "Question N <categoria>"
  - Le domande scavalcano le pagine: i marker di un'opzione possono stare sulla
    pagina successiva allo stem. Il parsing costruisce quindi UN SOLO stream
    ordinato per tutto il documento (chiave pagina*10000 + coordinata Y), non un
    parsing pagina per pagina.
  - Multi-select: si legge dal NUMERO DI MARKER VERDI, non dalla frase
    "(Choose two.)" nello stem -- che manca in 53 domande su 121 multi-select e,
    nei 2 casi osservati in cui e' presente ma con un solo marker verde, e' il
    PDF stesso a essere incoerente (il marker resta l'unica fonte di verita').
  - L'header "Question N" non richiede una parola di stato dopo il numero: nella
    maggior parte dei casi e' "Question N Not Attempted <Categoria>", ma la
    prima domanda di alcuni set (es. eser-2#1) e' semplicemente
    "Question 1 <Categoria>" perche' quella domanda risulta "Incorrect" nel
    report da cui il PDF e' stato esportato.

Uso:
    python3 extract_questions.py --from-git 4625480^
    python3 extract_questions.py --from-git 4625480^ --sets 1,7,16
    python3 extract_questions.py --pdf-dir /percorso/fuori/dal/repo
    python3 extract_questions.py --from-git 4625480^ -o simulator/questions.json

NOTA: non fare `git show REF:file.pdf | python3 extract_questions.py ...` --
pdfplumber legge/contende lo stdin e fallisce con "No /Root object!". Lo script
invoca git internamente via subprocess, quindi va eseguito normalmente.
"""
import argparse
import io
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pdfplumber

# --- Costanti derivate empiricamente dai 16 PDF (vedi docstring del modulo) ---
MARKER_GREEN = (0.1333, 0.7725, 0.3686)
MARKER_GREY = (0.4200, 0.4473, 0.5020)
MARKER_SIZE = 12  # pt, esatto: esclude il puntino interno 4x2 e i cerchi dei grafici

X0_STEM = 53.2
X0_OVERALL = 65.2
X0_OPTION = 86.2
X0_HEADER = 61.5
X0_TOL = 1.5

SIZE_OPTION = 12.0
SIZE_EXPL = 10.5
SIZE_HEADER = 9.0
SIZE_TOL = 0.3

STATUS_WORDS = {
    "Not", "Attempted", "Correct", "Incorrect", "Skipped",
    "Partially", "Unanswered", "Marked", "Review", "for",
}

SETS_ALL = list(range(1, 17))


def _color_matches(c, ref, tol=0.01):
    if not c or len(c) != 3:
        return False
    return all(abs(a - b) <= tol for a, b in zip(c, ref))


def _load_pdf_bytes_from_git(ref: str, n: int) -> bytes:
    path = f"simulator/eser-{n}.pdf"
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        capture_output=True, check=True,
    )
    return result.stdout


def build_event_stream(pdf):
    """Costruisce un unico stream (pos, kind, payload) ordinato su tutto il documento."""
    stream = []
    dropped = Counter()

    for pi, page in enumerate(pdf.pages):
        base = pi * 10000

        # 1. Marker radio: cerchi 12x12pt verdi o grigi
        for cv in page.curves:
            w, h = cv.get("width"), cv.get("height")
            if w is None or h is None:
                continue
            if round(w) != MARKER_SIZE or round(h) != MARKER_SIZE:
                continue
            sc = cv.get("stroking_color")
            if _color_matches(sc, MARKER_GREEN):
                stream.append((base + cv["top"], "marker", True))
            elif _color_matches(sc, MARKER_GREY):
                stream.append((base + cv["top"], "marker", False))

        # 2. Immagini (diagrammi raster referenziati dallo stem)
        for img in page.images:
            if img.get("width", 0) > 100 and img.get("height", 0) > 40:
                stream.append((base + img["top"], "image", None))

        # 3. Righe di testo, raggruppate per riga e classificate per size + x0
        words = page.extract_words(extra_attrs=["size", "fontname"])
        rows = {}
        for w in words:
            key = round(w["top"], 1)
            rows.setdefault(key, []).append(w)

        for key in sorted(rows):
            ws = sorted(rows[key], key=lambda x: x["x0"])
            lead = ws[0]
            size = round(lead["size"], 1)
            x0 = lead["x0"]
            font = lead["fontname"]
            text = " ".join(x["text"] for x in ws).strip()
            if not text:
                continue
            top = lead["top"]

            def near(v, ref):
                return abs(v - ref) <= X0_TOL

            def sz(v, ref):
                return abs(v - ref) <= SIZE_TOL

            tokens = text.split()
            if (
                sz(size, SIZE_HEADER) and "Semibold" in font
                and near(x0, X0_HEADER)
                and tokens and tokens[0] == "Question"
                and len(tokens) > 1 and tokens[1].isdigit()
            ):
                num = int(tokens[1])
                category = " ".join(t for t in tokens[2:] if t not in STATUS_WORDS)
                category = category.rstrip(",")
                stream.append((base + top, "header", (num, category)))
            elif (
                sz(size, SIZE_EXPL) and "Semibold" in font
                and near(x0, X0_OVERALL) and text.startswith("Overall Explanation")
            ):
                stream.append((base + top, "overall_start", None))
            elif sz(size, SIZE_OPTION) and near(x0, X0_STEM):
                stream.append((base + top, "text", ("stem", text)))
            elif sz(size, SIZE_OPTION) and near(x0, X0_OVERALL):
                stream.append((base + top, "text", ("overall", text)))
            elif sz(size, SIZE_OPTION) and near(x0, X0_OPTION):
                stream.append((base + top, "text", ("option", text)))
            elif sz(size, SIZE_EXPL) and near(x0, X0_OPTION):
                stream.append((base + top, "text", ("option_expl", text)))
            else:
                dropped[(size, round(x0, 1))] += 1

    stream.sort(key=lambda e: e[0])
    return stream, dropped


def fold_stream(stream, source):
    """Piega lo stream ordinato in record di domande (macchina a 3 stati)."""
    questions = []
    cur = None
    phase = None
    misplaced = Counter()

    def flush():
        if cur is not None:
            questions.append(cur)

    for _, kind, payload in stream:
        if kind == "header":
            flush()
            num, category = payload
            cur = {
                "number": num, "category": category, "source": source,
                "stem_lines": [], "options": [], "overall_lines": [],
                "has_image": False,
            }
            phase = "stem"
        elif cur is None:
            continue
        elif kind == "marker":
            is_green = payload
            cur["options"].append({"text_lines": [], "expl_lines": [], "correct": is_green})
            phase = "options"
        elif kind == "overall_start":
            phase = "overall"
        elif kind == "image":
            cur["has_image"] = True
        elif kind == "text":
            role, text = payload
            if phase == "stem" and role == "stem":
                cur["stem_lines"].append(text)
            elif phase == "overall" and role == "overall":
                cur["overall_lines"].append(text)
            elif phase == "options" and role == "option" and cur["options"]:
                cur["options"][-1]["text_lines"].append(text)
            elif phase == "options" and role == "option_expl" and cur["options"]:
                cur["options"][-1]["expl_lines"].append(text)
            else:
                misplaced[(phase, role)] += 1
    flush()
    return questions, misplaced


def _join(lines):
    return re.sub(r"\s+", " ", " ".join(lines)).strip()


def emit_records(questions):
    records = []
    for q in questions:
        answers = []
        for opt in q["options"]:
            answers.append({
                "text": _join(opt["text_lines"]),
                "explanation": _join(opt["expl_lines"]),
                "correct": opt["correct"],
            })
        correct_count = sum(1 for a in answers if a["correct"])
        records.append({
            "id": f"{q['source']}#{q['number']}",
            "number": q["number"],
            "category": q["category"],
            "source": q["source"],
            "question": _join(q["stem_lines"]),
            "answers": answers,
            "overall_explanation": _join(q["overall_lines"]),
            "has_correct": correct_count > 0,
            "correct_count": correct_count,
            "has_image": q["has_image"],
        })
    return records


def extract_set(pdf_bytes: bytes, n: int, verbose=False):
    source = f"eser-{n}"
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        stream, dropped = build_event_stream(pdf)
    questions, misplaced = fold_stream(stream, source)
    records = emit_records(questions)
    if verbose:
        print(f"  {source}: {len(records)} domande, dropped_text_buckets={len(dropped)}, "
              f"misplaced={sum(misplaced.values())}", file=sys.stderr)
    return records


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--from-git", metavar="REF",
                      help="Legge i PDF da un ref/commit git (es. 4625480^) invece che dal disco")
    src.add_argument("--pdf-dir", metavar="DIR",
                      help="Legge eser-N.pdf da questa cartella (deve stare fuori dal repo)")
    ap.add_argument("--sets", default=None,
                     help="Sottoinsieme di set da elaborare, es. '1,7,16' (default: tutti 1-16)")
    ap.add_argument("-o", "--output", default="simulator/questions.json")
    args = ap.parse_args()

    set_nums = SETS_ALL
    if args.sets:
        set_nums = [int(x) for x in args.sets.split(",")]

    all_records = []
    for n in set_nums:
        if args.from_git:
            pdf_bytes = _load_pdf_bytes_from_git(args.from_git, n)
        else:
            path = Path(args.pdf_dir) / f"eser-{n}.pdf"
            pdf_bytes = path.read_bytes()
        all_records.extend(extract_set(pdf_bytes, n, verbose=True))

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(all_records, f, ensure_ascii=False, indent=2)

    print(f"\nScritte {len(all_records)} domande in {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
