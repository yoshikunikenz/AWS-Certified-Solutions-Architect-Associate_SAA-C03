# EC2 - Instance Types, Placement Groups, Auto Scaling

> Sources: PACKT Ch.4 (p.186-206), PACKT Ch.14 (p.552-560), KIMIKO (p.305-308), DOJO (p.46-58)

---

## Glossary: the services you will encounter in this document

- **EC2 (Elastic Compute Cloud)** — a virtual machine in the cloud. Like having a computer (Linux or Windows) running in AWS data centers. You can install whatever you want on it. You pay for the time it's running and for the power you choose (CPU, RAM). There are different instance "families": some optimized for compute, others for memory, others for storage.

- **AMI (Amazon Machine Image)** — a "snapshot" of the operating system and pre-installed software. When you launch an EC2 instance, you choose an AMI that defines what's inside. Like choosing an ISO image to install an operating system, but ready to use.

- **Instance Store** — storage physically attached to the server hosting your EC2 instance. Very fast (it's a local disk), but **temporary**: when you stop the instance, the data disappears. Think of it like a computer's RAM — fast but volatile.

- **Auto Scaling Group (ASG)** — a group of EC2 instances that grows and shrinks automatically based on load. If traffic increases, it launches new instances. If it decreases, it shuts them down. It's like having a team of waiters in a restaurant: during peak times you call in more, when it's quiet you send them home.

- **Launch Template** — the "blueprint" that tells the ASG how to create new instances: which AMI to use, what instance type, which security groups, what storage. Like a pre-filled order form at a restaurant.

- **Spot Instance** — unused EC2 capacity that AWS sells at a discounted price (up to -90%). The catch: AWS can reclaim it with 2 minutes notice if someone else needs it. Like a last-minute airline ticket: costs very little but you might get bumped from the flight.

- **Reserved Instance (RI)** — you commit to using a certain instance type for 1 or 3 years in exchange for a discount (up to -72%). Like an annual gym membership: you pay less per month but you're locked in.

- **Savings Plan** — similar to RIs but more flexible. You commit to spending a certain amount per hour for 1-3 years, and the discount applies automatically to EC2, Lambda, Fargate. Like an "all-inclusive" membership that covers gym, pool, and sauna.

- **Placement Group** — a way to control WHERE your EC2 instances are physically placed in data centers. Cluster (close together for low latency), Spread (separated for resilience), Partition (isolated groups).

- **Elastic Fabric Adapter (EFA)** — a special network interface for HPC and machine learning workloads that need network throughput beyond normal TCP. Like a dedicated highway lane for heavy trucks.

---

## Compute Overview on AWS

PACKT introduces EC2 as *"il primo servizio mai rilasciato da AWS. Amazon EC2 è un servizio fondamentale che fornisce capacità di calcolo ridimensionabile nel cloud."*

The Dojo adds: *"EC2 è considerato il building block base in AWS — è usato in quasi ogni servizio!"*

### Choosing the Compute Service (from PACKT)

PACKT lists the compute options and when to use them:

| Service | When to use it |
|---|---|
| **Amazon EC2** | Web app hosting, backend services, batch processing, WordPress, microservices, data analytics |
| **Elastic Beanstalk** | Deploy and manage web apps/APIs without managing servers. Java, Python, Node.js, PHP |
| **Amazon ECS** | Containerized applications with Docker, microservices, batch processing |
| **Amazon EKS** | Kubernetes clusters for containerized applications |
| **AWS Fargate** | Containers without managing infrastructure, quick and simple scaling |
| **AWS Batch** | Large data volumes, compute-intensive tasks, analytics pipelines, rendering, simulations |
| **AWS Lambda** | Event-driven, responses to data changes, HTTP requests, messages from other services |

> **Exam tip (PACKT)**: *"There will be questions in the exam where you will need to decide the best service to use for a specific type of workload, so understanding the key differences between them is critical."*

### VM vs Container (from PACKT)

PACKT explains the difference:
- **VM**: software emulation of a physical computer, includes an entire OS stack (kernel, libraries, binaries). Strong isolation but resource overhead
- **Container**: lightweight and portable runtime environment. Shares the host OS kernel. More efficient, fast startup, ideal for microservices and CI/CD

---

## EC2 Instance Types

### Instance Families (from PACKT and Dojo)

| Family | Optimized for | Use cases (PACKT + Dojo) |
|---|---|---|
| **General Purpose** (T, M) | Compute/memory/networking balance | Web servers, dev environments, small-medium databases |
| **Compute Optimized** (C) | High CPU power | HPC, batch processing, media transcoding, gaming servers, ML inference (Dojo) |
| **Memory Optimized** (R, X) | Large in-memory datasets | In-memory databases, real-time analytics, large-scale caching |
| **Storage Optimized** (I, D) | High-performance access to local storage | NoSQL databases, data warehousing, log processing, tens of thousands of IOPS (Dojo) |
| **Accelerated Computing** (P, G) | Specialized hardware (GPU) | ML inference, graphics rendering, video processing |
| **HPC Optimized** | High-power compute, low-latency networking | Scientific research, financial modeling, engineering simulations |

### Burstable vs Standard (from PACKT)

PACKT makes an important distinction:

**Burstable Instances** (prefix `t`, e.g. t3.micro):
- For workloads with variable CPU usage
- Accumulate **CPU credits** during low-activity periods
- Use credits during bursts of higher demand
- *"È essenziale monitorare i CPU credits per assicurare performance consistenti perché quando i credits finiscono, vedrai degradazione delle performance (standard mode) o costi aumentati (unlimited mode)"*

**Standard Instances** (M, C, R, etc.):
- Fixed CPU performance based on selected size
- No CPU credit management required
- For steady-state workloads or those requiring predictable performance

### Nitro-based Instances (from Dojo)

The Dojo mentions Nitro instances: *"Il Nitro System fornisce capacità bare metal che eliminano l'overhead di virtualizzazione. Quando monti volumi EBS Provisioned IOPS su istanze Nitro-based, puoi provisionare da 100 IOPS fino a 64,000 IOPS per volume, rispetto a solo 32,000 su altre istanze."*

### Graviton (from PACKT Ch.14)

PACKT mentions: *"AWS offre il suo tipo di processore, Graviton. Alcuni tipi di istanza vengono con processori Graviton, e questi possono offrire performance migliori rispetto ai loro equivalenti Intel."*

---

## AMI — Amazon Machine Images (from PACKT and Dojo)

PACKT explains: when you launch an EC2 instance, you select an AMI that defines the initial software configuration and operating system. AWS offers pre-configured AMIs for Amazon Linux, Ubuntu, Windows Server, etc.

The Dojo details the EC2 instance components step by step:
1. **Choose AMI** — contains OS, settings, applications. Cannot be changed after launch
2. **Choose instance type and size** — determines CPU, RAM, network speed. You can change the type even after launch (**right sizing**)
3. **Configure settings** — number of instances, spot/on-demand, VPC/subnet, public IP, placement group, IAM role, shutdown behavior, termination protection, user data
4. **Add storage** — automatic EBS volume for OS, you can add more
5. **Add tags** — for identification and classification
6. **Configure Security Groups** — firewall for the instance
7. **Key pair** — for secure access. *"Non c'è modo di riassociare un'altra key pair dopo il lancio"* (Dojo)

### Instance Store vs EBS (from PACKT and Dojo)

| Feature | Instance Store | EBS |
|---|---|---|
| Type | Storage physically attached to the host | Network-attached storage |
| Persistence | **Temporary** — data lost when instance stops | **Persistent** — data survives stop/delete |
| Performance | Higher I/O (physically attached) | Good, but with network latency |
| Creation | Only at instance provisioning | At any time |

The Dojo adds an important performance detail: *"Se hai bisogno di IOPS davvero alti, bassa latenza, e i dati non devono necessariamente persistere, i volumi instance store su tipi di istanza specifici potrebbero essere preferibili ai volumi EBS Provisioned IOPS. I volumi instance store sono fisicamente attaccati alle istanze EC2, quindi le istanze possono accedere ai dati molto più velocemente."*

> **Exam tip (PACKT)**: *"It is important to remember that any data stored on an instance store volume is lost when the instance is stopped, whereas data on an EBS volume persists."*

---

## EC2 Purchase Options

### Overview (from Kimiko)

Kimiko explains the options from the console: *"Quando sei nella management console EC2 e lanci un'istanza, stai tipicamente facendo quello che si chiama acquistare un'istanza On-Demand. Ma ci sono molte opzioni per l'acquisto di risorse EC2."*

### Complete Table (from Dojo)

| Option | How it works | Discount | Ideal for |
|---|---|---|---|
| **On-Demand** | Pay per second/hour for each running instance. No commitment | None | Unpredictable workloads, testing, dev |
| **Savings Plans** | Commitment to a USD/hour amount for 1 or 3 years. **Compute SP**: applies to EC2, Fargate, Lambda regardless of family/size/AZ/region/OS. **EC2 Instance SP**: cheaper but limited to one family in one region | Up to 72% | Steady-state workloads with flexibility |
| **Reserved Instances** | Commitment to a specific configuration (type, region) for 1 or 3 years. **Standard RI**: maximum discount, sellable on Marketplace. **Convertible RI**: you can change attributes. **Scheduled RI**: for recurring schedules | Up to 72% | Predictable, steady-state workloads |
| **Spot Instances** | Unused EC2 capacity at reduced price. Instance is stopped/terminated with **2 minutes notice** when price rises | Up to 90% | Batch processing, analytics, interruptible workloads |
| **Dedicated Hosts** | Dedicated physical host. Supports BYOL (Bring Your Own License) | Variable | Compliance, per-socket/per-core licensing |
| **Dedicated Instances** | Instances on single-tenant hardware. Physical isolation at hardware level | Variable | Isolation, compliance |
| **Capacity Reservations** | Reserve capacity in a specific AZ. No duration commitment | None | Availability guarantee |

### Standard RI vs Convertible RI (from Dojo)

| Feature | Standard RI | Convertible RI |
|---|---|---|
| Applies to all AZs in the region | Yes | Yes |
| Shareable across accounts (consolidated billing) | Yes | Yes |
| Change AZ, instance size (Linux), networking type | Yes | Yes |
| Change instance family, OS, tenancy, payment option | **No** | **Yes** |
| Benefit from price reductions | **No** | **Yes** |
| Buy/sell on Marketplace | **Yes** | **No** |

### Dedicated Hosts vs Dedicated Instances (from Dojo)

| Feature | Dedicated Hosts | Dedicated Instances |
|---|---|---|
| Billing | Per-host | Per-instance |
| Socket, core, host ID visibility | Yes | No |
| Host and instance affinity | Yes (consistent deployment on the same physical server) | No |
| Targeted instance placement | Yes | No |
| BYOL | Yes | No |

> **Note from Kimiko**: *"La maggior parte di queste opzioni riguarda il risparmio. Ma poi arriviamo a qualcosa come il Dedicated Host e si tratta di spendere di più. È importante prima dell'esame essere ben armati con queste diverse opzioni."*

> **Note from Kimiko on billing**: *"Per molto tempo le risorse compute venivano addebitate su base oraria. Amazon è passata all'accumulo di addebiti al secondo, il che aiuterà a ridurre le bollette AWS per molti."*

---

## Placement Groups (from Dojo)

The Dojo describes three placement strategies:

| Strategy | How it works | Use case |
|---|---|---|
| **Cluster** | Instances close together in the same AZ. Can span peered VPCs in the same Region | Low latency, high network throughput |
| **Partition** | Instances distributed across logical partitions that don't share hardware. Max 7 partitions per AZ, multi-AZ | Reduces probability of correlated hardware failures (e.g. Hadoop, Cassandra, Kafka) |
| **Spread** | Each instance on a distinct hardware rack with its own network and power. Max 7 instances per AZ per group | Reduces correlated failures for critical applications |

Limitations (from Dojo):
- You cannot merge placement groups
- An instance cannot be in multiple placement groups
- You cannot launch Dedicated Hosts in placement groups
- A **cluster placement group cannot span multiple AZs**

---

## Auto Scaling — In Depth (from PACKT, Kimiko, Dojo)

### The 3 Components of Auto Scaling (from Dojo)

The Dojo identifies three main components:

1. **Auto Scaling Group**: logical unit for scaling and management. Has min, max, and desired number of instances
2. **Configuration Template**: launch template (recommended) or launch configuration. Contains AMI ID, instance type, key pair, security groups, block device mapping. The Dojo notes: *"È raccomandato usare un launch template piuttosto che una launch configuration, perché quest'ultima offre solo feature limitate."* With launch templates you can have **multiple versions** and **multiple instance types with different purchase options**
3. **Scaling Options**: dynamic, predictive, or scheduled

### Horizontal vs Vertical Scaling (from Dojo)

- **Horizontal Scaling**: add more servers. Distributed workload. Requires Auto Scaling + ELB. *"Ottimo per server stateless come web server pubblici"* (Dojo)
- **Vertical Scaling**: increase resources of a single server (CPU, RAM). *"Adatto per risorse stateful o operazioni difficili da gestire in modo distribuito, come write query su database"* (Dojo). For EC2 and RDS, the instance must be stopped before resizing

### Instance Warm-up and Cooldown (from Dojo)

- **Instance warm-up**: *"Il processo di lancio non è istantaneo. AWS deve recuperare l'AMI, fare la configurazione, eseguire lo user data, installare le applicazioni custom"* (Dojo)
- **Cooldown**: *"L'intervallo tra due azioni di scaling. Previene conflitti dove un'attività aggiunge istanze mentre un'altra le termina"* (Dojo)
- **Termination policy**: controls which instances are terminated first during scale-in (Dojo)

### Health Check with Load Balancer (from Dojo)

The Dojo notes: *"Quando associ un load balancer all'ASG, dovresti usare l'health check del load balancer per il monitoring. Quando un'istanza è considerata unhealthy dall'health check del LB, inizierà un evento di scaling per sostituire l'istanza difettosa."*

### Auto Scaling Groups — ASG (from PACKT)

PACKT describes ASGs as *"collezioni di istanze EC2 che condividono caratteristiche simili e servono uno scopo comune. Gli ASG ti permettono di specificare capacità minima, massima e desiderata."*

### Scaling Policies (from PACKT and Dojo)

The Dojo provides details on the 3 types of scaling policy:

**Simple Scaling** (from Dojo):
- Based on a single metric (e.g. CPU > 80% → add 20% capacity)
- *"Quando EC2 Auto Scaling fu introdotto, questa era l'unica policy supportata. Non fornisce controllo fine-grained."*
- Must wait for health checks to complete and cooldown to expire before responding to another alarm

**Target Tracking** (from Dojo):
- You specify a metric and a target value that the ASG must always maintain
- Example: *"La metrica è average CPU utilization, il target è 80%. Quando CloudWatch rileva che la media è sopra 80%, triggera la policy per scalare out. Quando scende sotto 80%, scala in."*
- Limitation: *"Scala out proporzionalmente alla metrica il più velocemente possibile, ma scala in più gradualmente"*
- Predefined metrics: `ASGAverageCPUUtilization`, `ASGAverageNetworkIn`, `ASGAverageNetworkOut`, `ALBRequestCountPerTarget`

**Step Scaling** (from Dojo):
- Improves simple scaling with **step adjustments** — different actions based on breach size
- *"Con step scaling, la policy può continuare a rispondere ad allarmi aggiuntivi anche nel mezzo di un evento di scaling"* (unlike simple scaling)
- Example from Dojo: CPU 40-60% → maintain. CPU 60-70% → +10%. CPU >70% → +30%. CPU 30-40% → -10%. CPU <30% → -30%

Common metrics for scaling (from PACKT):
- **CPU utilization** — for CPU-bound applications
- **Network traffic** — for applications with variable network activity (web servers, APIs)
- **Custom application metrics** — response time, queue length, any metric indicative of performance

### Scaling Actions (from PACKT)

- **Launching new instances**: in response to increased demand
- **Terminating instances**: when demand decreases, to reduce costs
- **Timeout parameter**: prevents constant scaling on sudden spikes. *"Non ha senso provisionare una nuova istanza se, quando viene online, le metriche di traffico sono tornate sotto la soglia"*
- **Cooldown policies**: stop further scaling for a period (e.g. 5 minutes)

### Predictive Scaling (from PACKT)

*"Il predictive scaling è una feature avanzata che sfrutta algoritmi di machine learning per prevedere la domanda futura basandosi su pattern storici."* Example: an accounting firm is busier in the last days of each month. Predictive scaling learns this pattern and starts scaling before demand grows.

### Lifecycle Hooks (from PACKT)

Allow custom actions during instance launch or termination:
- Before termination: graceful shutdown to avoid data loss
- Before receiving traffic: health checks and readiness validations
- Before serving: settings initialization (e.g. reading parameters from Parameter Store or Secrets Manager)

---

## High-Performance Compute (from PACKT Ch.14)

### Decoupling for Independent Scaling (from PACKT Ch.14)

PACKT Ch.14 explains: *"In un'applicazione web containerizzata, il frontend web può essere scalato separatamente dai container che gestiscono la logica applicativa. Questo permette maggiore scalabilità del frontend durante periodi di alto traffico, anche se il layer applicativo rimane invariato."*

### Choosing the Right Instance Type (from PACKT Ch.14)

PACKT Ch.14 provides guidelines:
- **High processing power** → Compute-optimized (C6i) for batch processing and HPC
- **Lots of memory** → Memory-optimized (R6g) for in-memory databases and real-time analytics
- **AI/ML** → Tranium and Inferentia instance types
- **High disk throughput** → Storage-optimized (I3) for data warehousing and distributed file systems

> **Exam tip (PACKT Ch.14)**: *"You may be expected to know what each of the instance family types are optimized for, so try to have a high-level understanding of each of the families."*

### Enhanced Networking (from Dojo)

The Dojo mentions advanced networking features:
- **Elastic Network Adapter (ENA)** — for high-performance networking
- **Intel 82599 Virtual Function (VF)** — alternative interface
- **Elastic Fabric Adapter (EFA)** — for HPC and ML workloads, network throughput beyond standard TCP

---

## Typical Exam Scenarios

### Scenario 1: Low-cost interruptible workload
**Question**: You have a batch processing job that can be interrupted. How to save money?

**Answer**: **Spot Instances** — up to 90% discount, with 2 minutes notice (Dojo).

### Scenario 2: Steady-state workload for 3 years
**Question**: An application runs 24/7 with predictable load for the next 3 years.

**Answer**: **Reserved Instances** or **Savings Plans** for 3 years with upfront payment for maximum discount (PACKT, Dojo).

### Scenario 3: Low latency between instances
**Question**: An HPC cluster requires the lowest possible latency between instances.

**Answer**: **Cluster Placement Group** in the same AZ (Dojo).

### Scenario 4: Temporary storage with very high IOPS
**Question**: You need storage with the highest possible IOPS, data doesn't need to persist.

**Answer**: **Instance Store** (Dojo: *"Instance store volumes are physically attached to the EC2 instances, so your instances are able to access the data much faster"*).

### Scenario 5: Per-socket licensing
**Question**: The company has per-socket software licenses that need to be brought to the cloud.

**Answer**: **Dedicated Hosts** — supports BYOL with socket and core visibility (Dojo).

### Scenario 6: Predictive scaling
**Question**: An application has predictable traffic patterns (end-of-month spikes).

**Answer**: **Predictive Scaling** with Auto Scaling (PACKT: *"Predictive scaling can learn this pattern and start to autoscale before demand grows"*).

---

## Quick Recap for the Exam

- **Instance families**: General (T/M), Compute (C), Memory (R/X), Storage (I/D), Accelerated (P/G), HPC (PACKT, Dojo)
- **Burstable (T)**: CPU credits, monitor to avoid degradation (PACKT)
- **Nitro**: up to 64,000 IOPS per EBS volume (Dojo)
- **Instance Store**: temporary, highest IOPS, data lost on stop (PACKT, Dojo)
- **EBS**: persistent, network-attached, snapshots possible (PACKT)
- **On-Demand**: no commitment. **Spot**: up to -90%, interruptible. **RI/Savings Plans**: 1-3 year commitment (Dojo, Kimiko)
- **Savings Plans**: more flexible than RIs. Compute SP also applies to Fargate and Lambda (Dojo)
- **Standard RI**: sellable on Marketplace. **Convertible RI**: change attributes but not sellable (Dojo)
- **Dedicated Hosts**: BYOL, hardware visibility. **Dedicated Instances**: isolation without visibility (Dojo)
- **Placement Groups**: Cluster (low latency, same AZ), Partition (isolated failures, max 7/AZ), Spread (distinct racks, max 7 instances/AZ) (Dojo)
- **Auto Scaling**: 3 components (ASG + template + scaling options). Launch template > launch configuration (Dojo)
- **Horizontal = more servers (stateless), Vertical = more resources (stateful)** (Dojo)
- **Warm-up**: time to prepare the instance. **Cooldown**: interval between scaling actions (Dojo)
- **ASG + LB**: use LB health check to replace unhealthy instances (Dojo)
- **Lifecycle Hooks**: custom actions before serving traffic or before termination (PACKT, Dojo)
- **EFA**: for HPC and ML, throughput beyond TCP (Dojo)
