# ☁️ AWS Certified Solutions Architect Associate (SAA-C03)

Materiale di studio e simulatore d'esame per la certificazione **AWS Solutions Architect Associate (SAA-C03)**.

## 📁 Struttura del Progetto

| Cartella | Contenuto |
|----------|-----------|
| `simulator/` | Simulatore d'esame con 1006 domande estratte da 16 set di esercizi |
| `worked_topics/` | Appunti e schede di studio per argomento |

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

## 🔗 Risorse Utili

- [AWS SAA-C03 Exam Guide](https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Exam-Guide.pdf)
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [AWS Free Tier](https://aws.amazon.com/free/)
