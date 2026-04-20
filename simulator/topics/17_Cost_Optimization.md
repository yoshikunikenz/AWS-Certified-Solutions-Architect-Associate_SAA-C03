# Cost Optimization - Pricing, Storage, Compute, Database, Network

> Fonti: PACKT Cap.15 (p.588-605), KIMIKO Cost Optimization (p.109-117) + Cost Explorer (p.47-49) + Billing (p.303-304), DOJO (p.263, p.285)

---

## Glossario: i concetti che incontrerai in questo documento

- **On-Demand** — il modello di pricing base di AWS. Paghi per quello che usi, quando lo usi, senza impegni. Come prendere un taxi: paghi la corsa e basta. Nessuno sconto, ma massima flessibilità.

- **Reserved Instance (RI)** — ti impegni a usare un certo tipo di istanza per 1 o 3 anni in cambio di uno sconto fino al 72%. Come un abbonamento annuale ai mezzi pubblici: paghi meno per corsa ma sei vincolato.

- **Savings Plan** — come le RI ma più flessibile. Ti impegni a spendere un certo importo all'ora, e lo sconto si applica automaticamente a EC2, Lambda, Fargate, SageMaker. Come un abbonamento "all-inclusive" che copre bus, metro e tram.

- **Spot Instance** — capacità EC2 inutilizzata venduta a prezzo scontato (fino a -90%). AWS può riprendersela con 2 minuti di preavviso. Come un biglietto aereo last-minute: costa pochissimo ma potresti essere "bumpato".

- **Cost Explorer** — lo strumento per analizzare i tuoi costi AWS nel tempo. Mostra grafici, trend, e raccomandazioni per risparmiare. Come il cruscotto della tua auto che mostra il consumo di carburante.

- **AWS Budgets** — ti permette di impostare budget e ricevere alert quando i costi si avvicinano alla soglia. Come impostare un limite di spesa sulla carta di credito.

- **Lifecycle Policy** — una regola automatica che sposta i dati tra storage class nel tempo (es. da S3 Standard a Glacier dopo 90 giorni). Ottimizza i costi automaticamente senza intervento manuale.

- **Right-Sizing** — scegliere il tipo e la dimensione giusta delle risorse per il workload. Non troppo grande (sprechi soldi), non troppo piccolo (performance scarse). Puoi sempre cambiare dopo. Come scegliere la taglia giusta di scarpe: non compri la 45 "per sicurezza" se porti la 42.

- **Data Transfer** — il costo per spostare dati dentro e fuori da AWS. Regola generale: **non paghi per i dati che ENTRANO in AWS, paghi per i dati che ESCONO**. Come un parcheggio: entrare è gratis, uscire costa.

---

## I Principi del Cost Optimization (da Kimiko)

Kimiko analizza il documento AWS Cost Optimization Pillar (35 pagine) e ne estrae i principi:

### 1. Adopt a Consumption Model
*"Paga solo per le risorse di computing che consumi. Se sei un ufficio con un solo turno, puoi disabilitare diversi server durante le ore serali e riportarli online solo quando gli utenti ne hanno bisogno."*

Kimiko distingue:
- **Servizi 24/7**: quelli per i clienti, che potrebbero servire sempre
- **Servizi business-hours**: quelli per i dipendenti, che puoi spegnere la sera e riaccendere la mattina

### 2. Measure Overall Efficiency
*"Monitora il valore di business che ogni sistema produce rispetto al suo costo. Se un dipartimento consuma il 30% dei costi AWS ma produce solo il 5% del valore di business, rivaluta."*

### 3. Stop Spending Money on Data Center Operations
*"AWS fa rack & stack per te. Non devi spendere per costruire un data center per testare una nuova soluzione."*

### 4. Analyze and Attribute Expenditure
*"Guarda da dove vengono i costi in AWS e assicurati di capire quale dipartimento li sta consumando."*

### 5. Use Managed Services to Reduce Cost of Ownership
*"Quando usi servizi gestiti come RDS invece di un database su EC2, non servono tante ore-uomo per gestire il database."*

### I 4 Sotto-Pilastri (da Kimiko)

1. **Use cost-effective resources** — *"A volte è meno costoso usare un'istanza più potente che costa di più all'ora, perché finisce il lavoro più velocemente"*
2. **Match supply with demand** — Auto Scaling per avere il numero giusto di server
3. **Expenditure awareness** — usa billing alerts per sapere quando superi una soglia
4. **Optimize over time** — *"Man mano che implementi più soluzioni AWS, impari di più su come fare il lavoro con meno spese possibili. Ma ci vuole tempo ed esperienza"*

---

## Cost-Optimized Storage (dal PACKT Cap.15)

### Pricing dei Servizi Storage

| Servizio | Come si paga | Note |
|---|---|---|
| **S3** | Storage + richieste (PUT/COPY/POST/LIST) + data transfer out | Più salvi, meno costa per GB. Non paghi per transfer IN |
| **S3 Glacier** | Storage (molto basso) + retrieval fees | Fee di retrieval dipendono dalla classe e velocità |
| **EFS** | Storage + throughput provisionato (burst o provisioned) + data transfer | Due tier: Standard e IA |
| **EBS** | Tipo volume + storage + throughput + IOPS provisionati + snapshot | gp3 spesso più economico di gp2 perché IOPS/throughput configurabili separatamente |

### Strategie di Ottimizzazione Storage (dal PACKT Cap.15)

**Batch vs Individual Uploads**: AWS addebita per richiesta PUT/COPY/POST/LIST. Per milioni di oggetti, usa **S3 Batch Operations** ($0.25/job + $1/milione operazioni).

**Storage Tiering e Lifecycle**: *"Nella domanda d'esame sulle storage class S3, identifica il caso d'uso dei dati e se ci sono requisiti di disponibilità o costo. La domanda spesso dice che i dati servono regolarmente per X mesi, dopo di che servono ancora ma raramente. In questo caso, tieni i dati in Standard per X mesi, poi spostali in Glacier."*

**Intelligent-Tiering**: sposta automaticamente i dati tra Standard e IA basandosi sui pattern di accesso.

**EBS Snapshots**: incrementali dopo il primo full snapshot. Usa **Amazon Data Lifecycle Manager** per gestire retention.

> **Tip esame (PACKT Cap.15)**: *"gp3 è più performante di gp2 — ricordare questo dovrebbe essere sufficiente per selezionare la risposta corretta se devi scegliere tra i due."*

---

## Cost-Optimized Compute (dal PACKT Cap.15)

### Pricing Models — Quando Usare Cosa

| Modello | Sconto | Quando usarlo (PACKT Cap.15) |
|---|---|---|
| **On-Demand** | 0% | Workload imprevedibili, test, dev |
| **Reserved Instances** | Fino a 72% | Workload consistenti e noti, impegno 1-3 anni |
| **Savings Plans** | Fino a 72% | Come RI ma include anche **Fargate, Lambda, SageMaker** |
| **Spot Instances** | Fino a 90% | Workload spiky, interrompibili |
| **Dedicated Hosts** | Variabile | Hardware dedicato richiesto, BYOL |

> **Tip esame (PACKT Cap.15)**: *"Se la scelta è tra Savings Plans e Reserved Instances, cerca se la domanda menziona Fargate o Lambda. Solo i Savings Plans coprono compute diverso dalle istanze."*

> **Tip esame (PACKT Cap.15)**: *"Se la domanda dice che il cliente ha licenze che vuole usare, la risposta è Dedicated Hosts."*

### Scegliere il Servizio Compute Giusto (dal PACKT Cap.15)

| Workload | Servizio | Perché |
|---|---|---|
| **Steady, known** | EC2 | Prevedibile, ottimizzabile con RI/SP |
| **Unknown, spiky** | Lambda | Paghi solo quando gira, perfetto per workload intermittenti |
| **Variable, longer-running** | Fargate | Billing al secondo, perfetto per workload intermittenti che Lambda non gestisce (timeout 15 min) |

> **Tip esame (PACKT Cap.15)**: *"La cosa chiave da cercare nella domanda è se il workload è consistente e steady o se è intermittente."*

### Ottimizzare l'Utilizzo (dal PACKT Cap.15)

- **Auto Scaling** per EC2 e Fargate/ECS — scala su quando serve, scala giù quando non serve
- **Spegni le istanze** quando non in uso — EC2 addebita solo quando le istanze sono running
- **Schedula lo shutdown** con una Lambda function per istanze non necessarie fuori orario

### Ottimizzazione Regionale (dal PACKT Cap.15)

*"Region diverse hanno prezzi diversi. Minimizza il data transfer inter-region. Usa CloudFront per salvare contenuti statici all'edge."*

---

## Cost-Optimized Database (dal PACKT Cap.15)

### Scegliere il Database Giusto

| Servizio | Ottimizzazione costo (PACKT Cap.15) |
|---|---|
| **RDS** | Seleziona instance type appropriato (non troppo grande — puoi sempre aumentare). Usa RI e Savings Plans |
| **Aurora** | Sfrutta autoscaling (aggiunge/rimuove read replica automaticamente). Aurora Serverless per workload spiky |
| **DynamoDB** | Provisiona capacity units adeguate (non di più). Modificabile dopo |

### Strategie di Risparmio (dal PACKT Cap.15)

- **Read replicas**: scarica workload read-heavy dal primario → puoi usare un'istanza primaria meno costosa
- **Serverless databases**: paghi per uso effettivo, non per capacità fissa. Scala automaticamente
- **Caching** (ElastiCache): scarica letture dal DB → puoi usare un'istanza DB più piccola e meno costosa
- **Backup**: usa lifecycle policies S3 per spostare backup in cold storage. Attenzione a RPO/RTO nella domanda d'esame

### Widget Makers — Cost Optimization (da Kimiko)

Kimiko applica i principi allo scenario Widget Makers:

| Sistema | Raccomandazione costo |
|---|---|
| **Order Processing** | Usa managed database (RDS) → meno ore-uomo di gestione |
| **Inventory Management** | Stessa cosa — managed database |
| **Payroll** | Managed database + **read replica attiva solo quando serve**. *"Puoi portare online la read replica durante il downtime la sera prima del payroll. Così paghi solo poche ore ogni due settimane"* |
| **User Data** | **Monitora** cosa gli utenti mettono nei bucket S3. *"Dato che paghiamo per storage basato sulla dimensione, assicuriamoci di non mettere informazioni non necessarie"* |
| **Website** | **Classe giusta, non di più** (puoi sempre upgradare). Monitora accessi anomali — *"Se qualcuno trova una vulnerabilità WordPress per caricare file pirata, i costi di bandwidth esplodono"* |

> **Insight geniale da Kimiko**: la read replica del payroll si accende la sera prima dell'elaborazione, replica i dati durante la notte, il payroll gira la mattina, poi si spegne. Paghi poche ore ogni 2 settimane invece di 24/7.

---

## Cost-Optimized Network (dal PACKT Cap.15)

### Regola Generale sui Data Transfer (dal PACKT Cap.15)

*"La regola generale è: non paghi per il data transfer IN AWS ma paghi per il data transfer OUT di AWS. Non è sempre così, ma è una buona linea guida."*

### Strategie (dal PACKT Cap.15)

- **Direct Connect**: il più costoso, mesi per configurare. *"Puoi di solito escludere Direct Connect cercando nella domanda menzioni di low-cost o implementazione rapida"*
- **VPN**: opzione cost-effective per connessioni sicure on-premises ↔ cloud
- **Transit Gateway**: semplifica la gestione e riduce i costi di data transfer centralizzando il routing
- **PrivateLink/VPC Endpoints**: accesso a servizi AWS interni senza costi di internet egress o NAT gateway
- **Minimizza traffico cross-region**: paghi per data transfer out di una region
- **Global Accelerator**: ottimizza routing e riduce costi di data transfer per app globali
- **CloudFront**: salva contenuti statici all'edge per ridurre data transfer

> **Tip esame (PACKT Cap.15)**: *"L'area chiave da ricordare è controllare i costi di data transfer. Sono tipicamente i costi più grandi e quelli da evitare."*

---

## AWS Cost Management Tools (dal PACKT Cap.15 e Kimiko)

### AWS Cost Explorer (da Kimiko)

Kimiko mostra Cost Explorer nella console: *"La prima volta che vieni qui, non sarà abilitato. Quando lo abiliti, non vedrai nulla per 24 ore. Ma dopo, puoi vedere dati storici e dati correnti."*

Features mostrate da Kimiko:
- **Overview dei costi** con grafici temporali
- **Savings Plans**: puoi acquistare piani di risparmio
- **Budgets**: crea e gestisci budget per pianificazione finanziaria
- **Recommendations**: *"L'unica raccomandazione che ho è per EC2 — posso risparmiare $87 annualmente passando a un t2.nano reserved instance"*

### Strumenti (dal PACKT Cap.15)

| Strumento | Cosa fa |
|---|---|
| **Cost Explorer** | Analisi dettagliata costi e utilizzo. Report custom e alert |
| **AWS Budgets** | Budget custom per servizi specifici. Alert quando i costi si avvicinano alla soglia |
| **Cost and Usage Reports (CUR)** | Dati dettagliati line-item su utilizzo e costi. Per identificare opportunità di ottimizzazione |
| **Tagging Strategy** | Categorizza e traccia risorse e costi associati per dipartimento/progetto |

> **Tip esame (PACKT Cap.15)**: *"Assicurati di capire le limitazioni di ogni strumento perché potresti ricevere una domanda su quale modo usare per monitorare e rimediare i costi."*

### Billing Alarms (da Kimiko)

Kimiko mostra come configurare billing alarms: *"Puoi impostare alert di billing così sai quando hai superato una certa soglia nelle tue spese."*

---

## Scenari Tipici d'Esame

### Scenario 1: Workload steady-state per 3 anni con Lambda
**Domanda**: Un'applicazione usa EC2 e Lambda con carico prevedibile per 3 anni. Come risparmiare?

**Risposta**: **Savings Plans** (non RI) — perché coprono sia EC2 che Lambda (PACKT Cap.15).

### Scenario 2: Dati acceduti per 3 mesi poi archiviati
**Domanda**: I dati sono acceduti frequentemente per 3 mesi, poi raramente per 7 anni.

**Risposta**: S3 Standard per 3 mesi → **lifecycle policy** → Glacier dopo 90 giorni → Deep Archive dopo 1 anno → Delete dopo 7 anni (PACKT Cap.15).

### Scenario 3: Database usato solo durante il payroll
**Domanda**: La read replica del database serve solo 2 giorni al mese.

**Risposta**: **Accendi la read replica solo quando serve** — la sera prima del payroll, spegnila dopo (Kimiko scenario Widget Makers).

### Scenario 4: Ridurre costi di data transfer
**Domanda**: I costi di data transfer sono troppo alti per un'applicazione globale.

**Risposta**: **CloudFront** per contenuti statici all'edge + **VPC Endpoints** per accesso a servizi AWS senza internet egress (PACKT Cap.15).

### Scenario 5: Scegliere tra gp2 e gp3
**Domanda**: Serve un volume EBS con IOPS specifiche ma storage minimo.

**Risposta**: **gp3** — IOPS e throughput configurabili separatamente dallo storage, spesso più economico di gp2 (PACKT Cap.15).

---

## Riepilogo Veloce per l'Esame

- **Consumption model**: paga solo per quello che usi, spegni quello che non serve (Kimiko)
- **Managed services**: meno ore-uomo = meno costi operativi (Kimiko)
- **Right-sizing**: non provisionare troppo, puoi sempre aumentare dopo (PACKT, Kimiko)
- **A volte più potente = meno costoso** perché finisce prima (Kimiko)
- **Savings Plans > RI** quando serve copertura per Lambda/Fargate/SageMaker (PACKT Cap.15)
- **Spot**: fino a -90%, per workload interrompibili. **RI/SP**: fino a -72%, per workload steady (PACKT Cap.15)
- **Dedicated Hosts**: quando il cliente ha licenze BYOL (PACKT Cap.15)
- **S3 lifecycle policies**: Standard → IA → Glacier → Deep Archive → Delete (PACKT Cap.15)
- **gp3 > gp2**: più flessibile e spesso più economico (PACKT Cap.15)
- **Data transfer**: non paghi IN, paghi OUT. Minimizza cross-region. Usa VPC Endpoints e CloudFront (PACKT Cap.15)
- **Direct Connect**: costoso e lento da implementare — escludilo se la domanda chiede low-cost o veloce (PACKT Cap.15)
- **Read replica on-demand**: accendila solo quando serve (Kimiko — payroll ogni 2 settimane)
- **Monitora i bucket S3**: utenti che caricano dati non necessari aumentano i costi (Kimiko)
- **Cost Explorer**: analisi costi, raccomandazioni, 24h per attivarsi (Kimiko)
- **Budgets**: alert quando i costi si avvicinano alla soglia (PACKT Cap.15)
- **Auto Scaling**: scala giù quando non serve = risparmio automatico (PACKT Cap.15)
