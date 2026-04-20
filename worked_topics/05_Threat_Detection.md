# Threat Detection - GuardDuty, Inspector, Macie, Security Hub

> Fonti: PACKT Cap.10 (p.450-455), KIMIKO (p.18-24, p.262-263), DOJO (p.221-223)

---

## Panoramica

Il PACKT introduce la sezione con una nota importante per l'esame: *"Non devi conoscere questi servizi in dettaglio per l'esame SAA-C03, ma dovresti capire cosa sono ad alto livello e capire come ogni servizio differisce dagli altri. Questo ti aiuterà a determinare la risposta corretta."*

I quattro servizi principali di threat detection sono: **AWS Security Hub, Amazon Inspector, Amazon GuardDuty e Amazon Macie**.

---

## Amazon Inspector (dal PACKT e Dojo)

Il PACKT descrive Inspector come *"un servizio automatizzato di security assessment. Aiuta a identificare vulnerabilità e deviazioni dalle best practice di sicurezza nelle istanze Amazon EC2 e nelle immagini container."*

Il Dojo aggiunge: *"Dopo aver eseguito un assessment, Amazon Inspector produce una lista dettagliata di security findings prioritizzati per livello di severità. Fornisce un report automatizzato che identifica accesso di rete non intenzionale alle tue istanze EC2 e vulnerabilità in quelle istanze."*

Caratteristiche chiave (dal PACKT):
- Usa **rules packages predefiniti** regolarmente aggiornati per controllare CVE (Common Vulnerabilities and Exposures), accessibilità di rete non intenzionale, e non-compliance con best practice
- Permette di creare **template e rules packages custom** per requisiti specifici
- Si integra con **Security Hub e GuardDuty** per centralizzare i findings

---

## Amazon GuardDuty (dal PACKT)

Il PACKT descrive GuardDuty come *"un servizio di threat detection che monitora e analizza continuamente specifiche data sources e log AWS nel tuo ambiente. Sfruttando feed di threat intelligence e modelli di machine learning, GuardDuty identifica e ti avvisa di attività inaspettate e potenzialmente non autorizzate."*

### Cosa Rileva (dal PACKT)

- **Escalation di privilegi** e uso di credenziali esposte
- **Comunicazione con IP e domini malevoli**
- **Malware** su istanze EC2 e container workloads
- **File appena caricati** in bucket S3
- **Pattern di login anomali** sui database
- **Istanze EC2 compromesse** che eseguono software malevolo o attività non autorizzate come **mining di criptovalute**
- **Accesso sospetto all'account** — deploy insoliti in regioni non familiari o chiamate API atipiche che suggeriscono modifiche alle security policy

### Come Funziona (dal PACKT)

- Ogni finding è categorizzato come **high, medium, o low** con raccomandazioni per la remediation
- Le funzionalità base monitorano: **CloudTrail event logs e management events, VPC flow logs, e DNS logs**
- Insight aggiuntivi disponibili per: **EKS, Lambda, RDS, S3**, più malware detection per EC2 e runtime monitoring
- Ogni pacchetto aggiuntivo è disponibile a un **costo extra**
- Si integra con **Security Hub** per una visione unificata

---

## Amazon Macie (dal PACKT e Kimiko)

Il PACKT descrive Macie come *"un servizio fully managed di data security e data privacy. È progettato per aiutarti a scoprire, monitorare e proteggere i tuoi dati sensibili salvati in bucket Amazon S3."*

### Caratteristiche Chiave (dal PACKT)

- **Sensitive data discovery**: usa ML e pattern matching per scoprire e classificare automaticamente dati sensibili — PII, dati finanziari, proprietà intellettuale
- **Continuous monitoring**: monitora continuamente l'attività di accesso e uso dei dati in S3
- **Anomaly detection**: usa ML per stabilire una baseline di pattern normali e avvisa su attività anomale
- **Compliance reporting**: report personalizzabili per GDPR, HIPAA, PCI-DSS

### Contesto da Kimiko

Kimiko spiega perché Macie è nato: *"Questo prodotto è nato perché c'erano così tante istanze di imbarazzo per le aziende che avevano informazioni sensibili nei bucket S3 senza le appropriate security policy in atto. Le persone potevano leggere informazioni dai bucket S3 che l'azienda non avrebbe mai voluto esporre."*

Kimiko mostra nella console: *"La prima volta che visiti Macie, c'è un grande pulsante 'Get Started' e hai un trial gratuito di 30 giorni. Anche se sei ben oltre il tuo anno di free tier, la prima volta che lanci Macie, andrà a categorizzare i tuoi S3: public, unencrypted, shared."*

> **Nota da Kimiko**: *"Macie non sarà un focus enorme nell'esame, ma devi conoscerlo. Pensa ai molti ruoli che Macie potrebbe avere per te: sicurezza, categorizzazione, pianificazione e redesign dell'approccio S3, compliance."*

> **Tip esame (PACKT)**: *"Se hai una domanda d'esame con Macie come risposta, prima stabilisci se i dati sono salvati in S3. Se no, puoi escludere Macie. Inoltre, Macie cerca specificamente PII. Se la domanda è su PII, cerca una risposta contenente Macie."*

---

## AWS Security Hub (dal PACKT e Dojo)

Il PACKT descrive Security Hub come *"uno strumento completo di sicurezza e compliance che fornisce una visione unificata della tua postura di sicurezza nel tuo ambiente AWS."*

Il Dojo aggiunge: *"Funziona come un hub che raccoglie alert e findings di sicurezza da più servizi AWS, come Amazon GuardDuty, Amazon Inspector, Amazon Macie, AWS IAM Access Analyzer, AWS Firewall Manager e altre fonti."*

### Caratteristiche Chiave

- **Aggrega findings** da vari servizi AWS e strumenti di sicurezza di terze parti (PACKT)
- **Analizza findings**, identifica trend di sicurezza, fornisce raccomandazioni prioritizzate (PACKT)
- **Compliance monitoring**: puoi usare Security Hub per compliance con **PCI DSS, CIS Benchmarks** e molti altri standard (Dojo)
- **Automazione delle risposte**: puoi creare workflow di sicurezza custom per triggerare automaticamente investigazioni, notificare team, o rimediare problemi identificati (PACKT)

---

## Amazon Detective (dal Dojo)

Il Dojo descrive Detective: *"Amazon Detective rende facile analizzare, investigare e identificare rapidamente la root cause di potenziali problemi di sicurezza o attività sospette. Detective raccoglie automaticamente log data dalle tue risorse AWS — da CloudTrail, VPC Flow Logs, GuardDuty findings e altri servizi AWS — poi usa machine learning per analizzare e condurre investigazioni di sicurezza."*

---

## AWS Network Firewall (dal Dojo)

Il Dojo fornisce la descrizione più dettagliata: *"AWS Network Firewall è un servizio di firewall di rete gestito per i tuoi Amazon VPC. Viene con capacità di intrusion prevention e detection."*

### Casi d'Uso (dal Dojo)
- Ispezione traffico VPC-to-VPC
- Filtraggio traffico outbound
- Protezione connessioni Direct Connect e VPN
- Filtraggio traffico Internet
- Controlli di sicurezza fine-grained per VPC interconnessi via Transit Gateway

### Componenti (dal Dojo)
1. **Firewall**: la risorsa connessa al VPC, deploy in più AZ (una subnet per zona)
2. **Firewall Policy**: definisce il comportamento con regole stateless e stateful. Un firewall può avere solo una policy
3. **Rule Group**: collezione di regole stateless o stateful. Include 5-tuple (source IP, source port, dest IP, dest port, protocol) e domain name filtering

### Stateless vs Stateful (dal Dojo)
- **Stateless**: non ha contesto del flusso di traffico, controlla solo il pacchetto stesso
- **Stateful**: conosce il contesto/stato del pacchetto, inclusa la direzione del flusso

> **Nota Dojo**: *"Questo concetto è simile a NACLs e Security Groups. Una NACL è stateless, mentre un Security Group è stateful."*

---

## Lab Security Services di Kimiko

Kimiko dedica un intero lab ai servizi di sicurezza, mostrando nella console:

### KMS (Key Management Service)
- Mostra le chiavi esistenti (AWS RDS key, AWS Lightsail key, chiavi custom)
- Crea una nuova chiave: scelta tra KMS o materiale esterno, tag, permessi admin, permessi d'uso
- Azioni sulle chiavi: enable/disable, add/edit tags, **schedule key deletion**
- *"Per la rotazione delle chiavi, scheduli la cancellazione della vecchia e crei una nuova, poi configuri le applicazioni per usare la nuova chiave."*

### CloudHSM
- *"Un hardware security module che non è realmente hardware, è nel cloud. È un HSM virtuale."*
- Funzionamento: crei un **cluster**, poi crei HSM nel cluster. Le applicazioni li chiamano programmaticamente per **offloadare il processing di encryption**
- Puoi anche chiamare un HSM nel cloud AWS da un server on-premises

### Directory Services
- **AWS Managed AD**: *"È vero Microsoft Active Directory. Lancia istanze di Windows Server con Active Directory."*
- **Simple AD**: *"Non è vero Active Directory. È una versione ridotta che gira su Linux Samba."*
- **AD Connector**: per connettersi a un'infrastruttura Active Directory esistente
- **Cognito**: può essere usato come directory service

### Security AMIs nel Marketplace
Kimiko mostra che ci sono **428+ prodotti di sicurezza** nel Marketplace AWS, inclusi Cisco Cloud Services Router, Trend Micro, firewall next-gen, e persino **Kali Linux** per penetration testing nel cloud.

---

## Scenari Tipici d'Esame

### Scenario 1: Dati PII in S3
**Domanda**: Devi verificare che nessun bucket S3 contenga dati PII non protetti.

**Risposta**: **Amazon Macie** (PACKT: *"Macie specifically looks for PII. If the exam question is about PII, look for an answer containing Macie"*).

### Scenario 2: Vulnerabilità nelle istanze EC2
**Domanda**: Vuoi scansionare automaticamente le istanze EC2 per vulnerabilità software.

**Risposta**: **Amazon Inspector** (PACKT: *"Helps identify vulnerabilities and deviations from security best practices in EC2 instances and container images"*).

### Scenario 3: Attività malevola nell'account
**Domanda**: Sospetti che un'istanza EC2 stia facendo mining di criptovalute.

**Risposta**: **Amazon GuardDuty** (PACKT: *"GuardDuty can uncover compromised EC2 instances running malicious software or engaging in unauthorized activities such as cryptocurrency mining"*).

### Scenario 4: Dashboard di sicurezza centralizzata
**Domanda**: Il CISO vuole una visione unificata della sicurezza su tutti gli account.

**Risposta**: **AWS Security Hub** (Dojo: *"Provides a centralized and comprehensive view of the security posture across multiple AWS accounts"*).

### Scenario 5: Investigare un incidente
**Domanda**: GuardDuty ha rilevato un accesso anomalo. Devi capire la root cause.

**Risposta**: **Amazon Detective** (Dojo: *"Makes it easy to analyze, investigate, and quickly identify the root cause of potential security issues"*).

---

## Riepilogo Veloce per l'Esame

- **GuardDuty**: threat detection continua, analizza CloudTrail/VPC Flow/DNS logs, ML-based, rileva crypto mining (PACKT)
- **Inspector**: vulnerability assessment (CVE), scansiona EC2 e container, report prioritizzati (PACKT, Dojo)
- **Macie**: trova PII in S3, ML + pattern matching, compliance GDPR/HIPAA/PCI-DSS (PACKT, Kimiko)
- **Security Hub**: aggrega findings da tutti i servizi, compliance PCI DSS/CIS, automazione risposte (PACKT, Dojo)
- **Detective**: investigazione post-incidente, root cause analysis, raccoglie log automaticamente (Dojo)
- **Network Firewall**: firewall VPC gestito, IPS/IDS, stateless + stateful rules, 5-tuple filtering (Dojo)
- **Macie → solo S3 e PII** (PACKT tip esame)
- **Non servono dettagli profondi** per l'esame, ma devi sapere cosa fa ciascun servizio e come differiscono (PACKT)
- **CloudHSM**: per offload encryption processing, cluster-based, chiamabile anche da on-premises (Kimiko)
- **Directory Services**: AWS Managed AD (vero AD), Simple AD (Linux Samba), AD Connector (bridge) (Kimiko)
