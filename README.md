# ☁️ AWS Certified Solutions Architect Associate (SAA-C03)

Materiale di studio e simulatore d'esame per la certificazione **AWS Solutions Architect Associate (SAA-C03)**.

## 📁 Struttura del Progetto

| Cartella | Contenuto |
|----------|-----------|
| `dispense/` | 8 dispense PDF per argomento (Storage, Compute, Networking, Databases, Security, Serverless, Monitoring, Cost Optimization) |
| `simulator/` | Simulatore d'esame con 1006 domande estratte da 16 set di esercizi |
| `worked_topics/` | Appunti e schede di studio per argomento |
| `STUDY_GUIDE_SAA-C03.md` | Guida di studio incrociata — mappa ogni argomento dell'esame ai capitoli specifici di ogni risorsa |

## 🎮 Exam Simulator

Simulatore web single-file con supporto italiano/inglese e filtro per categoria.

### Avvio rapido

```bash
# Avvia un server locale dalla cartella simulator/
cd simulator
python3 -m http.server 8080

# Apri nel browser: http://localhost:8080/simulator.html
```

### Funzionalità

- 🇬🇧/🇮🇹 Cambio lingua (domande + interfaccia)
- 📂 Filtro per categoria (Storage, Security, Networking, Compute, Databases, ecc.)
- 📋 Filtro per set di esercizi (1-16)
- ⏱️ Timer configurabile (default 130 min come esame reale)
- ✅ Correzione immediata con spiegazione
- 📊 Risultati con breakdown per categoria
- 🔄 Revisione completa post-esame

### Rigenerare le domande (opzionale)

```bash
pip install pdfplumber
python3 extract_final2.py
```

### Rigenerare la traduzione italiana (opzionale)

```bash
pip install deep-translator
python3 translate_simple.py
```

## 📚 Guida di Studio

Il file `STUDY_GUIDE_SAA-C03.md` mappa ogni argomento dell'esame ai capitoli specifici delle risorse di studio, organizzato per dominio:

- **Dominio 1** — Design Secure Architectures (30%)
- **Dominio 2** — Design Resilient Architectures (26%)
- **Dominio 3** — Design High-Performing Architectures (24%)
- **Dominio 4** — Design Cost-Optimized Architectures (20%)

## 🔗 Risorse Utili

- [AWS SAA-C03 Exam Guide](https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Exam-Guide.pdf)
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [AWS Free Tier](https://aws.amazon.com/free/)
