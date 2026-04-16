# 📚 AWS SAA-C03 - Guida di Studio Incrociata

> Questa guida mappa ogni argomento dell'esame ai capitoli/sezioni specifici di ogni documento nel workspace.
> Usala per dire a Kiro: "Studiamo il topic X" e lui saprà esattamente dove andare a pescare le info.

## Legenda Documenti

| Alias | Documento | Tipo |
|-------|-----------|------|
| **PACKT** | `AWS-Certified-Solutions-Architect-Associate-_SAA-C03_-Exam-Michelle-Chismon_-Kate-Gawron-2024-Packt-.pdf` | PDF, 629 pagine |
| **KIMIKO** | `LEARN AWS CLOUD ARCHITECT_ Master the AWS Certified -- Furuta Kimiko -- 2024 -- *.pdf` | PDF, ~310 pagine |
| **DOJO** | `aws tutorial.pdf` (Tutorials Dojo Study Guide & Cheat Sheets) | PDF, 288 pagine |
| **LINKEDIN** | `Linkedin_Posts_2024_Blue.pdf` (ByteByteGo-style posts) | PDF, 368 pagine - contenuti generali system design |

---

## 🔐 DOMINIO 1: Design Secure Architectures (30%)

### 1.1 IAM - Identity and Access Management
- **PACKT**: Cap. 3 (p.156-185) - Users, Groups, Roles, Policies, IdPs, Access Analyzer, Policy Simulator + Hands-on
- **PACKT**: Cap. 12 (p.502-517) - Secure Access design, RBAC, IAM at scale
- **KIMIKO**: IAM (p.275-281) + Hands-on Challenge (p.280)
- **DOJO**: AWS IAM (p.204-210)

### 1.2 VPC Security - Security Groups, NACLs, VPC Endpoints
- **PACKT**: Cap. 2 (p.119-127) - Security Groups e NACLs, Stateful vs Stateless
- **PACKT**: Cap. 12 (p.509-510) - Application Network Security
- **KIMIKO**: VPCs (p.208-224) + Hands-on Building a VPC (p.213)
- **KIMIKO**: Firewalls in AWS (p.282-285)
- **DOJO**: Amazon VPC (p.163-172)

### 1.3 Encryption, KMS, Secrets Management
- **PACKT**: Cap. 10 (p.443-449) - Encryption at Rest/Transit, KMS, Secrets Manager
- **PACKT**: Cap. 12 (p.511-514) - Data Security Controls
- **KIMIKO**: AWS KMS (p.292-298)
- **DOJO**: AWS KMS (p.211-214)
- **DOJO**: Confronto KMS vs CloudHSM (p.283)

### 1.4 WAF, Shield, Network Firewall
- **PACKT**: Cap. 10 (p.455-458) - WAF e Shield
- **KIMIKO**: AWS WAF and Other Tools (p.286-291)
- **DOJO**: AWS WAF (p.215-216)
- **DOJO**: Confronto WAF vs Shield Basic vs Shield Advanced (p.281)

### 1.5 Threat Detection - GuardDuty, Inspector, Macie, Security Hub
- **PACKT**: Cap. 10 (p.450-455) - Inspector, GuardDuty, Macie, Security Hub
- **KIMIKO**: Lab Security Services (p.18-24), Macie (p.262-263)
- **DOJO**: Inspector, Detective, Security Hub, Network Firewall (p.221-223)

### 1.6 AWS Organizations, Multi-Account Strategy
- **PACKT**: Cap. 11 (p.466-472) - Organizations, Control Tower, Guardrails
- **KIMIKO**: AWS Organizations (p.301-302)

### 1.7 Shared Responsibility Model
- **PACKT**: Cap. 1 (p.81) + Cap. 12 (p.502-514)
- **KIMIKO**: Secure Design (p.102-108) + Scenario (p.106)

### 1.8 Controlling Access & Data Protection
- **PACKT**: Cap. 12 (p.502-514) - Design completo architetture sicure
- **KIMIKO**: Secure Design Scenario (p.106-108)
- **LINKEDIN**: Cloud Security Cheat Sheet (p.65), Cybersecurity 101 (p.295), HTTPS/SSL (p.190)

---

## 🔄 DOMINIO 2: Design Resilient Architectures (26%)

### 2.1 Elastic Load Balancing (ALB, NLB, GWLB)
- **PACKT**: Cap. 6 (p.288-309) - ELB, Target Groups, Listeners, ALB/NLB/GLB
- **KIMIKO**: Load Balancing (p.160-162)
- **DOJO**: AWS ELB (p.182-190)
- **LINKEDIN**: Key Use Cases for Load Balancers (p.35), Top 6 LB Algorithms (p.42), Cloud LB Cheat Sheet (p.109)

### 2.2 EC2 Auto Scaling
- **PACKT**: Cap. 4 (p.202-206) - ASGs, Scaling Policies, Predictive Scaling, Lifecycle Hooks
- **KIMIKO**: Autoscaling (p.155-159)
- **DOJO**: EC2 Auto Scaling (p.59-82)

### 2.3 Multi-AZ e Multi-Region Architectures
- **PACKT**: Cap. 1 (p.74-78) - Regions, AZs, Edge Locations
- **PACKT**: Cap. 13 (p.519-527) - HA e Fault-Tolerant Architectures
- **KIMIKO**: AWS Global Infrastructure (p.73-75)
- **DOJO**: AWS Basics - Global Infrastructure (p.35-44)

### 2.4 Disaster Recovery (RTO e RPO)
- **PACKT**: Cap. 13 (p.528-533) - DR Strategies
- **KIMIKO**: Resilient Design (p.85-91) + Scenario (p.89)
- **DOJO**: Disaster Recovery in AWS (p.45)
- **LINKEDIN**: Cloud Disaster Recovery Strategies (p.50), Fault-Tolerant Systems Cheat Sheet (p.330)

### 2.5 Decoupling - SQS, SNS, EventBridge
- **PACKT**: Cap. 9 (p.420-436) - SQS, SNS, EventBridge, Step Functions
- **KIMIKO**: SQS (p.143-147), SNS (p.148-152), Decoupling (p.140-142)
- **DOJO**: SNS (p.228-232), SQS (p.233-237)
- **LINKEDIN**: Top 6 Cloud Messaging Patterns (p.174)

### 2.6 Serverless Scalability
- **PACKT**: Cap. 13 (p.539-543) - Serverless Scalability patterns
- **PACKT**: Cap. 9 (p.413-419) - Lambda overview
- **KIMIKO**: API Gateway (p.153-154)
- **DOJO**: AWS Lambda (p.95-99)

### 2.7 Scalable & Loosely Coupled Architectures
- **PACKT**: Cap. 13 (p.534-543) - Design patterns
- **KIMIKO**: Multi-Tier Architecture (p.124-139), Decoupling (p.140-142)
- **LINKEDIN**: 9 Best Practices Microservices (p.102), System Design Blueprint (p.96)

---

## ⚡ DOMINIO 3: Design High-Performing Architectures (24%)

### 3.1 EC2 - Instance Types, Placement Groups
- **PACKT**: Cap. 4 (p.186-240) - EC2 completo, AMIs, Instance Store vs EBS, Spot, Reserved
- **PACKT**: Cap. 14 (p.552-560) - Compute ad alte prestazioni
- **KIMIKO**: EC2 Instance Purchase Options (p.305-308)
- **DOJO**: Amazon EC2 (p.46-58)

### 3.2 Lambda e Serverless/Container Services
- **PACKT**: Cap. 9 (p.413-419) - Lambda, event-driven, concurrency
- **PACKT**: Cap. 4 (p.212-226) - ECS, EKS, Fargate, AWS Batch
- **KIMIKO**: ECS (p.198-199)
- **DOJO**: Lambda (p.95-99), ECS (p.83-92), EKS (p.93-94)

### 3.3 S3 - Storage Classes, Lifecycle, Performance
- **PACKT**: Cap. 5 (p.246-256) - S3 Security, Versioning, Lifecycle, Replication
- **PACKT**: Cap. 14 (p.548-551) - Storage ad alte prestazioni
- **KIMIKO**: Hands-on S3 (p.169-174), S3 Storage Classes (p.309-310)
- **DOJO**: Amazon S3 (p.100-110), S3 Glacier (p.111-112)
- **DOJO**: Confronto S3 vs EBS vs EFS (p.269-270)

### 3.4 EBS, EFS, FSx - Block, File, Specialized Storage
- **PACKT**: Cap. 5 (p.256-266) - EBS, EFS, FSx, AWS Backup
- **KIMIKO**: Storage Gateway (p.200-203), Choosing Resilient Storage (p.163-168)
- **DOJO**: EBS (p.116-124), EFS (p.125-131), FSx (p.132-134)
- **DOJO**: Confronto EBS vs Instance Store (p.267), EFS vs FSx (p.276)

### 3.5 Database Services - RDS, Aurora, DynamoDB
- **PACKT**: Cap. 7 (p.314-377) - RDS, Aurora, RDS Proxy, DynamoDB, ElastiCache, DocumentDB, Neptune, Keyspaces, QLDB
- **PACKT**: Cap. 14 (p.561-568) - Database ad alte prestazioni, caching, read replicas
- **KIMIKO**: AWS RDS (p.237-239), DynamoDB (p.240-241), ElastiCache (p.242-245), Redshift (p.246-248)
- **DOJO**: RDS (p.135-141), Aurora (p.142-147), DynamoDB (p.148-155), Redshift (p.156-158)
- **DOJO**: Confronto RDS vs DynamoDB (p.278), Redis vs Memcached (p.280), RDS Read Replica vs Multi-AZ (p.284)

### 3.6 CloudFront, Route 53, Global Accelerator
- **PACKT**: Cap. 6 (p.277-309) - DNS, Route 53, CloudFront
- **PACKT**: Cap. 14 (p.569-577) - Network ad alte prestazioni
- **KIMIKO**: Route 53 (p.225-230), CloudFront (p.231-233)
- **DOJO**: Route 53 (p.173-181), CloudFront (p.191-198), Global Accelerator (p.203)
- **DOJO**: Confronto Global Accelerator vs CloudFront (p.271), Latency Routing vs CloudFront (p.275)

### 3.7 Data Ingestion & Analytics
- **PACKT**: Cap. 7 (p.354-377) - Redshift, EMR, QuickSight, Glue, Athena, Lake Formation
- **PACKT**: Cap. 7 (p.372-377) - Kinesis, MSK
- **PACKT**: Cap. 14 (p.578-583) - Data ingestion ad alte prestazioni
- **KIMIKO**: Analytics Engines (p.25-33), Athena (p.255-261), Kinesis (p.264-266)
- **DOJO**: Kinesis (p.238-242), Glue (p.243), Athena (p.364-365)
- **DOJO**: Confronto Kinesis vs SQS (p.274)

### 3.8 VPC Connectivity & Networking Avanzato
- **PACKT**: Cap. 2 (p.102-153) - VPC completo, CIDR, Subnetting, IGW, NAT, VPN, Peering, Transit GW
- **PACKT**: Cap. 14 (p.569-577) - Network scalabili
- **KIMIKO**: AWS Transit Gateway (p.43-44), VPCs (p.208-224)
- **DOJO**: VPC (p.163-172), Direct Connect (p.199-202)
- **DOJO**: Confronto Interface vs Gateway Endpoint (p.272)

---

## 💰 DOMINIO 4: Design Cost-Optimized Architectures (20%)

### 4.1 Modelli di Pricing (On-Demand, Reserved, Spot, Savings Plans)
- **PACKT**: Cap. 4 (p.200-201) - Spot e Reserved Instances
- **PACKT**: Cap. 15 (p.593-596) - Compute pricing models
- **KIMIKO**: EC2 Instance Purchase Options (p.305-308)
- **KIMIKO**: Cost Optimization (p.109-117) + Scenario (p.114)

### 4.2 Storage Cost Optimization
- **PACKT**: Cap. 15 (p.588-593) - S3, Glacier, EFS, EBS cost optimization
- **KIMIKO**: S3 Storage Classes (p.309-310), Working with Glacier (p.175-178)
- **DOJO**: S3 Glacier (p.111-112)

### 4.3 Database Cost Optimization
- **PACKT**: Cap. 15 (p.597-600) - Database cost planning
- **DOJO**: Confronto RDS Read Replica vs Multi-AZ vs Scaling (p.284), DynamoDB scaling (p.285)

### 4.4 Network Cost Optimization
- **PACKT**: Cap. 15 (p.601-602) - Network connectivity costs
- **DOJO**: Confronto S3 Transfer Acceleration vs Direct Connect vs VPN vs Snowball (p.263)

### 4.5 AWS Cost Management Tools
- **PACKT**: Cap. 11 (p.488-489) - Budgets, Cost Explorer, Cost & Usage Reports
- **PACKT**: Cap. 15 (p.603-605) - Cost management tools
- **KIMIKO**: AWS Cost Explorer (p.47-49), Billing Alarms (p.303-304)
- **LINKEDIN**: Cloud Cost Reduction Techniques (p.156)

### 4.6 Cloud Economics (TCO, ROI)
- **PACKT**: Cap. 1 (p.84-91) - Cloud Costs, TCO, ROI
- **KIMIKO**: Cost Optimization Scenario (p.114-117)

---

## 🔧 TRASVERSALI: Management, Governance & Migration

### Logging & Monitoring
- **PACKT**: Cap. 11 (p.485-487) - CloudTrail, CloudWatch
- **KIMIKO**: Cloud Watch (p.194-197)
- **DOJO**: CloudWatch (p.217-220), CloudTrail (p.224-227)
- **DOJO**: Confronto CloudTrail vs CloudWatch (p.261)

### Infrastructure as Code & Deployment
- **PACKT**: Cap. 11 (p.472-481) - CloudFormation, Service Catalog
- **KIMIKO**: Hands-on CloudFormation (p.179-188)
- **DOJO**: CloudFormation (p.256), Elastic Beanstalk (p.257), CodeDeploy (p.258)

### Migration & Data Transfer
- **PACKT**: Cap. 8 (p.386-410) - DataSync, Transfer Family, Storage Gateway, Snow Family, DMS
- **KIMIKO**: Storage Gateway (p.200-203), Snowball (p.204-207), DMS (p.249-251), DataSync (p.252-254)
- **DOJO**: Storage Gateway (p.113-115), DataSync vs Storage Gateway (p.262)

### Systems Manager & Config
- **PACKT**: Cap. 11 (p.481-484) - SSM, Patch Manager, Run Command, Parameter Store, AWS Config

### Well-Architected Framework
- **PACKT**: Cap. 1 (p.78-83) - I 4 pilastri del design
- **KIMIKO**: The Well Architected Framework (p.71-72), Operational Excellence (p.76-80)
- **KIMIKO**: Widget Makers Scenario (p.81-84)

---

## 🎯 RISORSE BONUS dal LinkedIn Posts PDF

Questi post non sono specifici SAA-C03 ma rinforzano concetti chiave di system design:

| Concetto | Pagina |
|----------|--------|
| Cloud Services Cheat Sheet | p.30, p.119 |
| Cloud Monitoring Cheat Sheet | p.31 |
| Cloud Security Cheat Sheet | p.65 |
| Cloud Disaster Recovery | p.50 |
| Cloud Load Balancer Cheat Sheet | p.109 |
| Cloud Cost Reduction | p.156 |
| AWS Services Cheat Sheet | p.236 |
| Database Types | p.64, p.131 |
| Caching Strategies | p.76, p.199, p.349 |
| API Gateway 101 | p.310 |
| VPN How it works | p.60 |
| Docker & Kubernetes | p.129, p.298, p.316 |
| Microservices Best Practices | p.102, p.161 |
| System Design Patterns | p.96, p.115, p.178 |
| Fault-Tolerant Systems | p.330 |
| Network Protocols | p.353 |

---

## 📋 Come Usare Questa Guida con Kiro

Quando vuoi studiare un argomento, scrivi qualcosa come:

> "Studiamo il topic 1.1 IAM"

Kiro andrà a leggere le sezioni specifiche da PACKT, KIMIKO e DOJO per darti una visione completa e incrociata dell'argomento, con le diverse prospettive di ogni autore.

### Ordine di Studio Consigliato

1. **Well-Architected Framework** (base concettuale)
2. **Dominio 1** - Security (30%) → IAM → VPC Security → Encryption → WAF/Shield → Threat Detection → Organizations
3. **Dominio 3** - High-Performing (24%) → EC2 → S3 → EBS/EFS → Databases → CloudFront/Route53 → Networking
4. **Dominio 2** - Resilient (26%) → ELB → Auto Scaling → Multi-AZ/Region → DR → Decoupling → Serverless
5. **Dominio 4** - Cost-Optimized (20%) → Pricing Models → Storage Costs → DB Costs → Network Costs → Tools
6. **Trasversali** → Monitoring → IaC → Migration → Systems Manager
