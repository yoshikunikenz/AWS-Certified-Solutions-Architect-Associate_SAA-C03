# Cost Optimization - Pricing, Storage, Compute, Database, Network

> Sources: PACKT Ch.15 (p.588-605), KIMIKO Cost Optimization (p.109-117) + Cost Explorer (p.47-49) + Billing (p.303-304), DOJO (p.263, p.285)

---

## Glossary: the concepts you will encounter in this document

- **On-Demand** — the base AWS pricing model. You pay for what you use, when you use it, with no commitments. Like taking a taxi: you pay for the ride and that's it. No discounts, but maximum flexibility.

- **Reserved Instance (RI)** — you commit to using a certain instance type for 1 or 3 years in exchange for a discount of up to 72%. Like an annual public transit pass: you pay less per ride but you're locked in.

- **Savings Plan** — like RIs but more flexible. You commit to spending a certain amount per hour, and the discount automatically applies to EC2, Lambda, Fargate, SageMaker. Like an "all-inclusive" pass that covers bus, metro, and tram.

- **Spot Instance** — unused EC2 capacity sold at a discounted price (up to -90%). AWS can reclaim it with 2 minutes notice. Like a last-minute airline ticket: costs very little but you might get "bumped".

- **Cost Explorer** — the tool for analyzing your AWS costs over time. Shows graphs, trends, and recommendations for saving. Like your car's dashboard showing fuel consumption.

- **AWS Budgets** — lets you set budgets and receive alerts when costs approach the threshold. Like setting a spending limit on your credit card.

- **Lifecycle Policy** — an automatic rule that moves data between storage classes over time (e.g., from S3 Standard to Glacier after 90 days). Optimizes costs automatically without manual intervention.

- **Right-Sizing** — choosing the right type and size of resources for the workload. Not too big (you waste money), not too small (poor performance). You can always change later. Like choosing the right shoe size: you don't buy size 45 "just in case" if you wear 42.

- **Data Transfer** — the cost of moving data in and out of AWS. General rule: **you don't pay for data coming INTO AWS, you pay for data going OUT**. Like a parking lot: entering is free, exiting costs money.

---

## Cost Optimization Principles (from Kimiko)

Kimiko analyzes the AWS Cost Optimization Pillar document (35 pages) and extracts the principles:

### 1. Adopt a Consumption Model
*"Paga solo per le risorse di computing che consumi. Se sei un ufficio con un solo turno, puoi disabilitare diversi server durante le ore serali e riportarli online solo quando gli utenti ne hanno bisogno."*

Kimiko distinguishes:
- **24/7 services**: those for customers, which might be needed at all times
- **Business-hours services**: those for employees, which you can turn off in the evening and turn back on in the morning

### 2. Measure Overall Efficiency
*"Monitora il valore di business che ogni sistema produce rispetto al suo costo. Se un dipartimento consuma il 30% dei costi AWS ma produce solo il 5% del valore di business, rivaluta."*

### 3. Stop Spending Money on Data Center Operations
*"AWS fa rack & stack per te. Non devi spendere per costruire un data center per testare una nuova soluzione."*

### 4. Analyze and Attribute Expenditure
*"Guarda da dove vengono i costi in AWS e assicurati di capire quale dipartimento li sta consumando."*

### 5. Use Managed Services to Reduce Cost of Ownership
*"Quando usi servizi gestiti come RDS invece di un database su EC2, non servono tante ore-uomo per gestire il database."*

### The 4 Sub-Pillars (from Kimiko)

1. **Use cost-effective resources** — *"A volte è meno costoso usare un'istanza più potente che costa di più all'ora, perché finisce il lavoro più velocemente"*
2. **Match supply with demand** — Auto Scaling to have the right number of servers
3. **Expenditure awareness** — use billing alerts to know when you exceed a threshold
4. **Optimize over time** — *"Man mano che implementi più soluzioni AWS, impari di più su come fare il lavoro con meno spese possibili. Ma ci vuole tempo ed esperienza"*

---

## Cost-Optimized Storage (from PACKT Ch.15)

### Storage Service Pricing

| Service | How you pay | Notes |
|---|---|---|
| **S3** | Storage + requests (PUT/COPY/POST/LIST) + data transfer out | The more you store, the less it costs per GB. You don't pay for transfer IN |
| **S3 Glacier** | Storage (very low) + retrieval fees | Retrieval fees depend on class and speed |
| **EFS** | Storage + provisioned throughput (burst or provisioned) + data transfer | Two tiers: Standard and IA |
| **EBS** | Volume type + storage + throughput + provisioned IOPS + snapshots | gp3 often cheaper than gp2 because IOPS/throughput are configurable separately |

### Storage Optimization Strategies (from PACKT Ch.15)

**Batch vs Individual Uploads**: AWS charges per PUT/COPY/POST/LIST request. For millions of objects, use **S3 Batch Operations** ($0.25/job + $1/million operations).

**Storage Tiering and Lifecycle**: *"Nella domanda d'esame sulle storage class S3, identifica il caso d'uso dei dati e se ci sono requisiti di disponibilità o costo. La domanda spesso dice che i dati servono regolarmente per X mesi, dopo di che servono ancora ma raramente. In questo caso, tieni i dati in Standard per X mesi, poi spostali in Glacier."*

**Intelligent-Tiering**: automatically moves data between Standard and IA based on access patterns.

**EBS Snapshots**: incremental after the first full snapshot. Use **Amazon Data Lifecycle Manager** to manage retention.

> **Exam tip (PACKT Ch.15)**: *"gp3 è più performante di gp2 — ricordare questo dovrebbe essere sufficiente per selezionare la risposta corretta se devi scegliere tra i due."*

---

## Cost-Optimized Compute (from PACKT Ch.15)

### Pricing Models — When to Use What

| Model | Discount | When to use (PACKT Ch.15) |
|---|---|---|
| **On-Demand** | 0% | Unpredictable workloads, test, dev |
| **Reserved Instances** | Up to 72% | Consistent and known workloads, 1-3 year commitment |
| **Savings Plans** | Up to 72% | Like RI but also includes **Fargate, Lambda, SageMaker** |
| **Spot Instances** | Up to 90% | Spiky, interruptible workloads |
| **Dedicated Hosts** | Variable | Dedicated hardware required, BYOL |

> **Exam tip (PACKT Ch.15)**: *"Se la scelta è tra Savings Plans e Reserved Instances, cerca se la domanda menziona Fargate o Lambda. Solo i Savings Plans coprono compute diverso dalle istanze."*

> **Exam tip (PACKT Ch.15)**: *"Se la domanda dice che il cliente ha licenze che vuole usare, la risposta è Dedicated Hosts."*

### Choosing the Right Compute Service (from PACKT Ch.15)

| Workload | Service | Why |
|---|---|---|
| **Steady, known** | EC2 | Predictable, optimizable with RI/SP |
| **Unknown, spiky** | Lambda | Pay only when it runs, perfect for intermittent workloads |
| **Variable, longer-running** | Fargate | Per-second billing, perfect for intermittent workloads that Lambda can't handle (15 min timeout) |

> **Exam tip (PACKT Ch.15)**: *"La cosa chiave da cercare nella domanda è se il workload è consistente e steady o se è intermittente."*

### Optimizing Utilization (from PACKT Ch.15)

- **Auto Scaling** for EC2 and Fargate/ECS — scale up when needed, scale down when not
- **Turn off instances** when not in use — EC2 charges only when instances are running
- **Schedule shutdown** with a Lambda function for instances not needed after hours

### Regional Optimization (from PACKT Ch.15)

*"Region diverse hanno prezzi diversi. Minimizza il data transfer inter-region. Usa CloudFront per salvare contenuti statici all'edge."*

---

## Cost-Optimized Database (from PACKT Ch.15)

### Choosing the Right Database

| Service | Cost optimization (PACKT Ch.15) |
|---|---|
| **RDS** | Select appropriate instance type (not too big — you can always increase). Use RI and Savings Plans |
| **Aurora** | Leverage autoscaling (adds/removes read replicas automatically). Aurora Serverless for spiky workloads |
| **DynamoDB** | Provision adequate capacity units (not more). Adjustable afterwards |

### Savings Strategies (from PACKT Ch.15)

- **Read replicas**: offload read-heavy workload from the primary → you can use a less expensive primary instance
- **Serverless databases**: pay for actual usage, not fixed capacity. Scales automatically
- **Caching** (ElastiCache): offload reads from the DB → you can use a smaller, less expensive DB instance
- **Backup**: use S3 lifecycle policies to move backups to cold storage. Watch for RPO/RTO in the exam question

### Widget Makers — Cost Optimization (from Kimiko)

Kimiko applies the principles to the Widget Makers scenario:

| System | Cost recommendation |
|---|---|
| **Order Processing** | Use managed database (RDS) → fewer man-hours of management |
| **Inventory Management** | Same thing — managed database |
| **Payroll** | Managed database + **read replica active only when needed**. *"Puoi portare online la read replica durante il downtime la sera prima del payroll. Così paghi solo poche ore ogni due settimane"* |
| **User Data** | **Monitor** what users put in S3 buckets. *"Dato che paghiamo per storage basato sulla dimensione, assicuriamoci di non mettere informazioni non necessarie"* |
| **Website** | **Right class, nothing more** (you can always upgrade). Monitor anomalous access — *"Se qualcuno trova una vulnerabilità WordPress per caricare file pirata, i costi di bandwidth esplodono"* |

> **Brilliant insight from Kimiko**: the payroll read replica is turned on the evening before processing, replicates data overnight, payroll runs in the morning, then it's turned off. You pay a few hours every 2 weeks instead of 24/7.

---

## Cost-Optimized Network (from PACKT Ch.15)

### General Data Transfer Rule (from PACKT Ch.15)

*"La regola generale è: non paghi per il data transfer IN AWS ma paghi per il data transfer OUT di AWS. Non è sempre così, ma è una buona linea guida."*

### Strategies (from PACKT Ch.15)

- **Direct Connect**: the most expensive, takes months to set up. *"Puoi di solito escludere Direct Connect cercando nella domanda menzioni di low-cost o implementazione rapida"*
- **VPN**: cost-effective option for secure on-premises ↔ cloud connections
- **Transit Gateway**: simplifies management and reduces data transfer costs by centralizing routing
- **PrivateLink/VPC Endpoints**: access to internal AWS services without internet egress or NAT gateway costs
- **Minimize cross-region traffic**: you pay for data transfer out of a region
- **Global Accelerator**: optimizes routing and reduces data transfer costs for global apps
- **CloudFront**: saves static content at the edge to reduce data transfer

> **Exam tip (PACKT Ch.15)**: *"L'area chiave da ricordare è controllare i costi di data transfer. Sono tipicamente i costi più grandi e quelli da evitare."*

---

## AWS Cost Management Tools (from PACKT Ch.15 and Kimiko)

### AWS Cost Explorer (from Kimiko)

Kimiko shows Cost Explorer in the console: *"La prima volta che vieni qui, non sarà abilitato. Quando lo abiliti, non vedrai nulla per 24 ore. Ma dopo, puoi vedere dati storici e dati correnti."*

Features shown by Kimiko:
- **Cost overview** with time-series graphs
- **Savings Plans**: you can purchase savings plans
- **Budgets**: create and manage budgets for financial planning
- **Recommendations**: *"L'unica raccomandazione che ho è per EC2 — posso risparmiare $87 annualmente passando a un t2.nano reserved instance"*

### Tools (from PACKT Ch.15)

| Tool | What it does |
|---|---|
| **Cost Explorer** | Detailed cost and usage analysis. Custom reports and alerts |
| **AWS Budgets** | Custom budgets for specific services. Alerts when costs approach the threshold |
| **Cost and Usage Reports (CUR)** | Detailed line-item data on usage and costs. To identify optimization opportunities |
| **Tagging Strategy** | Categorize and track resources and associated costs by department/project |

> **Exam tip (PACKT Ch.15)**: *"Assicurati di capire le limitazioni di ogni strumento perché potresti ricevere una domanda su quale modo usare per monitorare e rimediare i costi."*

### Billing Alarms (from Kimiko)

Kimiko shows how to configure billing alarms: *"Puoi impostare alert di billing così sai quando hai superato una certa soglia nelle tue spese."*

---

## Typical Exam Scenarios

### Scenario 1: Steady-state workload for 3 years with Lambda
**Question**: An application uses EC2 and Lambda with predictable load for 3 years. How to save?

**Answer**: **Savings Plans** (not RI) — because they cover both EC2 and Lambda (PACKT Ch.15).

### Scenario 2: Data accessed for 3 months then archived
**Question**: Data is accessed frequently for 3 months, then rarely for 7 years.

**Answer**: S3 Standard for 3 months → **lifecycle policy** → Glacier after 90 days → Deep Archive after 1 year → Delete after 7 years (PACKT Ch.15).

### Scenario 3: Database used only during payroll
**Question**: The database read replica is needed only 2 days per month.

**Answer**: **Turn on the read replica only when needed** — the evening before payroll, turn it off after (Kimiko Widget Makers scenario).

### Scenario 4: Reduce data transfer costs
**Question**: Data transfer costs are too high for a global application.

**Answer**: **CloudFront** for static content at the edge + **VPC Endpoints** for access to AWS services without internet egress (PACKT Ch.15).

### Scenario 5: Choose between gp2 and gp3
**Question**: An EBS volume with specific IOPS but minimal storage is needed.

**Answer**: **gp3** — IOPS and throughput configurable separately from storage, often cheaper than gp2 (PACKT Ch.15).

---

## Quick Review for the Exam

- **Consumption model**: pay only for what you use, turn off what you don't need (Kimiko)
- **Managed services**: fewer man-hours = lower operational costs (Kimiko)
- **Right-sizing**: don't over-provision, you can always increase later (PACKT, Kimiko)
- **Sometimes more powerful = less expensive** because it finishes faster (Kimiko)
- **Savings Plans > RI** when coverage for Lambda/Fargate/SageMaker is needed (PACKT Ch.15)
- **Spot**: up to -90%, for interruptible workloads. **RI/SP**: up to -72%, for steady workloads (PACKT Ch.15)
- **Dedicated Hosts**: when the customer has BYOL licenses (PACKT Ch.15)
- **S3 lifecycle policies**: Standard → IA → Glacier → Deep Archive → Delete (PACKT Ch.15)
- **gp3 > gp2**: more flexible and often cheaper (PACKT Ch.15)
- **Data transfer**: you don't pay IN, you pay OUT. Minimize cross-region. Use VPC Endpoints and CloudFront (PACKT Ch.15)
- **Direct Connect**: expensive and slow to implement — exclude it if the question asks for low-cost or fast (PACKT Ch.15)
- **On-demand read replica**: turn it on only when needed (Kimiko — payroll every 2 weeks)
- **Monitor S3 buckets**: users uploading unnecessary data increases costs (Kimiko)
- **Cost Explorer**: cost analysis, recommendations, 24h to activate (Kimiko)
- **Budgets**: alerts when costs approach the threshold (PACKT Ch.15)
- **Auto Scaling**: scale down when not needed = automatic savings (PACKT Ch.15)
