# ☁️ AWS SAA-C03 Exam Simulator

Simulatore per la certificazione **AWS Solutions Architect Associate (SAA-C03)**.  
1006 domande estratte da 16 set di esercizi, con supporto italiano/inglese e filtro per categoria.

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

## Rigenerare le domande (opzionale)

Se modifichi i PDF o ne aggiungi di nuovi:

```bash
# Installa dipendenza
pip install pdfplumber

# Estrai domande dai PDF
python3.11.exe extract_final2.py
```

## Rigenerare la traduzione italiana (opzionale)

```bash
# Installa dipendenza
pip install deep-translator

# Traduci questions.json → questions_it.json
python3.11.exe translate_simple.py
```

Lo script supporta il resume: se si interrompe, rilancialo e riprende da dove era rimasto.

## Struttura file

| File | Descrizione |
|------|-------------|
| `simulator.html` | App simulatore (unico file, nessun build) |
| `questions.json` | Domande in inglese |
| `questions_it.json` | Domande in italiano |
| `eser-*.pdf` | PDF sorgente con le domande |
| `extract_final2.py` | Script estrazione domande dai PDF |
| `translate_simple.py` | Script traduzione EN → IT |

## Funzionalità

- 🇬🇧/🇮🇹 Cambio lingua (domande + interfaccia)
- 📂 Filtro per categoria (Storage, Security, Networking, Compute, Databases, ecc.)
- 📋 Filtro per set di esercizi (1-16)
- ⏱️ Timer configurabile (default 130 min come esame reale)
- ✅ Correzione immediata con spiegazione
- 📊 Risultati con breakdown per categoria
- 🔄 Revisione completa post-esame
