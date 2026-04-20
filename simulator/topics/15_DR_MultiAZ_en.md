# Disaster Recovery, Multi-AZ and Fault Tolerance

> Sources: PACKT Ch.13 (p.519-543), KIMIKO Resilient Design (p.85-91), DOJO (p.45)

---

## Glossary: the concepts you will encounter in this document

- **High Availability (HA)** — the system remains available even when a component fails. Redundant copies ready to take over. There may be a brief downtime during failover. Like having a backup generator: if the power goes out, the generator starts and the lights come back on in a few seconds.

- **Fault Tolerance** — the system continues to operate WITHOUT interruption even during component degradation. Zero perceived downtime. Like a plane with 4 engines: if one shuts down, the other 3 keep flying without passengers noticing.

- **Disaster Recovery (DR)** — strategies for restoring systems after a major disaster (an entire AWS Region going down, a data center destroyed). It's not the same as HA: HA handles small daily failures, DR handles catastrophes.

- **RTO (Recovery Time Objective)** — how long you can afford to be offline after a disaster. If your RTO is 4 hours, you must be able to restore everything within 4 hours. Like the maximum time a restaurant can stay closed before losing too many customers.

- **RPO (Recovery Point Objective)** — how much data you can afford to lose. If your RPO is 1 hour, you must back up at least every hour. Like deciding how often to save your Word document: every 5 minutes (low RPO) or every hour (high RPO)?

- **Multi-AZ** — distributing resources across multiple Availability Zones in the same Region. If one AZ goes down (fire, blackout), resources in the other AZ continue to work. It's the basic way to achieve HA in AWS.

- **Multi-Region** — distributing resources across multiple AWS Regions (e.g., Europe + USA). Protects against disasters that hit an entire Region. More expensive than Multi-AZ but protects against worse scenarios.

- **Pilot Light** — a DR strategy where you keep only the core components running (e.g., the database with a replica) in a second Region. The rest is started only when needed. Like keeping the gas pilot light on: it doesn't heat the house, but you can turn on the heating quickly.

- **Warm Standby** — a DR strategy where you keep a reduced but functional environment in a second Region, always in sync. When needed, you scale it to full size. Like keeping a small branch office always open: in an emergency, you move all the staff there.

---

## AWS Global Infrastructure — Details (from Dojo)

Dojo provides important details about the physical structure:

### Regions
- Geographic areas with multiple AZs, connected with low-latency, high-throughput, and highly redundant networking
- Each Region is completely independent

### Availability Zones
- Consist of **one or more discrete data centers**, each with redundant power, networking, and connectivity
- Represented by a region code + letter (e.g., `us-east-1a`)
- *"Un'AZ non è un singolo data center — può essere un gruppo di data center nella stessa città"* (Dojo)

### Local Zones and Wavelength Zones
- **Local Zone**: single data center to complement an existing Region, for low latency near large populations
- **Wavelength Zone**: for 5G ultra-low latency applications

### Edge Locations
- Sites used by CloudFront to cache content
- Also used by Lambda@Edge to run code at the edge

### Pricing per Region (from Dojo)

Dojo notes: *"Ci sono tre driver fondamentali di costo con AWS: Compute, Storage, e Outbound data transfer."*

- **Reserved Instances**: savings up to 75% compared to On-Demand. The more you pay upfront, the more you save
- **All Upfront**: maximum discount
- **Partial Upfront**: partial payment + discounted hourly rate
- **No Upfront**: no upfront payment, discounted hourly rate
- **Volume discounts** for services like S3
- **Free Tier**: 12 months of limited free usage for new accounts

---

## Designing Highly Available Architectures (from PACKT Ch.13)

PACKT introduces: *"Werner Vogels è famoso per la frase 'Everything fails, all the time' — sono buone parole da seguire, specialmente quando si gestiscono applicazioni e infrastrutture mission-critical."*

### Evolution of a 3-Tier Architecture (from PACKT Ch.13)

PACKT shows step by step how to transform a standard architecture into an HA one:

**Step 1 — Problem**: all infrastructure in a single AZ. If the AZ goes down, the application stops working.

**Step 2 — Multi-AZ**: distribute infrastructure across 2 AZs. If one AZ breaks, the application continues in the other.

**Step 3 — Load Balancer**: with infrastructure in 2 AZs, you need an LB to distribute traffic and not send it to unhealthy instances. If one AZ goes down, the LB automatically sends all traffic to the other AZ.

**Step 4 — RDS Managed**: replace the database on EC2 with RDS. Configure Multi-AZ to have a secondary DB. In case of failure of the primary DB's AZ, RDS automatically fails over to the secondary.

**Step 5 — RDS Proxy**: for high-performance applications that open many connections. *"RDS Proxy fa pool delle connessioni, riducendo il carico sui database server e offloadando l'autenticazione al proxy. Ha un costo aggiuntivo — fai attenzione a frasi nell'esame che parlano di 'soluzione più cost-effective'."*

> **Exam tip (PACKT Ch.13)**: *"Una domanda comune nell'esame riguarda quanti server devono essere deployati su quante AZ per soddisfare un SLA di performance. Assicurati che la risposta selezionata abbia sempre almeno un server attivo in qualsiasi scenario di failure."*

---

## RPO and RTO (from PACKT Ch.13 and Dojo)

PACKT defines:
- **RPO** (Recovery Point Objective): *"La massima quantità accettabile di perdita dati misurata in tempo. Se l'RPO è 4 ore, la strategia di backup deve garantire il recupero dei dati fino alle ultime 4 ore prima del disastro."*
- **RTO** (Recovery Time Objective): *"La massima quantità accettabile di tempo che un sistema può essere offline dopo un disastro."*

---

## The 4 Disaster Recovery Strategies

### Comparison (from PACKT Ch.13 and Dojo)

| Strategy | How it works | RTO | RPO | Cost |
|---|---|---|---|---|
| **Backup & Restore** | Frequent backups in a safe location, restore when needed (PACKT). *"Di solito l'opzione più economica ma con il RTO più lungo"* (Dojo) | Highest (hours) | Depends on backup frequency | Lowest |
| **Pilot Light** | Core components always running (e.g., DB with replica). *"Recovery più veloce perché i pezzi core sono già in esecuzione e aggiornati"* (Dojo) | Medium | Minimal for core | Low-Medium |
| **Warm Standby** | Reduced but functional environment, always in sync. *"Devi solo fare riconfigurazione minima per ristabilire l'ambiente"* (Dojo). PACKT shows: only half the infrastructure is running in the second Region | Low (minutes) | Minimal | Medium-High |
| **Active-Active (Multi-Site)** | Full copy in active-active configuration. *"Tutto quello che devi fare è redirigere il traffico"* (Dojo). PACKT notes: *"La strategia DR più costosa. Risulta in RTO e RPO quasi zero perché nulla deve scalare e non serve ripristinare dati"* | Near zero | Near zero | Highest |

> **Exam tip (PACKT Ch.13)**: *"La maggior parte delle volte, la strategia DR è usata per impostare il contesto della domanda, ma a volte le strategie formano la risposta e devi selezionare l'opzione migliore."*

> **Dojo Note**: *"AWS promuove AWS Elastic Disaster Recovery come soluzione preferita per workload DR."*

---

## Resilient Design Scenario: Widget Makers (from Kimiko)

Kimiko returns to the Widget Makers scenario to apply resilience principles:

### Key Principles (from Kimiko)

*"Con il resilient design, parliamo di un design che fornisce affidabilità. Un punto chiave è che NON può richiedere interazione dagli amministratori. Deve essere implementato con automazione: recovery automatico, scaling automatico, backup automatici. Se queste cose devono essere fatte manualmente, non è resiliente come sarebbe se fosse tutto automatico."*

### Recommendations per System (from Kimiko)

| System | Recommendation |
|---|---|
| **Order Processing** | SQL Server → **RDS managed instance + Multi-AZ**. Don't launch EC2 with Windows and SQL Server — let AWS manage the database |
| **Inventory Management** | MySQL → **RDS managed instance + Multi-AZ**. No clustering needed for the number of users |
| **Payroll** | SQL Server → **RDS + Multi-AZ + Read Replica**. *"Il payroll processing può essere intensivo. Facciamo molte letture durante quella finestra di tempo. Con una read replica, otteniamo performance senza impattare il database principale read-write"* |
| **User Data** | Shared files → **S3 buckets** (intrinsic resilience). *"Dentro AWS non c'è modo di mappare una drive letter a un bucket S3 di default. Serve un tool di terze parti"* |
| **Website** | WordPress → **2 instances behind Elastic Load Balancer**. *"Se uno dei server fallisce, l'altro è ancora lì"* |

> **Insight from Kimiko**: *"La chiave di questo piano di resilienza sono: Multi-AZ per i database, S3 per il file storage (resilienza intrinseca), e ELB per il website. Potrebbe dare loro resilienza migliore di quella che hanno oggi on-premises."*

---

## Scaling and Loose Coupling (from PACKT Ch.13)

### Horizontal Scaling with Auto Scaling

PACKT shows how to add ASGs to the web and app tiers: *"Con auto-scaling, le istanze possono aumentare o diminuire per accomodare le fluttuazioni di traffico real-time. Ricorda di impostare un upper bound per l'azione di scaling — questo minimizzerà costi inaspettati."*

### Database Scaling

- **Read replicas**: horizontal scaling for read operations. *"Tipicamente ci sono più operazioni di lettura che di scrittura"*
- **Vertical scaling**: for increased write operations — increase the instance size
- **ElastiCache**: for repetitive queries, *"può rendere le operazioni di lettura fino a 80x più veloci e ridurre i costi riducendo le query al database"*

### Caching with CloudFront

PACKT notes: *"Usando CloudFront, puoi salvare contenuti statici in S3 e usare CloudFront per cacharli nelle edge location nel mondo. Questo è un argomento comune per l'esame SAA-C03."*

### Serverless Scalability (from PACKT Ch.13)

PACKT warns: *"È facile dimenticare che devi progettare workload serverless per la scalabilità perché i servizi stessi sono fully managed."*

Key concepts:
- **Stateless microservices**: don't maintain state between requests. Each request is independent. Simplifies scaling and resilience
- **Stateful microservices**: when necessary, require careful design to avoid becoming bottlenecks or single points of failure
- **API Gateway caching**: caches API responses — if the same request comes again, the response comes from cache

---

## Decoupling Services — Which One to Choose (from PACKT Ch.13)

PACKT provides the key rule:

> *"Ricorda: SQS è comunicazione one-to-one, SNS è comunicazione one-to-many, EventBridge è comunicazione many-to-many. Ricordare questa distinzione ti porterà spesso alla risposta corretta."*

> *"Quando hai diverse Lambda functions da coordinare, considera Step Functions piuttosto che disaccoppiare con SQS. Questo ti dà più controllo sul processo di chaining delle Lambda."*

---

## Typical Exam Scenarios

### Scenario 1: HA architecture for a web app
**Question**: How to make a 3-tier web application highly available?

**Answer**: Multi-AZ (at least 2 AZs), ALB in front of the web tier, RDS Multi-AZ for the database, Auto Scaling for web and app tiers (PACKT Ch.13).

### Scenario 2: DR with minimum cost
**Question**: The company wants DR with the lowest possible cost. An RPO of 24 hours is acceptable.

**Answer**: **Backup & Restore** — daily backups, restore when needed (PACKT, Dojo).

### Scenario 3: DR with near-zero RTO
**Question**: The mission-critical application cannot have downtime. Budget is not an issue.

**Answer**: **Active-Active (Multi-Site)** — full copy in two Regions, near-zero RTO and RPO (PACKT, Dojo).

### Scenario 4: Read-heavy database with resilience
**Question**: The database is overloaded with reads and must be resilient.

**Answer**: **Read Replicas** + **Multi-AZ** (Kimiko Widget Makers scenario: read replica for payroll + Multi-AZ for resilience).

### Scenario 5: How many servers for HA?
**Question**: The SLA requires the application to handle 4 requests/second. Each server handles 2 req/sec. How many servers and AZs are needed?

**Answer**: At least **4 servers across 2 AZs** (2 per AZ) — so if one AZ goes down, the remaining 2 instances still handle 4 req/sec (PACKT Ch.13 tip).

---

## Quick Review for the Exam

- **Multi-AZ**: distribute across at least 2 AZs for HA. If one AZ goes down, the other continues (PACKT)
- **LB + Multi-AZ**: the LB sends traffic only to healthy instances, automatic failover (PACKT)
- **RDS Multi-AZ**: automatic failover to the secondary DB (PACKT)
- **RDS Proxy**: connection pooling, reduces DB load, additional cost (PACKT)
- **RPO**: how much data you can lose. **RTO**: how long you can be down (PACKT, Dojo)
- **DR strategies**: Backup&Restore (cheapest, longest RTO) → Pilot Light → Warm Standby → Active-Active (most expensive, near-zero RTO/RPO) (PACKT, Dojo)
- **Resilience MUST be automatic**: recovery, scaling, backup — all automatic (Kimiko)
- **Widget Makers**: Multi-AZ for DB, S3 for files (intrinsic resilience), ELB for website (Kimiko)
- **Read replicas**: read scaling. **Vertical scaling**: write scaling. **ElastiCache**: repetitive queries up to 80x faster (PACKT)
- **CloudFront**: caches static content at edge locations — common exam topic (PACKT)
- **SQS = 1:1, SNS = 1:many, EventBridge = many:many** (PACKT Ch.13)
- **Step Functions**: to coordinate multiple Lambda, more control than SQS (PACKT Ch.13)
- **Stateless > Stateful** for microservices: simplifies scaling and resilience (PACKT Ch.13)
