# Database Services - RDS, Aurora, DynamoDB, ElastiCache

> Sources: PACKT Ch.7 (p.314-377), PACKT Ch.14 (p.561-568), KIMIKO (p.237-248), DOJO (p.135-158, p.278, p.280, p.284)

---

## Glossary: the services you will encounter in this document

- **RDS (Relational Database Service)** — AWS's managed relational database service. "Managed" means AWS takes care of: installation, operating system patching, automatic backups, database software updates. You only worry about your data and your queries. Supports MySQL, PostgreSQL, SQL Server, Oracle, MariaDB, DB2. It's like having a DBA (database administrator) working 24/7 for free on the infrastructure side.

- **Aurora** — AWS's proprietary relational database. Compatible with MySQL and PostgreSQL, but designed from scratch for the cloud. Up to 5x faster than MySQL and 3x faster than PostgreSQL. Storage is "decoupled" from the instance and scales automatically up to 128 TB. Costs a bit more than standard RDS but offers superior performance and resilience.

- **DynamoDB** — AWS's NoSQL (non-relational) database. Instead of tables with rows and columns linked together (like SQL), it uses key-value pairs and JSON documents. Very fast (millisecond latency) and scales automatically. Perfect for applications that need very fast responses with simple access patterns (e.g. e-commerce cart, user sessions, gaming). Think of it as a giant dictionary: give the key, get the value instantly.

- **ElastiCache** — an in-memory caching service. Puts the most requested data in RAM for ultra-fast access (microseconds). Supports Redis and Memcached. Example: instead of querying the database every time a user loads the homepage, you put the result in cache. Subsequent requests read from cache (very fast) instead of the database (slower). Like keeping the most used documents on your desk instead of in the filing cabinet.

- **Read Replica** — a read-only copy of your database. The primary database handles reads AND writes. The read replica handles ONLY reads. It serves to: 1) lighten the load on the primary database, 2) improve read performance. Data is automatically replicated from primary to replica (asynchronously, so with a small delay).

- **Multi-AZ** — means having a copy of the database in another Availability Zone. If the primary database has a problem, AWS automatically fails over to the copy. Your database comes back online in minutes without manual intervention. The copy is synchronous (for non-Aurora) so you don't lose data.

- **RDS Proxy** — an intermediary between your application and the database. Manages a "pool" of connections to avoid overloading the database. Like a receptionist managing the customer queue instead of letting everyone into the store at once.

- **DAX (DynamoDB Accelerator)** — an in-memory cache specific to DynamoDB. Reduces latency from milliseconds to microseconds. Unlike ElastiCache, it's "seamless" — it integrates natively with DynamoDB without complex configuration.

- **Redshift** — AWS's data warehousing service. For analyzing petabytes of data with complex SQL queries. It's not for daily operations (that's RDS), but for analytics and business intelligence. Like the difference between the cash register (RDS) and the annual sales report (Redshift).

---

## Overview

PACKT introduces: *"AWS attualmente offre 15 database diversi tra cui scegliere. Questo è un numero enorme, e quindi questo argomento è visto come uno dei più difficili da molti solutions architect. Per l'esame SAA-C03, dovrai conoscere i casi d'uso base e i benefici di ogni tipo di database."*

### Relational vs NoSQL (from PACKT)

PACKT explains the history: *"Negli anni '70, quando i database divennero popolari, i costi di storage erano estremamente alti. Qualsiasi dato duplicato o ridondante era molto costoso. Per prevenire la duplicazione, le tabelle divennero un contenitore per un tipo di oggetto, collegate ad altre tabelle."* Example: an Orders table contains only orderID, customerID, productID. To get all the information, you need to look in the Customers and Products tables.

Relational databases are still the most popular in the world (~50 ZB of data). But they have challenges: storage growth, spiky usage patterns, patching, backup, HA testing.

---

## Amazon RDS — Relational Database Service

### Overview (from PACKT, Kimiko, Dojo)

PACKT describes RDS as a service for moving existing databases to AWS and delegating day-to-day management.

Kimiko shows the process in the console: *"Possiamo avere Amazon che si occupa di tutto: backup, upgrade del software, sicurezza fisica, replicazione, alta disponibilità."* She shows the step-by-step creation: choose Standard Create or Easy Create (best practice configurations), select the engine (SQL Server, Oracle, PostgreSQL, MariaDB, MySQL, Aurora), the version, the environment (production/dev-test/free tier), credentials, instance size, storage (General Purpose SSD or Provisioned IOPS SSD).

The Dojo adds a fundamental comparison: *"Puoi hostare il tuo database su un'istanza EC2 invece di usare RDS. Il problema è l'overhead di gestione: patching manuale, scaling dello storage, backup regolari, HA, monitoring CPU/memoria/storage. Con RDS, tutte queste attività sono significativamente ridotte o eliminate."*

**Supported engines**: Oracle, SQL Server, MySQL, MariaDB, PostgreSQL, DB2, and **Amazon Aurora**.

### RDS vs Self-Hosted on EC2 (from PACKT and Dojo)

| Feature | RDS | Self-Hosted on EC2 |
|---|---|---|
| **OS Management** | AWS | You |
| **DB Patching** | Automatic (maintenance window) | Manual |
| **Backup** | Automatic, point-in-time recovery | Manual |
| **HA/Failover** | Multi-AZ with one click | You must configure replication and failover |
| **Scaling** | Change instance type with minimal downtime | Manual intervention, complex |
| **OS Access** | **You cannot SSH/RDP** to the underlying instance (Dojo) | Full access |
| **Configuration** | Via Parameter Groups and Option Groups (Dojo) | Direct config file modification (my.cnf, etc.) |
| **Cost** | Potentially higher for the managed service | Lower but more man-hours (PACKT) |
| **Flexibility** | Limited to supported engines | Any database |

> **Dojo note**: *"A differenza di un database self-hosted, non puoi accedere direttamente all'istanza EC2 sottostante del tuo database RDS. Non puoi stabilire una connessione SSH o RDP. Usi Parameter Groups e Option Groups per la configurazione."*

### Backup (from PACKT)

- Automatic backups saved to S3, include transactional data for **point-in-time recovery**
- Default: enabled for **7 days**, maximum **35 days** retention
- Free backup storage up to the allocated database size (e.g. 100 GB DB = 100 GB free backup)
- **Manual snapshots**: can be shared with other accounts, sent to other Regions for DR
- The Dojo adds: *"Se stai pianificando un backup o snapshot, puoi usare l'istanza standby invece della primaria. In questo modo non sospendi le attività I/O del database di produzione."*

### Patching and Upgrades (from PACKT)

- AWS automates patching and minor upgrades during a configurable **maintenance window**
- With **Multi-AZ**: AWS patches the standby first, does switchover, then patches the old primary → **zero downtime**
- AWS **never** automatically upgrades to a major version (e.g. MySQL 5.7 → 8.0) — always manual, via in-place upgrade, Blue/Green Deployments, or DMS
- **Extended Support**: additional costs if you don't upgrade when the version reaches end of support
- If you delay upgrades too long and go outside the published schedule, *"AWS potrebbe forzare gli upgrade anche fuori dalla tua maintenance window, causando un outage inaspettato"* (PACKT)

### Multi-AZ — In Depth (from PACKT and Dojo)

PACKT explains: *"Multi-AZ replica automaticamente il tuo database in un'AZ diversa e automatizza switchover e failover. Offre anche un SLA migliorato: Multi-AZ ha 99.95% uptime vs single-AZ con 99.5%."*

The Dojo details the mechanism:
- **Synchronous replication** for non-Aurora (MariaDB, MySQL, Oracle, PostgreSQL): *"Un update SQL committed viene scritto sia sull'istanza primaria che sulla standby simultaneamente"*
- **SQL Server** uses Database Mirroring (DBM) or Always On Availability Groups
- The standby **cannot serve read traffic** — for that you need Read Replicas
- When converting from Single-AZ to Multi-AZ: *"RDS prende uno snapshot della primaria e lo ripristina in un'altra AZ, poi configura la replicazione sincrona"* (Dojo)
- In case of failover: *"RDS cambia automaticamente il record DNS dell'istanza DB per puntare alla standby"* (Dojo)

### Read Replicas — In Depth (from PACKT and Dojo)

PACKT explains the use case: *"Le read replicas sono particolarmente utili quando fai report con query complesse che possono causare rallentamenti sul database — queste query possono essere scaricate su un database diverso."*

The Dojo provides technical details:
- **Asynchronous** replication — *"RDS scrive i dati sulla primaria PRIMA di scrivere sulla replica. Le repliche potrebbero restituire dati stale"*
- You can create replicas in the **same AZ, different AZ, or different Region**
- Cross-Region replication takes more time
- Based on the **native replication features** of the DB engines (MySQL, Oracle, etc.)
- Can be **manually promoted** to a standalone instance — *"Quando promuovi una read replica, l'istanza DB viene riavviata prima di diventare disponibile"* (Dojo)
- Perfect for **OLTP** (Online Transaction Processing) — *"Un sito e-commerce è un tipo di applicazione OLTP che processa centinaia o migliaia di transazioni online all'ora"* (Dojo)

> **Key difference Multi-AZ vs Read Replica**: Multi-AZ = **availability** (automatic failover, standby doesn't serve queries). Read Replica = **performance** (read scaling, asynchronous, manual promotion).

### RDS Storage (from PACKT)

| Type | IOPS | Use |
|---|---|---|
| **gp2** | 3 IOPS per GB, min 100 | Most cases |
| **gp3** | Min 3,000 IOPS (increases with storage), extra IOPS purchasable | **Recommended** — more flexible and often cheaper than gp2 |
| **io1/io2** | User-controllable | Critical high-performance databases |

> **PACKT note**: *"Lo storage allocato controlla anche gli IOPS. Se hai bisogno di IOPS più alti di quelli allocati, vedrai le disk queue salire e le performance del database calare."*

> **PACKT warning**: *"Puoi aumentare lo storage allocato senza downtime. Ma NON puoi ridurlo senza migrare a una nuova istanza. Alloca solo il minimo necessario."*

### RDS Authentication (from PACKT and Dojo)

Three options:
1. **Username and password** — traditional, password stored in Secrets Manager for rotation
2. **IAM Authentication** — *"Crei un ruolo IAM con permesso di connessione e lo assegni agli utenti. IAM non concede permessi oltre il diritto di connettersi"* (PACKT). The Dojo adds: *"Migliora la sicurezza delle applicazioni su EC2 perché non devi salvare la password del database — usi l'instance profile per connetterti"*
3. **Kerberos/Active Directory** — for enterprise environments with AD

### RDS Proxy — In Depth (from PACKT)

PACKT dedicates a specific section: *"RDS Proxy è particolarmente utile per applicazioni con workload imprevedibili o che devono gestire molte connessioni simultanee. Fa pool e condivisione delle connessioni per ridurre l'overhead sul database."*

Specific benefits from PACKT:
- **Reduces downtime during failover**: is constantly aware of the RDS system state, can release sessions as soon as the system is available
- **Reduces application errors**: during a failover, *"RDS Proxy mantiene o mette in pausa le connessioni invece di inviare un errore. L'applicazione non deve gestire questi errori o reinviare le query — RDS Proxy le invia, in ordine, appena il failover è completo"*
- **Integration with Secrets Manager** for secure storage and automatic credential rotation
- **Additional cost** — *"Fai attenzione a frasi nell'esame che parlano di 'soluzione più cost-effective'"* (PACKT)

---

## Amazon Aurora — In Depth

### Overview (from PACKT)

PACKT describes Aurora as AWS's proprietary relational database: *"Combina le performance e la disponibilità di database commerciali high-end con la semplicità e il rapporto costo-efficacia dei database open source."*

Kimiko notes from the console: *"Aurora è la selezione di default. Vedrai tutto il marketing language intorno ad Aurora — ottimizzazioni, risparmi, performance che non puoi ottenere in nessun altro modo."*

### Key Features (from PACKT)

- Compatible with **MySQL and PostgreSQL** (only these two)
- Up to **5x the performance of MySQL** and **3x of PostgreSQL**
- Storage **decoupled** from the instance — scales automatically up to **128 TiB**
- Data replicated across **multiple AZs** with continuous backups to S3
- **Two endpoints**: one for read-write, one for read-only — Aurora automatically routes to the best instance

### Aurora vs Standard RDS (from PACKT)

| Feature | Standard RDS | Aurora |
|---|---|---|
| Storage | Tied to the instance, IOPS depends on allocated storage | **Decoupled**, scales automatically, IOPS independent |
| Read scaling | Manual read replicas | Reader instances with **CPU-based auto-scale** |
| Failover | Failover to Multi-AZ standby | Failover to **reader instances** (more options) |
| Endpoint | Single | **Two endpoints** (read-write + read-only) |
| Performance | Standard | 5x MySQL, 3x PostgreSQL |
| Cloning | Snapshot + restore (slow) | **Fast Cloning** in minutes (lazy loading) |

### Aurora Serverless (from PACKT)

*"A differenza delle istanze database tradizionali, Aurora Serverless regola automaticamente la capacità in base alla domanda dell'applicazione. Non devi provisionare o gestire istanze database manualmente."*

> **PACKT note**: *"Come regola, Aurora Serverless è il doppio più costoso per unità (CPU e memoria) rispetto ad Aurora Provisioned. Risparmia costi solo se il workload è spiky e non gira a un livello costante."*

### Aurora Parallel Query (from PACKT)

*"Permette a certe query di essere eseguite direttamente contro il layer di storage, invece di passare attraverso il database stesso. Riduce lo strain sulla cache del database e riduce il consumo di memoria e CPU."*

### Aurora Fast Cloning (from PACKT)

*"Può creare una copia del tuo database in minuti, indipendentemente dalla dimensione. Usa il lazy loading: quando il clone legge dati, i blocchi vengono copiati nel suo storage."*

### Aurora Global Databases (from PACKT Ch.14)

*"Per applicazioni distribuite globalmente, offre letture a bassa latenza e replicazione cross-region veloce."*

---

## Amazon DynamoDB — In Depth

### Overview (from PACKT)

PACKT describes DynamoDB as *"un database fully managed, serverless, key-value pair progettato per supportare tempi di query sub-millisecondo a quasi qualsiasi scala, capace di gestire oltre 20 milioni di richieste al secondo."*

- **Fully managed**: AWS handles hardware provisioning, setup, configuration, replication, patching, scaling
- **Serverless**: scales elastically without provisioning specific servers — you only pay for what you use

### Capacity Modes (from PACKT)

| Mode | How it works | When to use it |
|---|---|---|
| **On-Demand** | Pay per read/write request. No provisioning | Unpredictable workloads, new tables |
| **Provisioned** | You specify Read Capacity Units (RCU) and Write Capacity Units (WCU) | Predictable workloads, lower costs |

> **PACKT note**: *"Se non hai abbastanza capacity units provisionati, potresti trovare che il database throttla o droppa connessioni."*

### Consistency Models (from PACKT)

| Type | Latency | Cost | Use |
|---|---|---|---|
| **Eventually Consistent** | Lower | 1 RCU = 2 reads/sec (4KB) | Default, most cases |
| **Strongly Consistent** | Slightly higher | 1 RCU = 1 read/sec (4KB) | When you need the most recent data |

### Indexes (from PACKT and Kimiko)

- **Primary Key**: partition key (required) + sort key (optional)
- **Local Secondary Index (LSI)**: same partition key, different sort key. Must be created at table creation
- **Global Secondary Index (GSI)**: different partition key and sort key. Can be created after. Kimiko: *"Questi permettono di fare query più efficienti basate su altri campi della tabella"*

### DynamoDB Streams (from PACKT and Kimiko)

PACKT describes: *"DynamoDB Streams cattura una sequenza ordinata nel tempo di modifiche a livello di item in una tabella DynamoDB. Può essere usato per triggerare Lambda functions in risposta a cambiamenti nei dati."*

Kimiko adds: *"Se attiviamo DynamoDB Streams, possiamo organizzare global tables che spannano regioni nel mondo."*

### Global Tables (from PACKT)

*"Le Global Tables forniscono una soluzione di database multi-Region, multi-active e fully managed. Replicano automaticamente le tabelle DynamoDB nelle Region AWS che scegli."*

### DynamoDB Accelerator — DAX (from PACKT and Kimiko)

PACKT describes DAX as *"una cache in-memory compatibile con DynamoDB che fornisce performance fino a 10x migliori — da millisecondi a microsecondi — anche con milioni di richieste al secondo."*

Kimiko clarifies the difference with ElastiCache: *"DAX è molto più facile da configurare, è seamless. Con ElastiCache per DynamoDB, devi fare manutenzione e tuning costante. Ci sono case study di aziende che sono migrate da ElastiCache+DynamoDB a DAX con grandi successi in performance e riduzione del carico amministrativo."*

### Other NoSQL Databases on AWS (from PACKT)

| Database | Type | Use case |
|---|---|---|
| **DocumentDB** | Document store (MongoDB compatible) | JSON data, content management |
| **Neptune** | Graph database | Complex relationships, social networks, fraud detection |
| **Keyspaces** | Wide-column (Cassandra compatible) | IoT, time-series data |
| **QLDB** | Ledger database | Immutable transactions, audit trail, supply chain |

---

## ElastiCache — In Depth (from Kimiko)

Kimiko explains: *"ElastiCache è un servizio gestito per due tipi di caching: Redis e Memcached. Questi sono molto popolari e la tua organizzazione potrebbe già usarli. Gli strumenti esistenti funzioneranno perfettamente contro la tua implementazione AWS."*

### Redis vs Memcached (from Kimiko and Dojo)

| Feature | Redis | Memcached |
|---|---|---|
| Complexity | More complex | Simpler |
| Data types | Supports complex types (lists, sets, hashes) | Whole object caching |
| Backup/Restore | **Yes** | No |
| Replication | Publisher/subscriber model, Multi-AZ | Scale out, multi-thread |
| Persistence | **Yes** | No |
| Cluster mode | Yes (enabled/disabled) | Yes |
| Use | When you need persistence, complex types, pub/sub | When you need simplicity and multi-threading |

### When to Use ElastiCache (from Dojo)

The Dojo is specific: *"Se hai item acceduti frequentemente, puoi cacharli in ElastiCache e ridurre il carico sulla tua istanza DB. ElastiCache non è una buona opzione se il database è più write-heavy che read-heavy. Confrontando cache e read replica: una cache è più adatta se l'applicazione interroga gli stessi item ripetutamente o i risultati sono statici. Se gli item letti variano troppo, una read replica potrebbe essere migliore."*

---

## Key Comparisons for the Exam

### Read Replica vs Multi-AZ vs Vertical Scaling vs ElastiCache (from Dojo)

| Solution | What it does | When to use it |
|---|---|---|
| **Read Replicas** | Horizontal read scaling. Asynchronous. Manual promotion to master. Cross-region possible | Read-heavy databases, reporting, analytics. *"Scaling sulla capacità di lettura riducendo il carico sulla primaria"* |
| **Multi-AZ** | HA with automatic failover. Synchronous (non-Aurora). Standby doesn't serve queries | When you need **availability**, not performance. *"Lo standby non può gestire query read e write"* |
| **Vertical Scaling** | More CPU, memory, throughput | When you need more read AND write resources. *"Best practice: alloca abbastanza RAM per il working set in memoria. Downtime minimo con Multi-AZ (failover allo standby upgradato)"* |
| **ElastiCache** | In-memory cache for frequently accessed data | Repetitive queries, static results. *"Non ideale per database write-heavy"* |

### Relational vs Non-Relational (from PACKT)

| Type | Service | Ideal for |
|---|---|---|
| **Relational** | RDS, Aurora | Complex queries, JOINs, transactional consistency (ACID), structured data, SQL |
| **Key-Value** | DynamoDB | Ultra-fast key lookups, massive scaling, simple access patterns |
| **Document** | DocumentDB | JSON data, content management |
| **Graph** | Neptune | Complex relationships between entities |
| **Wide-Column** | Keyspaces | IoT, time-series |
| **Ledger** | QLDB | Immutable transactions, audit |
| **Data Warehouse** | Redshift | Analytics on petabytes of structured data |

> **Exam tip (PACKT Ch.14)**: *"La differenza chiave è dati strutturati vs non strutturati. Se la domanda specifica il tipo di dati, questo ti aiuterà a eliminare risposte errate."*

---

## Typical Exam Scenarios

### Scenario 1: Read-heavy database with complex reports
**Question**: Complex reports are slowing down the production database.

**Answer**: **Read Replicas** — offload reporting queries to the replica (PACKT: *"Read replicas sono particolarmente utili per report con query complesse che causano rallentamenti"*).

### Scenario 2: HA with automatic failover
**Question**: The database must continue working if an AZ goes down.

**Answer**: **Multi-AZ** — automatic failover, automatic DNS change (Dojo). SLA 99.95% vs 99.5% single-AZ (PACKT).

### Scenario 3: Application with millions of requests/sec
**Question**: The application requires sub-millisecond latency with 20M+ requests/sec.

**Answer**: **DynamoDB** — *"Progettato per supportare tempi di query sub-millisecondo a quasi qualsiasi scala, capace di gestire oltre 20 milioni di richieste al secondo"* (PACKT).

### Scenario 4: Caching for DynamoDB
**Question**: You need caching for DynamoDB with minimal setup.

**Answer**: **DAX** — *"Performance fino a 10x migliori, da millisecondi a microsecondi. Molto più facile di ElastiCache per DynamoDB"* (PACKT, Kimiko).

### Scenario 5: Spiky workload with optimized costs
**Question**: The database has unpredictable traffic spikes. How to optimize costs?

**Answer**: **Aurora Serverless** — scales automatically. But beware: *"2x più costoso per unità rispetto ad Aurora Provisioned, risparmia solo se il workload è spiky"* (PACKT).

### Scenario 6: Many simultaneous connections with fast failover
**Question**: The application opens thousands of connections and failover must be as fast as possible.

**Answer**: **RDS Proxy** — connection pooling, *"mantiene le connessioni durante il failover invece di inviare errori"* (PACKT). But has additional cost.

### Scenario 7: Database with complex relationships (social network)
**Question**: The application must navigate complex relationships between millions of entities.

**Answer**: **Neptune** — graph database for complex relationships (PACKT).

### Scenario 8: Clone a database for testing
**Question**: You need a copy of the production database for testing, as quickly as possible.

**Answer**: **Aurora Fast Cloning** — *"Crea una copia in minuti, indipendentemente dalla dimensione"* (PACKT).

---

## Quick Recap for the Exam

- **RDS**: 6 engines + Aurora, backup 7-35 days, automatic patching, Multi-AZ (synchronous), Read Replicas (asynchronous) (PACKT, Dojo)
- **You cannot SSH to RDS** — use Parameter Groups for configuration (Dojo)
- **Multi-AZ**: HA, automatic failover, SLA 99.95%, standby doesn't serve queries, synchronous for non-Aurora (PACKT, Dojo)
- **Read Replicas**: read scaling, asynchronous, cross-region, manual promotion, potentially stale data (PACKT, Dojo)
- **Multi-AZ = availability, Read Replica = performance** (Dojo)
- **RDS Proxy**: connection pooling, fast failover, maintains connections, additional cost (PACKT)
- **Storage**: gp3 recommended (more flexible than gp2), io1/io2 for critical IOPS. You cannot reduce storage (PACKT)
- **Aurora**: MySQL/PostgreSQL, 5x/3x performance, decoupled storage up to 128 TiB, 2 endpoints, Fast Cloning, Parallel Query (PACKT)
- **Aurora Serverless**: auto-scale, 2x more expensive per unit, only for spiky workloads (PACKT)
- **DynamoDB**: serverless, key-value, sub-ms latency, 20M+ req/sec, On-Demand or Provisioned capacity (PACKT)
- **DynamoDB**: Eventually vs Strongly Consistent reads, GSI/LSI for flexible queries, Streams for triggers (PACKT)
- **DAX**: in-memory cache for DynamoDB, 10x performance, more seamless than ElastiCache (PACKT, Kimiko)
- **ElastiCache**: Redis (persistent, complex, pub/sub) vs Memcached (simple, multi-thread) (Kimiko, Dojo)
- **Cache for repetitive/static queries, Read Replica for variable queries** (Dojo)
- **Structured → RDS/Aurora, Key-Value → DynamoDB, Graph → Neptune, Document → DocumentDB, Ledger → QLDB** (PACKT)
