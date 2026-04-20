# Trasversali: Monitoring, IaC, Migration

> Fonti: PACKT Cap.11 (p.472-490), PACKT Cap.8 (p.386-410), KIMIKO (p.179-188, p.194-197, p.200-207, p.249-254), DOJO (p.217-227, p.261-263)

---

## Glossario: i servizi che incontrerai in questo documento

### Monitoring

- **CloudTrail** — registra TUTTE le chiamate API fatte nel tuo account AWS. Chi ha fatto cosa, quando, da dove. È il "registro delle attività" del tuo account. Fondamentale per audit, compliance e investigazione di incidenti di sicurezza. Come le telecamere di sorveglianza di un edificio: registrano chi entra, chi esce, e cosa fa.

- **CloudWatch** — il servizio di monitoraggio di AWS. Raccoglie metriche (CPU, memoria, disco, rete) da tutte le tue risorse, mostra grafici, e può triggerare allarmi. Esempio: se la CPU di un'istanza supera l'80% per 5 minuti, CloudWatch può mandare un'email o lanciare un'azione di Auto Scaling. Come il cruscotto della tua auto: ti mostra velocità, temperatura, livello carburante.

- **AWS Config** — monitora e registra le configurazioni delle risorse AWS nel tempo. Non impedisce le modifiche, le rileva e segnala. Può verificare se le risorse sono conformi a regole di compliance. Come un auditor che controlla periodicamente che tutto sia in regola.

### Infrastructure as Code

- **CloudFormation** — il servizio per definire la tua infrastruttura come codice (template JSON o YAML). Descrivi cosa vuoi (2 istanze EC2, 1 database RDS, 1 load balancer) in un file, e CloudFormation crea tutto automaticamente. Se devi ricreare l'ambiente, lanci lo stesso template e hai tutto identico in minuti. Come un progetto architettonico: lo dai al costruttore e lui costruisce la casa esattamente come nel progetto.

- **SSM (Systems Manager)** — una suite di strumenti per gestire l'infrastruttura. Include: Patch Manager (patching automatico), Run Command (esegui comandi senza SSH), Parameter Store (salva configurazioni), Session Manager (accesso sicuro senza porte SSH aperte).

### Migration

- **DataSync** — per trasferire grandi volumi di file tra on-premises e AWS (o tra servizi AWS). Come un servizio di trasloco professionale: impacchetta tutto, lo trasporta, e lo mette a posto nella nuova casa.

- **DMS (Database Migration Service)** — per migrare database da on-premises ad AWS, o tra servizi AWS. Supporta migrazione iniziale + replicazione continua. Funziona anche con lo Schema Conversion Tool per cambiare tipo di database durante la migrazione.

- **Snow Family** — dispositivi fisici per trasferire enormi quantità di dati quando internet non basta. Snowball (terabyte), Snowball Edge (terabyte + compute all'edge), Snowmobile (petabyte/exabyte — letteralmente un camion). Come spedire un container pieno di hard disk invece di provare a caricare tutto via internet.

- **Storage Gateway** — un ponte tra on-premises e cloud per accesso continuo ibrido. A differenza di DataSync (che trasferisce), Storage Gateway mantiene l'accesso ai dati sia da on-premises che dal cloud.

- **Transfer Family** — per trasferire file usando protocolli standard (SFTP, FTPS, FTP). Utile per condividere file con partner esterni che usano questi protocolli.

---

## PARTE 1: Logging e Monitoring

### AWS CloudTrail (dal PACKT)

Il PACKT descrive: *"CloudTrail abilita il monitoraggio e logging continuo della tua infrastruttura AWS. Registra tutte le azioni nel tuo account, incluse le chiamate API fatte da utenti, ruoli o servizi."*

Dettagli chiave dal PACKT:
- **Abilitato di default** — salva gli ultimi **90 giorni** di eventi gratuitamente nell'event history
- Per una vista custom, crei un **trail** specificando: quali eventi loggare, quale bucket S3, quali Region, se ricevere notifiche

**Due tipi di eventi** (dal PACKT):
| Tipo | Cosa logga | Costo |
|---|---|---|
| **Management events** | API calls che creano, modificano o cancellano risorse AWS, o cambiano configurazioni | **Gratuiti** |
| **Data events** | Attività sulle risorse stesse (accesso a S3 bucket, invocazione Lambda) | **A pagamento** |

> **Tip esame (PACKT)**: *"CloudTrail NON è un servizio real-time. Può richiedere circa 15 minuti perché un'attività appaia in CloudTrail. Questo è un punto chiave per l'esame."*

### Amazon CloudWatch (dal PACKT e Kimiko)

Il PACKT descrive CloudWatch come il servizio per *"raccogliere, analizzare e agire su varie metriche e log generati dalle tue risorse AWS."*

Kimiko mostra CloudWatch nella console: *"CloudWatch è dove monitoriamo le nostre risorse. Possiamo vedere metriche come CPU, memoria, disco, rete. Possiamo impostare allarmi che triggerano azioni."*

### CloudTrail vs CloudWatch (dal Dojo)

Il Dojo fornisce il confronto chiave:

| Caratteristica | CloudTrail | CloudWatch |
|---|---|---|
| **Focus** | **Chi ha fatto cosa** — audit trail delle API calls | **Come stanno le risorse** — metriche e performance |
| **Domanda** | "Chi ha modificato questa risorsa?" | "La CPU è al 90%?" |
| **Tipo** | Logging di attività | Monitoring di metriche |
| **Azione** | Audit, compliance, investigazione | Allarmi, auto scaling, notifiche |

> **Regola per l'esame**: CloudTrail = audit/compliance (chi ha fatto cosa). CloudWatch = monitoring/performance (come stanno le risorse).

---

## PARTE 2: Infrastructure as Code

### AWS CloudFormation (dal PACKT e Kimiko)

Il PACKT descrive CloudFormation come il servizio per *"definire e provisionare risorse AWS usando template. I template sono scritti in JSON o YAML e descrivono le risorse che vuoi creare."*

Kimiko mostra il processo nella console con un walkthrough dettagliato: *"CloudFormation è incredibilmente potente. Scrivi un template che descrive la tua infrastruttura, e CloudFormation crea tutto automaticamente. Se devi ricreare l'ambiente — disaster recovery, nuovo ambiente di test — lanci lo stesso template e hai tutto identico in minuti."*

Concetti chiave dal PACKT:
- **Stack**: un insieme di risorse AWS create da un template
- **Change Sets**: preview delle modifiche prima di applicarle
- **Drift Detection**: rileva se le risorse sono state modificate manualmente rispetto al template
- **Nested Stacks**: template che referenziano altri template per modularità
- **StackSets**: deploy di stack su più account e Region contemporaneamente

### AWS Service Catalog (dal PACKT)

Il PACKT descrive: *"Service Catalog permette alle organizzazioni di creare e gestire cataloghi di prodotti IT approvati. Gli utenti possono lanciare solo i prodotti approvati, garantendo compliance e governance."*

### AWS Systems Manager — SSM (dal PACKT)

Il PACKT descrive SSM come una suite di strumenti per gestire l'infrastruttura:
- **Patch Manager**: automatizza il patching di istanze EC2
- **Run Command**: esegui comandi su istanze EC2 senza SSH
- **Parameter Store**: salva parametri di configurazione e segreti
- **Session Manager**: accesso sicuro alle istanze senza aprire porte SSH
- **Automation**: automatizza task operativi comuni

---

## PARTE 3: Migration e Data Transfer

### AWS DataSync (dal PACKT e Kimiko)

Il PACKT descrive: *"DataSync supporta lo spostamento di grandi volumi di dati tra storage on-premises e AWS. Puoi anche usarlo per spostare dati tra soluzioni storage AWS."*

Kimiko spiega: *"Il Database Migration Service è fantastico, ma è appropriato se i tuoi dati sono in un database. E tutti quei dati che non sono in un database? Magari hai un network file server con migliaia di file di log. DataSync è la soluzione."*

> **Nota PACKT**: *"DataSync NON supporta migrazione a EBS. DataSync supporta lo spostamento di file, non blocchi. Se la domanda chiede come spostare storage da on-premises a EBS, DataSync non può essere la risposta corretta."*

### AWS Snow Family (da Kimiko)

Kimiko descrive l'evoluzione della Snow Family:

| Dispositivo | Cosa fa | Quando usarlo |
|---|---|---|
| **Import/Export** (classico) | Invii i tuoi media (thumb drive, hard drive, DVD) ad AWS | Piccole quantità, qualsiasi formato |
| **Snowball** | Dispositivo rugged spedito da AWS. Connetti al data center, trasferisci dati, rispedisci. GPS tracking, encryption di default | Grandi quantità di dati (terabyte) |
| **Snowball Edge** | Come Snowball ma con **servizi AWS integrati** (es. EC2). Resta al tuo data center come gateway | Quando serve compute all'edge + trasferimento dati |
| **Snowmobile** | Camion 18 ruote con guardie armate. Per **exabyte/petabyte** di dati | *"Per aziende con quantità massive di dati che richiederebbero decenni per trasferire con le tecnologie più veloci di oggi"* |

> **Tip da Kimiko**: *"Come solutions architect, assicurati di conoscere Snowball, Snowball Edge e Snowmobile e come ciascuno potrebbe trovare posto nella tua soluzione cloud."*

### AWS Database Migration Service — DMS (da Kimiko)

Kimiko descrive DMS: *"Le aziende arrivano ad AWS con database grandi, magari multipli tipi — SQL, NoSQL, data warehouse. DMS fa la migrazione iniziale di tutti i dati, ma puoi anche tenerlo in esecuzione per la replicazione continua."*

Caratteristiche chiave da Kimiko:
- **Migrazione iniziale** + **replicazione continua** opzionale
- Funziona con **AWS Schema Conversion Tool (SCT)** per cambiare schema durante la migrazione
- Funziona anche **cloud-to-cloud** (es. Azure → AWS)
- Crei una **replication instance** in un VPC, configuri endpoint e task di migrazione

### AWS Transfer Family (dal PACKT)

Il PACKT descrive Transfer Family per trasferimenti di file usando protocolli standard:
- Supporta **SFTP, FTPS, FTP, AS2**
- Integrazione con S3 e EFS
- Utile per condividere file con partner esterni

### AWS Application Migration Service — MGN (dal PACKT)

Il PACKT descrive MGN come il servizio per migrare applicazioni intere (lift-and-shift):
- Replica continuamente i server sorgente su AWS
- Permette test non-disruptivi prima del cutover
- Supporta migrazione da qualsiasi infrastruttura (on-premises, altri cloud)

### Storage Gateway (da Kimiko — già coperto nel topic 11)

Kimiko ricorda: *"Storage Gateway è tre prodotti: File Gateway (interfaccia S3 via NFS/SMB), Volume Gateway (block storage con backup AWS), Tape Gateway (emula librerie tape per backup cloud)."*

### DataSync vs Storage Gateway (dal Dojo)

Il Dojo fornisce la distinzione:
- **DataSync**: per **trasferimento/migrazione** di dati — one-time o scheduled
- **Storage Gateway**: per **accesso continuo** ibrido — i dati restano accessibili sia on-premises che in AWS

---

## Scenari Tipici d'Esame

### Scenario 1: Chi ha cancellato un bucket S3?
**Domanda**: Un bucket S3 è stato cancellato. Come scoprire chi l'ha fatto?

**Risposta**: **CloudTrail** — logga tutte le API calls, incluso chi ha fatto cosa e quando (PACKT).

### Scenario 2: Allarme quando CPU supera 80%
**Domanda**: Vuoi essere avvisato quando la CPU di un'istanza supera l'80%.

**Risposta**: **CloudWatch** alarm con soglia CPU > 80% + notifica SNS (Kimiko).

### Scenario 3: Migrare terabyte di file a S3
**Domanda**: Devi spostare 50 TB di file da un NFS server on-premises a S3.

**Risposta**: **DataSync** — per grandi volumi di file da on-premises a S3/EFS/FSx (PACKT, Kimiko).

### Scenario 4: Migrare petabyte di dati
**Domanda**: L'azienda ha 100 PB di dati da migrare. Il trasferimento via internet richiederebbe anni.

**Risposta**: **Snowmobile** (Kimiko: *"Per quantità massive che richiederebbero decenni via internet"*).

### Scenario 5: Migrare database Oracle a Aurora
**Domanda**: Devi migrare un database Oracle on-premises a Aurora PostgreSQL.

**Risposta**: **DMS + Schema Conversion Tool** — DMS migra i dati, SCT converte lo schema (Kimiko).

### Scenario 6: Infrastruttura riproducibile
**Domanda**: Devi poter ricreare l'intero ambiente in minuti per DR.

**Risposta**: **CloudFormation** — template che descrive tutta l'infrastruttura, lanci e ricrei tutto (PACKT, Kimiko).

### Scenario 7: Accesso ibrido continuo a file
**Domanda**: Gli utenti on-premises devono continuare ad accedere a file che sono anche in S3.

**Risposta**: **Storage Gateway (File Gateway)** — non DataSync (Dojo: DataSync è per trasferimento, Storage Gateway per accesso continuo).

---

## Riepilogo Veloce per l'Esame

**Monitoring:**
- **CloudTrail**: audit trail, chi ha fatto cosa, 90 giorni gratis, NON real-time (15 min delay), management events gratuiti, data events a pagamento (PACKT)
- **CloudWatch**: metriche, allarmi, auto scaling trigger, monitoring performance (PACKT, Kimiko)
- **CloudTrail = audit, CloudWatch = monitoring** (Dojo)

**IaC:**
- **CloudFormation**: template JSON/YAML, stack, change sets, drift detection, StackSets per multi-account (PACKT)
- **Service Catalog**: catalogo prodotti IT approvati per governance (PACKT)
- **SSM**: Patch Manager, Run Command, Parameter Store, Session Manager (PACKT)

**Migration:**
- **DataSync**: file transfer on-premises ↔ AWS (S3/EFS/FSx), NON supporta EBS (PACKT)
- **Snow Family**: Snowball (TB), Snowball Edge (compute + storage), Snowmobile (PB/EB) (Kimiko)
- **DMS**: database migration + replicazione continua + SCT per conversione schema (Kimiko)
- **Transfer Family**: SFTP/FTPS/FTP per condivisione file con partner (PACKT)
- **MGN**: lift-and-shift di applicazioni intere (PACKT)
- **DataSync = trasferimento, Storage Gateway = accesso continuo ibrido** (Dojo)
