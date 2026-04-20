# Shared Responsibility Model and Data Protection

> Sources: PACKT Ch.1 (p.78-83), PACKT Ch.12 (p.502-514), KIMIKO Secure Design (p.102-108)

---

## Shared Responsibility Model

### The Principle (from Kimiko)

Kimiko explains it clearly: *"AWS è responsabile per la sicurezza DEL cloud. Questo significa che AWS si occupa di proteggere il proprio hardware, le proprie location fisiche, e tutto ciò che implementano per far funzionare le cose per te. Ma TU sei responsabile per la sicurezza NEL cloud. Questo significa che ti occupi di praticamente tutto dal sistema operativo in su quando si tratta delle tue istanze. Sei tu il responsabile di assicurarti che i tuoi bucket S3 siano sicuri, sei tu il responsabile di assicurarti di avere la sicurezza appropriata dentro i tuoi database, e così via."*

### Security Design Principles (from Kimiko)

Kimiko analyzes the AWS Security Pillar document (33 pages) and extracts the key principles:

1. **Implement a strong identity foundation** — *"Assicurati di avere i ruoli, utenti e gruppi appropriati in IAM e di rispettare il principio di least privilege. Dai alle persone le capacità di cui hanno bisogno in AWS e niente di più."*

2. **Enable traceability** — *"Dobbiamo poter auditare e rivedere le azioni che avvengono in AWS. Questo lo realizziamo con CloudTrail."*
   > **Warning from Kimiko**: *"CloudTrail può loggare molte cose se gli fai loggare tutto. E quando lo fai, puoi aumentare i tuoi costi in modo significativo. Assicurati di implementare CloudTrail per monitorare le cose che ti servono ma non quelle che non ti servono."*

3. **Apply security at all layers** — *"Il vecchio concetto tradizionale di defense in depth. Implementa la sicurezza a livello di account AWS, a livello di VPC, a livello di subnet, a livello di istanza, e anche dentro le istanze."*

4. **Automate security best practices** — *"Non solo le nostre azioni AWS ma anche il codice che deployiamo nel cloud deve essere sicuro. Servono buone pratiche di gestione AWS, buona sicurezza del sistema operativo nelle istanze EC2, e codice sviluppato secondo best practice."*

5. **Protect data in transit and at rest** — *"SSL e SSH per la sicurezza in transito, e le opzioni di encryption AWS per la sicurezza at rest."*

6. **Keep people away from data** — *"Fai in modo che l'accesso ai dati sia programmatico, attraverso applicazioni, interfacce web. Questo può prevenire molti danni accidentali e anche danni intenzionali — la minaccia dell'utente interno."*

7. **Prepare for security events** — *"CloudTrail e allarmi associati per notifiche rapide. E poi un piano di risposta per entrare in azione quando c'è un problema."*

### General Guidelines (from Kimiko)

1. **Implement IAM correctly** — MFA for the root account, users and groups with least privilege
2. **Detective controls** — CloudTrail to monitor the environment
3. **Infrastructure protection** — each account/role accesses only what it needs (e.g. a DB admin manages RDS but not S3 or EC2)
4. **Data protection** — backup, recovery, encryption
5. **Incident response plan** — team ready, procedures defined

### Kimiko's Key Recommendation on Policies

Kimiko makes an important practical recommendation: *"Servono nuove security policy per il mondo cloud in cui siamo. Molte delle security policy che le aziende hanno funzionano solo per soluzioni on-premises. Non hanno policy che trattano il cloud. Il cloud è arrivato e non abbiamo davvero pensato all'impatto che sta avendo. Le nostre security policy non sono state necessariamente riviste per assicurarsi che funzionino ancora in un mondo cloud."*

*"Forse servono policy speciali per qualsiasi cloud computing che fai, per qualsiasi cloud storage che fai. Torna indietro e rivedi quelle security policy."*

---

## Secure Design Scenario: Widget Makers (from Kimiko)

Kimiko returns to the Widget Makers scenario to apply security principles to the 5 systems to migrate:

### Order Processing (SQL Server → RDS)
- **IAM groups and policies** for secure database management — only authorized people can manage managed RDS instances
- **Internal database security** — implement the correct permissions inside the database (who can delete/update data)
- **Client application security** — the app is installed only on the machines where it should be, with authentication for the appropriate users

### Inventory Management (MySQL → RDS)
- **IAM groups and policies** for database management
- **Internal database security** — no one can change inventory levels without the appropriate permissions

### Payroll (SQL Server → RDS + Read Replica)
- **IAM groups and policies** for database management
- **Only the accounting department** can access the read replicas — the payroll database might be a general employee database (HR and managers can access it), but the read replica for payroll processing is for accounting only
- **Internal database security** — only those who need to modify/process data can do so

### User Data (Shared files → S3)
- **Security policies on S3 buckets** — only people from the department the bucket is intended for can access it
- **Encryption at rest** in the buckets
- **SSL for transfers** — all communications encrypted, so anyone capturing packets from the network cannot access the data

### Website (WordPress → EC2 + ELB)
- **Minimal IAM roles** for web server instances — *"Non vogliamo che i web server girino con un ruolo admin, perché se qualcuno riesce a violare il web server, magari attraverso una vulnerabilità WordPress, può attaccare il resto della nostra infrastruttura AWS"*
- **Correct Security Groups** on network interfaces — allow HTTP and HTTPS, nothing else
- **Correct Security Groups on the VPC** — allow into the VPC only what needs to enter it

> **Insight from Kimiko**: *"Le nostre raccomandazioni sono piuttosto basilari per la sicurezza, e questa è la buona notizia. Una volta che capisci tutti i concetti e gli strumenti, è lì che sta la complessità. Ora dobbiamo solo implementare la soluzione giusta per le nostre esigenze."*

---

## Design Secure Architectures — Exam Overview (from PACKT Ch.12)

PACKT Ch.12 structures the "Design Secure Architectures" domain into three task statements:

### 1. Design Secure Access to AWS Resources

Required knowledge (from PACKT Ch.12):
- Access controls and management across multiple AWS accounts
- Federated access and identity services (IAM, IAM Identity Center)
- AWS global infrastructure
- Security best practices (least privilege, shared responsibility)

Required skills:
- Apply best practices to IAM users and root users (including MFA)
- Design a flexible authorization model with users, groups, roles and policies
- Design an RBAC strategy with STS, role switching, cross-account access
- Design a multi-account security strategy with Control Tower and SCP
- Determine the appropriate use of resource policies and when to federate a directory service with IAM roles

### 2. Design Secure Workloads and Applications

PACKT Ch.12 identifies the two common attacks on the exam:
- **DDoS** — protection with scalable architectures, Shield, WAF, Network Firewall
- **SQL Injection** — protection with WAF (match conditions for malicious SQL code)

Additionally: *"Assicurati di salvare qualsiasi application secret in AWS Secrets Manager."*

### 3. Determine Appropriate Data Security Controls

PACKT Ch.12 divides into two categories:

**Controlling Data**:
- Control who accesses data with IAM
- For self-hosted databases on EC2, configure authentication and store passwords in Secrets Manager
- *"Il problema più grande per i dati è l'errore umano. Un semplice errore può cancellare un intero database in secondi"*
- Know RPO and RTO and how they affect backup strategy
- Familiarize yourself with S3 lifecycle policies and Intelligent-Tiering
- Protection from accidental deletion: S3 Versioning, Object Lock, MFA delete, RDS delete protection

**Encrypting Data**:
- *"I dati dovrebbero essere cifrati durante tutto il loro ciclo di vita. At rest con KMS, in transit con TLS e certificati in ACM"*
- When managing your own keys in KMS, lock down the key to limit who can use it
- Key rotation can be automated in KMS
- Certificate renewal in ACM

---

## Typical Exam Scenarios

### Scenario 1: Web Server with Too Many Permissions
**Question**: A WordPress web server on EC2 has an IAM role with admin access. What is the risk?

**Answer**: If someone exploits a WordPress vulnerability, they can attack the entire AWS infrastructure (Kimiko: *"Se qualcuno può violare il web server, può attaccare il resto della nostra infrastruttura AWS"*). Solution: IAM role with only the necessary permissions.

### Scenario 2: Protection from Human Error
**Question**: How do you protect an RDS database from accidental deletion?

**Answer**: Enable **RDS delete protection** + regular backups based on RPO (PACKT Ch.12).

### Scenario 3: Sensitive Data in S3
**Question**: How do you protect sensitive employee data stored in S3?

**Answer**: Bucket policy per department + encryption at rest + SSL for transfers (Widget Makers scenario from Kimiko).

### Scenario 4: Corporate Security Policies
**Question**: The company is migrating to the cloud but existing security policies only cover on-premises.

**Answer**: Create dedicated security policies for the cloud (Kimiko: *"Servono nuove security policy per il mondo cloud. Le policy tradizionali on-premises spesso non coprono scenari cloud"*).

---

## Quick Recap for the Exam

- **Shared Responsibility**: AWS = security OF the cloud (hardware, physical locations), You = security IN the cloud (OS, data, access) (Kimiko)
- **Defense in depth**: security at every layer — account → VPC → subnet → instance → inside the instance (Kimiko)
- **Least privilege**: grant only the necessary permissions, nothing more (Kimiko, PACKT)
- **CloudTrail**: for traceability, but watch costs if you log everything (Kimiko)
- **Keep people away from data**: programmatic access, not direct — protects from insider threat (Kimiko)
- **Human error > malicious threats**: the biggest problem for data (PACKT Ch.12)
- **RPO/RTO**: read the exam question carefully to understand if they are defined (PACKT Ch.12)
- **Deletion protection**: S3 Versioning + Object Lock + MFA delete, RDS delete protection (PACKT Ch.12)
- **Encryption lifecycle**: at rest with KMS, in transit with TLS/ACM (PACKT Ch.12)
- **Web servers with minimal roles**: never admin access on web instances (Kimiko Widget Makers scenario)
- **Cloud-specific security policies**: review corporate policies for the cloud (Kimiko)
- **Widget Makers Security**: IAM groups/policies for each system, encryption at rest for S3, SSL for transfers, correct SGs for web servers (Kimiko)
