# ☁️ AWS Certified Solutions Architect Associate (SAA-C03)

Materiale di studio e simulatore d'esame per la certificazione **AWS Solutions Architect Associate (SAA-C03)**.

## 📁 Struttura del Progetto

| Cartella | Contenuto |
|----------|-----------|
| `simulator/` | Simulatore d'esame con 1017 domande estratte da 16 set di esercizi |
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
- ☑️ Domande multi-risposta ("Choose two/three") con punteggio tutto-o-nulla, come l'esame reale
- ⏱️ Timer configurabile (default 130 min come esame reale)
- ✅ Correzione immediata con spiegazione
- 📊 Risultati con breakdown per categoria
- 🔄 Revisione completa post-esame

### Rigenerare le domande (opzionale)

I PDF sorgente non sono nel repo ma restano recuperabili dalla history di git. Vedi
[simulator/README.md](simulator/README.md#provenienza-dei-dati) per il dettaglio su come i dati
vengono estratti (font/colore/posizione del PDF, non euristiche sulla prosa) e validati.

```bash
pip install pdfplumber
cd simulator
python3 extract_questions.py --from-git 4625480^ -o questions.json
python3 validate_questions.py questions.json
```

### Rigenerare la traduzione italiana

Vedi [simulator/README.md](simulator/README.md#rigenerare-la-traduzione-italiana).

## 🔗 Risorse Utili

- [AWS SAA-C03 Exam Guide](https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Exam-Guide.pdf)
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [AWS Free Tier](https://aws.amazon.com/free/)
