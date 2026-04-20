# 🎯 Keywords and Decision Patterns for the SAA-C03 Exam

> This document collects the "golden rules" scattered across the preparation books: the keywords in exam questions that guide you to the correct answer. Read it AFTER studying the topics — it's your cheat sheet for recognizing patterns.

---

## RULE #1: Read the Question Carefully

PACKT repeats it in every chapter: *"Read the question carefully."* The keywords in the question are deliberate clues. Here are the most important ones.

---

## 🔑 KEYWORD → SERVICE

### Compute

| If the question says... | The answer is probably... | Why |
|---|---|---|
| "cost-effective", "lowest cost", interruptible workload | **Spot Instances** | Up to -90%, but can be reclaimed |
| "steady-state", "predictable", 1-3 year commitment | **Reserved Instances** or **Savings Plans** | Up to -72% with commitment |
| "Lambda AND Fargate" in the workload | **Savings Plans** (not RI) | Only SP covers Lambda + Fargate + EC2 |
| "bring your own license", "per-socket", "per-core" | **Dedicated Hosts** | Visibility on sockets/cores for licensing |
| "dedicated hardware" without license mention | **Dedicated Instances** | Hardware isolation without visibility |
| "event-driven", "spiky", "unpredictable", < 15 min | **Lambda** | Serverless, pay per ms, auto-scale |
| "containers without managing servers" | **Fargate** | Serverless for containers |
| "containers with full control" | **ECS on EC2** or **EKS on EC2** | You manage the instances |
| "Kubernetes" | **EKS** | Managed Kubernetes |
| "batch processing", "large compute jobs" | **AWS Batch** | Manages provisioning and scheduling |

### Storage

| If the question says... | The answer is probably... | Why |
|---|---|---|
| "shared file system", "multiple instances", "NFS" | **EFS** | Shared file system, NFS, multi-mount |
| "Windows file share", "SMB", "Active Directory" | **FSx for Windows** | SMB + AD integration |
| "HPC", "machine learning", "Lustre", "high throughput" | **FSx for Lustre** | Hundreds of GB/s, millions of IOPS |
| "lowest cost storage", "rarely accessed", "archive" | **S3 Glacier Deep Archive** | The cheapest, retrieval up to 48h |
| "archive but need instant access" | **S3 Glacier Instant Retrieval** | Low cost, millisecond access |
| "data accessed infrequently, rapid access when needed" | **S3 Standard-IA** | Low storage cost, immediate retrieval |
| "non-critical data, can be recreated" | **S3 One Zone-IA** | -20% vs Standard-IA, but single AZ |
| "changing access patterns", "unknown access" | **S3 Intelligent-Tiering** | Automatically moves between tiers |
| "highest IOPS", "temporary", "data can be lost" | **Instance Store** | Physically attached, maximum IOPS |
| "persistent block storage", "database" | **EBS** | Persistent, one instance at a time |
| "IOPS > 16,000" or "sub-millisecond latency" for DB | **EBS io2** | Provisioned IOPS, 99.999% durability |
| "small random I/O" | **SSD** (gp3, io2) | SSD for random I/O |
| "large sequential I/O", "throughput" | **HDD** (st1) | HDD for sequential I/O |

### Database

| If the question says... | The answer is probably... | Why |
|---|---|---|
| "relational", "SQL", "complex queries", "ACID", "joins" | **RDS** or **Aurora** | Relational databases |
| "MySQL or PostgreSQL" + "high performance" | **Aurora** | 5x MySQL, 3x PostgreSQL |
| "key-value", "sub-millisecond", "NoSQL", "unstructured" | **DynamoDB** | Key-value, auto-scale, sub-ms |
| "20 million requests per second" | **DynamoDB** | Designed for this |
| "graph database", "complex relationships", "social network" | **Neptune** | Graph DB |
| "document store", "MongoDB", "JSON" | **DocumentDB** | MongoDB compatible |
| "immutable ledger", "audit trail", "blockchain-like" | **QLDB** | Immutable ledger |
| "data warehouse", "analytics", "petabyte", "BI" | **Redshift** | Data warehouse |
| "query S3 data with SQL", "serverless analytics" | **Athena** | SQL on S3, pay per query |
| "read-heavy database" | **Read Replicas** | Horizontal read scaling |
| "database high availability", "failover" | **Multi-AZ** | Automatic failover |
| "many database connections", "connection pooling" | **RDS Proxy** | Connection pooling, fast failover |
| "caching", "same queries repeated" | **ElastiCache** | In-memory cache |
| "caching for DynamoDB" | **DAX** | Native for DynamoDB, more seamless |
| "spiky database workload" | **Aurora Serverless** | Auto-scale, but 2x cost per unit |

### Networking

| If the question says... | The answer is probably... | Why |
|---|---|---|
| "static IP" + load balancer | **NLB** | ALB doesn't have static IPs |
| "HTTP/HTTPS" + advanced routing (URL, host) | **ALB** | Layer 7, routing rules |
| "TCP/UDP", "gaming", "IoT", "millions req/sec" | **NLB** | Layer 4, ultra-fast |
| "reduce latency for global users" + web content | **CloudFront** | CDN, cache at the edge |
| "reduce latency" + TCP/UDP + "static IP" | **Global Accelerator** | Optimized routing, static IPs |
| "block specific IP" | **NACL** (not Security Group) | SG doesn't have Deny rules |
| "private access to S3" from VPC | **Gateway Endpoint** | Free, route table |
| "private access to S3" from on-premises | **Interface Endpoint** | Paid, but accessible from VPN/DX |
| "connect VPCs" (few) | **VPC Peering** | Free, simple |
| "connect many VPCs" | **Transit Gateway** | Centralized hub |
| "expose service to thousands of VPCs" | **PrivateLink** | Scalable, private |
| "fastest connection on-premises ↔ AWS" | **VPN** (not Direct Connect) | DX takes months |
| "dedicated, consistent connection on-premises" | **Direct Connect** | Private, guaranteed bandwidth |
| "Direct Connect" + "encrypted" | **DX + VPN tunnel** (IPsec) | DX is not encrypted by default |

### Security

| If the question says... | The answer is probably... | Why |
|---|---|---|
| "SQL injection", "XSS", "bot protection" | **WAF** | Layer 7, web attacks |
| "DDoS protection" | **Shield** | Standard (free) or Advanced ($3K/month) |
| "DDoS" + "cost reimbursement" + "response team" | **Shield Advanced** | DRT + cost protection |
| "rate limiting requests" | **WAF rate-based rules** | Limits req per IP |
| "FIPS 140-2 Level 3" | **CloudHSM** | KMS is only Level 2 |
| "company must control encryption keys exclusively" | **CloudHSM** | Single-tenant HSM |
| "rotate database credentials automatically" | **Secrets Manager** | Native rotation for RDS |
| "configuration parameters" (not secrets) | **Parameter Store** | Free, no native rotation |
| "find PII in S3" | **Macie** | ML for sensitive data in S3 |
| "detect threats", "anomalous behavior", "crypto mining" | **GuardDuty** | Continuous threat detection |
| "vulnerability scanning", "CVE", "patching" | **Inspector** | Vulnerability assessment |
| "centralized security view", "compliance dashboard" | **Security Hub** | Aggregates findings |
| "investigate security incident", "root cause" | **Detective** | Post-incident investigation |
| "manage security rules across multiple accounts" | **Firewall Manager** | Centralized, requires Organizations |
| "prevent actions across all accounts" | **SCP** | Organization-level guardrail |
| "credentials in code" or "access keys on instance" | **ALWAYS WRONG** | Use IAM roles |

### Decoupling & Messaging

| If the question says... | The answer is probably... | Why |
|---|---|---|
| "decouple", "queue", "one-to-one" | **SQS** | Message queue 1:1 |
| "exactly-once", "ordered messages" | **SQS FIFO** | Guaranteed order, no duplicates |
| "notify multiple subscribers", "one-to-many" | **SNS** | Pub/sub |
| "fan-out to multiple queues" | **SNS + SQS** | SNS topic → multiple SQS |
| "event-driven", "many sources, many targets" | **EventBridge** | Many-to-many |
| "coordinate multiple Lambda functions" | **Step Functions** | Workflow orchestration |
| "real-time streaming", "multiple consumers" | **Kinesis Data Streams** | Streaming, replay |
| "load streaming data into S3/Redshift" | **Kinesis Firehose** | Auto-load, transform |

### Migration

| If the question says... | The answer is probably... | Why |
|---|---|---|
| "migrate files to S3/EFS" | **DataSync** | File transfer, doesn't support EBS |
| "migrate database" | **DMS** | + SCT for schema conversion |
| "terabytes of data, no good internet" | **Snowball Edge** | Physical device |
| "petabytes/exabytes" | **Snowmobile** | 18-wheel truck |
| "> 10 PB in one location" | **Snowmobile** | For datasets > 10 PB |
| "< 10 PB or multiple locations" | **Snowball Edge** | More flexible |
| "ongoing data transfer to AWS" | **Direct Connect** (not Snow) | Snow is for one-time |
| "hybrid access, files on-premises AND in S3" | **Storage Gateway** | Continuous hybrid access |
| "transfer files via SFTP/FTPS" | **Transfer Family** | Standard protocols |

---

## 🚫 COMMON TRAPS

### Keywords that EXCLUDE answers

| If the question says... | Exclude... | Why |
|---|---|---|
| "most cost-effective" | Direct Connect, RDS Proxy, Shield Advanced | Expensive |
| "fastest implementation" | Direct Connect | Takes months |
| "0.0.0.0/0" in the answers | Probably not "most secure" | Opens to all internet |
| "store credentials in code" | That answer | Always wrong — use IAM roles |
| "single AZ" for production | That answer | Not HA |
| "CLB" (Classic Load Balancer) | That answer | AWS recommends not using it |
| "data must not be lost" | Instance Store | Data lost on stop |

### Confusing Comparisons

| Confusion | How to Distinguish |
|---|---|
| **Multi-AZ vs Read Replica** | Multi-AZ = **availability** (failover, standby doesn't serve queries). Read Replica = **performance** (read scaling, asynchronous) |
| **CloudTrail vs CloudWatch** | CloudTrail = **who did what** (audit). CloudWatch = **how are resources doing** (metrics) |
| **DataSync vs Storage Gateway** | DataSync = **transfer** (one-time or scheduled). Storage Gateway = **continuous hybrid access** |
| **Security Group vs NACL** | SG = stateful, Allow only, instance. NACL = stateless, Allow+Deny, subnet |
| **Gateway Endpoint vs Interface Endpoint** | Gateway = free, S3/DynamoDB only, route table. Interface = paid, almost all services, ENI |
| **Secrets Manager vs Parameter Store** | Secrets Manager = automatic DB rotation, $0.40/secret. Parameter Store = general config, free |
| **CloudFront vs Global Accelerator** | CloudFront = HTTP, content caching. Global Accelerator = TCP/UDP, static IPs, optimized routing |
| **SQS vs Kinesis** | SQS = 1:1 decoupling, single consumer. Kinesis = real-time streaming, multiple consumers, replay |
| **Aurora Serverless vs RDS** | Aurora Serverless = spiky workloads (2x cost/unit). RDS = steady workloads |
| **Snowball vs Snowmobile** | Snowball Edge = < 10 PB or multiple locations. Snowmobile = > 10 PB, single location |

---

## 📊 QUICK DECISION TABLES

### Which Storage?

```
You need...
├── Block storage for EC2? → EBS
│   ├── High IOPS, random I/O? → gp3 or io2 (SSD)
│   └── High throughput, sequential? → st1 (HDD)
├── Shared file system?
│   ├── Linux? → EFS
│   ├── Windows? → FSx for Windows
│   └── HPC/ML? → FSx for Lustre
├── Object storage? → S3
│   ├── Frequent access? → Standard
│   ├── Rare access, fast retrieval? → Standard-IA
│   ├── Archive, retrieval in hours? → Glacier
│   └── Deep archive, retrieval in days? → Deep Archive
└── Temporary storage, maximum IOPS? → Instance Store
```

### Which Database?

```
Your data is...
├── Structured (SQL, relations, JOIN)?
│   ├── MySQL/PostgreSQL + high performance? → Aurora
│   ├── Oracle/SQL Server/DB2? → RDS
│   └── Spiky workload? → Aurora Serverless
├── Unstructured (key-value, JSON)?
│   ├── Sub-millisecond latency? → DynamoDB
│   ├── Document store (MongoDB)? → DocumentDB
│   └── Graph (complex relationships)? → Neptune
└── Analytics on petabytes? → Redshift
```

### Which Connectivity?

```
You need to connect...
├── VPC to S3/DynamoDB privately? → Gateway Endpoint (free)
├── VPC to other AWS services privately? → Interface Endpoint
├── On-premises to AWS?
│   ├── Immediately, limited budget? → VPN
│   ├── Dedicated, consistent bandwidth? → Direct Connect
│   └── Direct Connect + encryption? → DX + VPN tunnel
├── Two VPCs? → VPC Peering
├── Many VPCs? → Transit Gateway
└── Service to thousands of VPCs? → PrivateLink
```

### Which DR Strategy?

```
Your budget is...
├── Minimal (RPO hours, RTO hours)? → Backup & Restore
├── Medium (RPO minutes, RTO minutes)? → Pilot Light or Warm Standby
└── Unlimited (RPO ~0, RTO ~0)? → Active-Active
```

---

## 💡 GOLDEN RULES FROM THE BOOKS

1. **"If the question asks DDoS → Shield. If it asks SQLi/XSS → WAF"** (PACKT)
2. **"If the question asks S3 or DynamoDB endpoint → Gateway. Otherwise → Interface"** (PACKT)
3. **"If the question says 'most secure' and an answer has 0.0.0.0/0 → that's not it"** (PACKT)
4. **"If Macie is an answer, verify that the data is in S3 and that PII is mentioned"** (PACKT)
5. **"Read replicas are a common exam topic — understand what they can and cannot do"** (PACKT)
6. **"CloudTrail is NOT real-time — it takes ~15 minutes"** (PACKT)
7. **"gp3 is more performant than gp2 — remember this to choose between the two"** (PACKT)
8. **"Aurora Serverless is 2x more expensive per unit — saves only if the workload is spiky"** (PACKT)
9. **"Direct Connect takes months — if speed is needed, it's not the answer"** (PACKT)
10. **"RDS Proxy has additional cost — watch for 'most cost-effective'"** (PACKT)
11. **"SQS = 1:1, SNS = 1:many, EventBridge = many:many"** (PACKT)
12. **"Step Functions to coordinate Lambda, not SQS"** (PACKT)
13. **"Lambda max timeout 15 minutes — if the job takes longer, use EC2/Fargate/Batch"** (Dojo)
14. **"DataSync does NOT support EBS — only files (S3/EFS/FSx)"** (PACKT)
15. **"You can't SSH into RDS — use Parameter Groups for configuration"** (Dojo)
16. **"Snowball Edge < 10 PB. Snowmobile > 10 PB"** (Dojo)
17. **"S3 IA has minimum 128KB and 30 days — if you delete earlier, you still pay"** (Dojo)
18. **"You can't transition from Glacier Deep Archive to Glacier (only the reverse)"** (Dojo)


---

## 📦 DETAILED COMPARISONS FROM DOJO

### Data Transfer: S3 TA vs Direct Connect vs VPN vs Snow (from Dojo)

This comparison is fundamental for the exam — questions about how to transfer data are very frequent.

| Method | When to use | Key notes |
|---|---|---|
| **S3 Transfer Acceleration** | Transfers from distributed locations via public internet, variable throughput | Uses CloudFront edge locations. You pay only if there's improvement. Supports multipart upload |
| **Direct Connect** | Dedicated private connection, consistent bandwidth, security requirements | NOT encrypted by default. Not redundant (needs a second line). Months to implement |
| **VPN (Site-to-Site)** | Immediate need, limited budget, low-medium bandwidth, tolerance for internet variability | Encrypted (IPsec). Configurable in minutes. Throughput depends on internet |
| **Snowball Edge** | TB-PB of data, no good internet connection, isolated locations | Physical device, 50-80 TB per device. Transfer completed within 360 days. Supports export |
| **Snowmobile** | > 10 PB in a single location | 18-wheel truck, up to 100 PB. Armed guards, GPS, 24/7 video. **Does NOT support export** |

**Decision rules from Dojo:**
- *"Se il trasferimento via internet richiederebbe più di una settimana, o ci sono job ricorrenti con >25 Mbps di bandwidth disponibile → S3 Transfer Acceleration"*
- *"Puoi usare Snowball Edge per il trasferimento iniziale pesante, poi S3 TA per i cambiamenti incrementali"*
- *"Se trasferisci dati ad AWS su base continua → Direct Connect (non Snow)"*
- *"Se più utenti in location diverse interagiscono con S3 continuamente → S3 TA"*
- *"Non puoi esportare dati direttamente da S3 Glacier — devi prima ripristinarli in S3"*
- *"> 10 PB in una location → Snowmobile. < 10 PB o multiple location → Snowball Edge"*
- *"Se hai backbone ad alta velocità con centinaia di Gb/s spare → Snowmobile. Se bandwidth limitata → multiple Snowball Edge incrementali"*

### DynamoDB: Scaling RCU vs DAX vs Secondary Indexes vs ElastiCache (from Dojo)

| Solution | When to use | Limitations |
|---|---|---|
| **Scaling RCU** | High reads on different items, not suitable for cache. On-Demand (auto) or Provisioned (with auto-scaling) | On-Demand can become expensive with frequent spikes |
| **DAX** | Microsecond response time, same items read repeatedly, no code changes | No TLS. Only Go/Java/Node.js/Python/.NET. Not for strongly consistent reads or write-intensive workloads. Possible stale data |
| **Secondary Indexes** | Queries on non-primary key attributes. Avoids scanning the entire table | Performance still tied to the table's RCUs. More data structure optimization than performance boost |
| **ElastiCache** | Only if you specifically need Redis/Memcached, or features not supported by DAX | Requires code changes. More maintenance than DAX |

**Rule from Dojo:** *"Per caching DynamoDB, vai con DAX (no code changes). Preferisci ElastiCache solo se ti serve specificamente Redis/Memcached o una feature non supportata da DAX."*

### EFS vs FSx for Windows vs FSx for Lustre — Details (from Dojo)

| Feature | EFS | FSx for Windows | FSx for Lustre |
|---|---|---|---|
| **Protocol** | NFS | SMB | Lustre |
| **Supported OS** | Linux (EC2, ECS, EKS, Fargate, Lambda) | Windows, Linux, MacOS | **Linux only** (+ EKS, Batch) |
| **Auto-scale storage** | **Yes** (automatic) | **No** (manual) | **No** (manual, every 6 hours) |
| **Throughput** | Bursting or Provisioned | Configurable at creation | Hundreds of GB/s, millions of IOPS |
| **S3 Integration** | No | No | **Yes** (automatic import/export) |
| **Multi-AZ** | Yes (Standard class) | Yes (optional) | No (but Persistent replicates within the AZ) |
| **Encryption** | KMS at rest, TLS 1.2 in transit | KMS at rest, SMB Kerberos in transit | KMS at rest, in transit from supported EC2 |
| **On-premises access** | Via Direct Connect or VPN | Via Direct Connect or VPN | Not mentioned |
| **Deployment types** | N/A | Single-AZ or Multi-AZ | **Scratch** (temporary, no replica) or **Persistent** (HA, replica within AZ) |
| **Use cases** | Big data, analytics, web serving, CMS, home dir | CRM, ERP, .NET, home dir, media, build env | ML, HPC, video processing, financial modeling, genome |

### Numbers to Remember for the Exam

| Service | Number | Meaning |
|---|---|---|
| **S3** | 99.999999999% (11 nines) | Durability |
| **S3** | 99.99% | Availability |
| **S3** | 5 TB | Maximum single object size |
| **S3 IA** | 128 KB / 30 days | Minimum capacity / minimum duration charge |
| **S3 Glacier** | 40 KB / 90 days | Minimum capacity / minimum duration charge |
| **S3 Deep Archive** | 40 KB / 180 days | Minimum capacity / minimum duration charge |
| **Glacier Expedited** | 1-5 minutes | Fastest retrieval |
| **Glacier Standard** | 3-5 hours | Standard retrieval |
| **Glacier Deep Standard** | 12 hours | Standard retrieval |
| **Glacier Deep Bulk** | 48 hours | Slowest retrieval |
| **EBS io2** | 99.999% | Durability (vs 99.8-99.9% for others) |
| **EBS io2** | 500 IOPS/GiB | IOPS ratio |
| **EBS Nitro** | 64,000 IOPS | Max IOPS per volume on Nitro instances |
| **EBS non-Nitro** | 32,000 IOPS | Max IOPS per volume |
| **RDS Multi-AZ** | 99.95% | Uptime SLA |
| **RDS Single-AZ** | 99.5% | Uptime SLA |
| **RDS backup** | 7-35 days | Retention (default 7) |
| **DynamoDB** | 20M+ req/sec | Maximum capacity |
| **DynamoDB** | sub-millisecond | Latency |
| **Aurora** | 5x MySQL, 3x PostgreSQL | Performance |
| **Aurora** | 128 TiB | Maximum storage |
| **Lambda** | 15 minutes | Maximum timeout |
| **Lambda** | 10,240 MB | Maximum memory |
| **Lambda** | 1,769 MB = 1 vCPU | Memory/CPU equivalence |
| **Lambda** | 1,000 | Default concurrency per Region |
| **SQS FIFO** | 300 msg/sec | Throughput (3,000 with batching) |
| **SQS visibility timeout** | 30 seconds | Default |
| **CloudTrail** | 90 days | Free event history |
| **CloudTrail** | ~15 minutes | Delay (not real-time) |
| **Spot Instance** | 2 minutes | Notice before reclaim |
| **Spot Instance** | up to 90% | Maximum discount |
| **RI/Savings Plans** | up to 72% | Maximum discount |
| **Snowball Edge** | 50-80 TB | Capacity per device |
| **Snowball Edge** | 360 days | Maximum time to complete transfer |
| **Snowmobile** | 100 PB | Capacity per truck |
| **Shield Advanced** | $3,000/month | Cost |
| **NLB idle timeout** | 350 seconds | Fixed, not adjustable |
| **ALB idle timeout** | 60 seconds | Default, adjustable up to 4,000s |
| **Organizations** | 1,000 OU | Maximum |
| **Organizations** | 5 levels | Maximum OU nesting |
| **KMS CMK** | 4,096 bytes | Max direct encryption (then envelope) |
| **Key deletion** | 7 days | Minimum wait for deletion |


---

## 🔌 DIRECT CONNECT — Decision Patterns (from Dojo)

Direct Connect is a frequent exam topic. Dojo provides 4 connectivity scenarios:

| Scenario | Solution | Notes |
|---|---|---|
| Access to resources in **one VPC** | Private VIF → VPC's VGW | Max 50 VIF per DX connection. Limited to the DX location's Region |
| Access to **VPCs in different Regions** | Private VIF → **DX Gateway** → multiple VGW | One BGP peering per DX Gateway per connection. NO VPC-to-VPC connectivity |
| Access to **many VPCs in many locations** | Transit VIF → **DX Gateway** → **Transit Gateway** | Up to 3 TGW in different Regions/accounts on one VIF. **Most scalable and manageable** |
| Access to **public AWS services** (S3, DynamoDB, public EC2) | **VPN over DX public VIF** → Transit Gateway | VPN for encryption, DX for performance |

### Direct Connect Resilience (from Dojo)

| Setup | Resilience | Cost |
|---|---|---|
| **2 DX lines** on 2 different devices/routers | High — automatic failover | High (2x DX) |
| **1 DX line + VPN** as backup | Medium — VPN is slower but works | Medium (DX + VPN) |
| **Only 1 DX line** | **None** — single point of failure | Low but risky |

> **Dojo Rule**: *"Direct Connect di default NON è resiliente. Serve una seconda linea o un VPN backup. Abilita BFD (Bidirectional Forwarding Detection) per failover veloce."*

---

## 🔗 VPC ENDPOINTS — Complete Comparison (from Dojo)

| Feature | Interface Endpoint | Gateway Endpoint | GW Load Balancer Endpoint |
|---|---|---|---|
| **What it is** | ENI with private IP | Target in route table | Intercepts traffic to GWLB |
| **Services** | Almost all AWS services | **S3 and DynamoDB only** | Security appliances (firewall, IDS) |
| **Security Groups** | **Yes** | No | No |
| **Endpoint Policy** | Yes | Yes | No |
| **On-premises access** | **Yes** (via VPN/DX) | **No** | No |
| **Cross-region access** | **No** (same region only) | **No** | No |
| **VPC Peering** | **Yes** (intra-region from Nitro, inter-region from any) | **No** | No |
| **Protocol** | IPv4 TCP only | IPv4 only | IPv4 only |
| **Cost** | Paid | **Free** | Paid |

> **Exam rule**: S3/DynamoDB from VPC → **Gateway** (free). S3 from on-premises → **Interface**. Any other service → **Interface**.

---

## 🧠 CACHING — Where and How (from LinkedIn)

The LinkedIn PDF explains the caching layers in an architecture:

1. **Browser/Client** — HTTP response cache with expiry policy in the header
2. **CDN (CloudFront)** — cache of static resources at edge locations
3. **Load Balancer** — can cache resources
4. **API Gateway** — API response cache (avoids re-executing Lambda)
5. **Application layer (ElastiCache)** — in-memory cache for frequent data
6. **Database layer (DAX for DynamoDB)** — DB-specific cache

### Cache Problems (from LinkedIn)

| Problem | Description | Solution |
|---|---|---|
| **Thunder Herd** | Many cache keys expire simultaneously → all queries hit the DB | Add a random number to the expiry time. Allow only core data to hit the DB |
| **Cache Penetration** | Queries for data that doesn't exist → hits the DB every time | Cache "empty" results too with a short TTL |
| **Cache Avalanche** | The cache server goes down → all traffic hits the DB | Use cache cluster with replica. Circuit breaker |
| **Cache Stampede** | A popular key expires → hundreds of simultaneous requests to the DB | Lock on the key: only one request regenerates the cache, others wait |

---

## 🏗️ API GATEWAY — Key Functions (from LinkedIn)

| Function | Description |
|---|---|
| **Request Routing** | Directs API requests to the appropriate backend service |
| **Load Balancing** | Distributes requests across multiple servers |
| **Security** | Authentication, authorization, encryption |
| **Rate Limiting/Throttling** | Controls the number of requests per client in a period |
| **API Composition** | Combines multiple backend requests into a single frontend request |
| **Caching** | Temporarily saves responses to reduce repeated processing |

---

## 💰 CLOUD COST REDUCTION — Techniques (from LinkedIn)

The LinkedIn PDF lists cost reduction techniques:

1. **Reduce Usage** — turn off unused resources, right-size instances
2. **Reserved Capacity** — RI and Savings Plans for predictable workloads
3. **Spot Instances** — for interruptible workloads
4. **Auto Scaling** — scale down when not needed
5. **Storage Tiering** — lifecycle policies to move data to cheaper tiers
6. **Data Transfer Optimization** — minimize cross-region, use VPC endpoints, CloudFront
7. **Monitoring & Alerts** — Cost Explorer, Budgets, billing alerts
8. **Tagging** — track costs by department/project
9. **Managed Services** — fewer man-hours = lower operational costs
10. **Serverless** — pay only for actual execution

---

## 🔒 CLOUD SECURITY — Layers (from LinkedIn)

The LinkedIn PDF shows the cloud security layers:

1. **Identity & Access** — IAM, MFA, least privilege, federation
2. **Network** — VPC, SG, NACL, VPN, Direct Connect, PrivateLink
3. **Application** — WAF, Shield, API Gateway throttling
4. **Data** — Encryption at rest (KMS) and in transit (TLS/SSL)
5. **Monitoring** — CloudTrail, GuardDuty, Security Hub, Config
6. **Incident Response** — Detective, Lambda automation, SNS alerts
7. **Compliance** — Config Rules, Audit Manager, Organizations SCP

---

## 🔄 DISASTER RECOVERY — Visual Summary (from LinkedIn + Dojo)

```
INCREASING COST →
DECREASING RECOVERY TIME →

┌──────────────┬──────────────┬──────────────┬──────────────┐
│  BACKUP &    │  PILOT       │  WARM        │  ACTIVE-     │
│  RESTORE     │  LIGHT       │  STANDBY     │  ACTIVE      │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ RPO: hours   │ RPO: minutes │ RPO: seconds │ RPO: ~zero   │
│ RTO: hours   │ RTO: minutes │ RTO: minutes │ RTO: ~zero   │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ Only backup  │ Core always  │ Reduced but  │ Full copy    │
│ in S3/other  │ active (DB   │ functional   │ active-      │
│ Region.      │ with replica)│ environment, │ active.      │
│ Restore      │ Rest starts  │ always in    │ Just         │
│ when needed  │ when needed  │ sync. Scales │ redirect     │
│              │              │ up when      │ traffic      │
│              │              │ needed       │              │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ 💰           │ 💰💰         │ 💰💰💰       │ 💰💰💰💰     │
└──────────────┴──────────────┴──────────────┴──────────────┘
```


---

## 🖥️ EC2 ACCESS — Methods (from PACKT)

| Method | When to use |
|---|---|
| **SSH** (port 22) | Standard Linux access with private key |
| **RDP** (port 3389) | Windows access |
| **Bastion Host** | Secure access to instances in private subnet. Hardened server in public subnet |
| **Session Manager (SSM)** | **Most secure** — no open ports, no SSH keys, from the AWS console |
| **VPN** | Corporate access to private instances |

> **Exam tip**: most secure method to access EC2 → **Session Manager** (PACKT)

---

## 🌐 NAT Gateway vs Internet Gateway (from PACKT)

| | Internet Gateway | NAT Gateway |
|---|---|---|
| **For** | Public subnet | Private subnet (outbound only) |
| **Traffic** | Inbound + outbound | **Outbound only** |
| **Where** | Attached to VPC | In public subnet (requires IGW) |

---

## 🏗️ MULTI-TIER (from Kimiko)

Presentation (web) → Business Logic (app) → Data Access (DB). Separate tiers to scale independently. Horizontal scaling > Vertical scaling.

---

## 🐳 ECS vs EKS vs Fargate

"containers" → ECS/EKS. "Kubernetes" → EKS. "without managing servers" → Fargate. "Docker" → ECS.

---

## 📋 DEPLOYMENT (from Dojo)

"deploy infrastructure" → **CloudFormation**. "deploy web app quickly" → **Beanstalk**. "deploy code updates" → **CodeDeploy**.

---

## 🎯 MICROSERVICES Best Practice (from LinkedIn)

Separate data storage, single responsibility, stateless, containers, domain-driven design, orchestrate with Step Functions.

---

## 🛡️ FAULT TOLERANCE Principles (from LinkedIn)

Replication, Redundancy, Load Balancing, Failover Mechanisms, Graceful Degradation, Data Backup & Recovery.
