# ☁️ AWS SAA-C03 Exam Simulator

Simulatore per la certificazione **AWS Solutions Architect Associate (SAA-C03)**.  
1017 domande estratte da 16 set di esercizi, con supporto italiano/inglese, filtro per categoria
e domande multi-risposta ("Choose two/three").

## Requisiti

- Python 3.11+
- Browser moderno

## Avvio rapido

```bash
# 1. Avvia il server locale
python3.11.exe -m http.server 8080

# 2. Apri nel browser
# http://localhost:8080/simulator.html
```

## Provenienza dei dati

I PDF sorgente (`eser-N.pdf`, export HTML→PDF di itcertifications.io) non sono nel repo — rimossi
intenzionalmente per la pubblicazione pubblica — ma restano recuperabili dalla history di git
(`git show <ref>:simulator/eser-N.pdf`). `questions.json` viene ricostruito leggendo la
**struttura** del PDF, non indovinando dalla prosa:

- la risposta corretta è il pallino radio **verde** (`page.curves`, colore e dimensione esatti);
- il ruolo di ogni riga di testo (domanda, opzione, spiegazione, intestazione) è determinato da
  **font size + indentazione x0**, non dal contenuto delle parole;
- le domande multi-risposta si riconoscono dal **numero di marker verdi**, non dalla frase
  "(Choose two.)" nello stem (assente in oltre metà di quei casi).

Vedi il docstring di `extract_questions.py` per il dettaglio completo delle costanti e del
perché questo approccio sostituisce i vecchi estrattori basati su euristiche di testo.

## Rigenerare le domande (opzionale)

Se modifichi i PDF o ne aggiungi di nuovi:

```bash
# Installa dipendenza
pip install pdfplumber

# Estrai domande dai PDF (dalla history di git, senza bisogno dei PDF nel repo)
python3 extract_questions.py --from-git 4625480^ -o questions.json

# Oppure da una cartella locale fuori dal repo
python3 extract_questions.py --pdf-dir /percorso/ai/pdf -o questions.json

# Valida il risultato prima di committarlo (deve uscire con "Tutti i gate superati")
python3 validate_questions.py questions.json
```

`validate_questions.py` applica 17 controlli di qualità (conteggi, id, coerenza risposta
corretta, assenza di rumore PDF, categorie note, ecc.) — è il gate che ha permesso di scoprire
la corruzione della pipeline precedente ed è pensato per non ripetersi.

## Rigenerare la traduzione italiana

`questions_it.json` va rigenerato **dall'EN corretto**. Questa fase è deliberatamente fuori dallo
scope dell'ultima revisione dei dati EN — vedi la sezione "Fase successiva" del piano di
migrazione per i requisiti del nuovo script di traduzione (join per `id`, non per posizione).

## Struttura file

| File | Descrizione |
|------|-------------|
| `simulator.html` | App simulatore (unico file, nessun build) |
| `questions.json` | Domande in inglese |
| `questions_it.json` | Domande in italiano |
| `eser-*.pdf` | PDF sorgente con le domande (non nel repo, vedi "Provenienza dei dati") |
| `extract_questions.py` | Estrae `questions.json` dai PDF leggendone font/colore/posizione |
| `validate_questions.py` | Gate di qualità sui dati estratti |

## Funzionalità

- 🇬🇧/🇮🇹 Cambio lingua (domande + interfaccia)
- 📂 Filtro per categoria (Storage, Security, Networking, Compute, Databases, ecc.)
- 📋 Filtro per set di esercizi (1-16)
- ☑️ Domande multi-risposta ("Choose two/three") con punteggio tutto-o-nulla, come l'esame reale
- ⏱️ Timer configurabile (default 130 min come esame reale)
- ✅ Correzione immediata con spiegazione
- 📊 Risultati con breakdown per categoria
- 🔄 Revisione completa post-esame
