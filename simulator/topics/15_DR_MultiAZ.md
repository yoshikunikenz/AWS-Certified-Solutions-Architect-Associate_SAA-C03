# Disaster Recovery, Multi-AZ e Fault Tolerance

> Fonti: PACKT Cap.13 (p.519-543), KIMIKO Resilient Design (p.85-91), DOJO (p.45)

---

## Glossario: i concetti che incontrerai in questo documento

- **High Availability (HA)** — il sistema rimane disponibile anche quando un componente fallisce. Copie ridondanti pronte a subentrare. Può esserci un breve downtime durante il failover. Come avere un generatore di backup: se manca la corrente, il generatore parte e le luci si riaccendono in pochi secondi.

- **Fault Tolerance** — il sistema continua a funzionare SENZA interruzione anche durante il degrado di un componente. Zero downtime percepito. Come un aereo con 4 motori: se uno si spegne, gli altri 3 continuano a volare senza che i passeggeri se ne accorgano.

- **Disaster Recovery (DR)** — le strategie per ripristinare i sistemi dopo un disastro grave (un'intera Region AWS che va giù, un data center distrutto). Non è la stessa cosa di HA: HA gestisce i piccoli guasti quotidiani, DR gestisce le catastrofi.

- **RTO (Recovery Time Objective)** — quanto tempo puoi permetterti di stare offline dopo un disastro. Se il tuo RTO è 4 ore, devi essere in grado di ripristinare tutto entro 4 ore. Come il tempo massimo che un ristorante può restare chiuso prima di perdere troppi clienti.

- **RPO (Recovery Point Objective)** — quanti dati puoi permetterti di perdere. Se il tuo RPO è 1 ora, devi fare backup almeno ogni ora. Come decidere quanto spesso salvare il tuo documento Word: ogni 5 minuti (RPO basso) o ogni ora (RPO alto)?

- **Multi-AZ** — distribuire le risorse su più Availability Zone nella stessa Region. Se un'AZ va giù (incendio, blackout), le risorse nell'altra AZ continuano a funzionare. È il modo base per ottenere HA in AWS.

- **Multi-Region** — distribuire le risorse su più Region AWS (es. Europa + USA). Protegge da disastri che colpiscono un'intera Region. Più costoso di Multi-AZ ma protegge da scenari peggiori.

- **Pilot Light** — una strategia DR dove tieni accesi solo i componenti core (es. il database con replica) in una seconda Region. Il resto lo avvii solo quando serve. Come tenere il pilota del gas acceso: non scalda la casa, ma puoi accendere il riscaldamento velocemente.

- **Warm Standby** — una strategia DR dove tieni un ambiente ridotto ma funzionante in una seconda Region, sempre in sync. Quando serve, lo scali alla dimensione piena. Come tenere una filiale piccola sempre aperta: in emergenza, ci sposti tutto il personale.

---

## AWS Global Infrastructure — Dettagli (dal Dojo)

Il Dojo fornisce dettagli importanti sulla struttura fisica:

### Regions
- Aree geografiche con multiple AZ, connesse con networking a bassa latenza, alto throughput e altamente ridondante
- Ogni Region è completamente indipendente

### Availability Zones
- Consistono di **uno o più data center discreti**, ciascuno con alimentazione, networking e connettività ridondanti
- Rappresentate da un codice region + lettera (es. `us-east-1a`)
- *"Un'AZ non è un singolo data center — può essere un gruppo di data center nella stessa città"* (Dojo)

### Local Zones e Wavelength Zones
- **Local Zone**: singolo data center per complementare una Region esistente, per bassa latenza vicino a grandi popolazioni
- **Wavelength Zone**: per applicazioni 5G a ultra-bassa latenza

### Edge Locations
- Siti usati da CloudFront per cachare contenuti
- Anche usati da Lambda@Edge per eseguire codice all'edge

### Pricing per Region (dal Dojo)

Il Dojo nota: *"Ci sono tre driver fondamentali di costo con AWS: Compute, Storage, e Outbound data transfer."*

- **Reserved Instances**: risparmio fino al 75% rispetto a On-Demand. Più paghi upfront, più risparmi
- **All Upfront**: sconto massimo
- **Partial Upfront**: pagamento parziale + tariffa oraria scontata
- **No Upfront**: nessun pagamento anticipato, tariffa oraria scontata
- **Volume discounts** per servizi come S3
- **Free Tier**: 12 mesi di uso limitato gratuito per nuovi account

---

## Progettare Architetture Highly Available (dal PACKT Cap.13)

Il PACKT introduce: *"Werner Vogels è famoso per la frase 'Everything fails, all the time' — sono buone parole da seguire, specialmente quando si gestiscono applicazioni e infrastrutture mission-critical."*

### Evoluzione di un'Architettura a 3 Livelli (dal PACKT Cap.13)

Il PACKT mostra passo passo come trasformare un'architettura standard in una HA:

**Step 1 — Problema**: tutta l'infrastruttura in una singola AZ. Se l'AZ va giù, l'applicazione smette di funzionare.

**Step 2 — Multi-AZ**: distribuisci l'infrastruttura su 2 AZ. Se una AZ si rompe, l'applicazione continua nell'altra.

**Step 3 — Load Balancer**: con infrastruttura in 2 AZ, serve un LB per distribuire il traffico e non inviarlo a istanze unhealthy. Se una AZ va giù, il LB invia automaticamente tutto il traffico all'altra AZ.

**Step 4 — RDS Managed**: sostituisci il database su EC2 con RDS. Configura Multi-AZ per avere un DB secondario. In caso di failure dell'AZ del DB primario, RDS fa failover automatico al secondario.

**Step 5 — RDS Proxy**: per applicazioni ad alte performance che aprono molte connessioni. *"RDS Proxy fa pool delle connessioni, riducendo il carico sui database server e offloadando l'autenticazione al proxy. Ha un costo aggiuntivo — fai attenzione a frasi nell'esame che parlano di 'soluzione più cost-effective'."*

> **Tip esame (PACKT Cap.13)**: *"Una domanda comune nell'esame riguarda quanti server devono essere deployati su quante AZ per soddisfare un SLA di performance. Assicurati che la risposta selezionata abbia sempre almeno un server attivo in qualsiasi scenario di failure."*

---

## RPO e RTO (dal PACKT Cap.13 e Dojo)

Il PACKT definisce:
- **RPO** (Recovery Point Objective): *"La massima quantità accettabile di perdita dati misurata in tempo. Se l'RPO è 4 ore, la strategia di backup deve garantire il recupero dei dati fino alle ultime 4 ore prima del disastro."*
- **RTO** (Recovery Time Objective): *"La massima quantità accettabile di tempo che un sistema può essere offline dopo un disastro."*

---

## Le 4 Strategie di Disaster Recovery

### Confronto (dal PACKT Cap.13 e Dojo)

| Strategia | Come funziona | RTO | RPO | Costo |
|---|---|---|---|---|
| **Backup & Restore** | Backup frequenti in location sicura, ripristino al bisogno (PACKT). *"Di solito l'opzione più economica ma con il RTO più lungo"* (Dojo) | Più alto (ore) | Dipende dalla frequenza backup | Più basso |
| **Pilot Light** | Componenti core sempre attivi (es. DB con replica). *"Recovery più veloce perché i pezzi core sono già in esecuzione e aggiornati"* (Dojo) | Medio | Minimo per i core | Basso-Medio |
| **Warm Standby** | Ambiente ridotto ma funzionante, sempre in sync. *"Devi solo fare riconfigurazione minima per ristabilire l'ambiente"* (Dojo). Il PACKT mostra: solo metà dell'infrastruttura è in esecuzione nella seconda Region | Basso (minuti) | Minimo | Medio-Alto |
| **Active-Active (Multi-Site)** | Copia completa in configurazione active-active. *"Tutto quello che devi fare è redirigere il traffico"* (Dojo). Il PACKT nota: *"La strategia DR più costosa. Risulta in RTO e RPO quasi zero perché nulla deve scalare e non serve ripristinare dati"* | Quasi zero | Quasi zero | Più alto |

> **Tip esame (PACKT Cap.13)**: *"La maggior parte delle volte, la strategia DR è usata per impostare il contesto della domanda, ma a volte le strategie formano la risposta e devi selezionare l'opzione migliore."*

> **Nota Dojo**: *"AWS promuove AWS Elastic Disaster Recovery come soluzione preferita per workload DR."*

---

## Resilient Design Scenario: Widget Makers (da Kimiko)

Kimiko torna allo scenario Widget Makers per applicare i principi di resilienza:

### Principi Chiave (da Kimiko)

*"Con il resilient design, parliamo di un design che fornisce affidabilità. Un punto chiave è che NON può richiedere interazione dagli amministratori. Deve essere implementato con automazione: recovery automatico, scaling automatico, backup automatici. Se queste cose devono essere fatte manualmente, non è resiliente come sarebbe se fosse tutto automatico."*

### Raccomandazioni per Sistema (da Kimiko)

| Sistema | Raccomandazione |
|---|---|
| **Order Processing** | SQL Server → **RDS managed instance + Multi-AZ**. Non lanciare EC2 con Windows e SQL Server — lascia che AWS gestisca il database |
| **Inventory Management** | MySQL → **RDS managed instance + Multi-AZ**. No clustering necessario per il numero di utenti |
| **Payroll** | SQL Server → **RDS + Multi-AZ + Read Replica**. *"Il payroll processing può essere intensivo. Facciamo molte letture durante quella finestra di tempo. Con una read replica, otteniamo performance senza impattare il database principale read-write"* |
| **User Data** | File condivisi → **S3 buckets** (resilienza intrinseca). *"Dentro AWS non c'è modo di mappare una drive letter a un bucket S3 di default. Serve un tool di terze parti"* |
| **Website** | WordPress → **2 istanze dietro Elastic Load Balancer**. *"Se uno dei server fallisce, l'altro è ancora lì"* |

> **Insight da Kimiko**: *"La chiave di questo piano di resilienza sono: Multi-AZ per i database, S3 per il file storage (resilienza intrinseca), e ELB per il website. Potrebbe dare loro resilienza migliore di quella che hanno oggi on-premises."*

---

## Scaling e Loose Coupling (dal PACKT Cap.13)

### Horizontal Scaling con Auto Scaling

Il PACKT mostra come aggiungere ASG ai tier web e app: *"Con auto-scaling, le istanze possono aumentare o diminuire per accomodare le fluttuazioni di traffico real-time. Ricorda di impostare un upper bound per l'azione di scaling — questo minimizzerà costi inaspettati."*

### Database Scaling

- **Read replicas**: scaling orizzontale per operazioni di lettura. *"Tipicamente ci sono più operazioni di lettura che di scrittura"*
- **Vertical scaling**: per aumento di operazioni di scrittura — aumenta la dimensione dell'istanza
- **ElastiCache**: per query ripetitive, *"può rendere le operazioni di lettura fino a 80x più veloci e ridurre i costi riducendo le query al database"*

### Caching con CloudFront

Il PACKT nota: *"Usando CloudFront, puoi salvare contenuti statici in S3 e usare CloudFront per cacharli nelle edge location nel mondo. Questo è un argomento comune per l'esame SAA-C03."*

### Serverless Scalability (dal PACKT Cap.13)

Il PACKT avverte: *"È facile dimenticare che devi progettare workload serverless per la scalabilità perché i servizi stessi sono fully managed."*

Concetti chiave:
- **Stateless microservices**: non mantengono stato tra richieste. Ogni richiesta è indipendente. Semplifica scaling e resilienza
- **Stateful microservices**: quando necessari, richiedono design attento per non diventare bottleneck o single point of failure
- **API Gateway caching**: cacha le risposte API — se la stessa richiesta arriva di nuovo, la risposta viene dalla cache

---

## Decoupling Services — Quale Scegliere (dal PACKT Cap.13)

Il PACKT fornisce la regola chiave:

> *"Ricorda: SQS è comunicazione one-to-one, SNS è comunicazione one-to-many, EventBridge è comunicazione many-to-many. Ricordare questa distinzione ti porterà spesso alla risposta corretta."*

> *"Quando hai diverse Lambda functions da coordinare, considera Step Functions piuttosto che disaccoppiare con SQS. Questo ti dà più controllo sul processo di chaining delle Lambda."*

---

## Scenari Tipici d'Esame

### Scenario 1: Architettura HA per web app
**Domanda**: Come rendere un'applicazione web a 3 livelli altamente disponibile?

**Risposta**: Multi-AZ (almeno 2 AZ), ALB davanti al web tier, RDS Multi-AZ per il database, Auto Scaling per web e app tier (PACKT Cap.13).

### Scenario 2: DR con costo minimo
**Domanda**: L'azienda vuole DR con il costo più basso possibile. RPO di 24 ore è accettabile.

**Risposta**: **Backup & Restore** — backup giornalieri, ripristino al bisogno (PACKT, Dojo).

### Scenario 3: DR con RTO quasi zero
**Domanda**: L'applicazione mission-critical non può avere downtime. Budget non è un problema.

**Risposta**: **Active-Active (Multi-Site)** — copia completa in due Region, RTO e RPO quasi zero (PACKT, Dojo).

### Scenario 4: Database read-heavy con resilienza
**Domanda**: Il database è sovraccarico di letture e deve essere resiliente.

**Risposta**: **Read Replicas** + **Multi-AZ** (Kimiko scenario Widget Makers: read replica per payroll + Multi-AZ per resilienza).

### Scenario 5: Quanti server per HA?
**Domanda**: L'SLA richiede che l'applicazione gestisca 4 richieste/secondo. Ogni server gestisce 2 req/sec. Quanti server e AZ servono?

**Risposta**: Almeno **4 server su 2 AZ** (2 per AZ) — così se una AZ va giù, le 2 istanze rimanenti gestiscono ancora 4 req/sec (PACKT Cap.13 tip).

---

## Riepilogo Veloce per l'Esame

- **Multi-AZ**: distribuisci su almeno 2 AZ per HA. Se una AZ va giù, l'altra continua (PACKT)
- **LB + Multi-AZ**: il LB invia traffico solo a istanze sane, failover automatico (PACKT)
- **RDS Multi-AZ**: failover automatico al DB secondario (PACKT)
- **RDS Proxy**: connection pooling, riduce carico DB, costo aggiuntivo (PACKT)
- **RPO**: quanti dati puoi perdere. **RTO**: quanto tempo puoi stare giù (PACKT, Dojo)
- **DR strategies**: Backup&Restore (cheapest, longest RTO) → Pilot Light → Warm Standby → Active-Active (most expensive, near-zero RTO/RPO) (PACKT, Dojo)
- **Resilienza DEVE essere automatica**: recovery, scaling, backup — tutto automatico (Kimiko)
- **Widget Makers**: Multi-AZ per DB, S3 per file (resilienza intrinseca), ELB per website (Kimiko)
- **Read replicas**: scaling letture. **Vertical scaling**: scaling scritture. **ElastiCache**: query ripetitive fino a 80x più veloci (PACKT)
- **CloudFront**: cacha contenuti statici nelle edge location — argomento comune nell'esame (PACKT)
- **SQS = 1:1, SNS = 1:many, EventBridge = many:many** (PACKT Cap.13)
- **Step Functions**: per coordinare multiple Lambda, più controllo di SQS (PACKT Cap.13)
- **Stateless > Stateful** per microservizi: semplifica scaling e resilienza (PACKT Cap.13)
