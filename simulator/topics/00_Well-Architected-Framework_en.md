# AWS Well-Architected Framework (WAF)

> Sources: PACKT Ch.1 (p.78-98), KIMIKO (p.71-120), DOJO (p.38-45)

---

## Glossary: AWS Services You'll Find in This Document

Before diving in, let's clarify what each AWS service mentioned here actually does. So when you read "use RDS with Multi-AZ" you know exactly what that means.

### Compute

- **EC2 (Elastic Compute Cloud)** — a virtual machine in the cloud. Like having a computer (Linux or Windows) running in AWS data centers instead of your office. You can install anything: a web server, a database, an application. You pay for uptime and the power you choose (CPU, RAM, disk). There are different EC2 instance "classes": some optimized for heavy compute, others for memory, others for storage.

- **Lambda** — AWS's serverless service. You write your code, upload it, and AWS runs it when something happens (an event). No servers to manage: no OS to update, no instances to size. You pay only for actual execution time (milliseconds). It scales automatically: if 1000 concurrent requests arrive, Lambda runs 1000 copies of your code in parallel.

- **Auto Scaling** — the mechanism that automatically adds or removes EC2 instances based on load. If traffic increases, it launches new instances. If it decreases, it shuts them down. So you don't pay for idle servers and don't run out of resources during peaks.

### Storage

- **S3 (Simple Storage Service)** — AWS's object/file storage. Think of it as an infinite hard drive in the cloud where you can put any file: images, videos, documents, backups. Files are organized in "buckets" (containers). S3 is extremely durable (AWS guarantees 99.999999999% durability — you practically never lose a file) and redundant by default (data is automatically replicated across multiple facilities). You can also host a static website directly from S3.

- **S3 Glacier** — the "archive" version of S3. Much cheaper, but data isn't immediately available: when you request it, retrieval can take minutes to hours. Perfect for data you must keep for legal/compliance reasons but rarely access (e.g., old logs, historical backups).

- **EBS (Elastic Block Store)** — a virtual hard drive you attach to an EC2 instance. Like the SSD or HDD in your computer, but in the cloud. Data persists even if you stop the instance (unlike Instance Store which is temporary). You can choose between SSD (fast, for databases and apps) and magnetic HDD (slower, cheaper, for sequential data).

- **EFS (Elastic File System)** — a shared file system in the cloud. Unlike EBS (attached to ONE instance), EFS can be mounted by MANY EC2 instances simultaneously. Like a shared network folder in the office, but in the cloud. Scales automatically.

### Database

- **RDS (Relational Database Service)** — AWS's managed relational database service. "Managed" means AWS handles: installation, OS patching, automatic backups, database software updates. You only manage your data and queries. Supports multiple engines: MySQL, PostgreSQL, SQL Server, Oracle, MariaDB. It's like having a DBA (database administrator) working 24/7 for free on the infrastructure side.

- **Aurora** — AWS's proprietary relational database. Compatible with MySQL and PostgreSQL, but designed from scratch for the cloud. Up to 5x faster than MySQL and 3x faster than PostgreSQL. Automatically replicates data across 3 Availability Zones. Costs a bit more than standard RDS but offers superior performance and resilience.

- **DynamoDB** — AWS's NoSQL (non-relational) database. Instead of tables with rows and columns linked together (like SQL), it uses key-value pairs and JSON documents. Extremely fast (millisecond latency) and scales automatically. Perfect for applications needing ultra-fast responses with simple access patterns (e.g., e-commerce cart, user sessions, gaming).

- **ElastiCache** — an in-memory caching service. Puts the most requested data in RAM for ultra-fast access (microseconds). Supports Redis and Memcached. Example: instead of querying the database every time a user loads the homepage, put the result in cache. Subsequent requests read from cache (very fast) instead of the database (slower).

- **Read Replica** — a read-only copy of your database. The primary database handles reads AND writes. The read replica handles ONLY reads. Serves two purposes: 1) offload the primary database, 2) improve read performance. Data is automatically replicated from primary to replica. Example: payroll reads thousands of records → it does so from the read replica, so the primary database continues working normally for everyone else.

### Networking

- **VPC (Virtual Private Cloud)** — your private virtual network inside AWS. Like your office LAN, but in the cloud. Inside the VPC you define your subnets, access rules, who can talk to whom. Every AWS resource (EC2, RDS, etc.) lives inside a VPC.

- **Availability Zone (AZ)** — a physical data center (or group of data centers) within an AWS Region. Each Region has at least 2-3 AZs, physically separated (different buildings, different power supplies). If one data center goes down (fire, flood, blackout), the other AZs in the same Region keep working.

- **Multi-AZ** — means distributing your resources across multiple Availability Zones. For RDS, Multi-AZ automatically creates a database copy in another AZ. If the primary AZ has a problem, AWS performs automatic failover to the copy in the other AZ. Your database comes back online in minutes without manual intervention.

- **Region** — a geographic area where AWS has its data centers (e.g., eu-south-1 = Milan, us-east-1 = Virginia). Each Region is completely independent. Choose the Region closest to your users to reduce latency.

- **Edge Location** — mini data centers spread worldwide (hundreds of them). Used by CloudFront and other "edge" services to bring content as close as possible to end users.

- **ELB (Elastic Load Balancer)** — AWS's load balancer. Distributes incoming traffic across multiple EC2 instances. If you have 2 web servers, ELB sends 50% of requests to one and 50% to the other. If a server goes down, ELB stops sending traffic to it and directs everything to the other. Serves both performance (distribute load) and resilience (if one fails, the other continues).

- **CloudFront** — AWS's CDN (Content Delivery Network). Takes your content (images, videos, web pages) and copies it to Edge Locations worldwide. When a user in Italy requests an image, they get it from the nearest Edge Location instead of the server in Virginia. Result: much faster loading.

- **Route 53** — AWS's DNS service. Translates domain names (e.g., www.mysite.com) into IP addresses. Also offers intelligent routing: can send users to the nearest server, perform health checks, and redirect traffic if a server is down.

- **Security Group** — a virtual firewall for your EC2 instances. Defines which ports and protocols are allowed inbound and outbound. Example: for a web server you allow HTTP (port 80) and HTTPS (port 443) inbound, block everything else. It's "stateful": if you allow inbound traffic, the outbound response is automatically allowed.

### Security

- **IAM (Identity and Access Management)** — AWS's access management system. Controls WHO can do WHAT on which resources. You create users, groups, roles and policies (rules). Example: user "mario" belongs to group "developers" which has a policy allowing S3 reads but not EC2 instance deletion. The fundamental principle is "least privilege": give everyone ONLY the permissions they need, nothing more.

- **KMS (Key Management Service)** — the service for managing encryption keys. Creates and manages the keys you use to encrypt your data (in S3, EBS, RDS, etc.). You don't need to worry about securely storing keys: AWS does it for you.

- **CloudTrail** — records ALL API calls made in your AWS account. Who did what, when, from where. It's the "activity log" of your account. Essential for audit, compliance, and security incident investigation.

### Messaging and Integration

- **SQS (Simple Queue Service)** — a message queue. Application A puts a message in the queue, Application B reads and processes it when ready. Used to decouple components: if B is down or slow, messages wait in the queue without losing anything. Example: an e-commerce puts orders in the queue, the processing system handles them one at a time.

- **SNS (Simple Notification Service)** — a pub/sub (publish/subscribe) notification service. A publisher sends a message to a "topic", and all subscribers to that topic receive it. Can send emails, SMS, push notifications, or trigger Lambda. Example: when inventory drops below a threshold, SNS sends an email to the warehouse manager.

### Infrastructure as Code

- **CloudFormation** — the service for defining your infrastructure as code (JSON or YAML templates). You describe what you want (2 EC2 instances, 1 RDS database, 1 load balancer) in a file, and CloudFormation creates everything automatically. If you need to recreate the environment (disaster recovery, new test environment), launch the same template and have everything identical in minutes.

### Monitoring

- **CloudWatch** — AWS's monitoring service. Collects metrics (CPU, memory, disk, network) from all your resources, shows graphs, and can trigger alarms. Example: if an instance's CPU exceeds 80% for 5 minutes, CloudWatch can send an email or trigger an Auto Scaling action.

---

## What is the Well-Architected Framework

The WAF is the set of principles and best practices AWS defined for designing reliable, secure, efficient, and cost-effective cloud architectures. It's the compass for the SAA-C03 exam: the 4 exam domains directly correspond to 4 of the framework's 6 pillars.

The framework helps you evaluate your architectures against best practices and identify areas for improvement. It's not a rigid checklist, but a way to think critically about architectural decisions.

---

## The 6 Pillars

### 1. Operational Excellence

The ability to support development, run workloads effectively, and continuously improve processes.

Design Principles:
- **Perform operations as code** — treat infrastructure as code (CloudFormation, IaC)
- **Make frequent, small, reversible changes** — small changes reduce risk
- **Refine operations procedures frequently** — review and improve processes regularly
- **Anticipate failure** — design thinking about what can go wrong
- **Learn from all operational failures** — every incident is a learning opportunity

> In the SAA-C03 exam this pillar doesn't have a dedicated domain, but is cross-cutting across all questions.

---

### 2. Security (→ Exam Domain 1, 30%)

The ability to protect data, systems, and assets leveraging cloud technologies.

Design Principles:
- **Implement a strong identity foundation** — IAM with least privilege. Create appropriate users, groups, and roles. Use MFA for the root account
- **Enable traceability** — monitor and audit everything with CloudTrail. Warning: logging everything can significantly increase costs, log what matters
- **Apply security at all layers** — defense in depth: security at AWS account level, VPC, subnet, instance, and inside the instance itself
- **Automate security best practices** — secure code, hardened OS, automated configurations
- **Protect data in transit and at rest** — SSL/SSH for transit, AWS encryption for data at rest
- **Keep people away from data** — data access should be programmatic (via apps, APIs), not direct. Protects against accidental and intentional damage (insider threat)
- **Prepare for security events** — rapid notifications (CloudTrail + alarms) and a response plan ready

General guidelines:
- Implement IAM correctly (MFA, least privilege, groups with policies)
- Detective controls (CloudTrail to monitor activities)
- Infrastructure protection (each account/role accesses only what it needs)
- Data protection (backup, recovery, encryption)
- Incident response plan (team ready, defined procedures)

#### Shared Responsibility Model

Fundamental concept that frequently appears on the exam:

| AWS is responsible for... | You are responsible for... |
|---|---|
| Security **of** the cloud | Security **in** the cloud |
| Physical hardware | Guest operating system |
| Data centers and facilities | OS patches and updates |
| Network infrastructure | Firewall/security groups configuration |
| Virtualization | IAM (users, roles, policies) |
| | Encryption of your data |
| | Application security |
| | S3 bucket, database configuration, etc. |

> **Practical tip from Kimiko**: You need new security policies specific to the cloud. Traditional on-premises security policies often don't cover cloud scenarios. Review company policies and create dedicated policies for cloud computing and cloud storage.

---

### 3. Reliability (→ Exam Domain 2, 26%)

The ability of a workload to perform correctly and consistently over time.

Design Principles:
- **Test recovery procedures** — if you don't test recovery, you don't know if it works. Always try restoring from backups, launch CloudFormation templates to verify they work
- **Automatically recover from failure** — use CloudWatch to monitor and trigger automatic actions (e.g., launch new instances when existing ones are overloaded)
- **Scale horizontally** — decouple the application into separate components instead of scaling vertically (more CPU/RAM). Horizontal scaling = more instances. Vertical scaling = more powerful instance
- **Stop guessing capacity** — don't guess. Analyze actual usage (performance monitor, logs) and size accordingly
- **Manage change in automation** — scaling out/in, scaling up/down of RDS databases, everything must be automated. If it requires manual intervention, it's not truly resilient

Key concepts:
- **Five nines (99.999%)** and **Four nines (99.99%)** — target availability levels
- Resilience MUST be automatic: automatic recovery, automatic scaling, automatic backups
- Resilience ≠ Performance. Resilience = the system is available. Performance = the system responds quickly

---

### 4. Performance Efficiency (→ Exam Domain 3, 24%)

The ability to use computing resources efficiently and maintain that efficiency over time.

Design Principles:
- **Democratize advanced technologies** — don't reinvent the wheel. Use managed services (RDS instead of installing a DB on EC2, DynamoDB instead of writing files to S3). AWS has already optimized these services for you
- **Go global in minutes** — multi-region deploy to bring servers closer to users. Reduces latency, increases throughput
- **Use serverless architectures** — Lambda and API Gateway scale better than server-based architectures. Serverless scales automatically to the required level
- **Experiment more often** — the cloud makes testing affordable. You can create accounts, try different configurations, without buying hardware. Experiment because now you can afford it
- **Mechanical sympathy** — use the right technology for the right task. Think about the process, the tasks involved, and choose the best AWS solution for that specific process (e.g., consider data access patterns when choosing database or storage)

#### Storage Types and Performance

| Type | Service | Latency | Throughput | Sharing |
|---|---|---|---|---|
| Block Storage | EBS | Lowest, consistent | Single (1 instance) | Only through the instance |
| File System | EFS | Low, consistent | Multiple (N instances) | Yes, multi-client |
| Object Storage | S3 | Low | Web-scale | Yes, many clients |
| Archival | Glacier | Minutes → hours | High (once released) | No, only you |

> **Golden rule**: choosing the right instance type is the most important factor for performance. This concept repeats for every system: database, web server, applications. Right class = right performance.

---

### 5. Cost Optimization (→ Exam Domain 4, 20%)

The ability to run systems that deliver business value at the lowest possible cost.

Design Principles:
- **Adopt a consumption model** — pay only for what you consume. If you're a single-shift office, shut down servers at night and restart them in the morning. Distinguish between 24/7 services (for customers) and business-hours services (for employees)
- **Measure overall efficiency** — monitor the business value each system produces relative to its cost. If a department consumes 30% of AWS costs but produces 5% of value, re-evaluate
- **Stop spending money on data center operations** — AWS does rack & stack for you. Don't spend on building data centers to test new solutions
- **Analyze and attribute expenditure** — track where costs come from, by department, by project. Use AWS billing management tools
- **Use managed services to reduce cost of ownership** — RDS costs less in man-hours compared to managing a DB on EC2 (no OS management, patching, etc.)

The 4 sub-pillars of cost optimization:
1. **Use cost-effective resources** — sometimes a more powerful (and hourly expensive) instance is cheaper because it finishes the job faster
2. **Match supply with demand** — Auto Scaling to have the right number of servers at every moment
3. **Expenditure awareness** — use billing alerts to know when you exceed a threshold
4. **Optimize over time** — cost optimization is a continuous process. The more experience you have, the better you optimize

---

### 6. Sustainability

The ability to maximize efficiency and reduce environmental impact.

Design Principles:
- Understand your impact
- Establish sustainability goals
- Maximize utilization
- Anticipate and adopt new, more efficient hardware and software offerings
- Use managed services
- Reduce the downstream impact of your cloud workloads

> In the SAA-C03 exam this pillar, like Operational Excellence, is cross-cutting.

---

## Pillars → Exam Domain Mapping

| WAF Pillar | SAA-C03 Domain | Exam Weight |
|---|---|---|
| Security | Domain 1: Design Secure Architectures | **30%** |
| Reliability | Domain 2: Design Resilient Architectures | **26%** |
| Performance Efficiency | Domain 3: Design High-Performing Architectures | **24%** |
| Cost Optimization | Domain 4: Design Cost-Optimized Architectures | **20%** |
| Operational Excellence | Cross-cutting | — |
| Sustainability | Cross-cutting | — |

---

## Fundamental Cross-Cutting Concepts

### Cloud Economics: CapEx vs OpEx

| | CapEx (On-Premises) | OpEx (Cloud) |
|---|---|---|
| Model | Upfront hardware/software purchase | Pay-as-you-go |
| Initial investment | High | Minimal |
| Scalability | Expensive and complex, risk of over-provisioning | Easy and cost-effective, aligned with demand |
| Flexibility | Limited, slow to adapt | Wide range of services, rapid adaptation |
| Infrastructure management | Direct (hardware, staff, electricity, physical security) | Delegated to provider |

### TCO (Total Cost of Ownership)

TCO is the total cost of ownership over the entire lifecycle. Includes hidden costs often forgotten in cloud vs on-premises comparisons.

Practical example from PACKT (5 years):

**On-premises:**
- Initial cost (hardware + licenses): $10,000
- Annual recurring costs (maintenance $2,000 + energy $500 + IT staff $3,000) × 5 = $27,500
- **5-year TCO = $37,500**

**Cloud:**
- Monthly subscription: $500 × 12 × 5 = $30,000
- **5-year TCO = $30,000**

> Cloud wins by $7,500 in this scenario, and doesn't include hidden on-premises costs (physical space, cooling, physical security, training, downtime).

### ROI (Return on Investment)

ROI measures investment profitability: (net profit / total cost).
- **TCO** = what you'll spend (cost)
- **ROI** = what you'll gain (benefit)
- Use them together for a complete financial analysis

### Elasticity vs Scalability

- **Scalability** = I can grow (add resources)
- **Elasticity** = I can grow AND shrink (add AND remove resources)
- Auto Scaling is elastic: scales out (adds instances) and scales in (removes instances)
- Elastic Load Balancing is elastic: add and remove nodes from the set

### High Availability vs Fault Tolerance

- **High Availability** = redundant copies ready to take over. If a component fails, another takes its place. There may be brief downtime during failover
- **Fault Tolerance** = the system continues working even during component degradation. Detects the problem and reroutes automatically. Zero perceived downtime

### Disaster Recovery — The 4 Strategies

From cheapest to most expensive:

| Strategy | How it works | RTO | RPO | Cost |
|---|---|---|---|---|
| **Backup & Restore** | Frequent backups in secure location, restore when needed | Highest (hours) | Depends on backup frequency | Lowest |
| **Pilot Light** | Core components always active (e.g., DB with replica), rest starts on demand | Medium | Minimal for core components | Low-Medium |
| **Warm Standby** | Scaled-down but functional environment, always in sync, scale up on disaster | Low (minutes) | Minimal | Medium-High |
| **Multi-Site (Active-Active)** | Complete replica in active-active configuration, just redirect traffic | Lowest (seconds) | Near zero | Highest |

> **RTO** (Recovery Time Objective) = how long you can be down
> **RPO** (Recovery Point Objective) = how much data you can afford to lose

---

## Architectural Best Practices (from Dojo)

These best practices are a powerful summary of how to think "cloud-native":

### Design for Failure
- Clustering: extra instances ready to take over
- Multi-AZ: instances in different data centers
- Backups: for worst-case scenarios
- Alternative AWS account as cold/warm site

### Disposable Resources
- Treat servers as disposable, not as pets
- Bootstrapping, Docker images, golden AMIs to recreate resources quickly
- Infrastructure as Code (CloudFormation) to make everything reproducible

### Loose Coupling
- **Well-Defined Interfaces** — components interact only through APIs (e.g., RESTful)
- **Service Discovery** — microservices must be discoverable without knowing network topology
- **Asynchronous Integration** — if immediate response isn't needed, use durable intermediate storage (SQS)
- **Distributed Systems Best Practices** — handle component failure gracefully

### Services, Not Servers
- Prefer managed services (RDS, DynamoDB, SQS) over self-managed solutions on EC2
- Serverless (Lambda) for event-driven and synchronous services without managing infrastructure

### Removing Single Points of Failure
- **Standby redundancy** — failover to secondary resource (used for stateful components like relational DBs)
- **Active redundancy** — requests distributed across multiple resources, if one fails the others absorb the load
- **Synchronous replication** — confirms transaction only after written to primary AND replica (maximum integrity)
- **Asynchronous replication** — decouples primary and replica, introduces replication lag but better performance
- **Quorum-based replication** — mix of both, defines minimum number of nodes for a successful write

### Optimize for Cost
- **Right Sizing** — choose the right type and size for the workload
- **Elasticity** — use and release resources, don't keep them idle
- **Purchasing Options** — Reserved Instances, Spot Instances, Savings Plans

### Caching
- **Application Data Caching** — in-memory cache (ElastiCache) for frequently accessed data
- **Edge Caching** — CloudFront to serve content from infrastructure close to users

---

## Practical Scenario: Widget Makers (from Kimiko)

Kimiko presents a real-world scenario of a company ("Widget Makers") that needs to migrate 5 systems to the cloud. For each pillar, concrete recommendations are shown. This is gold for understanding how to apply theory.

### The Company
Widget Makers has 5 systems to migrate:
1. **Order Processing** — SQL Server database for orders
2. **Inventory Management** — MySQL database for inventory
3. **Payroll** — SQL Server database for payroll
4. **User Data** — shared files on local servers (~700MB per user)
5. **Website** — WordPress on internal servers

### Reliability Pillar — What to Do

| System | Recommendation |
|---|---|
| Order Processing | SQL Server → RDS managed instance + **Multi-AZ** |
| Inventory Management | MySQL → RDS managed instance + **Multi-AZ** (no clustering needed) |
| Payroll | SQL Server → RDS + Multi-AZ + **Read Replica** (payroll is read-intensive during processing) |
| User Data | Shared files → **S3 buckets** (inherent resilience). Need a third-party tool to map drive letters to S3 |
| Website | WordPress → **2 instances behind Elastic Load Balancer** (if one fails, the other continues) |

> **Key insight**: the read replica for payroll is brilliant. Payroll runs every 1-2 weeks, does many intensive reads. The read replica avoids impacting the primary database during processing.

### Performance Pillar — What to Do

| System | Recommendation |
|---|---|
| Order Processing | Choose the **right instance class** for sufficient memory and CPU |
| Inventory Management | Same + automate inventory notifications with **SNS** + consider CloudWatch for automatic orders below threshold |
| Payroll | Right class + process payroll **only from the read replica** for better performance |
| User Data | **S3 bucket per department** to distribute load + alarms for users exceeding 700MB |
| Website | Right class + **EBS on SSD** (not magnetic) + ELB for load balancing between web servers |

> **Repeated tip**: "Ensure instances are in a class providing sufficient memory and processing capabilities" — this is THE most important pattern for performance. Right class = right performance.

> **Often forgotten tip**: when migrating to the cloud, verify that the company's **internet connection** is sufficient. You can have the most performant AWS architecture in the world, but if you have 50 Mbps for 200 users, performance will be poor.

### Security Pillar — What to Do

| System | Recommendation |
|---|---|
| Order Processing | IAM groups + policies for DB management + internal DB security (SQL permissions) + client app security |
| Inventory Management | IAM groups + policies + internal DB security (no one modifies inventory without permissions) |
| Payroll | IAM groups + policies + **only accounting accesses the read replica** + internal DB security |
| User Data | **S3 bucket policies** per department + **encryption at rest** + **SSL for transfers** |
| Website | Instances with **minimal IAM roles** (no admin access, otherwise a WordPress breach compromises all of AWS) + correct **Security Groups** (HTTP/HTTPS only) + correct SGs on VPC |

> **Critical insight**: if the web server runs with an admin role and someone exploits a WordPress vulnerability, they can attack the entire AWS infrastructure. Give the web server ONLY the permissions it needs.

### Cost Optimization Pillar — What to Do

| System | Recommendation |
|---|---|
| Order Processing | Use **managed database** (RDS) → fewer man-hours of management |
| Inventory Management | Same, managed database |
| Payroll | Managed database + **read replica active only when needed** (don't keep it running 24/7 if payroll runs every 2 weeks) |
| User Data | **Monitor** what users put in buckets. If they upload personal photos/videos, costs rise and performance drops |
| Website | **Right class, no more** (you can always upgrade later) + monitor anomalous access (e.g., someone exploits a vulnerability to host pirated files → bandwidth costs skyrocket) |

> **Brilliant insight**: the payroll read replica turns on the evening before processing, replicates data overnight, payroll runs in the morning, then shuts down. You pay for a few hours every 2 weeks instead of 24/7.

---

## Quick Recap for the Exam

- The WAF has **6 pillars**, the exam directly tests **4**
- **Security is the heaviest domain** (30%) — IAM, encryption, defense in depth
- **Shared Responsibility**: AWS = security OF the cloud, You = security IN the cloud
- **Elasticity > Scalability**: elasticity = grow AND shrink
- **DR strategies**: Backup&Restore → Pilot Light → Warm Standby → Multi-Site (increasing cost, decreasing RTO/RPO)
- **Loose coupling** (SQS, SNS) prevents cascading failures
- **Managed services** > self-managed (lower operational costs, better performance)
- **Right-sizing** is fundamental: right class = right performance = right cost
- **Infrastructure as Code** (CloudFormation) for reproducibility and disaster recovery
- **Consumption model**: pay only for what you use, shut down what you don't need
