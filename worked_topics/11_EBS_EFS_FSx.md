# EBS, EFS, FSx - Block, File e Specialized Storage

> Fonti: PACKT Cap.5 (p.256-266), KIMIKO (p.163-168, p.200-203), DOJO (p.116-134, p.267, p.269-270, p.276)

---

## Glossario: i servizi che incontrerai in questo documento

- **EBS (Elastic Block Store)** — il disco rigido virtuale che attacchi a un'istanza EC2. Come l'SSD o l'HDD del tuo computer, ma nel cloud. I dati persistono anche se spegni l'istanza. Puoi scegliere tra SSD (veloce, per database) e HDD (più lento, più economico, per dati sequenziali). Ogni volume EBS vive in una sola AZ.

- **EFS (Elastic File System)** — un file system condiviso nel cloud. A differenza di EBS (che si attacca a UNA sola istanza), EFS può essere montato da MOLTE istanze EC2 contemporaneamente. Come una cartella di rete condivisa in ufficio, ma nel cloud. Scala automaticamente. Usa il protocollo NFS. Funziona meglio con Linux.

- **FSx for Windows File Server** — come EFS ma per Windows. Usa il protocollo SMB (quello delle cartelle condivise Windows), si integra con Active Directory, supporta NTFS. Se la tua applicazione è Windows e ha bisogno di file condivisi, questo è il servizio giusto.

- **FSx for Lustre** — un file system ad altissime performance per HPC (High Performance Computing) e machine learning. Può raggiungere centinaia di GB/s di throughput e milioni di IOPS. Si integra con S3 per importare/esportare dati automaticamente. Solo per Linux.

- **Instance Store** — storage fisicamente attaccato al server host dell'istanza EC2. Le IOPS più alte possibili (è un disco locale, non di rete), ma i dati vengono **persi** quando l'istanza si ferma. Perfetto per cache, buffer, dati temporanei.

- **AWS Backup** — un servizio centralizzato per gestire i backup di tutti i tuoi servizi AWS (EC2, EBS, RDS, DynamoDB, EFS) da un unico punto. Definisci un "backup plan" con schedule e retention, e AWS fa tutto automaticamente.

- **Storage Gateway** — un ponte tra il tuo data center on-premises e il cloud AWS. È una VM che installi nel tuo ambiente e che fa da gateway verso S3, EBS o Glacier. Tre varianti: File Gateway (file via NFS/SMB → S3), Volume Gateway (block storage → AWS), Tape Gateway (emula librerie tape → Glacier).

---

## Amazon EBS — Elastic Block Store

### Panoramica (dal PACKT)

Il PACKT descrive EBS come *"un servizio di block storage ad alte performance progettato per l'uso con EC2 per tutti i tipi di workload a qualsiasi scala. I volumi EBS sono automaticamente replicati all'interno della loro Availability Zone per proteggere i dati da guasti dei componenti."*

> **Nota PACKT critica per l'esame**: *"EBS non è shared storage. Non puoi attaccare simultaneamente un volume EBS a più di un'istanza EC2. Se hai bisogno di farlo per file condivisi, devi usare Amazon EFS. Questo dettaglio è spesso testato nell'esame."*

### SSD vs HDD — Regola per l'Esame (dal Dojo)

Il Dojo fornisce una regola fondamentale: *"Nell'esame, considera sempre la differenza tra SSD e HDD. Questo ti permetterà di eliminare facilmente tipi EBS specifici nelle opzioni."*

| Tipo | I/O Pattern | Uso |
|---|---|---|
| **SSD** (gp2, gp3, io1, io2) | Performance consistenti sia per I/O **random che sequenziale** | Database, boot volumes, app interattive |
| **HDD** (st1, sc1) | Performance ottimali solo per I/O **grandi e sequenziali** | Big data, data warehouse, log processing, archivio |

> **Regola**: domanda chiede small/random I/O → **SSD**. Domanda chiede large/sequential I/O → **HDD**.

### Dettagli Volume (dal Dojo)

| Volume | Tipo | IOPS | Durabilità | Caso d'uso |
|---|---|---|---|---|
| **gp3** | General Purpose SSD | 3,000 base, scalabile | 99.8-99.9% | Virtual desktop, DB medio, dev/test, boot |
| **gp2** | General Purpose SSD | 3 per GB, burst | 99.8-99.9% | Boot volumes, app interattive, dev/test |
| **io2** | Provisioned IOPS SSD | 500 IOPS per GiB | **99.999%** | Sub-millisecond latency, business-critical |
| **io1** | Provisioned IOPS SSD | Configurabile | 99.8-99.9% | Latency-sensitive transactional |
| **st1** | Throughput Optimized HDD | Throughput-based | 99.8-99.9% | Big data, data warehouse, log processing |
| **sc1** | Cold HDD | Lowest cost | 99.8-99.9% | Dati cold, accesso raro |

> **Nota Dojo**: *"io2 è un upgrade di io1 — offre durabilità 99.999% e ratio IOPS/GiB più alto (500 IOPS per GiB), allo stesso costo di io1."*

### Tipi di Volume EBS (dal PACKT)

| Tipo | Nome | Uso | Note |
|---|---|---|---|
| **General Purpose SSD** | gp2, gp3 | Workload transazionali, boot volumes | gp3 permette di scalare IOPS e throughput indipendentemente. Il più usato |
| **Provisioned IOPS SSD** | io1, io2 | Workload I/O-intensive, database | io2 offre durabilità e IOPS/GiB superiori. Per >16,000 IOPS o >250 MiB/s |
| **Throughput Optimized HDD** | st1 | Big data, data warehouse, log processing | Alto throughput, basso costo. Non usabile come boot volume |
| **Cold HDD** | sc1 | Dati acceduti raramente, archivio | Costo più basso per GB di tutti i tipi EBS |

### EBS vs Instance Store (dal Dojo)

| Caratteristica | EBS | Instance Store |
|---|---|---|
| **Definizione** | Dischi virtuali montati su EC2 per storage persistente | Dischi fisici montati direttamente sull'host computer |
| **Persistenza** | Esiste indipendentemente dall'istanza EC2. Sopravvive a stop/terminate | **Cancellato** quando l'istanza si ferma, riavvia o termina |
| **Tipi** | gp2/gp3, io1/io2, st1, sc1 | HDD, SSD, NVMe SSD |
| **Dimensione** | Min 1 GiB, max 16 TiB. Ridimensionabile senza downtime | Dipende dal tipo di istanza. Max 10 GB come root volume |
| **Rimontaggio** | Può essere staccato e riattaccato a un'altra istanza EC2 | Non rimontabile — fisicamente attaccato all'host |
| **Multi-attach** | Sì, per io1/io2 nella stessa AZ | Non supportato |
| **Backup** | Snapshot EBS (incrementali, salvati su S3) | Solo backup AMI |

### Data Persistence e Snapshot (dal PACKT)

Il PACKT spiega: *"I dati su un volume EBS persistono indipendentemente dalla vita dell'istanza EC2 associata. Puoi anche staccare un volume EBS e spostarlo su un'istanza EC2 diversa."*

**Snapshot EBS** (dal PACKT):
- **Incrementali** — solo i blocchi cambiati dall'ultimo snapshot vengono salvati
- Possono essere usati per creare nuovi volumi, spostare volumi tra AZ
- Possono essere **condivisi con altri account** — utile per creare ambienti di test con dati di produzione

### Resilienza EBS (da Kimiko)

Kimiko spiega la strategia di resilienza: *"L'EBS è localizzato nell'AZ dove si trova l'istanza EC2 che ne ha bisogno. Ma puoi in qualsiasi momento fare uno snapshot point-in-time del volume EBS e poi parcheggiarlo in un'AZ diversa. Puoi prendere snapshot e assicurarti che vengano spostati in un'altra AZ, e poi puoi rapidamente lanciare una risorsa EC2 identica da quel volume EBS nella diversa AZ."*

> **Nota PACKT**: *"EBS non ha lifecycle policy o storage classes come S3. Se devi archiviare dati per compliance, devi copiare i dati su un sistema di storage diverso come S3 o EFS."*

---

## Amazon EFS — Elastic File System

### Panoramica (dal PACKT)

Il PACKT descrive EFS come *"un servizio di file storage cloud-native e scalabile che può essere usato simultaneamente da multiple istanze EC2. Con EFS, puoi scalare lo storage su o giù man mano che i file crescono o si riducono, senza gestire direttamente la capacità."*

EFS supporta **migliaia di connessioni NFS concorrenti** e può essere usato anche con computer on-premises (a differenza di EBS).

> **Nota PACKT per l'esame**: *"EFS è progettato per e funziona meglio con sistemi operativi Linux. Se usi Windows, dovresti considerare Amazon FSx for Windows File Server. Questo può apparire nell'esame e cogliere gli studenti di sorpresa!"*

### EFS dal Dojo — Confronto con EFS/FSx

Il Dojo fornisce il confronto chiave:
- **EFS**: serverless, scalabile, NFS protocol, accesso da EC2 Linux/ECS/EKS/Fargate/Lambda, auto-scale a petabyte, strong consistency e file locking, migliaia di accessi concorrenti
- **FSx for Windows**: SMB protocol, Active Directory integration, NTFS, accesso da Windows/Linux/MacOS
- **FSx for Lustre**: high-performance per HPC/ML, centinaia di GB/s throughput, milioni di IOPS, integrazione con S3, **solo Linux**

### Storage Classes e Lifecycle (dal PACKT)

EFS offre solo **due classi** (molto meno di S3):
- **Standard**: default, per file acceduti frequentemente, latenza più bassa
- **Infrequent Access (IA)**: per file non acceduti frequentemente, costo più basso

Puoi creare lifecycle policy per spostare file automaticamente tra le due classi.

### Performance Modes (dal PACKT)

| Mode | Uso | Caratteristica |
|---|---|---|
| **General Purpose** | Web hosting, CMS, home directory | Bassa latenza, operazioni rapide |
| **Max I/O** | Big data, ML, centinaia di server | Più operazioni in parallelo, latenza leggermente più alta |

### Throughput Modes (dal PACKT)

| Mode | Come funziona |
|---|---|
| **Bursting** | Throughput scala con la dimensione del file system. Burst per periodi di alta domanda |
| **Provisioned** | Specifichi il throughput indipendentemente dalla quantità di dati salvati |

> **Nota PACKT**: *"EFS non supporta snapshot. Per il backup, usa AWS Backup."*

### Resilienza EFS (da Kimiko)

Kimiko spiega: *"EFS sfrutta la replicazione automatica tra availability zone. Avrai grande resilienza lì."*

---

## Amazon FSx

### FSx for Windows File Server (dal PACKT)

Il PACKT spiega: *"Molti clienti che eseguono applicazioni Windows on-premises faticano a migrare su AWS perché dipendono da feature native Windows per gestire lo storage. FSx for Windows offre un file system Microsoft Windows nativo fully managed."*

Caratteristiche: protocollo **SMB**, integrazione **Active Directory**, **NTFS**.

### FSx for Lustre (dal PACKT)

Il PACKT descrive: *"Per HPC che spesso coinvolge ML o applicazioni AI avanzate che richiedono di processare enormi quantità di dati velocemente. FSx for Lustre si integra con Amazon S3, permettendo di linkare il file system con un bucket S3 per import/export automatico dei dati."*

### Quando Usare Cosa (dal Dojo)

| Servizio | Protocollo | OS | Caso d'uso |
|---|---|---|---|
| **EFS** | NFS | Linux (EC2, ECS, EKS, Fargate, Lambda) | Web serving, CMS, analytics, container |
| **FSx for Windows** | SMB | Windows, Linux, MacOS | CRM, ERP, .NET apps, home directory, Active Directory |
| **FSx for Lustre** | Lustre | **Solo Linux** | ML, HPC, video processing, financial modeling, genome sequencing |

---

## AWS Backup (dal PACKT)

Il PACKT descrive AWS Backup come soluzione per backup cross-service:
- Supporta: EC2, EBS, RDS, DynamoDB, EFS e altro
- **Backup plans** automatizzati con schedule e retention rules
- **Encryption** con KMS
- **Lifecycle management**: transizione a cold storage, cancellazione automatica
- **Cross-service**: gestisci backup di tutti i servizi da una singola console

---

## Storage Gateway (da Kimiko)

Kimiko spiega: *"Storage Gateway è davvero tre prodotti. Hai una VM che ottieni da Amazon e questa VM viene implementata nel tuo ambiente on-premises. È il gateway tra il tuo ambiente on-premises e il cloud AWS."*

| Tipo | Cosa fa |
|---|---|
| **File Gateway** | Interfaccia per S3 — file accessibili on-premises via NFS/SMB, salvati in S3 |
| **Volume Gateway** | Block storage on-premises con backup su AWS |
| **Tape Gateway** | Emula librerie di tape per backup su cloud |

---

## Kimiko: Scegliere lo Storage Resiliente

Kimiko fornisce una panoramica della resilienza per tipo di storage:

| Storage | Resilienza |
|---|---|
| **S3** | Replicazione automatica su diverse AZ nella Region |
| **EBS** | Localizzato in una AZ, ma snapshot possono essere copiati in altre AZ |
| **EFS** | Replicazione automatica cross-AZ |
| **FSx for Windows** | Puoi scegliere single-AZ o multi-AZ |

Kimiko mostra anche nella console come scegliere la storage class per ogni oggetto S3 individualmente: *"Siamo in grado di dettare cose come performance e resilienza appropriatamente per gli oggetti. Questo è estremamente potente."*

---

## Scenari Tipici d'Esame

### Scenario 1: Storage condiviso tra più istanze EC2
**Domanda**: Più istanze EC2 Linux devono accedere agli stessi file contemporaneamente.

**Risposta**: **EFS** (PACKT: *"EBS non è shared storage. Se hai bisogno di file condivisi, usa EFS"*).

### Scenario 2: Applicazioni Windows con Active Directory
**Domanda**: Un'applicazione Windows richiede file storage con integrazione AD e protocollo SMB.

**Risposta**: **FSx for Windows File Server** (PACKT: *"EFS è progettato per Linux. Se usi Windows, considera FSx for Windows"*).

### Scenario 3: HPC con dati in S3
**Domanda**: Un workload di machine learning deve processare dataset enormi salvati in S3 con altissimo throughput.

**Risposta**: **FSx for Lustre** — integrazione nativa con S3, centinaia di GB/s throughput (PACKT, Dojo).

### Scenario 4: Database con IOPS garantite
**Domanda**: Un database critico richiede IOPS consistenti e bassa latenza.

**Risposta**: **EBS Provisioned IOPS SSD (io2)** — per >16,000 IOPS (PACKT).

### Scenario 5: Storage temporaneo ad altissime performance
**Domanda**: Serve storage con le IOPS più alte possibili, i dati non devono persistere.

**Risposta**: **Instance Store** — fisicamente attaccato, NVMe SSD disponibile (Dojo).

### Scenario 6: Backup centralizzato multi-servizio
**Domanda**: Devi gestire backup di EC2, RDS, EFS e DynamoDB da un unico punto.

**Risposta**: **AWS Backup** — cross-service, backup plans automatizzati (PACKT).

### Scenario 7: File on-premises accessibili via S3
**Domanda**: Gli utenti on-premises devono accedere a file salvati in S3 come se fossero su un file server locale.

**Risposta**: **Storage Gateway (File Gateway)** — VM on-premises, interfaccia NFS/SMB verso S3 (Kimiko).

---

## Riepilogo Veloce per l'Esame

- **EBS**: block storage, persistente, una istanza alla volta (tranne io1/io2 multi-attach), snapshot incrementali (PACKT)
- **EBS types**: gp3 (general, raccomandato), gp2 (legacy), io2 (high IOPS, 99.999% durability), io1, st1 (throughput HDD), sc1 (cold HDD) (PACKT, Dojo)
- **SSD = random I/O, HDD = sequential I/O** — regola per eliminare risposte nell'esame (Dojo)
- **io2 > io1**: stessa price, durabilità 99.999%, 500 IOPS/GiB (Dojo)
- **Instance Store**: temporaneo, IOPS più alte, cancellato allo stop — per cache/buffer/dati temporanei (Dojo)
- **EFS**: file storage condiviso, NFS, Linux, auto-scale, migliaia di connessioni concorrenti (PACKT, Dojo)
- **EFS ≠ Windows** — per Windows usa FSx for Windows (PACKT)
- **FSx for Windows**: SMB, Active Directory, NTFS (PACKT, Dojo)
- **FSx for Lustre**: HPC/ML, solo Linux, integrazione S3, centinaia GB/s (PACKT, Dojo)
- **EFS lifecycle**: solo 2 classi (Standard, IA). No snapshot — usa AWS Backup (PACKT)
- **EBS no lifecycle** — per archiviazione usa S3 (PACKT)
- **Storage Gateway**: 3 tipi (File/Volume/Tape), VM on-premises come bridge verso AWS (Kimiko)
- **AWS Backup**: cross-service, backup plans, encryption KMS, lifecycle management (PACKT)
- **Resilienza**: S3 auto-replica cross-AZ, EBS snapshot per cross-AZ, EFS auto cross-AZ, FSx single o multi-AZ (Kimiko)
