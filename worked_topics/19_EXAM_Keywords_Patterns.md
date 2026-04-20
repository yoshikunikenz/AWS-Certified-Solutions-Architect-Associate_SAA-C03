# 🎯 Keyword e Pattern Decisionali per l'Esame SAA-C03

> Questo documento raccoglie le "regole d'oro" sparse nei libri di preparazione: le keyword nelle domande d'esame che ti guidano verso la risposta corretta. Leggilo DOPO aver studiato i topic — è il tuo cheat sheet per riconoscere i pattern.

---

## REGOLA #1: Leggi la Domanda con Attenzione

Il PACKT lo ripete in ogni capitolo: *"Read the question carefully."* Le keyword nella domanda sono indizi deliberati. Ecco le più importanti.

---

## 🔑 KEYWORD → SERVIZIO

### Compute

| Se la domanda dice... | La risposta è probabilmente... | Perché |
|---|---|---|
| "cost-effective", "lowest cost", workload interrompibile | **Spot Instances** | Fino a -90%, ma possono essere reclamate |
| "steady-state", "predictable", impegno 1-3 anni | **Reserved Instances** o **Savings Plans** | Fino a -72% con commitment |
| "Lambda AND Fargate" nel workload | **Savings Plans** (non RI) | Solo SP coprono Lambda + Fargate + EC2 |
| "bring your own license", "per-socket", "per-core" | **Dedicated Hosts** | Visibilità su socket/core per licensing |
| "dedicated hardware" senza menzione licenze | **Dedicated Instances** | Isolamento hardware senza visibilità |
| "event-driven", "spiky", "unpredictable", < 15 min | **Lambda** | Serverless, pay per ms, auto-scale |
| "containers without managing servers" | **Fargate** | Serverless per container |
| "containers with full control" | **ECS su EC2** o **EKS su EC2** | Tu gestisci le istanze |
| "Kubernetes" | **EKS** | Managed Kubernetes |
| "batch processing", "large compute jobs" | **AWS Batch** | Gestisce provisioning e scheduling |

### Storage

| Se la domanda dice... | La risposta è probabilmente... | Perché |
|---|---|---|
| "shared file system", "multiple instances", "NFS" | **EFS** | File system condiviso, NFS, multi-mount |
| "Windows file share", "SMB", "Active Directory" | **FSx for Windows** | SMB + AD integration |
| "HPC", "machine learning", "Lustre", "high throughput" | **FSx for Lustre** | Centinaia GB/s, milioni IOPS |
| "lowest cost storage", "rarely accessed", "archive" | **S3 Glacier Deep Archive** | Il più economico, retrieval fino a 48h |
| "archive but need instant access" | **S3 Glacier Instant Retrieval** | Costo basso, accesso in millisecondi |
| "data accessed infrequently, rapid access when needed" | **S3 Standard-IA** | Costo storage basso, retrieval immediato |
| "non-critical data, can be recreated" | **S3 One Zone-IA** | -20% vs Standard-IA, ma una sola AZ |
| "changing access patterns", "unknown access" | **S3 Intelligent-Tiering** | Sposta automaticamente tra tier |
| "highest IOPS", "temporary", "data can be lost" | **Instance Store** | Fisicamente attaccato, IOPS massime |
| "persistent block storage", "database" | **EBS** | Persistente, una istanza alla volta |
| "IOPS > 16,000" o "sub-millisecond latency" per DB | **EBS io2** | Provisioned IOPS, 99.999% durability |
| "small random I/O" | **SSD** (gp3, io2) | SSD per random I/O |
| "large sequential I/O", "throughput" | **HDD** (st1) | HDD per sequential I/O |

### Database

| Se la domanda dice... | La risposta è probabilmente... | Perché |
|---|---|---|
| "relational", "SQL", "complex queries", "ACID", "joins" | **RDS** o **Aurora** | Database relazionali |
| "MySQL or PostgreSQL" + "high performance" | **Aurora** | 5x MySQL, 3x PostgreSQL |
| "key-value", "sub-millisecond", "NoSQL", "unstructured" | **DynamoDB** | Key-value, auto-scale, sub-ms |
| "20 million requests per second" | **DynamoDB** | Progettato per questo |
| "graph database", "complex relationships", "social network" | **Neptune** | Graph DB |
| "document store", "MongoDB", "JSON" | **DocumentDB** | MongoDB compatibile |
| "immutable ledger", "audit trail", "blockchain-like" | **QLDB** | Ledger immutabile |
| "data warehouse", "analytics", "petabyte", "BI" | **Redshift** | Data warehouse |
| "query S3 data with SQL", "serverless analytics" | **Athena** | SQL su S3, pay per query |
| "read-heavy database" | **Read Replicas** | Scaling orizzontale letture |
| "database high availability", "failover" | **Multi-AZ** | Failover automatico |
| "many database connections", "connection pooling" | **RDS Proxy** | Pool connessioni, failover veloce |
| "caching", "same queries repeated" | **ElastiCache** | Cache in-memory |
| "caching for DynamoDB" | **DAX** | Nativo per DynamoDB, più seamless |
| "spiky database workload" | **Aurora Serverless** | Auto-scale, ma 2x costo per unità |

### Networking

| Se la domanda dice... | La risposta è probabilmente... | Perché |
|---|---|---|
| "static IP" + load balancer | **NLB** | ALB non ha IP statici |
| "HTTP/HTTPS" + routing avanzato (URL, host) | **ALB** | Layer 7, routing rules |
| "TCP/UDP", "gaming", "IoT", "millions req/sec" | **NLB** | Layer 4, ultra-fast |
| "reduce latency for global users" + contenuti web | **CloudFront** | CDN, cache all'edge |
| "reduce latency" + TCP/UDP + "static IP" | **Global Accelerator** | Routing ottimizzato, IP statici |
| "block specific IP" | **NACL** (non Security Group) | SG non ha regole Deny |
| "private access to S3" da VPC | **Gateway Endpoint** | Gratuito, route table |
| "private access to S3" da on-premises | **Interface Endpoint** | A pagamento, ma accessibile da VPN/DX |
| "connect VPCs" (pochi) | **VPC Peering** | Gratuito, semplice |
| "connect many VPCs" | **Transit Gateway** | Hub centralizzato |
| "expose service to thousands of VPCs" | **PrivateLink** | Scalabile, privato |
| "fastest connection on-premises ↔ AWS" | **VPN** (non Direct Connect) | DX richiede mesi |
| "dedicated, consistent connection on-premises" | **Direct Connect** | Privato, bandwidth garantita |
| "Direct Connect" + "encrypted" | **DX + VPN tunnel** (IPsec) | DX non è cifrato di default |

### Security

| Se la domanda dice... | La risposta è probabilmente... | Perché |
|---|---|---|
| "SQL injection", "XSS", "bot protection" | **WAF** | Layer 7, web attacks |
| "DDoS protection" | **Shield** | Standard (gratis) o Advanced ($3K/mese) |
| "DDoS" + "cost reimbursement" + "response team" | **Shield Advanced** | DRT + cost protection |
| "rate limiting requests" | **WAF rate-based rules** | Limita req per IP |
| "FIPS 140-2 Level 3" | **CloudHSM** | KMS è solo Level 2 |
| "company must control encryption keys exclusively" | **CloudHSM** | Single-tenant HSM |
| "rotate database credentials automatically" | **Secrets Manager** | Rotazione nativa per RDS |
| "configuration parameters" (non segreti) | **Parameter Store** | Gratuito, no rotazione nativa |
| "find PII in S3" | **Macie** | ML per dati sensibili in S3 |
| "detect threats", "anomalous behavior", "crypto mining" | **GuardDuty** | Threat detection continua |
| "vulnerability scanning", "CVE", "patching" | **Inspector** | Vulnerability assessment |
| "centralized security view", "compliance dashboard" | **Security Hub** | Aggrega findings |
| "investigate security incident", "root cause" | **Detective** | Post-incident investigation |
| "manage security rules across multiple accounts" | **Firewall Manager** | Centralizzato, richiede Organizations |
| "prevent actions across all accounts" | **SCP** | Guardrail a livello organizzazione |
| "credentials in code" o "access keys on instance" | **SEMPRE SBAGLIATO** | Usa ruoli IAM |

### Decoupling & Messaging

| Se la domanda dice... | La risposta è probabilmente... | Perché |
|---|---|---|
| "decouple", "queue", "one-to-one" | **SQS** | Coda messaggi 1:1 |
| "exactly-once", "ordered messages" | **SQS FIFO** | Ordine garantito, no duplicati |
| "notify multiple subscribers", "one-to-many" | **SNS** | Pub/sub |
| "fan-out to multiple queues" | **SNS + SQS** | SNS topic → multiple SQS |
| "event-driven", "many sources, many targets" | **EventBridge** | Many-to-many |
| "coordinate multiple Lambda functions" | **Step Functions** | Orchestrazione workflow |
| "real-time streaming", "multiple consumers" | **Kinesis Data Streams** | Streaming, replay |
| "load streaming data into S3/Redshift" | **Kinesis Firehose** | Auto-load, transform |

### Migration

| Se la domanda dice... | La risposta è probabilmente... | Perché |
|---|---|---|
| "migrate files to S3/EFS" | **DataSync** | File transfer, non supporta EBS |
| "migrate database" | **DMS** | + SCT per conversione schema |
| "terabytes of data, no good internet" | **Snowball Edge** | Dispositivo fisico |
| "petabytes/exabytes" | **Snowmobile** | Camion 18 ruote |
| "> 10 PB in una location" | **Snowmobile** | Per dataset > 10 PB |
| "< 10 PB o multiple locations" | **Snowball Edge** | Più flessibile |
| "ongoing data transfer to AWS" | **Direct Connect** (non Snow) | Snow è per one-time |
| "hybrid access, files on-premises AND in S3" | **Storage Gateway** | Accesso continuo ibrido |
| "transfer files via SFTP/FTPS" | **Transfer Family** | Protocolli standard |

---

## 🚫 TRAPPOLE COMUNI

### Keyword che ESCLUDONO risposte

| Se la domanda dice... | Escludi... | Perché |
|---|---|---|
| "most cost-effective" | Direct Connect, RDS Proxy, Shield Advanced | Costosi |
| "fastest implementation" | Direct Connect | Richiede mesi |
| "0.0.0.0/0" nelle risposte | Probabilmente non è "most secure" | Apre a tutto internet |
| "store credentials in code" | Quella risposta | Sempre sbagliato — usa ruoli IAM |
| "single AZ" per produzione | Quella risposta | Non è HA |
| "CLB" (Classic Load Balancer) | Quella risposta | AWS raccomanda di non usarlo |
| "data must not be lost" | Instance Store | Dati persi allo stop |

### Confronti che Confondono

| Confusione | Come Distinguere |
|---|---|
| **Multi-AZ vs Read Replica** | Multi-AZ = **disponibilità** (failover, standby non serve query). Read Replica = **performance** (scaling letture, asincrono) |
| **CloudTrail vs CloudWatch** | CloudTrail = **chi ha fatto cosa** (audit). CloudWatch = **come stanno le risorse** (metriche) |
| **DataSync vs Storage Gateway** | DataSync = **trasferimento** (one-time o scheduled). Storage Gateway = **accesso continuo** ibrido |
| **Security Group vs NACL** | SG = stateful, solo Allow, istanza. NACL = stateless, Allow+Deny, subnet |
| **Gateway Endpoint vs Interface Endpoint** | Gateway = gratuito, solo S3/DynamoDB, route table. Interface = a pagamento, quasi tutti i servizi, ENI |
| **Secrets Manager vs Parameter Store** | Secrets Manager = rotazione automatica DB, $0.40/segreto. Parameter Store = config generica, gratuito |
| **CloudFront vs Global Accelerator** | CloudFront = HTTP, cache contenuti. Global Accelerator = TCP/UDP, IP statici, routing ottimizzato |
| **SQS vs Kinesis** | SQS = decoupling 1:1, singolo consumer. Kinesis = streaming real-time, multipli consumer, replay |
| **Aurora Serverless vs RDS** | Aurora Serverless = workload spiky (2x costo/unità). RDS = workload steady |
| **Snowball vs Snowmobile** | Snowball Edge = < 10 PB o multiple location. Snowmobile = > 10 PB, singola location |

---

## 📊 TABELLE DECISIONALI RAPIDE

### Quale Storage?

```
Hai bisogno di...
├── Block storage per EC2? → EBS
│   ├── IOPS alte, random I/O? → gp3 o io2 (SSD)
│   └── Throughput alto, sequential? → st1 (HDD)
├── File system condiviso?
│   ├── Linux? → EFS
│   ├── Windows? → FSx for Windows
│   └── HPC/ML? → FSx for Lustre
├── Object storage? → S3
│   ├── Accesso frequente? → Standard
│   ├── Accesso raro, retrieval veloce? → Standard-IA
│   ├── Archivio, retrieval in ore? → Glacier
│   └── Archivio profondo, retrieval in giorni? → Deep Archive
└── Storage temporaneo, IOPS massime? → Instance Store
```

### Quale Database?

```
I tuoi dati sono...
├── Strutturati (SQL, relazioni, JOIN)?
│   ├── MySQL/PostgreSQL + alte performance? → Aurora
│   ├── Oracle/SQL Server/DB2? → RDS
│   └── Workload spiky? → Aurora Serverless
├── Non strutturati (key-value, JSON)?
│   ├── Sub-millisecond latency? → DynamoDB
│   ├── Document store (MongoDB)? → DocumentDB
│   └── Graph (relazioni complesse)? → Neptune
└── Analytics su petabyte? → Redshift
```

### Quale Connettività?

```
Devi connettere...
├── VPC a S3/DynamoDB privatamente? → Gateway Endpoint (gratis)
├── VPC ad altri servizi AWS privatamente? → Interface Endpoint
├── On-premises a AWS?
│   ├── Subito, budget limitato? → VPN
│   ├── Bandwidth dedicata, consistente? → Direct Connect
│   └── Direct Connect + encryption? → DX + VPN tunnel
├── Due VPC? → VPC Peering
├── Molti VPC? → Transit Gateway
└── Servizio a migliaia di VPC? → PrivateLink
```

### Quale DR Strategy?

```
Il tuo budget è...
├── Minimo (RPO ore, RTO ore)? → Backup & Restore
├── Medio (RPO minuti, RTO minuti)? → Pilot Light o Warm Standby
└── Illimitato (RPO ~0, RTO ~0)? → Active-Active
```

---

## 💡 REGOLE D'ORO DAI LIBRI

1. **"Se la domanda chiede DDoS → Shield. Se chiede SQLi/XSS → WAF"** (PACKT)
2. **"Se la domanda chiede S3 o DynamoDB endpoint → Gateway. Altrimenti → Interface"** (PACKT)
3. **"Se la domanda dice 'most secure' e una risposta ha 0.0.0.0/0 → non è quella"** (PACKT)
4. **"Se Macie è una risposta, verifica che i dati siano in S3 e che si parli di PII"** (PACKT)
5. **"Read replicas sono un argomento comune nell'esame — capisci cosa possono e non possono fare"** (PACKT)
6. **"CloudTrail NON è real-time — ci vogliono ~15 minuti"** (PACKT)
7. **"gp3 è più performante di gp2 — ricordalo per scegliere tra i due"** (PACKT)
8. **"Aurora Serverless è 2x più costoso per unità — risparmia solo se il workload è spiky"** (PACKT)
9. **"Direct Connect richiede mesi — se serve velocità, non è la risposta"** (PACKT)
10. **"RDS Proxy ha costo aggiuntivo — attenzione a 'most cost-effective'"** (PACKT)
11. **"SQS = 1:1, SNS = 1:many, EventBridge = many:many"** (PACKT)
12. **"Step Functions per coordinare Lambda, non SQS"** (PACKT)
13. **"Lambda timeout max 15 minuti — se il job dura di più, usa EC2/Fargate/Batch"** (Dojo)
14. **"DataSync NON supporta EBS — solo file (S3/EFS/FSx)"** (PACKT)
15. **"Non puoi fare SSH a RDS — usa Parameter Groups per configurazione"** (Dojo)
16. **"Snowball Edge < 10 PB. Snowmobile > 10 PB"** (Dojo)
17. **"S3 IA ha minimum 128KB e 30 giorni — se cancelli prima, paghi comunque"** (Dojo)
18. **"Non puoi transitare da Glacier Deep Archive a Glacier (solo il contrario)"** (Dojo)


---

## 📦 CONFRONTI DETTAGLIATI DAL DOJO

### Data Transfer: S3 TA vs Direct Connect vs VPN vs Snow (dal Dojo)

Questo confronto è fondamentale per l'esame — le domande su come trasferire dati sono frequentissime.

| Metodo | Quando usarlo | Note chiave |
|---|---|---|
| **S3 Transfer Acceleration** | Trasferimenti da location distribuite via internet pubblico, throughput variabile | Usa edge location CloudFront. Paghi solo se c'è miglioramento. Supporta multipart upload |
| **Direct Connect** | Connessione privata dedicata, bandwidth consistente, requisiti di sicurezza | NON cifrato di default. Non ridondante (serve seconda linea). Mesi per implementare |
| **VPN (Site-to-Site)** | Bisogno immediato, budget limitato, bandwidth bassa-media, tolleranza per variabilità internet | Cifrato (IPsec). Configurabile in minuti. Throughput dipende da internet |
| **Snowball Edge** | TB-PB di dati, no buona connessione internet, location isolate | Dispositivo fisico, 50-80 TB per device. Trasferimento completato entro 360 giorni. Supporta export |
| **Snowmobile** | > 10 PB in una singola location | Camion 18 ruote, fino a 100 PB. Guardie armate, GPS, video 24/7. **NON supporta export** |

**Regole decisionali dal Dojo:**
- *"Se il trasferimento via internet richiederebbe più di una settimana, o ci sono job ricorrenti con >25 Mbps di bandwidth disponibile → S3 Transfer Acceleration"*
- *"Puoi usare Snowball Edge per il trasferimento iniziale pesante, poi S3 TA per i cambiamenti incrementali"*
- *"Se trasferisci dati ad AWS su base continua → Direct Connect (non Snow)"*
- *"Se più utenti in location diverse interagiscono con S3 continuamente → S3 TA"*
- *"Non puoi esportare dati direttamente da S3 Glacier — devi prima ripristinarli in S3"*
- *"> 10 PB in una location → Snowmobile. < 10 PB o multiple location → Snowball Edge"*
- *"Se hai backbone ad alta velocità con centinaia di Gb/s spare → Snowmobile. Se bandwidth limitata → multiple Snowball Edge incrementali"*

### DynamoDB: Scaling RCU vs DAX vs Secondary Indexes vs ElastiCache (dal Dojo)

| Soluzione | Quando usarla | Limitazioni |
|---|---|---|
| **Scaling RCU** | Letture alte su item diversi, non adatti per cache. On-Demand (auto) o Provisioned (con auto-scaling) | On-Demand può diventare costoso con spike frequenti |
| **DAX** | Microsecond response time, stessi item letti ripetutamente, no code changes | No TLS. Solo Go/Java/Node.js/Python/.NET. Non per strongly consistent reads o workload write-intensive. Possibili dati stale |
| **Secondary Indexes** | Query su attributi non-primary key. Evita scan dell'intera tabella | Performance ancora legate alle RCU della tabella. Più ottimizzazione struttura dati che boost performance |
| **ElastiCache** | Solo se serve specificamente Redis/Memcached, o feature non supportate da DAX | Richiede code changes. Più manutenzione di DAX |

**Regola dal Dojo:** *"Per caching DynamoDB, vai con DAX (no code changes). Preferisci ElastiCache solo se ti serve specificamente Redis/Memcached o una feature non supportata da DAX."*

### EFS vs FSx for Windows vs FSx for Lustre — Dettagli (dal Dojo)

| Caratteristica | EFS | FSx for Windows | FSx for Lustre |
|---|---|---|---|
| **Protocollo** | NFS | SMB | Lustre |
| **OS supportati** | Linux (EC2, ECS, EKS, Fargate, Lambda) | Windows, Linux, MacOS | **Solo Linux** (+ EKS, Batch) |
| **Auto-scale storage** | **Sì** (automatico) | **No** (manuale) | **No** (manuale, ogni 6 ore) |
| **Throughput** | Bursting o Provisioned | Configurabile alla creazione | Centinaia GB/s, milioni IOPS |
| **Integrazione S3** | No | No | **Sì** (import/export automatico) |
| **Multi-AZ** | Sì (Standard class) | Sì (opzionale) | No (ma Persistent replica nella AZ) |
| **Encryption** | KMS at rest, TLS 1.2 in transit | KMS at rest, SMB Kerberos in transit | KMS at rest, in transit da EC2 supportate |
| **On-premises access** | Via Direct Connect o VPN | Via Direct Connect o VPN | Non menzionato |
| **Deployment types** | N/A | Single-AZ o Multi-AZ | **Scratch** (temporaneo, no replica) o **Persistent** (HA, replica nella AZ) |
| **Casi d'uso** | Big data, analytics, web serving, CMS, home dir | CRM, ERP, .NET, home dir, media, build env | ML, HPC, video processing, financial modeling, genome |

### Numeri da Ricordare per l'Esame

| Servizio | Numero | Significato |
|---|---|---|
| **S3** | 99.999999999% (11 nines) | Durabilità |
| **S3** | 99.99% | Disponibilità |
| **S3** | 5 TB | Dimensione massima singolo oggetto |
| **S3 IA** | 128 KB / 30 giorni | Minimum capacity / minimum duration charge |
| **S3 Glacier** | 40 KB / 90 giorni | Minimum capacity / minimum duration charge |
| **S3 Deep Archive** | 40 KB / 180 giorni | Minimum capacity / minimum duration charge |
| **Glacier Expedited** | 1-5 minuti | Retrieval più veloce |
| **Glacier Standard** | 3-5 ore | Retrieval standard |
| **Glacier Deep Standard** | 12 ore | Retrieval standard |
| **Glacier Deep Bulk** | 48 ore | Retrieval più lento |
| **EBS io2** | 99.999% | Durabilità (vs 99.8-99.9% per altri) |
| **EBS io2** | 500 IOPS/GiB | Ratio IOPS |
| **EBS Nitro** | 64,000 IOPS | Max IOPS per volume su istanze Nitro |
| **EBS non-Nitro** | 32,000 IOPS | Max IOPS per volume |
| **RDS Multi-AZ** | 99.95% | SLA uptime |
| **RDS Single-AZ** | 99.5% | SLA uptime |
| **RDS backup** | 7-35 giorni | Retention (default 7) |
| **DynamoDB** | 20M+ req/sec | Capacità massima |
| **DynamoDB** | sub-millisecond | Latenza |
| **Aurora** | 5x MySQL, 3x PostgreSQL | Performance |
| **Aurora** | 128 TiB | Storage massimo |
| **Lambda** | 15 minuti | Timeout massimo |
| **Lambda** | 10,240 MB | Memoria massima |
| **Lambda** | 1,769 MB = 1 vCPU | Equivalenza memoria/CPU |
| **Lambda** | 1,000 | Concurrency default per Region |
| **SQS FIFO** | 300 msg/sec | Throughput (3,000 con batching) |
| **SQS visibility timeout** | 30 secondi | Default |
| **CloudTrail** | 90 giorni | Event history gratuita |
| **CloudTrail** | ~15 minuti | Delay (non real-time) |
| **Spot Instance** | 2 minuti | Preavviso prima della reclaim |
| **Spot Instance** | fino a 90% | Sconto massimo |
| **RI/Savings Plans** | fino a 72% | Sconto massimo |
| **Snowball Edge** | 50-80 TB | Capacità per device |
| **Snowball Edge** | 360 giorni | Tempo massimo per completare il trasferimento |
| **Snowmobile** | 100 PB | Capacità per camion |
| **Shield Advanced** | $3,000/mese | Costo |
| **NLB idle timeout** | 350 secondi | Fisso, non modificabile |
| **ALB idle timeout** | 60 secondi | Default, modificabile fino a 4,000s |
| **Organizations** | 1,000 OU | Massimo |
| **Organizations** | 5 livelli | Nesting massimo OU |
| **KMS CMK** | 4,096 byte | Max encryption diretta (poi envelope) |
| **Key deletion** | 7 giorni | Minimo attesa per cancellazione |


---

## 🔌 DIRECT CONNECT — Pattern Decisionali (dal Dojo)

Direct Connect è un argomento frequente nell'esame. Il Dojo fornisce 4 scenari di connettività:

| Scenario | Soluzione | Note |
|---|---|---|
| Accesso a risorse in **un VPC** | Private VIF → VGW del VPC | Max 50 VIF per connessione DX. Limitato alla Region del DX location |
| Accesso a **VPC in Region diverse** | Private VIF → **DX Gateway** → multiple VGW | Un BGP peering per DX Gateway per connessione. NO VPC-to-VPC connectivity |
| Accesso a **molti VPC in molte location** | Transit VIF → **DX Gateway** → **Transit Gateway** | Fino a 3 TGW in Region/account diversi su un VIF. **Più scalabile e gestibile** |
| Accesso a **servizi pubblici AWS** (S3, DynamoDB, EC2 pubblici) | **VPN su DX public VIF** → Transit Gateway | VPN per encryption, DX per performance |

### Resilienza Direct Connect (dal Dojo)

| Setup | Resilienza | Costo |
|---|---|---|
| **2 linee DX** su 2 device/router diversi | Alta — failover automatico | Alto (2x DX) |
| **1 linea DX + VPN** come backup | Media — VPN più lento ma funziona | Medio (DX + VPN) |
| **Solo 1 linea DX** | **Nessuna** — single point of failure | Basso ma rischioso |

> **Regola Dojo**: *"Direct Connect di default NON è resiliente. Serve una seconda linea o un VPN backup. Abilita BFD (Bidirectional Forwarding Detection) per failover veloce."*

---

## 🔗 VPC ENDPOINTS — Confronto Completo (dal Dojo)

| Caratteristica | Interface Endpoint | Gateway Endpoint | GW Load Balancer Endpoint |
|---|---|---|---|
| **Cos'è** | ENI con IP privato | Target nella route table | Intercetta traffico verso GWLB |
| **Servizi** | Quasi tutti i servizi AWS | **Solo S3 e DynamoDB** | Appliance di sicurezza (firewall, IDS) |
| **Security Groups** | **Sì** | No | No |
| **Endpoint Policy** | Sì | Sì | No |
| **Accesso da on-premises** | **Sì** (via VPN/DX) | **No** | No |
| **Accesso cross-region** | **No** (solo stessa region) | **No** | No |
| **VPC Peering** | **Sì** (intra-region da Nitro, inter-region da qualsiasi) | **No** | No |
| **Protocollo** | IPv4 TCP only | IPv4 only | IPv4 only |
| **Costo** | A pagamento | **Gratuito** | A pagamento |

> **Regola per l'esame**: S3/DynamoDB da VPC → **Gateway** (gratis). S3 da on-premises → **Interface**. Qualsiasi altro servizio → **Interface**.

---

## 🧠 CACHING — Dove e Come (dal LinkedIn)

Il LinkedIn PDF spiega i livelli di caching in un'architettura:

1. **Browser/Client** — HTTP response cache con expiry policy nell'header
2. **CDN (CloudFront)** — cache di risorse statiche nelle edge location
3. **Load Balancer** — può cachare risorse
4. **API Gateway** — cache delle risposte API (evita di rieseguire Lambda)
5. **Application layer (ElastiCache)** — cache in-memory per dati frequenti
6. **Database layer (DAX per DynamoDB)** — cache specifica per il DB

### Problemi di Cache (dal LinkedIn)

| Problema | Descrizione | Soluzione |
|---|---|---|
| **Thunder Herd** | Molte chiavi cache scadono contemporaneamente → tutte le query vanno al DB | Aggiungi un numero random all'expiry time. Permetti solo dati core di colpire il DB |
| **Cache Penetration** | Query per dati che non esistono → ogni volta colpisce il DB | Cacha anche i risultati "vuoti" con TTL breve |
| **Cache Avalanche** | Il server cache va giù → tutto il traffico va al DB | Usa cluster cache con replica. Circuit breaker |
| **Cache Stampede** | Una chiave popolare scade → centinaia di richieste simultanee al DB | Lock sulla chiave: solo una richiesta rigenera la cache, le altre aspettano |

---

## 🏗️ API GATEWAY — Funzioni Chiave (dal LinkedIn)

| Funzione | Descrizione |
|---|---|
| **Request Routing** | Dirige le richieste API al backend service appropriato |
| **Load Balancing** | Distribuisce richieste su più server |
| **Security** | Autenticazione, autorizzazione, encryption |
| **Rate Limiting/Throttling** | Controlla il numero di richieste per client in un periodo |
| **API Composition** | Combina multiple richieste backend in una singola richiesta frontend |
| **Caching** | Salva risposte temporaneamente per ridurre processing ripetuto |

---

## 💰 CLOUD COST REDUCTION — Tecniche (dal LinkedIn)

Il LinkedIn PDF elenca le tecniche di riduzione costi:

1. **Reduce Usage** — spegni risorse non usate, right-size le istanze
2. **Reserved Capacity** — RI e Savings Plans per workload prevedibili
3. **Spot Instances** — per workload interrompibili
4. **Auto Scaling** — scala giù quando non serve
5. **Storage Tiering** — lifecycle policies per spostare dati in tier più economici
6. **Data Transfer Optimization** — minimizza cross-region, usa VPC endpoints, CloudFront
7. **Monitoring & Alerts** — Cost Explorer, Budgets, billing alerts
8. **Tagging** — traccia costi per dipartimento/progetto
9. **Managed Services** — meno ore-uomo = meno costi operativi
10. **Serverless** — paga solo per l'esecuzione effettiva

---

## 🔒 CLOUD SECURITY — Layers (dal LinkedIn)

Il LinkedIn PDF mostra i livelli di sicurezza cloud:

1. **Identity & Access** — IAM, MFA, least privilege, federation
2. **Network** — VPC, SG, NACL, VPN, Direct Connect, PrivateLink
3. **Application** — WAF, Shield, API Gateway throttling
4. **Data** — Encryption at rest (KMS) e in transit (TLS/SSL)
5. **Monitoring** — CloudTrail, GuardDuty, Security Hub, Config
6. **Incident Response** — Detective, Lambda automation, SNS alerts
7. **Compliance** — Config Rules, Audit Manager, Organizations SCP

---

## 🔄 DISASTER RECOVERY — Riepilogo Visivo (dal LinkedIn + Dojo)

```
COSTO CRESCENTE →
TEMPO DI RECOVERY DECRESCENTE →

┌──────────────┬──────────────┬──────────────┬──────────────┐
│  BACKUP &    │  PILOT       │  WARM        │  ACTIVE-     │
│  RESTORE     │  LIGHT       │  STANDBY     │  ACTIVE      │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ RPO: ore     │ RPO: minuti  │ RPO: secondi │ RPO: ~zero   │
│ RTO: ore     │ RTO: minuti  │ RTO: minuti  │ RTO: ~zero   │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ Solo backup  │ Core sempre  │ Ambiente     │ Copia        │
│ in S3/altra  │ attivo (DB   │ ridotto ma   │ completa     │
│ Region.      │ con replica).│ funzionante, │ active-      │
│ Ripristino   │ Resto si     │ sempre in    │ active.      │
│ al bisogno   │ avvia al     │ sync. Scala  │ Basta        │
│              │ bisogno      │ up al bisogno│ redirigere   │
│              │              │              │ il traffico  │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ 💰           │ 💰💰         │ 💰💰💰       │ 💰💰💰💰     │
└──────────────┴──────────────┴──────────────┴──────────────┘
```


---

## 🖥️ ACCESSO EC2 — Metodi (dal PACKT)

| Metodo | Quando usarlo |
|---|---|
| **SSH** (porta 22) | Accesso Linux standard con chiave privata |
| **RDP** (porta 3389) | Accesso Windows |
| **Bastion Host** | Accesso sicuro a istanze in private subnet. Server hardened in public subnet |
| **Session Manager (SSM)** | **Il più sicuro** — nessuna porta aperta, nessuna chiave SSH, dalla console AWS |
| **VPN** | Accesso aziendale a istanze private |

> **Tip esame**: metodo più sicuro per accedere a EC2 → **Session Manager** (PACKT)

---

## 🌐 NAT Gateway vs Internet Gateway (dal PACKT)

| | Internet Gateway | NAT Gateway |
|---|---|---|
| **Per** | Public subnet | Private subnet (outbound only) |
| **Traffico** | Inbound + outbound | **Solo outbound** |
| **Dove** | Attaccato al VPC | In public subnet (richiede IGW) |

---

## 🏗️ MULTI-TIER (da Kimiko)

Presentation (web) → Business Logic (app) → Data Access (DB). Separa i tier per scalare indipendentemente. Horizontal scaling > Vertical scaling.

---

## 🐳 ECS vs EKS vs Fargate

"containers" → ECS/EKS. "Kubernetes" → EKS. "without managing servers" → Fargate. "Docker" → ECS.

---

## 📋 DEPLOYMENT (dal Dojo)

"deploy infrastructure" → **CloudFormation**. "deploy web app quickly" → **Beanstalk**. "deploy code updates" → **CodeDeploy**.

---

## 🎯 MICROSERVICES Best Practice (dal LinkedIn)

Separate data storage, single responsibility, stateless, containers, domain-driven design, orchestrate con Step Functions.

---

## 🛡️ FAULT TOLERANCE Principi (dal LinkedIn)

Replication, Redundancy, Load Balancing, Failover Mechanisms, Graceful Degradation, Data Backup & Recovery.
