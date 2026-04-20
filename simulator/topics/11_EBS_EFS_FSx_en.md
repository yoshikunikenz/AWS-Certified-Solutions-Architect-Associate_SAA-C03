# EBS, EFS, FSx - Block, File and Specialized Storage

> Sources: PACKT Ch.5 (p.256-266), KIMIKO (p.163-168, p.200-203), DOJO (p.116-134, p.267, p.269-270, p.276)

---

## Glossary: the services you will encounter in this document

- **EBS (Elastic Block Store)** — the virtual hard drive you attach to an EC2 instance. Like the SSD or HDD of your computer, but in the cloud. Data persists even if you stop the instance. You can choose between SSD (fast, for databases) and HDD (slower, cheaper, for sequential data). Each EBS volume lives in a single AZ.

- **EFS (Elastic File System)** — a shared file system in the cloud. Unlike EBS (which attaches to ONE instance only), EFS can be mounted by MANY EC2 instances simultaneously. Like a shared network folder in the office, but in the cloud. Scales automatically. Uses the NFS protocol. Works best with Linux.

- **FSx for Windows File Server** — like EFS but for Windows. Uses the SMB protocol (the one for Windows shared folders), integrates with Active Directory, supports NTFS. If your application is Windows and needs shared files, this is the right service.

- **FSx for Lustre** — a very high-performance file system for HPC (High Performance Computing) and machine learning. Can reach hundreds of GB/s of throughput and millions of IOPS. Integrates with S3 to import/export data automatically. Linux only.

- **Instance Store** — storage physically attached to the EC2 instance's host server. The highest possible IOPS (it's a local disk, not network), but data is **lost** when the instance stops. Perfect for cache, buffers, temporary data.

- **AWS Backup** — a centralized service to manage backups of all your AWS services (EC2, EBS, RDS, DynamoDB, EFS) from a single point. You define a "backup plan" with schedule and retention, and AWS does everything automatically.

- **Storage Gateway** — a bridge between your on-premises data center and the AWS cloud. It's a VM you install in your environment that acts as a gateway to S3, EBS, or Glacier. Three variants: File Gateway (files via NFS/SMB → S3), Volume Gateway (block storage → AWS), Tape Gateway (emulates tape libraries → Glacier).

---

## Amazon EBS — Elastic Block Store

### Overview (from PACKT)

PACKT describes EBS as *"un servizio di block storage ad alte performance progettato per l'uso con EC2 per tutti i tipi di workload a qualsiasi scala. I volumi EBS sono automaticamente replicati all'interno della loro Availability Zone per proteggere i dati da guasti dei componenti."*

> **Critical PACKT note for the exam**: *"EBS non è shared storage. Non puoi attaccare simultaneamente un volume EBS a più di un'istanza EC2. Se hai bisogno di farlo per file condivisi, devi usare Amazon EFS. Questo dettaglio è spesso testato nell'esame."*

### SSD vs HDD — Exam Rule (from Dojo)

The Dojo provides a fundamental rule: *"Nell'esame, considera sempre la differenza tra SSD e HDD. Questo ti permetterà di eliminare facilmente tipi EBS specifici nelle opzioni."*

| Type | I/O Pattern | Use |
|---|---|---|
| **SSD** (gp2, gp3, io1, io2) | Consistent performance for both **random and sequential** I/O | Databases, boot volumes, interactive apps |
| **HDD** (st1, sc1) | Optimal performance only for **large and sequential** I/O | Big data, data warehouse, log processing, archival |

> **Rule**: question asks for small/random I/O → **SSD**. Question asks for large/sequential I/O → **HDD**.

### Volume Details (from Dojo)

| Volume | Type | IOPS | Durability | Use case |
|---|---|---|---|---|
| **gp3** | General Purpose SSD | 3,000 base, scalable | 99.8-99.9% | Virtual desktop, medium DB, dev/test, boot |
| **gp2** | General Purpose SSD | 3 per GB, burst | 99.8-99.9% | Boot volumes, interactive apps, dev/test |
| **io2** | Provisioned IOPS SSD | 500 IOPS per GiB | **99.999%** | Sub-millisecond latency, business-critical |
| **io1** | Provisioned IOPS SSD | Configurable | 99.8-99.9% | Latency-sensitive transactional |
| **st1** | Throughput Optimized HDD | Throughput-based | 99.8-99.9% | Big data, data warehouse, log processing |
| **sc1** | Cold HDD | Lowest cost | 99.8-99.9% | Cold data, rare access |

> **Dojo note**: *"io2 è un upgrade di io1 — offre durabilità 99.999% e ratio IOPS/GiB più alto (500 IOPS per GiB), allo stesso costo di io1."*

### EBS Volume Types (from PACKT)

| Type | Name | Use | Notes |
|---|---|---|---|
| **General Purpose SSD** | gp2, gp3 | Transactional workloads, boot volumes | gp3 allows scaling IOPS and throughput independently. Most commonly used |
| **Provisioned IOPS SSD** | io1, io2 | I/O-intensive workloads, databases | io2 offers superior durability and IOPS/GiB. For >16,000 IOPS or >250 MiB/s |
| **Throughput Optimized HDD** | st1 | Big data, data warehouse, log processing | High throughput, low cost. Cannot be used as boot volume |
| **Cold HDD** | sc1 | Rarely accessed data, archival | Lowest cost per GB of all EBS types |

### EBS vs Instance Store (from Dojo)

| Feature | EBS | Instance Store |
|---|---|---|
| **Definition** | Virtual disks mounted on EC2 for persistent storage | Physical disks mounted directly on the host computer |
| **Persistence** | Exists independently of the EC2 instance. Survives stop/terminate | **Deleted** when the instance stops, reboots, or terminates |
| **Types** | gp2/gp3, io1/io2, st1, sc1 | HDD, SSD, NVMe SSD |
| **Size** | Min 1 GiB, max 16 TiB. Resizable without downtime | Depends on instance type. Max 10 GB as root volume |
| **Remounting** | Can be detached and reattached to another EC2 instance | Not remountable — physically attached to the host |
| **Multi-attach** | Yes, for io1/io2 in the same AZ | Not supported |
| **Backup** | EBS Snapshots (incremental, saved to S3) | AMI backup only |

### Data Persistence and Snapshots (from PACKT)

PACKT explains: *"I dati su un volume EBS persistono indipendentemente dalla vita dell'istanza EC2 associata. Puoi anche staccare un volume EBS e spostarlo su un'istanza EC2 diversa."*

**EBS Snapshots** (from PACKT):
- **Incremental** — only blocks changed since the last snapshot are saved
- Can be used to create new volumes, move volumes between AZs
- Can be **shared with other accounts** — useful for creating test environments with production data

### EBS Resilience (from Kimiko)

Kimiko explains the resilience strategy: *"L'EBS è localizzato nell'AZ dove si trova l'istanza EC2 che ne ha bisogno. Ma puoi in qualsiasi momento fare uno snapshot point-in-time del volume EBS e poi parcheggiarlo in un'AZ diversa. Puoi prendere snapshot e assicurarti che vengano spostati in un'altra AZ, e poi puoi rapidamente lanciare una risorsa EC2 identica da quel volume EBS nella diversa AZ."*

> **PACKT note**: *"EBS non ha lifecycle policy o storage classes come S3. Se devi archiviare dati per compliance, devi copiare i dati su un sistema di storage diverso come S3 o EFS."*

---

## Amazon EFS — Elastic File System

### Overview (from PACKT)

PACKT describes EFS as *"un servizio di file storage cloud-native e scalabile che può essere usato simultaneamente da multiple istanze EC2. Con EFS, puoi scalare lo storage su o giù man mano che i file crescono o si riducono, senza gestire direttamente la capacità."*

EFS supports **thousands of concurrent NFS connections** and can also be used with on-premises computers (unlike EBS).

> **PACKT note for the exam**: *"EFS è progettato per e funziona meglio con sistemi operativi Linux. Se usi Windows, dovresti considerare Amazon FSx for Windows File Server. Questo può apparire nell'esame e cogliere gli studenti di sorpresa!"*

### EFS from Dojo — Comparison with EFS/FSx

The Dojo provides the key comparison:
- **EFS**: serverless, scalable, NFS protocol, access from EC2 Linux/ECS/EKS/Fargate/Lambda, auto-scale to petabytes, strong consistency and file locking, thousands of concurrent accesses
- **FSx for Windows**: SMB protocol, Active Directory integration, NTFS, access from Windows/Linux/MacOS
- **FSx for Lustre**: high-performance for HPC/ML, hundreds of GB/s throughput, millions of IOPS, S3 integration, **Linux only**

### Storage Classes and Lifecycle (from PACKT)

EFS offers only **two classes** (far fewer than S3):
- **Standard**: default, for frequently accessed files, lowest latency
- **Infrequent Access (IA)**: for infrequently accessed files, lower cost

You can create lifecycle policies to automatically move files between the two classes.

### Performance Modes (from PACKT)

| Mode | Use | Characteristic |
|---|---|---|
| **General Purpose** | Web hosting, CMS, home directory | Low latency, fast operations |
| **Max I/O** | Big data, ML, hundreds of servers | More parallel operations, slightly higher latency |

### Throughput Modes (from PACKT)

| Mode | How it works |
|---|---|
| **Bursting** | Throughput scales with file system size. Bursts for periods of high demand |
| **Provisioned** | You specify throughput independently of the amount of data stored |

> **PACKT note**: *"EFS non supporta snapshot. Per il backup, usa AWS Backup."*

### EFS Resilience (from Kimiko)

Kimiko explains: *"EFS sfrutta la replicazione automatica tra availability zone. Avrai grande resilienza lì."*

---

## Amazon FSx

### FSx for Windows File Server (from PACKT)

PACKT explains: *"Molti clienti che eseguono applicazioni Windows on-premises faticano a migrare su AWS perché dipendono da feature native Windows per gestire lo storage. FSx for Windows offre un file system Microsoft Windows nativo fully managed."*

Features: **SMB** protocol, **Active Directory** integration, **NTFS**.

### FSx for Lustre (from PACKT)

PACKT describes: *"Per HPC che spesso coinvolge ML o applicazioni AI avanzate che richiedono di processare enormi quantità di dati velocemente. FSx for Lustre si integra con Amazon S3, permettendo di linkare il file system con un bucket S3 per import/export automatico dei dati."*

### When to Use What (from Dojo)

| Service | Protocol | OS | Use case |
|---|---|---|---|
| **EFS** | NFS | Linux (EC2, ECS, EKS, Fargate, Lambda) | Web serving, CMS, analytics, containers |
| **FSx for Windows** | SMB | Windows, Linux, MacOS | CRM, ERP, .NET apps, home directory, Active Directory |
| **FSx for Lustre** | Lustre | **Linux only** | ML, HPC, video processing, financial modeling, genome sequencing |

---

## AWS Backup (from PACKT)

PACKT describes AWS Backup as a cross-service backup solution:
- Supports: EC2, EBS, RDS, DynamoDB, EFS and more
- Automated **backup plans** with schedule and retention rules
- **Encryption** with KMS
- **Lifecycle management**: transition to cold storage, automatic deletion
- **Cross-service**: manage backups of all services from a single console

---

## Storage Gateway (from Kimiko)

Kimiko explains: *"Storage Gateway è davvero tre prodotti. Hai una VM che ottieni da Amazon e questa VM viene implementata nel tuo ambiente on-premises. È il gateway tra il tuo ambiente on-premises e il cloud AWS."*

| Type | What it does |
|---|---|
| **File Gateway** | Interface to S3 — files accessible on-premises via NFS/SMB, stored in S3 |
| **Volume Gateway** | On-premises block storage with backup to AWS |
| **Tape Gateway** | Emulates tape libraries for cloud backup |

---

## Kimiko: Choosing Resilient Storage

Kimiko provides a resilience overview by storage type:

| Storage | Resilience |
|---|---|
| **S3** | Automatic replication across different AZs in the Region |
| **EBS** | Localized in one AZ, but snapshots can be copied to other AZs |
| **EFS** | Automatic cross-AZ replication |
| **FSx for Windows** | You can choose single-AZ or multi-AZ |

Kimiko also shows in the console how to choose the storage class for each individual S3 object: *"Siamo in grado di dettare cose come performance e resilienza appropriatamente per gli oggetti. Questo è estremamente potente."*

---

## Typical Exam Scenarios

### Scenario 1: Shared storage across multiple EC2 instances
**Question**: Multiple Linux EC2 instances need to access the same files simultaneously.

**Answer**: **EFS** (PACKT: *"EBS non è shared storage. Se hai bisogno di file condivisi, usa EFS"*).

### Scenario 2: Windows applications with Active Directory
**Question**: A Windows application requires file storage with AD integration and SMB protocol.

**Answer**: **FSx for Windows File Server** (PACKT: *"EFS è progettato per Linux. Se usi Windows, considera FSx for Windows"*).

### Scenario 3: HPC with data in S3
**Question**: A machine learning workload needs to process huge datasets stored in S3 with very high throughput.

**Answer**: **FSx for Lustre** — native S3 integration, hundreds of GB/s throughput (PACKT, Dojo).

### Scenario 4: Database with guaranteed IOPS
**Question**: A critical database requires consistent IOPS and low latency.

**Answer**: **EBS Provisioned IOPS SSD (io2)** — for >16,000 IOPS (PACKT).

### Scenario 5: Temporary storage with very high performance
**Question**: You need storage with the highest possible IOPS, data doesn't need to persist.

**Answer**: **Instance Store** — physically attached, NVMe SSD available (Dojo).

### Scenario 6: Centralized multi-service backup
**Question**: You need to manage backups of EC2, RDS, EFS, and DynamoDB from a single point.

**Answer**: **AWS Backup** — cross-service, automated backup plans (PACKT).

### Scenario 7: On-premises files accessible via S3
**Question**: On-premises users need to access files stored in S3 as if they were on a local file server.

**Answer**: **Storage Gateway (File Gateway)** — on-premises VM, NFS/SMB interface to S3 (Kimiko).

---

## Quick Recap for the Exam

- **EBS**: block storage, persistent, one instance at a time (except io1/io2 multi-attach), incremental snapshots (PACKT)
- **EBS types**: gp3 (general, recommended), gp2 (legacy), io2 (high IOPS, 99.999% durability), io1, st1 (throughput HDD), sc1 (cold HDD) (PACKT, Dojo)
- **SSD = random I/O, HDD = sequential I/O** — rule for eliminating exam answers (Dojo)
- **io2 > io1**: same price, 99.999% durability, 500 IOPS/GiB (Dojo)
- **Instance Store**: temporary, highest IOPS, deleted on stop — for cache/buffers/temporary data (Dojo)
- **EFS**: shared file storage, NFS, Linux, auto-scale, thousands of concurrent connections (PACKT, Dojo)
- **EFS ≠ Windows** — for Windows use FSx for Windows (PACKT)
- **FSx for Windows**: SMB, Active Directory, NTFS (PACKT, Dojo)
- **FSx for Lustre**: HPC/ML, Linux only, S3 integration, hundreds of GB/s (PACKT, Dojo)
- **EFS lifecycle**: only 2 classes (Standard, IA). No snapshots — use AWS Backup (PACKT)
- **EBS no lifecycle** — for archival use S3 (PACKT)
- **Storage Gateway**: 3 types (File/Volume/Tape), on-premises VM as bridge to AWS (Kimiko)
- **AWS Backup**: cross-service, backup plans, KMS encryption, lifecycle management (PACKT)
- **Resilience**: S3 auto-replicates cross-AZ, EBS snapshots for cross-AZ, EFS auto cross-AZ, FSx single or multi-AZ (Kimiko)
