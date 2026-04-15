#!/usr/bin/env python3
"""Generate PDF study guides for AWS SAA-C03 by category, based on exam questions."""

from fpdf import FPDF
import json
import textwrap

# ===== STUDY CONTENT PER CATEGORY =====
# Each guide covers the theory needed to answer the exam questions

GUIDES = {}

GUIDES['01-Storage'] = {
    'title': 'Storage',
    'icon': 'S3, EBS, EFS, FSx, Storage Gateway, Snow Family',
    'sections': [
        {
            'title': 'Amazon S3 (Simple Storage Service)',
            'content': """Amazon S3 e' un servizio di object storage con durabilita' 99.999999999% (11 nove).

Classi di storage:
- S3 Standard: accesso frequente, bassa latenza, alta disponibilita' (99.99%)
- S3 Intelligent-Tiering: sposta automaticamente gli oggetti tra tier in base ai pattern di accesso. Nessun costo di retrieval.
- S3 Standard-IA (Infrequent Access): per dati acceduti meno frequentemente ma che richiedono accesso rapido. Costo storage piu' basso, costo retrieval.
- S3 One Zone-IA: come Standard-IA ma in una sola AZ. Costo 20% inferiore. Per dati riproducibili.
- S3 Glacier Instant Retrieval: per archivi con accesso trimestrale. Retrieval in millisecondi.
- S3 Glacier Flexible Retrieval: retrieval in 1-5 minuti (Expedited), 3-5 ore (Standard), 5-12 ore (Bulk).
- S3 Glacier Deep Archive: costo piu' basso. Retrieval in 12 ore (Standard) o 48 ore (Bulk). Minimo 180 giorni.

Funzionalita' chiave:
- Versioning: mantiene versioni multiple degli oggetti. Protegge da cancellazioni accidentali.
- Lifecycle Policies: transizione automatica tra classi di storage o cancellazione dopo N giorni.
- S3 Transfer Acceleration: usa CloudFront edge locations per upload veloci su lunghe distanze.
- Multipart Upload: upload parallelo di parti per file grandi (obbligatorio sopra 5GB).
- Cross-Region Replication (CRR): replica oggetti tra bucket in regioni diverse. Richiede versioning.
- Same-Region Replication (SRR): replica nella stessa regione per compliance o aggregazione log.
- S3 Object Lock: WORM (Write Once Read Many). Governance mode o Compliance mode.
- S3 Select / Glacier Select: query SQL su oggetti senza scaricarli completamente.
- Server-Side Encryption: SSE-S3 (default), SSE-KMS (audit trail), SSE-C (chiave del cliente).
- Bucket Policies e ACL: controllo accessi a livello bucket e oggetto.
- S3 Event Notifications: trigger Lambda, SQS, SNS su eventi (PUT, DELETE, ecc.).
- S3 Static Website Hosting: hosting di siti statici direttamente da S3.
- Pre-signed URLs: accesso temporaneo a oggetti privati.
- S3 Access Points: endpoint dedicati con policy specifiche per diversi team/applicazioni."""
        },
        {
            'title': 'Amazon EBS (Elastic Block Store)',
            'content': """EBS fornisce volumi di block storage persistenti per EC2. Legato a una singola AZ.

Tipi di volume:
- gp3: SSD general purpose. 3000 IOPS base, fino a 16000 IOPS. Throughput fino a 1000 MB/s. Costo-efficace.
- gp2: SSD general purpose precedente. IOPS legati alla dimensione (3 IOPS/GB, burst fino a 3000).
- io2 Block Express: SSD ad alte prestazioni. Fino a 256000 IOPS, 4000 MB/s. Per database critici.
- io1: SSD provisioned IOPS. Fino a 64000 IOPS. Multi-attach possibile (fino a 16 istanze).
- st1: HDD throughput-optimized. Per big data, data warehouse. Non puo' essere boot volume.
- sc1: HDD cold. Costo piu' basso. Per dati acceduti raramente.

Concetti chiave:
- Snapshots: backup incrementali su S3. Possono essere copiati tra regioni.
- Encryption: AES-256 con KMS. Snapshots di volumi criptati sono criptati.
- Multi-Attach: solo io1/io2, permette di collegare un volume a piu' istanze nella stessa AZ.
- EBS-Optimized Instances: bandwidth dedicata per EBS (la maggior parte delle istanze moderne).
- RAID 0: striping per aumentare IOPS/throughput. RAID 1: mirroring per ridondanza."""
        },
        {
            'title': 'Amazon EFS (Elastic File System)',
            'content': """EFS e' un file system NFS managed, scalabile automaticamente, multi-AZ.

Caratteristiche:
- Protocollo NFSv4.1. Compatibile con istanze Linux (non Windows).
- Scala automaticamente da GB a PB senza provisioning.
- Multi-AZ: accessibile da piu' AZ contemporaneamente.
- Performance modes: General Purpose (bassa latenza) e Max I/O (alto throughput, latenza piu' alta).
- Throughput modes: Bursting (scala con dimensione), Provisioned (throughput fisso), Elastic (auto-scala).
- Storage classes: Standard e Infrequent Access (EFS-IA). Lifecycle policy per transizione automatica.
- EFS One Zone: costo inferiore, singola AZ. Per dev/test o dati riproducibili.
- Encryption at rest con KMS, in transit con TLS.
- Integrazione con ECS/Fargate per container stateful."""
        },
        {
            'title': 'Amazon FSx',
            'content': """FSx offre file system managed ad alte prestazioni.

FSx for Windows File Server:
- SMB protocol, Active Directory integration, NTFS.
- Per workload Windows: home directories, CMS, ERP.
- Multi-AZ per alta disponibilita'. Backup automatici su S3.
- Supporta DFS (Distributed File System) per namespace unificato.

FSx for Lustre:
- File system parallelo ad alte prestazioni per HPC, ML, media processing.
- Integrazione nativa con S3: legge/scrive direttamente su bucket S3.
- Scratch: storage temporaneo, alte prestazioni, nessuna replica. Per processing breve.
- Persistent: replica i dati nella stessa AZ. Per storage a lungo termine.
- Throughput fino a centinaia di GB/s, milioni di IOPS.

FSx for NetApp ONTAP:
- Compatibile con NFS, SMB, iSCSI. Multi-protocol.
- Compressione, deduplicazione, thin provisioning automatici.
- SnapMirror per replica tra regioni.

FSx for OpenZFS:
- Compatibile NFS. Snapshots, compressione, cloning."""
        },
        {
            'title': 'AWS Storage Gateway e Snow Family',
            'content': """Storage Gateway: ponte tra on-premises e cloud storage.

Tipi di gateway:
- S3 File Gateway: interfaccia NFS/SMB verso S3. Cache locale per accesso a bassa latenza.
- FSx File Gateway: cache locale per FSx for Windows File Server.
- Volume Gateway (Stored): volumi iSCSI completi on-premises, snapshot asincroni su S3.
- Volume Gateway (Cached): dati primari su S3, cache locale per dati frequenti.
- Tape Gateway: backup su nastro virtuale verso S3 Glacier. Compatibile con software di backup esistente.

AWS Snow Family:
- Snowcone: 8TB (HDD) o 14TB (SSD). Portatile, per edge computing e trasferimento dati.
- Snowball Edge Storage Optimized: 80TB. Per migrazione dati massiva.
- Snowball Edge Compute Optimized: 42TB + GPU opzionale. Per edge computing.
- Snowmobile: container da 100PB. Per migrazioni su scala exabyte.
- Tutti supportano crittografia e possono eseguire Lambda/EC2 localmente.

AWS DataSync:
- Trasferimento dati automatizzato tra on-premises e AWS (S3, EFS, FSx).
- Fino a 10x piu' veloce di strumenti open-source. Scheduling, verifica integrita'.
- Agente on-premises necessario. Trasferimento via internet o Direct Connect.

AWS Backup:
- Servizio centralizzato per backup di EBS, RDS, DynamoDB, EFS, FSx, EC2, S3.
- Backup plans con scheduling, retention, cross-region copy.
- Vault Lock per WORM compliance."""
        },
    ]
}

GUIDES['02-Compute'] = {
    'title': 'Compute',
    'icon': 'EC2, Lambda, ECS, EKS, Fargate, Elastic Beanstalk',
    'sections': [
        {
            'title': 'Amazon EC2 (Elastic Compute Cloud)',
            'content': """EC2 fornisce capacita' di calcolo ridimensionabile nel cloud.

Tipi di istanze (famiglie):
- General Purpose (M, T): bilanciamento CPU/memoria. T3/T4g con crediti burst.
- Compute Optimized (C): per workload CPU-intensive. Batch, HPC, gaming, ML inference.
- Memory Optimized (R, X, z): per database in-memory, cache, real-time processing.
- Storage Optimized (I, D, H): alto I/O sequenziale. Data warehouse, HDFS, database distribuiti.
- Accelerated Computing (P, G, Inf, Trn): GPU/FPGA per ML training, video encoding, HPC.

Modelli di acquisto:
- On-Demand: paga al secondo/ora. Nessun impegno. Per workload imprevedibili.
- Reserved Instances (RI): 1 o 3 anni. Sconto fino al 72%. Standard RI o Convertible RI.
- Savings Plans: impegno su spesa oraria ($/hr) per 1-3 anni. Piu' flessibile delle RI.
- Spot Instances: sconto fino al 90%. Possono essere interrotte con 2 minuti di preavviso.
  Ideali per batch, CI/CD, big data, workload fault-tolerant.
- Dedicated Hosts: server fisico dedicato. Per licenze software server-bound (BYOL).
- Dedicated Instances: istanze su hardware dedicato ma senza controllo sul server fisico.
- Capacity Reservations: riserva capacita' in una AZ specifica senza sconto.

Placement Groups:
- Cluster: istanze vicine nella stessa rack. Bassa latenza, alto throughput. Per HPC.
- Spread: istanze su hardware diverso. Max 7 per AZ. Per alta disponibilita'.
- Partition: gruppi di istanze su rack separate. Per HDFS, Cassandra, Kafka.

User Data: script eseguito al primo avvio dell'istanza per configurazione automatica.
Instance Metadata: informazioni sull'istanza accessibili da http://169.254.169.254.
AMI (Amazon Machine Image): template per lanciare istanze. Regione-specifica, copiabile tra regioni."""
        },
        {
            'title': 'Auto Scaling e Load Balancing',
            'content': """Auto Scaling Group (ASG):
- Scala automaticamente il numero di istanze EC2 in base alla domanda.
- Parametri: min, max, desired capacity.
- Scaling policies: Target Tracking (mantieni CPU al 50%), Step Scaling, Simple Scaling, Scheduled.
- Predictive Scaling: usa ML per prevedere il traffico e scalare in anticipo.
- Cooldown period: tempo di attesa tra azioni di scaling per evitare oscillazioni.
- Health checks: EC2 (default) o ELB. Istanze unhealthy vengono terminate e sostituite.
- Launch Template: definisce AMI, tipo istanza, security group, user data per le nuove istanze.

Elastic Load Balancer (ELB):
- Application Load Balancer (ALB): Layer 7 (HTTP/HTTPS). Path-based e host-based routing.
  Supporta WebSocket, HTTP/2, gRPC. Target groups: EC2, IP, Lambda, container.
  Sticky sessions con cookie. Integrazione con WAF e Cognito.
- Network Load Balancer (NLB): Layer 4 (TCP/UDP/TLS). Milioni di richieste/sec, latenza ultra-bassa.
  IP statico per AZ (o Elastic IP). Per performance estrema, protocolli non-HTTP.
- Gateway Load Balancer (GWLB): Layer 3. Per appliance di rete (firewall, IDS/IPS).
  Usa GENEVE protocol. Transparent network gateway + load balancer.
- Classic Load Balancer: legacy, Layer 4/7. Non raccomandato per nuove applicazioni.

Cross-Zone Load Balancing: distribuisce traffico uniformemente tra tutte le istanze in tutte le AZ.
Connection Draining (Deregistration Delay): tempo per completare richieste in-flight prima di deregistrare."""
        },
        {
            'title': 'Container: ECS, EKS, Fargate',
            'content': """Amazon ECS (Elastic Container Service):
- Orchestratore container managed di AWS. Supporta Docker.
- Launch types: EC2 (gestisci le istanze) o Fargate (serverless).
- Task Definition: blueprint del container (immagine, CPU, memoria, porte, volumi).
- Service: mantiene N task in esecuzione. Integrazione con ALB/NLB.
- ECR (Elastic Container Registry): registry Docker managed. Scan vulnerabilita' integrato.

Amazon EKS (Elastic Kubernetes Service):
- Kubernetes managed. Per chi ha gia' competenze/workload Kubernetes.
- Supporta EC2 e Fargate come worker nodes.
- EKS Anywhere: Kubernetes on-premises gestito da AWS.

AWS Fargate:
- Serverless compute per container. Nessuna gestione di istanze EC2.
- Paga per vCPU e memoria usata dal container.
- Compatibile con ECS e EKS.
- Ideale per microservizi, batch jobs, applicazioni event-driven.

AWS App Runner:
- Servizio fully managed per deploy di container o codice sorgente.
- Auto-scaling, HTTPS, load balancing automatici. Per applicazioni web semplici."""
        },
        {
            'title': 'AWS Lambda e Serverless',
            'content': """AWS Lambda:
- Compute serverless. Esegue codice in risposta a eventi. Paga solo per il tempo di esecuzione.
- Timeout massimo: 15 minuti. Memoria: 128MB - 10GB. Storage temporaneo: /tmp fino a 10GB.
- Concurrency: default 1000 per regione. Reserved concurrency per garantire capacita'.
- Provisioned Concurrency: mantiene istanze "calde" per eliminare cold start.
- Trigger: API Gateway, S3, DynamoDB Streams, SQS, SNS, EventBridge, Kinesis, CloudWatch Events.
- Layers: librerie condivise tra funzioni. Fino a 5 layer per funzione.
- VPC: Lambda puo' accedere a risorse in VPC (RDS, ElastiCache) tramite ENI.
- Lambda@Edge / CloudFront Functions: esecuzione ai margini della rete CDN.
- Destinations: invia risultati (successo/fallimento) a SQS, SNS, Lambda, EventBridge.

AWS Step Functions:
- Orchestrazione di workflow serverless. Coordina Lambda, ECS, API Gateway, ecc.
- Standard Workflows: fino a 1 anno, exactly-once execution.
- Express Workflows: fino a 5 minuti, at-least-once, alto volume.

Elastic Beanstalk:
- PaaS: deploy automatico di applicazioni web. Gestisce EC2, ASG, ELB, RDS.
- Supporta Java, .NET, PHP, Node.js, Python, Ruby, Go, Docker.
- Ambienti: Web Server (HTTP) e Worker (SQS background processing).
- Rolling, Rolling with additional batch, Immutable, Blue/Green deployment."""
        },
    ]
}

GUIDES['03-Networking'] = {
    'title': 'Networking',
    'icon': 'VPC, CloudFront, Route 53, Direct Connect, VPN, Transit Gateway',
    'sections': [
        {
            'title': 'Amazon VPC (Virtual Private Cloud)',
            'content': """VPC e' la rete virtuale isolata in AWS. Ogni VPC e' regione-specifica.

Componenti:
- Subnets: segmenti di rete in una AZ. Pubbliche (con route a Internet Gateway) o private.
- Internet Gateway (IGW): permette comunicazione tra VPC e internet. Una per VPC.
- NAT Gateway: permette a istanze in subnet private di accedere a internet (outbound only).
  Managed, alta disponibilita' in una AZ. Creare uno per AZ per resilienza.
- NAT Instance: alternativa self-managed su EC2. Meno consigliata, piu' economica.
- Route Tables: regole di routing per ogni subnet. Main route table + custom.
- Elastic IP: indirizzo IPv4 statico pubblico. Associabile a istanze o NAT Gateway.
- CIDR blocks: range IP del VPC (es. 10.0.0.0/16). Espandibile con secondary CIDR.

Security:
- Security Groups: firewall stateful a livello di istanza. Solo regole ALLOW. Default: deny all inbound.
  Possono referenziare altri security groups (es. permettere traffico dal SG del load balancer).
- Network ACL (NACL): firewall stateless a livello di subnet. Regole ALLOW e DENY con priorita' numerica.
  Default NACL: permette tutto. Custom NACL: nega tutto di default.
  Utile per bloccare IP specifici.

VPC Endpoints:
- Gateway Endpoint: per S3 e DynamoDB. Gratuito. Aggiunge route nella route table.
- Interface Endpoint (PrivateLink): ENI con IP privato. Per la maggior parte dei servizi AWS.
  Costo orario + costo per GB. Accessibile da on-premises via VPN/Direct Connect.

VPC Flow Logs: cattura informazioni sul traffico IP nelle interfacce di rete. Verso CloudWatch o S3.
VPC Peering: connessione diretta tra due VPC (anche cross-account/cross-region). Non transitiva.
Traffic Mirroring: copia del traffico di rete per analisi/monitoring."""
        },
        {
            'title': 'Connettivita Ibrida: VPN e Direct Connect',
            'content': """AWS Site-to-Site VPN:
- Connessione IPsec criptata tra on-premises e VPC via internet.
- Virtual Private Gateway (VGW) lato AWS, Customer Gateway lato on-premises.
- Due tunnel per alta disponibilita'. Bandwidth limitata (~1.25 Gbps per tunnel).
- Setup rapido (minuti). Costo basso. Per connettivita' immediata o backup di Direct Connect.

AWS Client VPN:
- VPN managed per utenti remoti. OpenVPN-based.
- Autenticazione: Active Directory, SAML, certificati mutual.

AWS Direct Connect:
- Connessione fisica dedicata tra on-premises e AWS. 1Gbps o 10Gbps (o hosted: 50Mbps-10Gbps).
- Latenza consistente, bandwidth elevata. Setup: settimane/mesi.
- Virtual Interfaces: Public VI (servizi pubblici AWS), Private VI (VPC), Transit VI (Transit Gateway).
- Direct Connect Gateway: connette Direct Connect a VPC in piu' regioni.
- Encryption: Direct Connect non e' criptato di default. Usare VPN over Direct Connect per crittografia.
- Resilienza: due connessioni in location diverse per alta disponibilita'.

AWS Transit Gateway:
- Hub centrale per connettere VPC, VPN, Direct Connect. Routing transitivo.
- Semplifica topologie complesse (hub-and-spoke). Supporta migliaia di VPC.
- Peering tra Transit Gateway in regioni diverse.
- Route tables multiple per segmentazione del traffico.
- Multicast support."""
        },
        {
            'title': 'Amazon CloudFront e Route 53',
            'content': """Amazon CloudFront (CDN):
- Content Delivery Network globale. 400+ edge locations.
- Origini: S3 bucket, ALB, EC2, HTTP server custom, MediaStore.
- Origin Access Control (OAC): accesso sicuro a S3 solo tramite CloudFront (sostituisce OAI).
- Cache behaviors: regole per path pattern diversi (es. /api/* verso ALB, /* verso S3).
- TTL: controlla quanto a lungo il contenuto resta in cache. Invalidation per forzare refresh.
- Lambda@Edge: esegue Lambda nelle edge locations (viewer/origin request/response).
- CloudFront Functions: piu' leggere di Lambda@Edge, per manipolazioni semplici di header/URL.
- Geo Restriction: blocca o permette accesso da paesi specifici.
- Signed URLs / Signed Cookies: accesso a contenuti privati con scadenza temporale.
- Field-Level Encryption: crittografia di campi specifici nei form POST.
- HTTPS: certificato ACM gratuito. Redirect HTTP to HTTPS. SNI per multi-domain.

Amazon Route 53 (DNS):
- DNS managed + health checking + traffic routing.
- Record types: A, AAAA, CNAME, Alias, MX, TXT, NS, SOA.
- Alias record: specifico AWS. Punta a risorse AWS (ELB, CloudFront, S3, ecc.). Gratuito per query.
  Non puo' puntare a un record CNAME. Puo' essere usato per zone apex (es. example.com).

Routing policies:
- Simple: un record, un valore (o piu' valori, scelti random dal client).
- Weighted: distribuisce traffico in percentuale tra risorse. Per blue/green deployment.
- Latency-based: instrada verso la regione con latenza piu' bassa per l'utente.
- Failover: active-passive. Health check determina quale risorsa servire.
- Geolocation: routing basato sulla posizione geografica dell'utente.
- Geoproximity: routing basato sulla distanza geografica. Bias per spostare traffico.
- Multi-value: come Simple ma con health check su ogni valore. Fino a 8 record healthy.
- IP-based: routing basato sull'IP del client. Per ottimizzazione ISP.

Health Checks: monitorano endpoint (HTTP, HTTPS, TCP). Integrazione con CloudWatch Alarms.
DNSSEC: firma digitale dei record DNS per prevenire spoofing."""
        },
        {
            'title': 'AWS Global Accelerator',
            'content': """Global Accelerator migliora disponibilita' e performance di applicazioni globali.

- Fornisce 2 IP anycast statici come punto di ingresso globale.
- Traffico instradato sulla rete privata AWS (non internet pubblico) verso l'endpoint piu' vicino.
- Endpoint groups in piu' regioni: ALB, NLB, EC2, Elastic IP.
- Health checking integrato con failover automatico tra regioni.
- Differenza con CloudFront: GA opera a Layer 4 (TCP/UDP), CloudFront a Layer 7 (HTTP).
  GA e' per applicazioni non-HTTP (gaming, IoT, VoIP) o che richiedono IP statici.
  CloudFront e' per contenuti HTTP/HTTPS con caching."""
        },
    ]
}

GUIDES['04-Databases'] = {
    'title': 'Databases',
    'icon': 'RDS, Aurora, DynamoDB, ElastiCache, Redshift, Neptune',
    'sections': [
        {
            'title': 'Amazon RDS (Relational Database Service)',
            'content': """RDS e' un servizio managed per database relazionali.

Engine supportati: MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, IBM Db2.

Caratteristiche:
- Multi-AZ: replica sincrona in standby AZ. Failover automatico (1-2 minuti). Per alta disponibilita'.
  Lo standby NON e' leggibile. Solo per failover.
- Read Replicas: replica asincrona per scalare le letture. Fino a 15 repliche.
  Possono essere cross-region. Promuovibili a database standalone.
  Costo di rete: gratuito nella stessa regione, a pagamento cross-region.
- Automated Backups: backup giornaliero + transaction logs ogni 5 minuti. Retention 0-35 giorni.
  Point-in-time recovery fino a 5 minuti fa.
- Manual Snapshots: backup manuali che persistono anche dopo la cancellazione del database.
- Encryption: at rest con KMS (deve essere abilitata alla creazione). In transit con SSL/TLS.
  Per criptare un DB non criptato: snapshot -> copia criptata -> restore.
- IAM Authentication: per MySQL e PostgreSQL. Token temporanei invece di password.
- RDS Proxy: connection pooling managed. Riduce failover time del 66%. Per Lambda + RDS.
- Storage Auto Scaling: aumenta automaticamente lo storage quando necessario.
- RDS Custom: per Oracle e SQL Server. Accesso al sistema operativo e database per personalizzazioni."""
        },
        {
            'title': 'Amazon Aurora',
            'content': """Aurora e' il database relazionale cloud-native di AWS. Compatibile MySQL e PostgreSQL.

Performance: fino a 5x MySQL e 3x PostgreSQL. Storage auto-scaling fino a 128TB.

Architettura:
- 6 copie dei dati su 3 AZ. Continua a funzionare con perdita di 2 copie (write) o 3 copie (read).
- Storage separato dal compute. Self-healing, auto-expanding.
- Writer endpoint: punta sempre all'istanza primaria.
- Reader endpoint: load balancing tra read replicas (fino a 15).

Funzionalita':
- Aurora Serverless v2: scala automaticamente la capacita' (ACU). Per workload variabili/imprevedibili.
  Scala in incrementi di 0.5 ACU. Paga per ACU usati al secondo.
- Aurora Global Database: replica cross-region con lag < 1 secondo. Fino a 5 regioni secondarie.
  Promozione di una regione secondaria in < 1 minuto per disaster recovery.
- Aurora Multi-Master: tutte le istanze possono scrivere. Per alta disponibilita' in scrittura.
- Backtrack: "riavvolgi" il database a un punto nel tempo senza restore. Solo Aurora MySQL.
- Cloning: crea una copia del database in secondi usando copy-on-write. Per test/dev.
- Aurora Machine Learning: integrazione con SageMaker e Comprehend direttamente nelle query SQL."""
        },
        {
            'title': 'Amazon DynamoDB',
            'content': """DynamoDB e' un database NoSQL key-value e document, fully managed, serverless.

Caratteristiche:
- Latenza single-digit millisecond a qualsiasi scala.
- Tabelle con partition key (obbligatoria) e sort key (opzionale).
- Capacity modes: On-Demand (paga per richiesta) o Provisioned (RCU/WCU con auto-scaling).
- RCU: 1 strongly consistent read/sec per item fino a 4KB. 2 eventually consistent reads.
- WCU: 1 write/sec per item fino a 1KB.

Funzionalita' avanzate:
- DynamoDB Accelerator (DAX): cache in-memory per DynamoDB. Latenza microsecondo.
  Compatibile con API DynamoDB. Per read-heavy workload.
- Global Tables: replica multi-region active-active. Scritture in qualsiasi regione.
  Richiede DynamoDB Streams abilitato.
- DynamoDB Streams: cattura modifiche alla tabella in tempo reale. Trigger Lambda.
  Retention 24 ore. Per event-driven architectures, replica, analytics.
- TTL (Time to Live): cancellazione automatica di item scaduti. Gratuito.
- Point-in-time Recovery (PITR): backup continuo con restore a qualsiasi secondo negli ultimi 35 giorni.
- Transactions: operazioni ACID su piu' item/tabelle. 2x costo di RCU/WCU.
- PartiQL: query SQL-like su DynamoDB.
- S3 export/import: esporta tabella su S3 in formato Parquet o DynamoDB JSON."""
        },
        {
            'title': 'ElastiCache, Redshift e altri database',
            'content': """Amazon ElastiCache:
- Cache in-memory managed. Due engine:
- Redis: strutture dati avanzate, persistence, replica, cluster mode, pub/sub, Lua scripting.
  Multi-AZ con auto-failover. Backup e restore. Encryption. Per session store, leaderboard, geospatial.
- Memcached: semplice key-value cache. Multi-threaded. Nessuna persistence/replica.
  Per caching semplice, session store senza persistence.
- Strategie di caching: Lazy Loading (cache on read miss), Write-Through (cache on write).

Amazon Redshift:
- Data warehouse colonnare basato su PostgreSQL. Per analytics e BI su petabyte di dati.
- Redshift Spectrum: query su dati in S3 senza caricarli in Redshift.
- Redshift Serverless: auto-scaling senza gestione cluster.
- Concurrency Scaling: aggiunge capacita' automaticamente per query concorrenti.
- AQUA: cache hardware-accelerated per query piu' veloci.
- Cross-region snapshots per disaster recovery.
- Non e' Multi-AZ (single AZ). Per HA: multi-node cluster + snapshots cross-region.

Amazon Neptune: database a grafo managed. Per social network, knowledge graph, fraud detection.
Amazon DocumentDB: compatibile MongoDB. Per document database managed.
Amazon Keyspaces: compatibile Apache Cassandra. Serverless.
Amazon QLDB: ledger database immutabile. Per audit trail, supply chain.
Amazon Timestream: database time-series. Per IoT, DevOps monitoring."""
        },
    ]
}

GUIDES['05-Security'] = {
    'title': 'Security',
    'icon': 'IAM, KMS, WAF, Shield, GuardDuty, Cognito, Secrets Manager',
    'sections': [
        {
            'title': 'AWS IAM (Identity and Access Management)',
            'content': """IAM gestisce autenticazione e autorizzazione per le risorse AWS.

Componenti:
- Users: identita' per persone o applicazioni. Credenziali: password (console) + access keys (API).
- Groups: raccolta di utenti. Le policy si applicano al gruppo.
- Roles: identita' temporanea assumibile da utenti, servizi o account esterni.
  EC2 Instance Role: permette a EC2 di accedere ad altri servizi AWS senza access keys.
  Cross-account Role: permette accesso da un altro account AWS.
  Service-linked Role: predefinito per un servizio AWS specifico.
- Policies: documenti JSON che definiscono permessi. Effect (Allow/Deny), Action, Resource, Condition.
  AWS Managed Policies: predefinite da AWS. Customer Managed: create dall'utente.
  Inline Policies: embedded direttamente in user/group/role.

Principi:
- Least Privilege: concedi solo i permessi necessari.
- Explicit Deny vince sempre su Allow.
- Policy Evaluation: deny di default -> valuta tutte le policy -> explicit deny vince.

Funzionalita':
- MFA (Multi-Factor Authentication): virtual MFA, hardware token, U2F key.
- Password Policy: lunghezza minima, complessita', rotazione.
- IAM Access Analyzer: identifica risorse condivise con entita' esterne.
- IAM Credentials Report: report su tutti gli utenti e lo stato delle credenziali.
- STS (Security Token Service): genera credenziali temporanee per AssumeRole.
- Permission Boundaries: limite massimo di permessi per un utente/ruolo.
- Service Control Policies (SCP): in AWS Organizations, limitano i permessi per account/OU."""
        },
        {
            'title': 'Crittografia: KMS, CloudHSM, ACM',
            'content': """AWS KMS (Key Management Service):
- Servizio managed per creare e gestire chiavi di crittografia.
- CMK (Customer Master Key): AWS managed, Customer managed, o AWS owned.
- Symmetric keys (AES-256): default, usate dalla maggior parte dei servizi AWS.
- Asymmetric keys (RSA, ECC): per encrypt/decrypt o sign/verify fuori da AWS.
- Key rotation: automatica ogni anno per customer managed keys.
- Key policies: controllano chi puo' usare/gestire la chiave.
- Envelope Encryption: KMS genera una data key, usata per criptare i dati localmente.
  GenerateDataKey API: restituisce plaintext + encrypted data key.
- Multi-Region Keys: stessa chiave replicata in piu' regioni. Per encrypt in una regione, decrypt in un'altra.
- Grants: permessi temporanei su una chiave senza modificare la key policy.

AWS CloudHSM:
- Hardware Security Module dedicato. FIPS 140-2 Level 3.
- Gestione completa delle chiavi da parte del cliente (AWS non ha accesso).
- Per requisiti di compliance stringenti, SSL/TLS offloading, Oracle TDE.
- Cluster multi-AZ per alta disponibilita'.

AWS Certificate Manager (ACM):
- Provisioning e gestione di certificati SSL/TLS gratuiti.
- Rinnovo automatico per certificati emessi da ACM.
- Integrazione con ALB, CloudFront, API Gateway.
- Per EC2: importare certificati manualmente (ACM non si integra direttamente con EC2)."""
        },
        {
            'title': 'Protezione: WAF, Shield, GuardDuty, Inspector',
            'content': """AWS WAF (Web Application Firewall):
- Protegge da attacchi web comuni (SQL injection, XSS, ecc.).
- Si applica a ALB, CloudFront, API Gateway, AppSync.
- Web ACL con regole: IP match, geo match, rate limiting, string match, regex.
- AWS Managed Rules: set di regole predefinite (OWASP Top 10, bot control, ecc.).
- Rate-based rules: blocca IP che superano una soglia di richieste.

AWS Shield:
- Shield Standard: protezione DDoS gratuita, automatica per tutti i clienti AWS.
  Protegge da attacchi Layer 3/4 (SYN flood, UDP reflection, ecc.).
- Shield Advanced: protezione DDoS avanzata. $3000/mese.
  Protezione Layer 7, DDoS Response Team (DRT) 24/7, cost protection (rimborso costi scaling).
  Si applica a EC2, ELB, CloudFront, Global Accelerator, Route 53.

Amazon GuardDuty:
- Threat detection intelligente. Analizza CloudTrail, VPC Flow Logs, DNS Logs, S3 Data Events.
- Rileva: account compromessi, istanze compromesse, reconnaissance, crypto mining.
- Machine learning per ridurre falsi positivi. Findings inviati a EventBridge.
- Delegated administrator in Organizations per gestione centralizzata.

Amazon Inspector:
- Vulnerability assessment automatizzato per EC2, container ECR, Lambda.
- Scansiona CVE, network reachability, best practices.
- Findings con severity score e remediation suggerita.

Amazon Macie:
- Scopre e protegge dati sensibili (PII) in S3 usando machine learning.
- Classifica automaticamente i dati. Alert su accessi anomali."""
        },
        {
            'title': 'Identita: Cognito, SSO, Directory Service',
            'content': """Amazon Cognito:
- User Pools: directory utenti per sign-up/sign-in. MFA, social login (Google, Facebook, SAML).
  Restituisce JWT token. Per autenticazione di applicazioni web/mobile.
- Identity Pools (Federated Identities): credenziali AWS temporanee per accesso diretto a servizi AWS.
  Supporta utenti anonimi. Integrazione con User Pools, social providers, SAML.
- Flusso tipico: User Pool autentica -> Identity Pool fornisce credenziali AWS -> accesso a S3/DynamoDB.

AWS IAM Identity Center (ex SSO):
- Single Sign-On centralizzato per account AWS e applicazioni cloud.
- Integrazione con Active Directory, SAML 2.0 identity providers.
- Permission Sets: definiscono i permessi per ogni account AWS.

AWS Directory Service:
- AWS Managed Microsoft AD: Active Directory managed su AWS. Trust con AD on-premises.
- AD Connector: proxy verso AD on-premises. Nessun dato in cloud.
- Simple AD: directory standalone basata su Samba. Per esigenze semplici.

AWS Secrets Manager:
- Gestione di segreti (password DB, API keys). Rotazione automatica con Lambda.
- Integrazione nativa con RDS, Redshift, DocumentDB per rotazione automatica.
- Costo: $0.40/segreto/mese + $0.05 per 10000 API calls.

AWS Systems Manager Parameter Store:
- Key-value store per configurazioni e segreti. Gratuito per parametri standard.
- SecureString: criptato con KMS. Nessuna rotazione automatica nativa.
- Gerarchia: /app/prod/db-password. Policy di accesso granulari."""
        },
    ]
}

GUIDES['06-Serverless'] = {
    'title': 'Serverless & Application Integration',
    'icon': 'Lambda, API Gateway, SQS, SNS, EventBridge, Step Functions, Kinesis',
    'sections': [
        {
            'title': 'Amazon SQS (Simple Queue Service)',
            'content': """SQS e' un servizio di message queuing fully managed.

Standard Queue:
- Throughput illimitato. At-least-once delivery (possibili duplicati).
- Best-effort ordering (ordine non garantito).
- Retention: 4 giorni default, max 14 giorni.
- Message size: max 256KB. Per messaggi piu' grandi: Extended Client Library con S3.

FIFO Queue:
- First-In-First-Out: ordine garantito. Exactly-once processing.
- Throughput: 300 msg/sec (senza batching), 3000 msg/sec (con batching).
- Message Group ID: ordine garantito all'interno del gruppo.
- Deduplication ID: previene duplicati in una finestra di 5 minuti.

Funzionalita':
- Visibility Timeout: tempo in cui un messaggio e' invisibile dopo essere stato letto. Default 30 sec.
  Se il consumer non lo cancella entro il timeout, torna visibile per altri consumer.
- Dead Letter Queue (DLQ): coda per messaggi che falliscono N volte (maxReceiveCount).
  Utile per debug. Impostare retention della DLQ piu' lunga della coda principale.
- Long Polling: riduce chiamate API vuote. WaitTimeSeconds fino a 20 sec.
- Delay Queue: ritarda la consegna dei messaggi. Fino a 15 minuti.
- SQS + Lambda: Lambda poll automaticamente la coda. Batch size configurabile.
- SQS + ASG: CloudWatch metric (ApproximateNumberOfMessages) per scalare EC2."""
        },
        {
            'title': 'Amazon SNS, EventBridge e Kinesis',
            'content': """Amazon SNS (Simple Notification Service):
- Pub/Sub messaging. Un messaggio, molti subscriber.
- Topic types: Standard (best-effort ordering) e FIFO (ordine garantito, solo SQS FIFO subscriber).
- Subscriber: SQS, Lambda, HTTP/S, Email, SMS, mobile push.
- Fan-out pattern: SNS topic -> multiple SQS queues per processing parallelo.
- Message filtering: policy JSON per filtrare messaggi per subscriber.
- Encryption: at rest con KMS, in transit con HTTPS.

Amazon EventBridge (ex CloudWatch Events):
- Event bus serverless. Connette applicazioni con eventi.
- Default event bus: eventi AWS (EC2 state change, S3, ecc.).
- Custom event bus: eventi da applicazioni custom.
- Partner event bus: eventi da SaaS (Zendesk, Datadog, ecc.).
- Rules: pattern matching su eventi -> target (Lambda, SQS, Step Functions, ecc.).
- Schema Registry: scopre e registra la struttura degli eventi.
- Archive & Replay: archivia eventi e riproducili per debug/test.
- Scheduler: cron/rate expressions per eventi schedulati.

Amazon Kinesis:
- Kinesis Data Streams: streaming dati in tempo reale. Shard-based (1MB/sec in, 2MB/sec out per shard).
  Retention: 24 ore default, fino a 365 giorni. Per real-time analytics, log aggregation.
  Consumer: KCL (Kinesis Client Library), Lambda, Kinesis Data Analytics.
  Enhanced fan-out: 2MB/sec per consumer per shard (push model).
- Kinesis Data Firehose: carica streaming data in S3, Redshift, OpenSearch, Splunk.
  Near real-time (buffer 60 sec minimo). Trasformazione con Lambda. Fully managed.
- Kinesis Data Analytics: SQL o Apache Flink su streaming data. Per real-time dashboards.
- Kinesis Video Streams: streaming video da dispositivi per analytics e ML."""
        },
        {
            'title': 'Amazon API Gateway',
            'content': """API Gateway e' un servizio managed per creare, pubblicare e gestire API.

Tipi di API:
- REST API: feature complete. Caching, throttling, API keys, usage plans, WAF.
- HTTP API: piu' semplice e economico. Per proxy Lambda/HTTP. Nessun caching.
- WebSocket API: comunicazione bidirezionale real-time. Per chat, gaming, dashboard live.

Funzionalita':
- Stages: ambienti (dev, staging, prod) con variabili di stage.
- Throttling: 10000 req/sec default, 5000 burst. Per-method throttling.
- Caching: riduce chiamate al backend. TTL 300 sec default. Da 0.5GB a 237GB.
- Authorization: IAM, Lambda Authorizer (custom), Cognito User Pools.
- API Keys + Usage Plans: per limitare e monitorare l'uso da parte di clienti.
- Request/Response transformation: mapping templates con VTL.
- CORS: configurabile per accesso cross-origin.
- Canary deployment: instrada percentuale di traffico a una nuova versione.
- Integration types: Lambda, HTTP, AWS Service, Mock, VPC Link (per risorse private)."""
        },
    ]
}

GUIDES['07-Monitoring'] = {
    'title': 'Monitoring, Logging & Automation',
    'icon': 'CloudWatch, CloudTrail, Config, Systems Manager, CloudFormation',
    'sections': [
        {
            'title': 'Amazon CloudWatch',
            'content': """CloudWatch e' il servizio di monitoring e observability di AWS.

Metrics:
- Metriche predefinite: CPU, Network, Disk (per EC2), RequestCount (per ELB), ecc.
- Custom Metrics: inviate via PutMetricData API. Risoluzione: standard (1 min) o high-res (1 sec).
- EC2 Detailed Monitoring: metriche ogni 1 minuto (default: 5 minuti). Costo aggiuntivo.
- Nota: RAM e disk space NON sono metriche predefinite EC2. Richiedono CloudWatch Agent.

Alarms:
- Monitorano una metrica e eseguono azioni quando supera una soglia.
- Stati: OK, ALARM, INSUFFICIENT_DATA.
- Azioni: SNS notification, Auto Scaling action, EC2 action (stop, terminate, reboot).
- Composite Alarms: combinano piu' alarms con AND/OR per ridurre rumore.

Logs:
- CloudWatch Logs: raccoglie e archivia log da EC2, Lambda, ECS, Route 53, ecc.
- Log Groups -> Log Streams. Retention configurabile (1 giorno - 10 anni o mai).
- Metric Filters: estraggono metriche custom dai log (es. contare errori).
- Logs Insights: query interattive sui log con linguaggio dedicato.
- Subscription Filters: streaming real-time verso Lambda, Kinesis, OpenSearch.
- Cross-account log sharing con Subscription Filters.

CloudWatch Agent:
- Installato su EC2 per raccogliere metriche OS (RAM, disk, processi) e log applicativi.
- Configurazione via SSM Parameter Store.

EventBridge (ex CloudWatch Events): vedi sezione Serverless.
CloudWatch Dashboards: visualizzazione personalizzata di metriche. Cross-region e cross-account."""
        },
        {
            'title': 'AWS CloudTrail e AWS Config',
            'content': """AWS CloudTrail:
- Registra tutte le chiamate API nel tuo account AWS. Chi ha fatto cosa, quando, da dove.
- Management Events: operazioni su risorse (CreateBucket, RunInstances). Abilitati di default.
- Data Events: operazioni sui dati (GetObject S3, Invoke Lambda). Non abilitati di default.
- Insights Events: rileva attivita' anomale (burst di API calls, errori).
- Trail: consegna log a S3 bucket e/o CloudWatch Logs. Multi-region trail raccomandato.
- Organization Trail: trail per tutti gli account in AWS Organizations.
- Log file integrity validation: verifica che i log non siano stati modificati.
- Retention: 90 giorni in CloudTrail console. Illimitata su S3.

AWS Config:
- Registra e valuta la configurazione delle risorse AWS nel tempo.
- Config Rules: regole per verificare compliance (es. "tutti i bucket S3 devono essere criptati").
  AWS Managed Rules (200+) o Custom Rules (Lambda).
- Remediation: azioni automatiche per correggere risorse non conformi (via SSM Automation).
- Configuration Recorder: registra cambiamenti di configurazione.
- Aggregator: vista multi-account/multi-region della compliance.
- Conformance Packs: pacchetti di Config Rules per framework di compliance (PCI-DSS, HIPAA).
- Config non previene i cambiamenti, li registra e valuta dopo."""
        },
        {
            'title': 'AWS Systems Manager e CloudFormation',
            'content': """AWS Systems Manager (SSM):
- Gestione operativa di risorse AWS e on-premises.
- SSM Agent: installato su EC2 (preinstallato su Amazon Linux 2, Windows). Richiede IAM role.
- Session Manager: accesso shell sicuro a EC2 senza SSH, bastion host o porte aperte.
  Logging su S3/CloudWatch. Audit trail completo.
- Run Command: esegue comandi su flotte di istanze senza SSH. Documenti predefiniti o custom.
- Patch Manager: automatizza patching OS e applicazioni. Patch baselines e maintenance windows.
- Parameter Store: vedi sezione Security.
- State Manager: mantiene configurazione desiderata sulle istanze.
- Inventory: raccoglie metadata su istanze (software installato, configurazioni).
- Automation: workflow per task operativi (es. creare AMI, resize istanze).
- Maintenance Windows: finestre temporali per task di manutenzione.

AWS CloudFormation:
- Infrastructure as Code (IaC). Template YAML/JSON per creare stack di risorse.
- Stack: insieme di risorse create da un template. Update e delete gestiti.
- Change Sets: preview delle modifiche prima di applicarle.
- Drift Detection: rileva modifiche manuali alle risorse dello stack.
- StackSets: deploy di stack su piu' account/regioni in Organizations.
- Nested Stacks: riutilizzo di template come componenti.
- Cross-stack references: Export/Import di valori tra stack.
- Rollback: automatico in caso di errore durante create/update.
- DeletionPolicy: Retain, Snapshot, Delete. Per proteggere risorse alla cancellazione dello stack.

AWS CDK (Cloud Development Kit): definisci infrastruttura con linguaggi di programmazione (TypeScript, Python, Java). Genera template CloudFormation."""
        },
    ]
}

GUIDES['08-CostOptimization'] = {
    'title': 'Cost Optimization & Well-Architected',
    'icon': 'Cost Explorer, Budgets, Trusted Advisor, Organizations, Well-Architected',
    'sections': [
        {
            'title': 'Gestione Costi AWS',
            'content': """AWS Cost Explorer:
- Visualizza e analizza costi e utilizzo AWS. Grafici e report personalizzabili.
- Forecast: previsione costi futuri basata su trend storici.
- Rightsizing Recommendations: suggerimenti per ridimensionare istanze EC2 sottoutilizzate.
- Savings Plans Recommendations: suggerimenti per acquistare Savings Plans.

AWS Budgets:
- Imposta budget su costi, utilizzo, RI coverage, Savings Plans.
- Alert via SNS/email quando si supera una soglia (actual o forecast).
- Budget Actions: azioni automatiche (es. applicare SCP, fermare istanze).

AWS Cost and Usage Report (CUR):
- Report dettagliato su tutti i costi AWS. Consegnato a S3.
- Integrabile con Athena, QuickSight, Redshift per analisi avanzate.

AWS Trusted Advisor:
- Raccomandazioni su 5 pilastri: Cost Optimization, Performance, Security, Fault Tolerance, Service Limits.
- Basic: check limitati (security groups, IAM, MFA su root, S3 bucket permissions).
- Business/Enterprise Support: tutti i check + API access + CloudWatch integration.

AWS Compute Optimizer:
- Analizza utilizzo di EC2, ASG, Lambda, EBS e raccomanda configurazioni ottimali.
- Usa machine learning su metriche CloudWatch.

Strategie di risparmio:
- Reserved Instances / Savings Plans per workload stabili.
- Spot Instances per workload fault-tolerant.
- S3 Lifecycle Policies per spostare dati in classi piu' economiche.
- Rightsizing: ridimensiona istanze sovradimensionate.
- Elimina risorse inutilizzate (EBS volumes, Elastic IPs, vecchi snapshots).
- Usa servizi serverless (Lambda, Fargate, DynamoDB on-demand) per workload variabili."""
        },
        {
            'title': 'AWS Organizations e Multi-Account',
            'content': """AWS Organizations:
- Gestione centralizzata di piu' account AWS.
- Organizational Units (OU): raggruppamento gerarchico di account.
- Consolidated Billing: fattura unica per tutti gli account. Volume discounts condivisi.
  RI e Savings Plans condivisi tra account nell'organizzazione.
- Service Control Policies (SCP): limiti di permessi per account/OU.
  Non concedono permessi, li limitano. Non si applicano al management account.
  Esempio: impedire la cancellazione di CloudTrail, forzare una regione specifica.

AWS Control Tower:
- Setup e governance automatizzata di ambienti multi-account.
- Landing Zone: ambiente multi-account pre-configurato con best practices.
- Guardrails: regole preventive (SCP) e detective (Config Rules).
- Account Factory: provisioning automatizzato di nuovi account.

AWS RAM (Resource Access Manager):
- Condivisione di risorse tra account (subnet, Transit Gateway, Route 53 Resolver, License Manager).
- Evita duplicazione di risorse. Funziona con Organizations o account specifici.

AWS Service Catalog:
- Catalogo di prodotti IT approvati (template CloudFormation).
- Governance: gli utenti possono lanciare solo prodotti approvati.
- Portfolios: collezioni di prodotti con permessi di accesso."""
        },
        {
            'title': 'Disaster Recovery e Alta Disponibilita',
            'content': """Strategie di Disaster Recovery (dal meno al piu' costoso):

1. Backup & Restore:
   - Backup regolari su S3/Glacier. Restore quando necessario.
   - RPO: ore. RTO: ore. Costo piu' basso.

2. Pilot Light:
   - Componenti core sempre attivi (es. database replicato). Infrastruttura minima.
   - Al disaster: scala l'infrastruttura (avvia EC2, scala ASG).
   - RPO: minuti. RTO: decine di minuti.

3. Warm Standby:
   - Versione ridotta dell'ambiente sempre in esecuzione.
   - Al disaster: scala a dimensione piena.
   - RPO: secondi. RTO: minuti.

4. Multi-Site / Hot Standby:
   - Ambiente completo attivo in piu' regioni. Active-active.
   - RPO: near zero. RTO: near zero. Costo piu' alto.

Concetti chiave:
- RPO (Recovery Point Objective): quanti dati puoi permetterti di perdere.
- RTO (Recovery Time Objective): quanto tempo puoi permetterti di essere offline.
- Route 53 Failover: routing automatico verso regione secondaria.
- Aurora Global Database: replica cross-region < 1 sec, promozione < 1 min.
- S3 Cross-Region Replication: replica oggetti tra regioni.
- DynamoDB Global Tables: replica active-active multi-region.

Alta Disponibilita':
- Multi-AZ: distribuisci risorse su piu' Availability Zones.
- ELB + ASG: load balancing e auto-scaling su piu' AZ.
- RDS Multi-AZ: failover automatico.
- S3: 11 nove di durabilita', multi-AZ di default.
- Design for failure: assume che ogni componente puo' fallire."""
        },
    ]
}

# ===== PDF GENERATION =====

class StudyGuidePDF(FPDF):
    def __init__(self, guide_title):
        super().__init__()
        self.guide_title = guide_title
        # Use built-in fonts with simple bullet
        self.bullet = '-'

    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, f'AWS SAA-C03 - {self.guide_title}', align='R')
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Pagina {self.page_no()}/{{nb}}', align='C')

    def add_cover(self, title, subtitle):
        self.add_page()
        self.ln(60)
        self.set_font('Helvetica', 'B', 28)
        self.set_text_color(255, 153, 0)
        self.cell(0, 15, 'AWS SAA-C03', align='C')
        self.ln(18)
        self.set_font('Helvetica', 'B', 22)
        self.set_text_color(40, 40, 40)
        self.cell(0, 12, title, align='C')
        self.ln(15)
        self.set_font('Helvetica', '', 12)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, subtitle, align='C')
        self.ln(8)
        self.cell(0, 8, 'Dispensa di Studio', align='C')
        self.ln(40)
        self.set_font('Helvetica', 'I', 10)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, 'Solutions Architect Associate - Certification Prep', align='C')

    def safe_text(self, text):
        # Replace special chars with ASCII equivalents
        replacements = {
            "'": "'", "'": "'", """: '"', """: '"',
            "–": "-", "—": "-", "…": "...", "•": "-",
            "è": "e'", "é": "e'", "à": "a'", "ù": "u'",
            "ò": "o'", "ì": "i'", "€": "EUR"
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        return text

    def add_section(self, title, content):
        self.add_page()
        # Section title
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(255, 153, 0)
        self.cell(0, 10, self.safe_text(title))
        self.ln(4)
        # Orange line
        self.set_draw_color(255, 153, 0)
        self.set_line_width(0.8)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(8)

        # Content
        self.set_text_color(40, 40, 40)
        for line in content.strip().split('\n'):
            line = self.safe_text(line.strip())
            if not line:
                self.ln(4)
                continue

            if line.endswith(':') and len(line) < 80:
                # Sub-heading
                self.ln(3)
                self.set_font('Helvetica', 'B', 11)
                self.multi_cell(0, 6, line)
                self.ln(1)
            elif line.startswith('- '):
                # Bullet point
                self.set_font('Helvetica', '', 10)
                self.cell(6, 6, '-')
                self.multi_cell(0, 6, line[2:].strip())
                self.ln(1)
            else:
                # Normal text
                self.set_font('Helvetica', '', 10)
                self.multi_cell(0, 6, line)
                self.ln(1)

def generate_pdf(key, guide):
    pdf = StudyGuidePDF(guide['title'])
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    pdf.add_cover(guide['title'], guide['icon'])

    for section in guide['sections']:
        pdf.add_section(section['title'], section['content'])

    filename = f'dispense/dispensa-{key}.pdf'
    pdf.output(filename)
    print(f'  -> {filename} ({pdf.page_no()} pagine)')

# Generate all
import os
os.makedirs('dispense', exist_ok=True)

print('Generazione dispense PDF...\n')
for key in sorted(GUIDES.keys()):
    guide = GUIDES[key]
    print(f'{guide["title"]}:')
    generate_pdf(key, guide)

print(f'\nFatto! {len(GUIDES)} dispense generate nella cartella "dispense/"')
