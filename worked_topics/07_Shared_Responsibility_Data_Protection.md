# Shared Responsibility Model e Data Protection

> Fonti: PACKT Cap.1 (p.78-83), PACKT Cap.12 (p.502-514), KIMIKO Secure Design (p.102-108)

---

## Shared Responsibility Model

### Il Principio (da Kimiko)

Kimiko lo spiega con chiarezza: *"AWS è responsabile per la sicurezza DEL cloud. Questo significa che AWS si occupa di proteggere il proprio hardware, le proprie location fisiche, e tutto ciò che implementano per far funzionare le cose per te. Ma TU sei responsabile per la sicurezza NEL cloud. Questo significa che ti occupi di praticamente tutto dal sistema operativo in su quando si tratta delle tue istanze. Sei tu il responsabile di assicurarti che i tuoi bucket S3 siano sicuri, sei tu il responsabile di assicurarti di avere la sicurezza appropriata dentro i tuoi database, e così via."*

### I Design Principles della Sicurezza (da Kimiko)

Kimiko analizza il documento AWS Security Pillar (33 pagine) e ne estrae i principi chiave:

1. **Implement a strong identity foundation** — *"Assicurati di avere i ruoli, utenti e gruppi appropriati in IAM e di rispettare il principio di least privilege. Dai alle persone le capacità di cui hanno bisogno in AWS e niente di più."*

2. **Enable traceability** — *"Dobbiamo poter auditare e rivedere le azioni che avvengono in AWS. Questo lo realizziamo con CloudTrail."*
   > **Avvertimento da Kimiko**: *"CloudTrail può loggare molte cose se gli fai loggare tutto. E quando lo fai, puoi aumentare i tuoi costi in modo significativo. Assicurati di implementare CloudTrail per monitorare le cose che ti servono ma non quelle che non ti servono."*

3. **Apply security at all layers** — *"Il vecchio concetto tradizionale di defense in depth. Implementa la sicurezza a livello di account AWS, a livello di VPC, a livello di subnet, a livello di istanza, e anche dentro le istanze."*

4. **Automate security best practices** — *"Non solo le nostre azioni AWS ma anche il codice che deployiamo nel cloud deve essere sicuro. Servono buone pratiche di gestione AWS, buona sicurezza del sistema operativo nelle istanze EC2, e codice sviluppato secondo best practice."*

5. **Protect data in transit and at rest** — *"SSL e SSH per la sicurezza in transito, e le opzioni di encryption AWS per la sicurezza at rest."*

6. **Keep people away from data** — *"Fai in modo che l'accesso ai dati sia programmatico, attraverso applicazioni, interfacce web. Questo può prevenire molti danni accidentali e anche danni intenzionali — la minaccia dell'utente interno."*

7. **Prepare for security events** — *"CloudTrail e allarmi associati per notifiche rapide. E poi un piano di risposta per entrare in azione quando c'è un problema."*

### Linee Guida Generali (da Kimiko)

1. **Implementa IAM correttamente** — MFA per il root account, utenti e gruppi con least privilege
2. **Detective controls** — CloudTrail per monitorare l'ambiente
3. **Infrastructure protection** — ogni account/ruolo accede solo a ciò che serve (es. un DB admin gestisce RDS ma non S3 o EC2)
4. **Data protection** — backup, recovery, encryption
5. **Incident response plan** — team pronto, procedure definite

### La Raccomandazione Chiave di Kimiko sulle Policy

Kimiko fa una raccomandazione pratica importante: *"Servono nuove security policy per il mondo cloud in cui siamo. Molte delle security policy che le aziende hanno funzionano solo per soluzioni on-premises. Non hanno policy che trattano il cloud. Il cloud è arrivato e non abbiamo davvero pensato all'impatto che sta avendo. Le nostre security policy non sono state necessariamente riviste per assicurarsi che funzionino ancora in un mondo cloud."*

*"Forse servono policy speciali per qualsiasi cloud computing che fai, per qualsiasi cloud storage che fai. Torna indietro e rivedi quelle security policy."*

---

## Secure Design Scenario: Widget Makers (da Kimiko)

Kimiko torna allo scenario Widget Makers per applicare i principi di sicurezza ai 5 sistemi da migrare:

### Order Processing (SQL Server → RDS)
- **IAM groups e policies** per gestione sicura del database — solo le persone autorizzate possono gestire le istanze RDS managed
- **Sicurezza interna del database** — implementare i permessi corretti dentro il database (chi può cancellare/aggiornare dati)
- **Sicurezza dell'applicazione client** — l'app è installata solo sulle macchine dove dovrebbe essere, con autenticazione per gli utenti appropriati

### Inventory Management (MySQL → RDS)
- **IAM groups e policies** per gestione database
- **Sicurezza interna del database** — nessuno può cambiare i livelli di inventario senza i permessi appropriati

### Payroll (SQL Server → RDS + Read Replica)
- **IAM groups e policies** per gestione database
- **Solo il dipartimento accounting** può accedere alle read replica — il database payroll potrebbe essere un database generale dei dipendenti (HR e manager possono accedervi), ma la read replica per l'elaborazione payroll è solo per accounting
- **Sicurezza interna del database** — solo chi deve modificare/processare dati può farlo

### User Data (File condivisi → S3)
- **Security policies sui bucket S3** — solo le persone del dipartimento per cui il bucket è destinato possono accedervi
- **Encryption at rest** nei bucket
- **SSL per i trasferimenti** — tutte le comunicazioni cifrate, così chiunque catturi i pacchetti dalla rete non potrà accedere ai dati

### Website (WordPress → EC2 + ELB)
- **Ruoli IAM minimi** per le istanze web server — *"Non vogliamo che i web server girino con un ruolo admin, perché se qualcuno riesce a violare il web server, magari attraverso una vulnerabilità WordPress, può attaccare il resto della nostra infrastruttura AWS"*
- **Security Groups corretti** sulle network interface — permettere HTTP e HTTPS, nient'altro
- **Security Groups corretti sul VPC** — permettere nel VPC solo ciò che deve entrarci

> **Insight da Kimiko**: *"Le nostre raccomandazioni sono piuttosto basilari per la sicurezza, e questa è la buona notizia. Una volta che capisci tutti i concetti e gli strumenti, è lì che sta la complessità. Ora dobbiamo solo implementare la soluzione giusta per le nostre esigenze."*

---

## Design Secure Architectures — Panoramica Esame (dal PACKT Cap.12)

Il PACKT Cap.12 struttura il dominio "Design Secure Architectures" in tre task statement:

### 1. Design Secure Access to AWS Resources

Conoscenze richieste (dal PACKT Cap.12):
- Controlli di accesso e gestione su più account AWS
- Servizi di federated access e identity (IAM, IAM Identity Center)
- Infrastruttura globale AWS
- Best practice di sicurezza (least privilege, shared responsibility)

Competenze richieste:
- Applicare best practice a utenti IAM e root users (incluso MFA)
- Progettare un modello di autorizzazione flessibile con utenti, gruppi, ruoli e policy
- Progettare una strategia RBAC con STS, role switching, cross-account access
- Progettare una strategia di sicurezza per più account con Control Tower e SCP
- Determinare l'uso appropriato di resource policies e quando federare un directory service con ruoli IAM

### 2. Design Secure Workloads and Applications

Il PACKT Cap.12 identifica i due attacchi comuni nell'esame:
- **DDoS** — protezione con architetture scalabili, Shield, WAF, Network Firewall
- **SQL Injection** — protezione con WAF (match conditions per codice SQL malevolo)

Inoltre: *"Assicurati di salvare qualsiasi application secret in AWS Secrets Manager."*

### 3. Determine Appropriate Data Security Controls

Il PACKT Cap.12 divide in due categorie:

**Controlling Data**:
- Controlla chi accede ai dati con IAM
- Per database self-hosted su EC2, configura l'autenticazione e salva le password in Secrets Manager
- *"Il problema più grande per i dati è l'errore umano. Un semplice errore può cancellare un intero database in secondi"*
- Conosci RPO e RTO e come influenzano la strategia di backup
- Familiarizzati con lifecycle policies S3 e Intelligent-Tiering
- Protezione da cancellazione accidentale: S3 Versioning, Object Lock, MFA delete, RDS delete protection

**Encrypting Data**:
- *"I dati dovrebbero essere cifrati durante tutto il loro ciclo di vita. At rest con KMS, in transit con TLS e certificati in ACM"*
- Quando gestisci le tue chiavi in KMS, blocca la chiave per limitare chi può usarla
- Rotazione delle chiavi automatizzabile in KMS
- Rinnovo certificati in ACM

---

## Scenari Tipici d'Esame

### Scenario 1: Web server con troppi permessi
**Domanda**: Un web server WordPress su EC2 ha un ruolo IAM con accesso admin. Qual è il rischio?

**Risposta**: Se qualcuno sfrutta una vulnerabilità WordPress, può attaccare l'intera infrastruttura AWS (Kimiko: *"Se qualcuno può violare il web server, può attaccare il resto della nostra infrastruttura AWS"*). Soluzione: ruolo IAM con solo i permessi necessari.

### Scenario 2: Protezione da errore umano
**Domanda**: Come proteggere un database RDS da cancellazione accidentale?

**Risposta**: Abilita **RDS delete protection** + backup regolari basati su RPO (PACKT Cap.12).

### Scenario 3: Dati sensibili in S3
**Domanda**: Come proteggere dati sensibili dei dipendenti salvati in S3?

**Risposta**: Bucket policy per dipartimento + encryption at rest + SSL per i trasferimenti (scenario Widget Makers di Kimiko).

### Scenario 4: Security policy aziendali
**Domanda**: L'azienda sta migrando al cloud ma le security policy esistenti coprono solo l'on-premises.

**Risposta**: Creare policy di sicurezza dedicate per il cloud (Kimiko: *"Servono nuove security policy per il mondo cloud. Le policy tradizionali on-premises spesso non coprono scenari cloud"*).

---

## Riepilogo Veloce per l'Esame

- **Shared Responsibility**: AWS = sicurezza DEL cloud (hardware, location fisiche), Tu = sicurezza NEL cloud (OS, dati, accessi) (Kimiko)
- **Defense in depth**: sicurezza a ogni livello — account → VPC → subnet → istanza → dentro l'istanza (Kimiko)
- **Least privilege**: dai solo i permessi necessari, niente di più (Kimiko, PACKT)
- **CloudTrail**: per traceability, ma attenzione ai costi se loggi tutto (Kimiko)
- **Keep people away from data**: accesso programmatico, non diretto — protegge da insider threat (Kimiko)
- **Errore umano > minacce malevole**: il problema più grande per i dati (PACKT Cap.12)
- **RPO/RTO**: leggi attentamente la domanda d'esame per capire se sono definiti (PACKT Cap.12)
- **Protezione da cancellazione**: S3 Versioning + Object Lock + MFA delete, RDS delete protection (PACKT Cap.12)
- **Encryption lifecycle**: at rest con KMS, in transit con TLS/ACM (PACKT Cap.12)
- **Web server con ruoli minimi**: mai admin access su istanze web (Kimiko scenario Widget Makers)
- **Security policy cloud-specific**: rivedi le policy aziendali per il cloud (Kimiko)
- **Widget Makers Security**: IAM groups/policies per ogni sistema, encryption at rest per S3, SSL per trasferimenti, SG corretti per web server (Kimiko)
