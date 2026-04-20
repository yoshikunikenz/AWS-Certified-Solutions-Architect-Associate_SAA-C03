# WAF, Shield e Network Firewall

> Fonti: PACKT Cap.10 (p.455-458), PACKT Cap.12 (p.507-509), KIMIKO (p.286-291), DOJO (p.215-216, p.281)

---

## AWS WAF — Web Application Firewall

### Panoramica

Il PACKT descrive WAF come *"un servizio di web application firewall che aiuta a proteggere le applicazioni web e le API da attacchi web comuni. È progettato per fornire una soluzione di sicurezza completa per chiunque ospiti le proprie applicazioni web sul cloud AWS."*

Il Dojo aggiunge: *"Puoi usare AWS WAF per creare regole custom che bloccano pattern di attacco comuni, come SQL injection e attacchi cross-site scripting."*

### Cosa Protegge

Kimiko lo spiega nel suo walkthrough: *"Configuriamo WAF per proteggere le nostre CloudFront distributions, Application Load Balancers e/o Amazon API Gateways."*

Il Dojo conferma l'integrazione: WAF è strettamente integrato con **Amazon CloudFront, Application Load Balancer (ALB), Amazon API Gateway e AWS AppSync**.

### Pricing (da Kimiko)

Kimiko mostra il pricing nella console e lo commenta: *"Che esempio incredibilmente granulare di pricing con AWS. Nella vita reale, in ambienti on-premises tradizionali, potremmo dover spendere centinaia di migliaia di dollari per equipaggiamento upfront per avere questo livello di protezione."*

- $5 per Web ACL al mese (prorated hourly)
- $1 per regola al mese
- $0.60 per milione di richieste processate

### Rule Statements (dal Dojo)

Il Dojo fornisce la tabella completa dei match statements disponibili:

| Match Statement | Caso d'uso |
|---|---|
| **Geographic match** | Permetti o blocca richieste web basate sul paese di origine. Se usi la geo restriction di CloudFront per bloccare un paese, le richieste da quel paese sono bloccate e non vengono inoltrate a WAF |
| **IP set match** | Ispeziona l'IP di una richiesta contro un set di IP e range che vuoi permettere o bloccare |
| **Label match** | Ispeziona la richiesta per label aggiunte da altre regole nella stessa Web ACL |
| **Regex pattern set** | Confronta pattern regex contro un componente specifico della richiesta web |
| **Size constraint** | Confronta la dimensione di un componente della richiesta contro un vincolo in byte |
| **SQLi attack** | Ispeziona per codice SQL malevolo in una richiesta web |
| **String match** | Cerca una stringa corrispondente in un componente della richiesta web |
| **XSS scripting attack** | Ispeziona per attacchi cross-site scripting in una richiesta web |
| **Rate-based** | Traccia il rate di richieste per ogni IP sorgente e triggera un'azione sugli IP che superano un limite. Puoi usare questo tipo di regola per mettere un blocco temporaneo su richieste da un IP che invia richieste eccessive |

### Walkthrough Pratico di Kimiko: Creare una Web ACL

Kimiko mostra il processo nella console:
1. Crea una Web ACL con nome e CloudWatch metric name
2. Seleziona la Region (es. US East)
3. Aggiungi regole — puoi creare le tue o usare **managed rule groups**
4. Kimiko sceglie il **Core Rule Set** di AWS: *"Generalmente applicabile alle applicazioni web. Fornisce protezione contro lo sfruttamento di un'ampia gamma di vulnerabilità, incluse quelle descritte nelle pubblicazioni OWASP."*
5. Nota la **capacity**: non puoi superare 1500 Web ACL Rule Capacity Units
6. L'azione di default per richieste che non matchano nessuna regola: **Allow**
7. Associa le risorse AWS (CloudFront distributions, API Gateways, ALB)

> **Nota da Kimiko**: *"C'è ancora il WAF Classic disponibile, ma non riesco a immaginare di usarlo alla luce del nuovo e migliorato Web Application Firewall."*

---

## AWS Shield

### Shield Standard vs Shield Advanced

Il PACKT spiega: *"AWS Shield offre due livelli di servizio: AWS Shield Standard è fornito senza costi aggiuntivi a tutti i clienti AWS e offre protezione base contro attacchi DDoS, mentre AWS Shield Advanced fornisce capacità di mitigazione DDoS più complete, incluso accesso a team dedicati di risposta DDoS e analytics avanzate, per un canone mensile."*

Kimiko aggiunge dalla console: *"AWS Shield Standard è la protezione DDoS distribuita che viene fatta contro il tuo account automaticamente. Stai già ottenendo quel beneficio automaticamente. Ma per $3,000 al mese più costi aggiuntivi di data transfer, puoi attivare AWS Shield Advanced, che ti darà feature molto più granulari, più supporto e più visibilità nella protezione DDoS."*

### Confronto Completo (dal Dojo)

| Caratteristica | AWS WAF | AWS Shield Basic | AWS Shield Advanced |
|---|---|---|---|
| **Protezione** | Monitora richieste HTTP/HTTPS. Protegge da SQL injection, XSS, rate-limiting, bad bots | Protezione contro attacchi L3/L4 comuni (SYN/UDP floods, reflection attacks, DDoS). Funziona con IPv4 e IPv6 | Protezioni aggiuntive contro attacchi più sofisticati e grandi. Notifiche near real-time di incidenti DDoS sospetti. Tecniche avanzate di mitigazione e routing |
| **Integrazione** | CloudFront, ALB, API Gateway, AppSync | La maggior parte delle risorse AWS sono automaticamente integrate e protette | EC2, ELB, CloudFront, Global Accelerator, Route 53 |
| **Pricing** | Basato su numero di Web ACL, regole per ACL, e richieste web ricevute | Gratuito, automaticamente abilitato per tutti i clienti AWS | $3,000/mese per organizzazione + costi di data transfer per risorse protette |
| **DDoS Response Team** | No | No | Sì (con Business o Enterprise support plan) |

### Protezione DDoS — Strategie (dal PACKT Cap.12)

Il PACKT Cap.12 elenca le strategie per proteggersi da DDoS:

1. **Architetture scalabili**: *"Il motivo principale per cui DDoS ha successo è che l'applicazione si blocca quando le sue risorse sono completamente utilizzate. Se la tua applicazione è scalabile, può scalare per soddisfare la domanda inaspettata."* Caveat: può essere incredibilmente costoso. Metti guardrail per limitare quanto l'infrastruttura può scalare. Usa Route 53 per failover e CloudFront per distribuire il traffico.

2. **AWS Shield Standard**: *"Automaticamente abilitato per tutti i clienti AWS senza costi aggiuntivi. Mitiga attacchi DDoS base e comuni facendo scrubbing di pacchetti malevoli e attività di scaling."*

3. **Bloccare traffico malevolo**: AWS Network Firewall e AWS WAF

> **Tip esame (PACKT Cap.12)**: *"Make sure you understand the difference between each of the security services. Learn which ones can actually perform mitigations and which ones are more about detection."*

### SQL Injection (dal PACKT Cap.12)

Il PACKT Cap.12 spiega: *"SQL injection funziona inviando una query SQL malevola al tuo database backend tramite il frontend web. Nel peggiore dei casi, può risultare nella perdita del tuo database."*

Protezioni:
1. **Sanitizzare gli input** — controlla lunghezza query, caratteri speciali, wildcard (buona pratica ma improbabile nell'esame)
2. **AWS WAF** — *"WAF allows you to create match conditions to identify malicious SQL code. This will likely be the correct answer for any question asking about the right way to prevent SQL injection in the exam."*

---

## AWS Firewall Manager (da Kimiko)

Kimiko mostra il Firewall Manager nella console: *"Una grande idea da Amazon per darci gestione centralizzata di tutte quelle regole firewall che potrebbero essere sparse nei nostri diversi account e nelle nostre diverse applicazioni."*

Costo: **$100/mese per policy** configurata per la gestione centralizzata.

Prerequisiti (da Kimiko):
1. L'account deve essere membro di **AWS Organizations** ✓
2. L'account deve essere l'**AWS Firewall Manager administrator** 
3. Deve essere configurato **AWS Config** per l'account/region

> **Nota da Kimiko**: *"Il Firewall Manager dipende direttamente da AWS Organizations, AWS Config e l'account administrator appropriato. Devi soddisfare tutte e tre le condizioni."*

---

## Tip Esame Chiave

### WAF vs Shield — Come Scegliere (dal PACKT)

Il PACKT fornisce una nota esplicita per l'esame:

> *"When deciding between Shield or WAF as the correct answer, look for whether the question is specifically asking for DDoS protection. If yes, Shield is probably the correct answer. If the question is more concerned about things such as SQL injection or XSS, then WAF is likely to be the correct answer. In reality, though, both should be used to provide a holistic security approach."*

### Insight di Kimiko sulla Sicurezza Cloud

Kimiko conclude con una riflessione importante: *"Quando sento panico riguardo alla sicurezza con un passaggio al cloud pubblico come AWS, certo, dobbiamo essere preoccupati per la sicurezza, ma se facciamo i compiti, se impariamo a usare questi strumenti, se li configuriamo correttamente, scommetto che quando guardiamo di nuovo attentamente le nostre architetture, scopriremo che abbiamo guadagnato molto in sicurezza. Non abbiamo perso nell'area della sicurezza, abbiamo guadagnato parecchio."*

---

## Scenari Tipici d'Esame

### Scenario 1: Protezione da SQL Injection
**Domanda**: L'applicazione web è vulnerabile a SQL injection. Come proteggerla?

**Risposta**: **AWS WAF** con match conditions per identificare codice SQL malevolo (PACKT Cap.12: *"This will likely be the correct answer for any question asking about the right way to prevent SQL injection"*).

### Scenario 2: Attacco DDoS
**Domanda**: L'applicazione è sotto attacco DDoS. Come proteggerla?

**Risposta**: **Shield** per DDoS (PACKT: *"If the question is specifically asking for DDoS protection, Shield is probably the correct answer"*). Shield Standard è già attivo gratuitamente. Per protezione avanzata con DRT: Shield Advanced.

### Scenario 3: Limitare richieste per IP
**Domanda**: Un bot sta facendo troppe richieste alla tua API.

**Risposta**: **WAF con rate-based rule** (Dojo: *"Tracks the rate of requests of each originating IP addresses, and triggers a rule action on IPs with rates that go over a limit"*).

### Scenario 4: Bloccare traffico da un paese specifico
**Domanda**: L'applicazione deve essere accessibile solo dall'Italia.

**Risposta**: **WAF con geographic match** (Dojo: *"Allows you to allow or block web requests based on country of origin"*).

### Scenario 5: Gestione centralizzata regole su più account
**Domanda**: L'organizzazione ha 50 account AWS e vuole applicare le stesse regole WAF a tutti.

**Risposta**: **AWS Firewall Manager** (Kimiko: gestione centralizzata, richiede Organizations + Config + admin account).

---

## Riepilogo Veloce per l'Esame

- **WAF**: protezione Layer 7 (SQLi, XSS, bot, rate limiting), funziona con ALB/CloudFront/API GW/AppSync (PACKT, Dojo)
- **Shield Standard**: gratuito, automatico per tutti, protezione DDoS base L3/L4 (PACKT, Kimiko)
- **Shield Advanced**: $3,000/mese, DRT, notifiche near real-time, mitigazione avanzata (Dojo, Kimiko)
- **WAF pricing**: $5/Web ACL + $1/regola + $0.60/milione richieste (Kimiko)
- **DDoS → Shield, SQLi/XSS → WAF** (PACKT nota esame)
- **Rate-based rules**: per limitare richieste per IP, anti-DDoS L7, anti-bot (Dojo)
- **Geo match**: per bloccare/permettere traffico per paese (Dojo)
- **Core Rule Set**: protezione OWASP out-of-the-box (Kimiko)
- **Firewall Manager**: gestione centralizzata multi-account, richiede Organizations + Config (Kimiko)
- **Entrambi WAF + Shield** per approccio olistico alla sicurezza (PACKT)
