# Cross-Cutting: Monitoring, IaC, Migration

> Sources: PACKT Ch.11 (p.472-490), PACKT Ch.8 (p.386-410), KIMIKO (p.179-188, p.194-197, p.200-207, p.249-254), DOJO (p.217-227, p.261-263)

---

## Glossary: the services you will encounter in this document

### Monitoring

- **CloudTrail** — records ALL API calls made in your AWS account. Who did what, when, from where. It's the "activity log" of your account. Essential for audit, compliance, and security incident investigation. Like the surveillance cameras of a building: they record who enters, who exits, and what they do.

- **CloudWatch** — the AWS monitoring service. It collects metrics (CPU, memory, disk, network) from all your resources, shows graphs, and can trigger alarms. Example: if an instance's CPU exceeds 80% for 5 minutes, CloudWatch can send an email or launch an Auto Scaling action. Like your car's dashboard: it shows you speed, temperature, fuel level.

- **AWS Config** — monitors and records AWS resource configurations over time. It doesn't prevent changes, it detects and reports them. It can verify whether resources comply with compliance rules. Like an auditor who periodically checks that everything is in order.

### Infrastructure as Code

- **CloudFormation** — the service for defining your infrastructure as code (JSON or YAML templates). You describe what you want (2 EC2 instances, 1 RDS database, 1 load balancer) in a file, and CloudFormation creates everything automatically. If you need to recreate the environment, you launch the same template and have everything identical in minutes. Like an architectural blueprint: you give it to the builder and they construct the house exactly as in the blueprint.

- **SSM (Systems Manager)** — a suite of tools for managing infrastructure. Includes: Patch Manager (automatic patching), Run Command (run commands without SSH), Parameter Store (save configurations), Session Manager (secure access without open SSH ports).

### Migration

- **DataSync** — for transferring large volumes of files between on-premises and AWS (or between AWS services). Like a professional moving service: packs everything, transports it, and puts it in place in the new house.

- **DMS (Database Migration Service)** — for migrating databases from on-premises to AWS, or between AWS services. Supports initial migration + continuous replication. Also works with the Schema Conversion Tool to change database type during migration.

- **Snow Family** — physical devices for transferring enormous amounts of data when internet isn't enough. Snowball (terabytes), Snowball Edge (terabytes + compute at the edge), Snowmobile (petabytes/exabytes — literally a truck). Like shipping a container full of hard drives instead of trying to upload everything via internet.

- **Storage Gateway** — a bridge between on-premises and cloud for continuous hybrid access. Unlike DataSync (which transfers), Storage Gateway maintains data access from both on-premises and the cloud.

- **Transfer Family** — for transferring files using standard protocols (SFTP, FTPS, FTP). Useful for sharing files with external partners who use these protocols.

---

## PART 1: Logging and Monitoring

### AWS CloudTrail (from PACKT)

PACKT describes: *"CloudTrail abilita il monitoraggio e logging continuo della tua infrastruttura AWS. Registra tutte le azioni nel tuo account, incluse le chiamate API fatte da utenti, ruoli o servizi."*

Key details from PACKT:
- **Enabled by default** — saves the last **90 days** of events for free in the event history
- For a custom view, you create a **trail** specifying: which events to log, which S3 bucket, which Regions, whether to receive notifications

**Two types of events** (from PACKT):
| Type | What it logs | Cost |
|---|---|---|
| **Management events** | API calls that create, modify, or delete AWS resources, or change configurations | **Free** |
| **Data events** | Activity on the resources themselves (S3 bucket access, Lambda invocation) | **Paid** |

> **Exam tip (PACKT)**: *"CloudTrail NON è un servizio real-time. Può richiedere circa 15 minuti perché un'attività appaia in CloudTrail. Questo è un punto chiave per l'esame."*

### Amazon CloudWatch (from PACKT and Kimiko)

PACKT describes CloudWatch as the service for *"raccogliere, analizzare e agire su varie metriche e log generati dalle tue risorse AWS."*

Kimiko shows CloudWatch in the console: *"CloudWatch è dove monitoriamo le nostre risorse. Possiamo vedere metriche come CPU, memoria, disco, rete. Possiamo impostare allarmi che triggerano azioni."*

### CloudTrail vs CloudWatch (from Dojo)

Dojo provides the key comparison:

| Feature | CloudTrail | CloudWatch |
|---|---|---|
| **Focus** | **Who did what** — audit trail of API calls | **How are resources doing** — metrics and performance |
| **Question** | "Who modified this resource?" | "Is the CPU at 90%?" |
| **Type** | Activity logging | Metrics monitoring |
| **Action** | Audit, compliance, investigation | Alarms, auto scaling, notifications |

> **Exam rule**: CloudTrail = audit/compliance (who did what). CloudWatch = monitoring/performance (how are resources doing).

---

## PART 2: Infrastructure as Code

### AWS CloudFormation (from PACKT and Kimiko)

PACKT describes CloudFormation as the service for *"definire e provisionare risorse AWS usando template. I template sono scritti in JSON o YAML e descrivono le risorse che vuoi creare."*

Kimiko shows the process in the console with a detailed walkthrough: *"CloudFormation è incredibilmente potente. Scrivi un template che descrive la tua infrastruttura, e CloudFormation crea tutto automaticamente. Se devi ricreare l'ambiente — disaster recovery, nuovo ambiente di test — lanci lo stesso template e hai tutto identico in minuti."*

Key concepts from PACKT:
- **Stack**: a set of AWS resources created from a template
- **Change Sets**: preview of changes before applying them
- **Drift Detection**: detects if resources have been manually modified compared to the template
- **Nested Stacks**: templates that reference other templates for modularity
- **StackSets**: deploy stacks across multiple accounts and Regions simultaneously

### AWS Service Catalog (from PACKT)

PACKT describes: *"Service Catalog permette alle organizzazioni di creare e gestire cataloghi di prodotti IT approvati. Gli utenti possono lanciare solo i prodotti approvati, garantendo compliance e governance."*

### AWS Systems Manager — SSM (from PACKT)

PACKT describes SSM as a suite of tools for managing infrastructure:
- **Patch Manager**: automates patching of EC2 instances
- **Run Command**: run commands on EC2 instances without SSH
- **Parameter Store**: save configuration parameters and secrets
- **Session Manager**: secure access to instances without opening SSH ports
- **Automation**: automates common operational tasks

---

## PART 3: Migration and Data Transfer

### AWS DataSync (from PACKT and Kimiko)

PACKT describes: *"DataSync supporta lo spostamento di grandi volumi di dati tra storage on-premises e AWS. Puoi anche usarlo per spostare dati tra soluzioni storage AWS."*

Kimiko explains: *"Il Database Migration Service è fantastico, ma è appropriato se i tuoi dati sono in un database. E tutti quei dati che non sono in un database? Magari hai un network file server con migliaia di file di log. DataSync è la soluzione."*

> **PACKT Note**: *"DataSync NON supporta migrazione a EBS. DataSync supporta lo spostamento di file, non blocchi. Se la domanda chiede come spostare storage da on-premises a EBS, DataSync non può essere la risposta corretta."*

### AWS Snow Family (from Kimiko)

Kimiko describes the evolution of the Snow Family:

| Device | What it does | When to use |
|---|---|---|
| **Import/Export** (classic) | You send your media (thumb drive, hard drive, DVD) to AWS | Small amounts, any format |
| **Snowball** | Rugged device shipped by AWS. Connect to data center, transfer data, ship back. GPS tracking, encryption by default | Large amounts of data (terabytes) |
| **Snowball Edge** | Like Snowball but with **integrated AWS services** (e.g., EC2). Stays at your data center as a gateway | When edge compute + data transfer is needed |
| **Snowmobile** | 18-wheel truck with armed guards. For **exabyte/petabyte** of data | *"Per aziende con quantità massive di dati che richiederebbero decenni per trasferire con le tecnologie più veloci di oggi"* |

> **Tip from Kimiko**: *"Come solutions architect, assicurati di conoscere Snowball, Snowball Edge e Snowmobile e come ciascuno potrebbe trovare posto nella tua soluzione cloud."*

### AWS Database Migration Service — DMS (from Kimiko)

Kimiko describes DMS: *"Le aziende arrivano ad AWS con database grandi, magari multipli tipi — SQL, NoSQL, data warehouse. DMS fa la migrazione iniziale di tutti i dati, ma puoi anche tenerlo in esecuzione per la replicazione continua."*

Key features from Kimiko:
- **Initial migration** + optional **continuous replication**
- Works with **AWS Schema Conversion Tool (SCT)** to change schema during migration
- Also works **cloud-to-cloud** (e.g., Azure → AWS)
- You create a **replication instance** in a VPC, configure endpoints and migration tasks

### AWS Transfer Family (from PACKT)

PACKT describes Transfer Family for file transfers using standard protocols:
- Supports **SFTP, FTPS, FTP, AS2**
- Integration with S3 and EFS
- Useful for sharing files with external partners

### AWS Application Migration Service — MGN (from PACKT)

PACKT describes MGN as the service for migrating entire applications (lift-and-shift):
- Continuously replicates source servers to AWS
- Allows non-disruptive testing before cutover
- Supports migration from any infrastructure (on-premises, other clouds)

### Storage Gateway (from Kimiko — already covered in topic 11)

Kimiko reminds: *"Storage Gateway è tre prodotti: File Gateway (interfaccia S3 via NFS/SMB), Volume Gateway (block storage con backup AWS), Tape Gateway (emula librerie tape per backup cloud)."*

### DataSync vs Storage Gateway (from Dojo)

Dojo provides the distinction:
- **DataSync**: for data **transfer/migration** — one-time or scheduled
- **Storage Gateway**: for **continuous hybrid access** — data remains accessible both on-premises and in AWS

---

## Typical Exam Scenarios

### Scenario 1: Who deleted an S3 bucket?
**Question**: An S3 bucket was deleted. How to find out who did it?

**Answer**: **CloudTrail** — logs all API calls, including who did what and when (PACKT).

### Scenario 2: Alarm when CPU exceeds 80%
**Question**: You want to be notified when an instance's CPU exceeds 80%.

**Answer**: **CloudWatch** alarm with CPU > 80% threshold + SNS notification (Kimiko).

### Scenario 3: Migrate terabytes of files to S3
**Question**: You need to move 50 TB of files from an on-premises NFS server to S3.

**Answer**: **DataSync** — for large volumes of files from on-premises to S3/EFS/FSx (PACKT, Kimiko).

### Scenario 4: Migrate petabytes of data
**Question**: The company has 100 PB of data to migrate. Internet transfer would take years.

**Answer**: **Snowmobile** (Kimiko: *"Per quantità massive che richiederebbero decenni via internet"*).

### Scenario 5: Migrate Oracle database to Aurora
**Question**: You need to migrate an on-premises Oracle database to Aurora PostgreSQL.

**Answer**: **DMS + Schema Conversion Tool** — DMS migrates the data, SCT converts the schema (Kimiko).

### Scenario 6: Reproducible infrastructure
**Question**: You need to be able to recreate the entire environment in minutes for DR.

**Answer**: **CloudFormation** — template that describes all the infrastructure, launch it and recreate everything (PACKT, Kimiko).

### Scenario 7: Continuous hybrid file access
**Question**: On-premises users need to continue accessing files that are also in S3.

**Answer**: **Storage Gateway (File Gateway)** — not DataSync (Dojo: DataSync is for transfer, Storage Gateway for continuous access).

---

## Quick Review for the Exam

**Monitoring:**
- **CloudTrail**: audit trail, who did what, 90 days free, NOT real-time (15 min delay), management events free, data events paid (PACKT)
- **CloudWatch**: metrics, alarms, auto scaling triggers, performance monitoring (PACKT, Kimiko)
- **CloudTrail = audit, CloudWatch = monitoring** (Dojo)

**IaC:**
- **CloudFormation**: JSON/YAML templates, stacks, change sets, drift detection, StackSets for multi-account (PACKT)
- **Service Catalog**: catalog of approved IT products for governance (PACKT)
- **SSM**: Patch Manager, Run Command, Parameter Store, Session Manager (PACKT)

**Migration:**
- **DataSync**: file transfer on-premises ↔ AWS (S3/EFS/FSx), does NOT support EBS (PACKT)
- **Snow Family**: Snowball (TB), Snowball Edge (compute + storage), Snowmobile (PB/EB) (Kimiko)
- **DMS**: database migration + continuous replication + SCT for schema conversion (Kimiko)
- **Transfer Family**: SFTP/FTPS/FTP for file sharing with partners (PACKT)
- **MGN**: lift-and-shift of entire applications (PACKT)
- **DataSync = transfer, Storage Gateway = continuous hybrid access** (Dojo)
