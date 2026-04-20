# Database Services - RDS, Aurora, DynamoDB, ElastiCache

> Fonti: PACKT Cap.7 (p.314-377), PACKT Cap.14 (p.561-568), KIMIKO (p.237-248), DOJO (p.135-158, p.278, p.280, p.284)

---

## Glossario: i servizi che incontrerai in questo documento

- **RDS (Relational Database Service)** — il servizio di database relazionali gestito da AWS. "Gestito" significa che AWS si occupa di: installazione, patching del sistema operativo, backup automatici, aggiornamenti del software del database. Tu ti occupi solo dei tuoi dati e delle tue query. Supporta MySQL, PostgreSQL, SQL Server, Oracle, MariaDB, DB2. È come avere un DBA (database administrator) che lavora 24/7 gratis per te sulla parte infrastrutturale.

- **Aurora** — il database relazionale proprietario di AWS. Compatibile con MySQL e PostgreSQL, ma progettato da zero per il cloud. Fino a 5x più veloce di MySQL e 3x più veloce di PostgreSQL. Lo storage è "decoupled" dall'istanza e scala automaticamente fino a 128 TB. Costa un po' di più di RDS standard ma offre performance e resilienza superiori.

- **DynamoDB** — il database NoSQL (non relazionale) di AWS. Invece di tabelle con righe e colonne collegate tra loro (come SQL), usa coppie chiave-valore e documenti JSON. Velocissimo (millisecondi di latenza) e scala automaticamente. Perfetto per applicazioni che hanno bisogno di risposte rapidissime con pattern di accesso semplici (es. carrello e-commerce, sessioni utente, gaming). Pensalo come un dizionario gigante: dai la chiave, ottieni il valore istantaneamente.

- **ElastiCache** — un servizio di cache in-memory. Mette i dati più richiesti in RAM per accesso ultra-rapido (microsecondi). Supporta Redis e Memcached. Esempio: invece di interrogare il database ogni volta che un utente carica la homepage, metti il risultato in cache. Le richieste successive leggono dalla cache (velocissimo) invece che dal database (più lento). Come tenere i documenti più usati sulla scrivania invece che nell'archivio.

- **Read Replica** — una copia di sola lettura del tuo database. Il database principale gestisce letture E scritture. La read replica gestisce SOLO le letture. Serve a: 1) alleggerire il carico sul database principale, 2) migliorare le performance di lettura. I dati vengono replicati automaticamente dal principale alla replica (in modo asincrono, quindi con un piccolo ritardo).

- **Multi-AZ** — significa avere una copia del database in un'altra Availability Zone. Se il database principale ha un problema, AWS fa failover automatico sulla copia. Il tuo database torna online in pochi minuti senza intervento manuale. La copia è sincrona (per non-Aurora) quindi non perdi dati.

- **RDS Proxy** — un intermediario tra la tua applicazione e il database. Gestisce un "pool" di connessioni per non sovraccaricare il database. Come un receptionist che gestisce la coda dei clienti invece di farli entrare tutti insieme nel negozio.

- **DAX (DynamoDB Accelerator)** — una cache in-memory specifica per DynamoDB. Riduce la latenza da millisecondi a microsecondi. A differenza di ElastiCache, è "seamless" — si integra nativamente con DynamoDB senza configurazione complessa.

- **Redshift** — il servizio di data warehousing di AWS. Per analizzare petabyte di dati con query SQL complesse. Non è per le operazioni quotidiane (quello è RDS), ma per analytics e business intelligence. Come la differenza tra il registro di cassa (RDS) e il report annuale delle vendite (Redshift).

---

## Panoramica

Il PACKT introduce: *"AWS attualmente offre 15 database diversi tra cui scegliere. Questo è un numero enorme, e quindi questo argomento è visto come uno dei più difficili da molti solutions architect. Per l'esame SAA-C03, dovrai conoscere i casi d'uso base e i benefici di ogni tipo di database."*

### Relational vs NoSQL (dal PACKT)

Il PACKT spiega la storia: *"Negli anni '70, quando i database divennero popolari, i costi di storage erano estremamente alti. Qualsiasi dato duplicato o ridondante era molto costoso. Per prevenire la duplicazione, le tabelle divennero un contenitore per un tipo di oggetto, collegate ad altre tabelle."* Esempio: una tabella Orders contiene solo orderID, customerID, productID. Per avere tutte le informazioni, devi cercare nelle tabelle Customers e Products.

I database relazionali sono ancora i più popolari al mondo (~50 ZB di dati). Ma hanno sfide: crescita dello storage, pattern di utilizzo spiky, patching, backup, HA testing.

---

## Amazon RDS — Relational Database Service

### Panoramica (dal PACKT, Kimiko, Dojo)

Il PACKT descrive RDS come un servizio per spostare database esistenti su AWS e delegare la gestione quotidiana.

Kimiko mostra il processo nella console: *"Possiamo avere Amazon che si occupa di tutto: backup, upgrade del software, sicurezza fisica, replicazione, alta disponibilità."* Mostra la creazione step-by-step: scegli Standard Create o Easy Create (best practice configurations), seleziona il motore (SQL Server, Oracle, PostgreSQL, MariaDB, MySQL, Aurora), la versione, l'ambiente (production/dev-test/free tier), le credenziali, l'instance size, lo storage (General Purpose SSD o Provisioned IOPS SSD).

Il Dojo aggiunge un confronto fondamentale: *"Puoi hostare il tuo database su un'istanza EC2 invece di usare RDS. Il problema è l'overhead di gestione: patching manuale, scaling dello storage, backup regolari, HA, monitoring CPU/memoria/storage. Con RDS, tutte queste attività sono significativamente ridotte o eliminate."*

**Motori supportati**: Oracle, SQL Server, MySQL, MariaDB, PostgreSQL, DB2, e **Amazon Aurora**.

### RDS vs Self-Hosted su EC2 (dal PACKT e Dojo)

| Caratteristica | RDS | Self-Hosted su EC2 |
|---|---|---|
| **Gestione OS** | AWS | Tu |
| **Patching DB** | Automatico (maintenance window) | Manuale |
| **Backup** | Automatici, point-in-time recovery | Manuali |
| **HA/Failover** | Multi-AZ con un click | Devi configurare replicazione e failover |
| **Scaling** | Cambi instance type con minimo downtime | Intervento manuale, complesso |
| **Accesso OS** | **Non puoi fare SSH/RDP** all'istanza sottostante (Dojo) | Pieno accesso |
| **Configurazione** | Via Parameter Groups e Option Groups (Dojo) | Modifica diretta file config (my.cnf, ecc.) |
| **Costo** | Potenzialmente più alto per il servizio gestito | Più basso ma più ore-uomo (PACKT) |
| **Flessibilità** | Limitata ai motori supportati | Qualsiasi database |

> **Nota Dojo**: *"A differenza di un database self-hosted, non puoi accedere direttamente all'istanza EC2 sottostante del tuo database RDS. Non puoi stabilire una connessione SSH o RDP. Usi Parameter Groups e Option Groups per la configurazione."*

### Backup (dal PACKT)

- Backup automatici salvati su S3, includono dati transazionali per **point-in-time recovery**
- Default: abilitati per **7 giorni**, massimo **35 giorni** di retention
- Storage backup gratuito fino alla dimensione del database allocato (es. 100 GB DB = 100 GB backup gratis)
- **Snapshot manuali**: possono essere condivisi con altri account, inviati in altre Region per DR
- Il Dojo aggiunge: *"Se stai pianificando un backup o snapshot, puoi usare l'istanza standby invece della primaria. In questo modo non sospendi le attività I/O del database di produzione."*

### Patching e Upgrade (dal PACKT)

- AWS automatizza patching e minor upgrade durante una **maintenance window** configurabile
- Con **Multi-AZ**: AWS patcha prima lo standby, fa switchover, poi patcha il vecchio primario → **zero downtime**
- AWS **non fa mai** upgrade automatici a major version (es. MySQL 5.7 → 8.0) — sempre manuali, via in-place upgrade, Blue/Green Deployments, o DMS
- **Extended Support**: costi aggiuntivi se non aggiorni quando la versione raggiunge fine supporto
- Se ritardi troppo gli upgrade e vai fuori dallo schedule pubblicato, *"AWS potrebbe forzare gli upgrade anche fuori dalla tua maintenance window, causando un outage inaspettato"* (PACKT)

### Multi-AZ — In Profondità (dal PACKT e Dojo)

Il PACKT spiega: *"Multi-AZ replica automaticamente il tuo database in un'AZ diversa e automatizza switchover e failover. Offre anche un SLA migliorato: Multi-AZ ha 99.95% uptime vs single-AZ con 99.5%."*

Il Dojo dettaglia il meccanismo:
- **Replicazione sincrona** per non-Aurora (MariaDB, MySQL, Oracle, PostgreSQL): *"Un update SQL committed viene scritto sia sull'istanza primaria che sulla standby simultaneamente"*
- **SQL Server** usa Database Mirroring (DBM) o Always On Availability Groups
- Lo standby **non può servire traffico di lettura** — per quello servono Read Replicas
- Quando converti da Single-AZ a Multi-AZ: *"RDS prende uno snapshot della primaria e lo ripristina in un'altra AZ, poi configura la replicazione sincrona"* (Dojo)
- In caso di failover: *"RDS cambia automaticamente il record DNS dell'istanza DB per puntare alla standby"* (Dojo)

### Read Replicas — In Profondità (dal PACKT e Dojo)

Il PACKT spiega il caso d'uso: *"Le read replicas sono particolarmente utili quando fai report con query complesse che possono causare rallentamenti sul database — queste query possono essere scaricate su un database diverso."*

Il Dojo fornisce dettagli tecnici:
- Replicazione **asincrona** — *"RDS scrive i dati sulla primaria PRIMA di scrivere sulla replica. Le repliche potrebbero restituire dati stale"*
- Puoi creare repliche nella **stessa AZ, diversa AZ, o diversa Region**
- La replicazione cross-Region richiede più tempo
- Basate sulle **feature di replicazione native** dei motori DB (MySQL, Oracle, ecc.)
- Possono essere **promosse manualmente** a istanza standalone — *"Quando promuovi una read replica, l'istanza DB viene riavviata prima di diventare disponibile"* (Dojo)
- Perfette per **OLTP** (Online Transaction Processing) — *"Un sito e-commerce è un tipo di applicazione OLTP che processa centinaia o migliaia di transazioni online all'ora"* (Dojo)

> **Differenza chiave Multi-AZ vs Read Replica**: Multi-AZ = **disponibilità** (failover automatico, standby non serve query). Read Replica = **performance** (scaling letture, asincrono, promozione manuale).

### Storage RDS (dal PACKT)

| Tipo | IOPS | Uso |
|---|---|---|
| **gp2** | 3 IOPS per GB, min 100 | La maggior parte dei casi |
| **gp3** | Min 3,000 IOPS (aumenta con storage), extra IOPS acquistabili | **Raccomandato** — più flessibile e spesso più economico di gp2 |
| **io1/io2** | Controllabili dall'utente | Database critici ad alte performance |

> **Nota PACKT**: *"Lo storage allocato controlla anche gli IOPS. Se hai bisogno di IOPS più alti di quelli allocati, vedrai le disk queue salire e le performance del database calare."*

> **Attenzione PACKT**: *"Puoi aumentare lo storage allocato senza downtime. Ma NON puoi ridurlo senza migrare a una nuova istanza. Alloca solo il minimo necessario."*

### Autenticazione RDS (dal PACKT e Dojo)

Tre opzioni:
1. **Username e password** — tradizionale, password salvata in Secrets Manager per rotazione
2. **IAM Authentication** — *"Crei un ruolo IAM con permesso di connessione e lo assegni agli utenti. IAM non concede permessi oltre il diritto di connettersi"* (PACKT). Il Dojo aggiunge: *"Migliora la sicurezza delle applicazioni su EC2 perché non devi salvare la password del database — usi l'instance profile per connetterti"*
3. **Kerberos/Active Directory** — per ambienti enterprise con AD

### RDS Proxy — In Profondità (dal PACKT)

Il PACKT dedica una sezione specifica: *"RDS Proxy è particolarmente utile per applicazioni con workload imprevedibili o che devono gestire molte connessioni simultanee. Fa pool e condivisione delle connessioni per ridurre l'overhead sul database."*

Benefici specifici dal PACKT:
- **Riduce downtime durante failover**: è costantemente consapevole dello stato del sistema RDS, può rilasciare sessioni appena il sistema è disponibile
- **Riduce errori applicativi**: durante un failover, *"RDS Proxy mantiene o mette in pausa le connessioni invece di inviare un errore. L'applicazione non deve gestire questi errori o reinviare le query — RDS Proxy le invia, in ordine, appena il failover è completo"*
- **Integrazione con Secrets Manager** per storage sicuro e rotazione automatica delle credenziali
- **Costo aggiuntivo** — *"Fai attenzione a frasi nell'esame che parlano di 'soluzione più cost-effective'"* (PACKT)

---

## Amazon Aurora — In Profondità

### Panoramica (dal PACKT)

Il PACKT descrive Aurora come il database relazionale proprietario di AWS: *"Combina le performance e la disponibilità di database commerciali high-end con la semplicità e il rapporto costo-efficacia dei database open source."*

Kimiko nota dalla console: *"Aurora è la selezione di default. Vedrai tutto il marketing language intorno ad Aurora — ottimizzazioni, risparmi, performance che non puoi ottenere in nessun altro modo."*

### Caratteristiche Chiave (dal PACKT)

- Compatibile con **MySQL e PostgreSQL** (solo questi due)
- Fino a **5x le performance di MySQL** e **3x di PostgreSQL**
- Storage **decoupled** dall'istanza — scala automaticamente fino a **128 TiB**
- Dati replicati su **multiple AZ** con backup continui su S3
- **Due endpoint**: uno per read-write, uno per read-only — Aurora instrada automaticamente al miglior istanza

### Aurora vs RDS Standard (dal PACKT)

| Caratteristica | RDS Standard | Aurora |
|---|---|---|
| Storage | Legato all'istanza, IOPS dipende da storage allocato | **Decoupled**, scala automaticamente, IOPS indipendente |
| Scaling letture | Read replicas manuali | Reader instances con **auto-scale basato su CPU** |
| Failover | Failover a standby Multi-AZ | Failover a **reader instances** (più opzioni) |
| Endpoint | Singolo | **Due endpoint** (read-write + read-only) |
| Performance | Standard | 5x MySQL, 3x PostgreSQL |
| Cloning | Snapshot + restore (lento) | **Fast Cloning** in minuti (lazy loading) |

### Aurora Serverless (dal PACKT)

*"A differenza delle istanze database tradizionali, Aurora Serverless regola automaticamente la capacità in base alla domanda dell'applicazione. Non devi provisionare o gestire istanze database manualmente."*

> **Nota PACKT**: *"Come regola, Aurora Serverless è il doppio più costoso per unità (CPU e memoria) rispetto ad Aurora Provisioned. Risparmia costi solo se il workload è spiky e non gira a un livello costante."*

### Aurora Parallel Query (dal PACKT)

*"Permette a certe query di essere eseguite direttamente contro il layer di storage, invece di passare attraverso il database stesso. Riduce lo strain sulla cache del database e riduce il consumo di memoria e CPU."*

### Aurora Fast Cloning (dal PACKT)

*"Può creare una copia del tuo database in minuti, indipendentemente dalla dimensione. Usa il lazy loading: quando il clone legge dati, i blocchi vengono copiati nel suo storage."*

### Aurora Global Databases (dal PACKT Cap.14)

*"Per applicazioni distribuite globalmente, offre letture a bassa latenza e replicazione cross-region veloce."*

---

## Amazon DynamoDB — In Profondità

### Panoramica (dal PACKT)

Il PACKT descrive DynamoDB come *"un database fully managed, serverless, key-value pair progettato per supportare tempi di query sub-millisecondo a quasi qualsiasi scala, capace di gestire oltre 20 milioni di richieste al secondo."*

- **Fully managed**: AWS gestisce hardware provisioning, setup, configurazione, replicazione, patching, scaling
- **Serverless**: scala elasticamente senza provisionare server specifici — paghi solo per quello che usi

### Capacity Modes (dal PACKT)

| Mode | Come funziona | Quando usarlo |
|---|---|---|
| **On-Demand** | Paghi per richiesta di lettura/scrittura. Nessun provisioning | Workload imprevedibili, nuove tabelle |
| **Provisioned** | Specifichi Read Capacity Units (RCU) e Write Capacity Units (WCU) | Workload prevedibili, costi più bassi |

> **Nota PACKT**: *"Se non hai abbastanza capacity units provisionati, potresti trovare che il database throttla o droppa connessioni."*

### Consistency Models (dal PACKT)

| Tipo | Latenza | Costo | Uso |
|---|---|---|---|
| **Eventually Consistent** | Più bassa | 1 RCU = 2 letture/sec (4KB) | Default, la maggior parte dei casi |
| **Strongly Consistent** | Leggermente più alta | 1 RCU = 1 lettura/sec (4KB) | Quando serve il dato più recente |

### Indici (dal PACKT e Kimiko)

- **Primary Key**: partition key (obbligatoria) + sort key (opzionale)
- **Local Secondary Index (LSI)**: stessa partition key, sort key diversa. Deve essere creato alla creazione della tabella
- **Global Secondary Index (GSI)**: partition key e sort key diverse. Può essere creato dopo. Kimiko: *"Questi permettono di fare query più efficienti basate su altri campi della tabella"*

### DynamoDB Streams (dal PACKT e Kimiko)

Il PACKT descrive: *"DynamoDB Streams cattura una sequenza ordinata nel tempo di modifiche a livello di item in una tabella DynamoDB. Può essere usato per triggerare Lambda functions in risposta a cambiamenti nei dati."*

Kimiko aggiunge: *"Se attiviamo DynamoDB Streams, possiamo organizzare global tables che spannano regioni nel mondo."*

### Global Tables (dal PACKT)

*"Le Global Tables forniscono una soluzione di database multi-Region, multi-active e fully managed. Replicano automaticamente le tabelle DynamoDB nelle Region AWS che scegli."*

### DynamoDB Accelerator — DAX (dal PACKT e Kimiko)

Il PACKT descrive DAX come *"una cache in-memory compatibile con DynamoDB che fornisce performance fino a 10x migliori — da millisecondi a microsecondi — anche con milioni di richieste al secondo."*

Kimiko chiarisce la differenza con ElastiCache: *"DAX è molto più facile da configurare, è seamless. Con ElastiCache per DynamoDB, devi fare manutenzione e tuning costante. Ci sono case study di aziende che sono migrate da ElastiCache+DynamoDB a DAX con grandi successi in performance e riduzione del carico amministrativo."*

### Altri Database NoSQL su AWS (dal PACKT)

| Database | Tipo | Caso d'uso |
|---|---|---|
| **DocumentDB** | Document store (MongoDB compatibile) | Dati JSON, content management |
| **Neptune** | Graph database | Relazioni complesse, social network, fraud detection |
| **Keyspaces** | Wide-column (Cassandra compatibile) | IoT, time-series data |
| **QLDB** | Ledger database | Transazioni immutabili, audit trail, supply chain |

---

## ElastiCache — In Profondità (da Kimiko)

Kimiko spiega: *"ElastiCache è un servizio gestito per due tipi di caching: Redis e Memcached. Questi sono molto popolari e la tua organizzazione potrebbe già usarli. Gli strumenti esistenti funzioneranno perfettamente contro la tua implementazione AWS."*

### Redis vs Memcached (da Kimiko e Dojo)

| Caratteristica | Redis | Memcached |
|---|---|---|
| Complessità | Più complesso | Più semplice |
| Tipi di dati | Supporta tipi complessi (liste, set, hash) | Caching di oggetti interi |
| Backup/Restore | **Sì** | No |
| Replicazione | Publisher/subscriber model, Multi-AZ | Scale out, multi-thread |
| Persistenza | **Sì** | No |
| Cluster mode | Sì (enabled/disabled) | Sì |
| Uso | Quando serve persistenza, tipi complessi, pub/sub | Quando serve semplicità e multi-threading |

### Quando Usare ElastiCache (dal Dojo)

Il Dojo è specifico: *"Se hai item acceduti frequentemente, puoi cacharli in ElastiCache e ridurre il carico sulla tua istanza DB. ElastiCache non è una buona opzione se il database è più write-heavy che read-heavy. Confrontando cache e read replica: una cache è più adatta se l'applicazione interroga gli stessi item ripetutamente o i risultati sono statici. Se gli item letti variano troppo, una read replica potrebbe essere migliore."*

---

## Confronti Chiave per l'Esame

### Read Replica vs Multi-AZ vs Vertical Scaling vs ElastiCache (dal Dojo)

| Soluzione | Cosa fa | Quando usarla |
|---|---|---|
| **Read Replicas** | Scaling orizzontale letture. Asincrono. Promozione manuale a master. Cross-region possibile | Database read-heavy, reporting, analytics. *"Scaling sulla capacità di lettura riducendo il carico sulla primaria"* |
| **Multi-AZ** | HA con failover automatico. Sincrono (non-Aurora). Standby non serve query | Quando serve **disponibilità**, non performance. *"Lo standby non può gestire query read e write"* |
| **Vertical Scaling** | Più CPU, memoria, throughput | Quando servono più risorse read E write. *"Best practice: alloca abbastanza RAM per il working set in memoria. Downtime minimo con Multi-AZ (failover allo standby upgradato)"* |
| **ElastiCache** | Cache in-memory per dati frequentemente acceduti | Query ripetitive, risultati statici. *"Non ideale per database write-heavy"* |

### Relational vs Non-Relational (dal PACKT)

| Tipo | Servizio | Ideale per |
|---|---|---|
| **Relational** | RDS, Aurora | Query complesse, JOIN, consistenza transazionale (ACID), dati strutturati, SQL |
| **Key-Value** | DynamoDB | Lookup per chiave ultra-veloci, scaling massivo, pattern di accesso semplici |
| **Document** | DocumentDB | Dati JSON, content management |
| **Graph** | Neptune | Relazioni complesse tra entità |
| **Wide-Column** | Keyspaces | IoT, time-series |
| **Ledger** | QLDB | Transazioni immutabili, audit |
| **Data Warehouse** | Redshift | Analytics su petabyte di dati strutturati |

> **Tip esame (PACKT Cap.14)**: *"La differenza chiave è dati strutturati vs non strutturati. Se la domanda specifica il tipo di dati, questo ti aiuterà a eliminare risposte errate."*

---

## Scenari Tipici d'Esame

### Scenario 1: Database read-heavy con report complessi
**Domanda**: Report complessi rallentano il database di produzione.

**Risposta**: **Read Replicas** — scarica le query di reporting sulla replica (PACKT: *"Read replicas sono particolarmente utili per report con query complesse che causano rallentamenti"*).

### Scenario 2: HA con failover automatico
**Domanda**: Il database deve continuare a funzionare se un'AZ va giù.

**Risposta**: **Multi-AZ** — failover automatico, cambio DNS automatico (Dojo). SLA 99.95% vs 99.5% single-AZ (PACKT).

### Scenario 3: Applicazione con milioni di richieste/sec
**Domanda**: L'applicazione richiede sub-millisecond latency con 20M+ richieste/sec.

**Risposta**: **DynamoDB** — *"Progettato per supportare tempi di query sub-millisecondo a quasi qualsiasi scala, capace di gestire oltre 20 milioni di richieste al secondo"* (PACKT).

### Scenario 4: Caching per DynamoDB
**Domanda**: Serve caching per DynamoDB con setup minimo.

**Risposta**: **DAX** — *"Performance fino a 10x migliori, da millisecondi a microsecondi. Molto più facile di ElastiCache per DynamoDB"* (PACKT, Kimiko).

### Scenario 5: Workload spiky con costi ottimizzati
**Domanda**: Il database ha picchi di traffico imprevedibili. Come ottimizzare i costi?

**Risposta**: **Aurora Serverless** — scala automaticamente. Ma attenzione: *"2x più costoso per unità rispetto ad Aurora Provisioned, risparmia solo se il workload è spiky"* (PACKT).

### Scenario 6: Molte connessioni simultanee con failover veloce
**Domanda**: L'applicazione apre migliaia di connessioni e il failover deve essere il più veloce possibile.

**Risposta**: **RDS Proxy** — connection pooling, *"mantiene le connessioni durante il failover invece di inviare errori"* (PACKT). Ma ha costo aggiuntivo.

### Scenario 7: Database con relazioni complesse (social network)
**Domanda**: L'applicazione deve navigare relazioni complesse tra milioni di entità.

**Risposta**: **Neptune** — graph database per relazioni complesse (PACKT).

### Scenario 8: Clonare un database per testing
**Domanda**: Serve una copia del database di produzione per testing, il più velocemente possibile.

**Risposta**: **Aurora Fast Cloning** — *"Crea una copia in minuti, indipendentemente dalla dimensione"* (PACKT).

---

## Riepilogo Veloce per l'Esame

- **RDS**: 6 engine + Aurora, backup 7-35 giorni, patching automatico, Multi-AZ (sincrono), Read Replicas (asincrono) (PACKT, Dojo)
- **Non puoi fare SSH a RDS** — usa Parameter Groups per configurazione (Dojo)
- **Multi-AZ**: HA, failover automatico, SLA 99.95%, standby non serve query, sincrono per non-Aurora (PACKT, Dojo)
- **Read Replicas**: scaling letture, asincrono, cross-region, promozione manuale, dati potenzialmente stale (PACKT, Dojo)
- **Multi-AZ = disponibilità, Read Replica = performance** (Dojo)
- **RDS Proxy**: connection pooling, failover veloce, mantiene connessioni, costo aggiuntivo (PACKT)
- **Storage**: gp3 raccomandato (più flessibile di gp2), io1/io2 per IOPS critiche. Non puoi ridurre storage (PACKT)
- **Aurora**: MySQL/PostgreSQL, 5x/3x performance, storage decoupled fino a 128 TiB, 2 endpoint, Fast Cloning, Parallel Query (PACKT)
- **Aurora Serverless**: auto-scale, 2x più costoso per unità, solo per workload spiky (PACKT)
- **DynamoDB**: serverless, key-value, sub-ms latency, 20M+ req/sec, On-Demand o Provisioned capacity (PACKT)
- **DynamoDB**: Eventually vs Strongly Consistent reads, GSI/LSI per query flessibili, Streams per trigger (PACKT)
- **DAX**: cache in-memory per DynamoDB, 10x performance, più seamless di ElastiCache (PACKT, Kimiko)
- **ElastiCache**: Redis (persistente, complesso, pub/sub) vs Memcached (semplice, multi-thread) (Kimiko, Dojo)
- **Cache per query ripetitive/statiche, Read Replica per query variabili** (Dojo)
- **Structured → RDS/Aurora, Key-Value → DynamoDB, Graph → Neptune, Document → DocumentDB, Ledger → QLDB** (PACKT)
