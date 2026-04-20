# Threat Detection - GuardDuty, Inspector, Macie, Security Hub

> Sources: PACKT Ch.10 (p.450-455), KIMIKO (p.18-24, p.262-263), DOJO (p.221-223)

---

## Overview

PACKT introduces the section with an important exam note: *"Non devi conoscere questi servizi in dettaglio per l'esame SAA-C03, ma dovresti capire cosa sono ad alto livello e capire come ogni servizio differisce dagli altri. Questo ti aiuterà a determinare la risposta corretta."*

The four main threat detection services are: **AWS Security Hub, Amazon Inspector, Amazon GuardDuty and Amazon Macie**.

---

## Amazon Inspector (from PACKT and Dojo)

PACKT describes Inspector as *"un servizio automatizzato di security assessment. Aiuta a identificare vulnerabilità e deviazioni dalle best practice di sicurezza nelle istanze Amazon EC2 e nelle immagini container."*

The Dojo adds: *"Dopo aver eseguito un assessment, Amazon Inspector produce una lista dettagliata di security findings prioritizzati per livello di severità. Fornisce un report automatizzato che identifica accesso di rete non intenzionale alle tue istanze EC2 e vulnerabilità in quelle istanze."*

Key characteristics (from PACKT):
- Uses **predefined rules packages** regularly updated to check for CVE (Common Vulnerabilities and Exposures), unintended network accessibility, and non-compliance with best practices
- Allows creating **custom templates and rules packages** for specific requirements
- Integrates with **Security Hub and GuardDuty** to centralize findings

---

## Amazon GuardDuty (from PACKT)

PACKT describes GuardDuty as *"un servizio di threat detection che monitora e analizza continuamente specifiche data sources e log AWS nel tuo ambiente. Sfruttando feed di threat intelligence e modelli di machine learning, GuardDuty identifica e ti avvisa di attività inaspettate e potenzialmente non autorizzate."*

### What It Detects (from PACKT)

- **Privilege escalation** and use of exposed credentials
- **Communication with malicious IPs and domains**
- **Malware** on EC2 instances and container workloads
- **Newly uploaded files** in S3 buckets
- **Anomalous login patterns** on databases
- **Compromised EC2 instances** running malicious software or unauthorized activities such as **cryptocurrency mining**
- **Suspicious account access** — unusual deployments in unfamiliar regions or atypical API calls suggesting security policy modifications

### How It Works (from PACKT)

- Each finding is categorized as **high, medium, or low** with remediation recommendations
- Base features monitor: **CloudTrail event logs and management events, VPC flow logs, and DNS logs**
- Additional insights available for: **EKS, Lambda, RDS, S3**, plus malware detection for EC2 and runtime monitoring
- Each additional package is available at an **extra cost**
- Integrates with **Security Hub** for a unified view

---

## Amazon Macie (from PACKT and Kimiko)

PACKT describes Macie as *"un servizio fully managed di data security e data privacy. È progettato per aiutarti a scoprire, monitorare e proteggere i tuoi dati sensibili salvati in bucket Amazon S3."*

### Key Characteristics (from PACKT)

- **Sensitive data discovery**: uses ML and pattern matching to automatically discover and classify sensitive data — PII, financial data, intellectual property
- **Continuous monitoring**: continuously monitors data access and usage activity in S3
- **Anomaly detection**: uses ML to establish a baseline of normal patterns and alerts on anomalous activity
- **Compliance reporting**: customizable reports for GDPR, HIPAA, PCI-DSS

### Context from Kimiko

Kimiko explains why Macie was created: *"Questo prodotto è nato perché c'erano così tante istanze di imbarazzo per le aziende che avevano informazioni sensibili nei bucket S3 senza le appropriate security policy in atto. Le persone potevano leggere informazioni dai bucket S3 che l'azienda non avrebbe mai voluto esporre."*

Kimiko shows in the console: *"La prima volta che visiti Macie, c'è un grande pulsante 'Get Started' e hai un trial gratuito di 30 giorni. Anche se sei ben oltre il tuo anno di free tier, la prima volta che lanci Macie, andrà a categorizzare i tuoi S3: public, unencrypted, shared."*

> **Note from Kimiko**: *"Macie non sarà un focus enorme nell'esame, ma devi conoscerlo. Pensa ai molti ruoli che Macie potrebbe avere per te: sicurezza, categorizzazione, pianificazione e redesign dell'approccio S3, compliance."*

> **Exam tip (PACKT)**: *"Se hai una domanda d'esame con Macie come risposta, prima stabilisci se i dati sono salvati in S3. Se no, puoi escludere Macie. Inoltre, Macie cerca specificamente PII. Se la domanda è su PII, cerca una risposta contenente Macie."*

---

## AWS Security Hub (from PACKT and Dojo)

PACKT describes Security Hub as *"uno strumento completo di sicurezza e compliance che fornisce una visione unificata della tua postura di sicurezza nel tuo ambiente AWS."*

The Dojo adds: *"Funziona come un hub che raccoglie alert e findings di sicurezza da più servizi AWS, come Amazon GuardDuty, Amazon Inspector, Amazon Macie, AWS IAM Access Analyzer, AWS Firewall Manager e altre fonti."*

### Key Characteristics

- **Aggregates findings** from various AWS services and third-party security tools (PACKT)
- **Analyzes findings**, identifies security trends, provides prioritized recommendations (PACKT)
- **Compliance monitoring**: you can use Security Hub for compliance with **PCI DSS, CIS Benchmarks** and many other standards (Dojo)
- **Response automation**: you can create custom security workflows to automatically trigger investigations, notify teams, or remediate identified issues (PACKT)

---

## Amazon Detective (from Dojo)

The Dojo describes Detective: *"Amazon Detective rende facile analizzare, investigare e identificare rapidamente la root cause di potenziali problemi di sicurezza o attività sospette. Detective raccoglie automaticamente log data dalle tue risorse AWS — da CloudTrail, VPC Flow Logs, GuardDuty findings e altri servizi AWS — poi usa machine learning per analizzare e condurre investigazioni di sicurezza."*

---

## AWS Network Firewall (from Dojo)

The Dojo provides the most detailed description: *"AWS Network Firewall è un servizio di firewall di rete gestito per i tuoi Amazon VPC. Viene con capacità di intrusion prevention e detection."*

### Use Cases (from Dojo)
- VPC-to-VPC traffic inspection
- Outbound traffic filtering
- Direct Connect and VPN connection protection
- Internet traffic filtering
- Fine-grained security controls for VPCs interconnected via Transit Gateway

### Components (from Dojo)
1. **Firewall**: the resource connected to the VPC, deployed in multiple AZs (one subnet per zone)
2. **Firewall Policy**: defines behavior with stateless and stateful rules. A firewall can have only one policy
3. **Rule Group**: collection of stateless or stateful rules. Includes 5-tuple (source IP, source port, dest IP, dest port, protocol) and domain name filtering

### Stateless vs Stateful (from Dojo)
- **Stateless**: has no context of the traffic flow, checks only the packet itself
- **Stateful**: knows the context/state of the packet, including the direction of the flow

> **Dojo Note**: *"Questo concetto è simile a NACLs e Security Groups. Una NACL è stateless, mentre un Security Group è stateful."*

---

## Kimiko's Security Services Lab

Kimiko dedicates an entire lab to security services, showing in the console:

### KMS (Key Management Service)
- Shows existing keys (AWS RDS key, AWS Lightsail key, custom keys)
- Creates a new key: choice between KMS or external material, tags, admin permissions, usage permissions
- Key actions: enable/disable, add/edit tags, **schedule key deletion**
- *"Per la rotazione delle chiavi, scheduli la cancellazione della vecchia e crei una nuova, poi configuri le applicazioni per usare la nuova chiave."*

### CloudHSM
- *"Un hardware security module che non è realmente hardware, è nel cloud. È un HSM virtuale."*
- How it works: you create a **cluster**, then create HSMs in the cluster. Applications call them programmatically to **offload encryption processing**
- You can also call an HSM in the AWS cloud from an on-premises server

### Directory Services
- **AWS Managed AD**: *"È vero Microsoft Active Directory. Lancia istanze di Windows Server con Active Directory."*
- **Simple AD**: *"Non è vero Active Directory. È una versione ridotta che gira su Linux Samba."*
- **AD Connector**: to connect to an existing Active Directory infrastructure
- **Cognito**: can be used as a directory service

### Security AMIs in the Marketplace
Kimiko shows that there are **428+ security products** in the AWS Marketplace, including Cisco Cloud Services Router, Trend Micro, next-gen firewalls, and even **Kali Linux** for penetration testing in the cloud.

---

## Typical Exam Scenarios

### Scenario 1: PII Data in S3
**Question**: You need to verify that no S3 buckets contain unprotected PII data.

**Answer**: **Amazon Macie** (PACKT: *"Macie specifically looks for PII. If the exam question is about PII, look for an answer containing Macie"*).

### Scenario 2: Vulnerabilities in EC2 Instances
**Question**: You want to automatically scan EC2 instances for software vulnerabilities.

**Answer**: **Amazon Inspector** (PACKT: *"Helps identify vulnerabilities and deviations from security best practices in EC2 instances and container images"*).

### Scenario 3: Malicious Activity in the Account
**Question**: You suspect an EC2 instance is doing cryptocurrency mining.

**Answer**: **Amazon GuardDuty** (PACKT: *"GuardDuty can uncover compromised EC2 instances running malicious software or engaging in unauthorized activities such as cryptocurrency mining"*).

### Scenario 4: Centralized Security Dashboard
**Question**: The CISO wants a unified security view across all accounts.

**Answer**: **AWS Security Hub** (Dojo: *"Provides a centralized and comprehensive view of the security posture across multiple AWS accounts"*).

### Scenario 5: Investigate an Incident
**Question**: GuardDuty detected anomalous access. You need to find the root cause.

**Answer**: **Amazon Detective** (Dojo: *"Makes it easy to analyze, investigate, and quickly identify the root cause of potential security issues"*).

---

## Quick Recap for the Exam

- **GuardDuty**: continuous threat detection, analyzes CloudTrail/VPC Flow/DNS logs, ML-based, detects crypto mining (PACKT)
- **Inspector**: vulnerability assessment (CVE), scans EC2 and containers, prioritized reports (PACKT, Dojo)
- **Macie**: finds PII in S3, ML + pattern matching, GDPR/HIPAA/PCI-DSS compliance (PACKT, Kimiko)
- **Security Hub**: aggregates findings from all services, PCI DSS/CIS compliance, response automation (PACKT, Dojo)
- **Detective**: post-incident investigation, root cause analysis, automatically collects logs (Dojo)
- **Network Firewall**: managed VPC firewall, IPS/IDS, stateless + stateful rules, 5-tuple filtering (Dojo)
- **Macie → S3 and PII only** (PACKT exam tip)
- **Deep details not needed** for the exam, but you must know what each service does and how they differ (PACKT)
- **CloudHSM**: for encryption processing offload, cluster-based, callable from on-premises too (Kimiko)
- **Directory Services**: AWS Managed AD (real AD), Simple AD (Linux Samba), AD Connector (bridge) (Kimiko)
