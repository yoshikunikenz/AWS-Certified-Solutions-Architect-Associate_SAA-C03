# AWS Well-Architected Framework (WAF)

> Fonti: PACKT Cap.1 (p.78-98), KIMIKO (p.71-120), DOJO (p.38-45)

---

## Glossario: i servizi AWS che incontrerai in questo documento

Prima di tutto, chiariamo cosa sono i servizi che verranno nominati. Così quando leggi "usa RDS con Multi-AZ" sai esattamente di cosa si parla.

### Compute (potenza di calcolo)

- **EC2 (Elastic Compute Cloud)** — è una macchina virtuale nel cloud. Come avere un computer (Linux o Windows) che gira nei data center di AWS invece che nel tuo ufficio. Ci puoi installare quello che vuoi: un web server, un database, un'applicazione. Paghi per il tempo in cui è accesa e per la potenza che scegli (CPU, RAM, disco). Esistono diverse "classi" di istanze EC2: alcune ottimizzate per calcolo pesante, altre per memoria, altre per storage.

- **Lambda** — è il servizio serverless di AWS. Scrivi il tuo codice, lo carichi, e AWS lo esegue quando succede qualcosa (un evento). Non devi gestire nessun server: niente OS da aggiornare, niente istanze da dimensionare. Paghi solo per il tempo effettivo di esecuzione del codice (millisecondi). Scala automaticamente: se arrivano 1000 richieste contemporanee, Lambda esegue 1000 copie del tuo codice in parallelo.

- **Auto Scaling** — è il meccanismo che aggiunge o rimuove automaticamente istanze EC2 in base al carico. Se il traffico aumenta, lancia nuove istanze. Se diminuisce, le spegne. Così non paghi per server inutilizzati e non rimani senza risorse nei momenti di picco.

### Storage (archiviazione)

- **S3 (Simple Storage Service)** — è lo storage di oggetti/file di AWS. Pensalo come un hard disk infinito nel cloud dove puoi mettere qualsiasi file: immagini, video, documenti, backup. I file sono organizzati in "bucket" (contenitori). S3 è estremamente durevole (AWS garantisce 99.999999999% di durabilità, cioè praticamente non perdi mai un file) e ridondante di default (i dati sono replicati automaticamente su più strutture). Puoi anche ospitare un sito web statico direttamente da S3.

- **S3 Glacier** — è la versione "archivio" di S3. Costa molto meno, ma i dati non sono immediatamente disponibili: quando li richiedi, possono volerci da minuti a ore per recuperarli. Perfetto per dati che devi conservare per legge o compliance ma che accedi raramente (es. log vecchi, backup storici).

- **EBS (Elastic Block Store)** — è il disco rigido virtuale che attacchi a un'istanza EC2. Come l'SSD o l'HDD del tuo computer, ma nel cloud. I dati persistono anche se spegni l'istanza (a differenza dell'Instance Store che è temporaneo). Puoi scegliere tra SSD (veloce, per database e applicazioni) e HDD magnetico (più lento, più economico, per dati sequenziali).

- **EFS (Elastic File System)** — è un file system condiviso nel cloud. A differenza di EBS (che si attacca a UNA sola istanza), EFS può essere montato da MOLTE istanze EC2 contemporaneamente. Come una cartella di rete condivisa in ufficio, ma nel cloud. Scala automaticamente.

### Database

- **RDS (Relational Database Service)** — è il servizio di database relazionali gestito da AWS. "Gestito" significa che AWS si occupa di: installazione, patching del sistema operativo, backup automatici, aggiornamenti del software del database. Tu ti occupi solo dei tuoi dati e delle tue query. Supporta diversi motori: MySQL, PostgreSQL, SQL Server, Oracle, MariaDB. È come avere un DBA (database administrator) che lavora 24/7 gratis per te sulla parte infrastrutturale.

- **Aurora** — è il database relazionale proprietario di AWS. Compatibile con MySQL e PostgreSQL, ma progettato da zero per il cloud. È fino a 5x più veloce di MySQL e 3x più veloce di PostgreSQL. Replica automaticamente i dati su 3 Availability Zone. Costa un po' di più di RDS standard ma offre performance e resilienza superiori.

- **DynamoDB** — è il database NoSQL (non relazionale) di AWS. Invece di tabelle con righe e colonne collegate tra loro (come SQL), usa coppie chiave-valore e documenti JSON. È velocissimo (millisecondi di latenza) e scala automaticamente. Perfetto per applicazioni che hanno bisogno di risposte rapidissime con pattern di accesso semplici (es. carrello e-commerce, sessioni utente, gaming).

- **ElastiCache** — è un servizio di cache in-memory. Mette i dati più richiesti in RAM per accesso ultra-rapido (microsecondi). Supporta Redis e Memcached. Esempio: invece di interrogare il database ogni volta che un utente carica la homepage, metti il risultato in cache. Le richieste successive leggono dalla cache (velocissimo) invece che dal database (più lento).

- **Read Replica** — è una copia di sola lettura del tuo database. Il database principale gestisce letture E scritture. La read replica gestisce SOLO le letture. Serve a due scopi: 1) alleggerire il carico sul database principale, 2) migliorare le performance di lettura. I dati vengono replicati automaticamente dal principale alla replica. Esempio: il payroll legge migliaia di record → lo fa dalla read replica, così il database principale continua a funzionare normalmente per tutti gli altri.

### Networking (rete)

- **VPC (Virtual Private Cloud)** — è la tua rete privata virtuale dentro AWS. Come la rete LAN del tuo ufficio, ma nel cloud. Dentro il VPC definisci le tue subnet (sotto-reti), le regole di accesso, chi può parlare con chi. Ogni risorsa AWS (EC2, RDS, ecc.) vive dentro un VPC.

- **Availability Zone (AZ)** — è un data center fisico (o un gruppo di data center) all'interno di una Region AWS. Ogni Region ha almeno 2-3 AZ, fisicamente separate tra loro (diversi edifici, diverse alimentazioni elettriche). Se un data center va giù (incendio, alluvione, blackout), gli altri AZ nella stessa Region continuano a funzionare.

- **Multi-AZ** — significa distribuire le tue risorse su più Availability Zone. Per RDS, Multi-AZ crea automaticamente una copia del database in un'altra AZ. Se l'AZ principale ha un problema, AWS fa failover automatico sulla copia nell'altra AZ. Il tuo database torna online in pochi minuti senza intervento manuale.

- **Region** — è un'area geografica dove AWS ha i suoi data center (es. eu-south-1 = Milano, us-east-1 = Virginia). Ogni Region è completamente indipendente dalle altre. Scegli la Region più vicina ai tuoi utenti per ridurre la latenza.

- **Edge Location** — sono mini data center sparsi in tutto il mondo (ce ne sono centinaia). Servono per CloudFront e altri servizi "edge" per portare i contenuti il più vicino possibile agli utenti finali.

- **ELB (Elastic Load Balancer)** — è il bilanciatore di carico di AWS. Distribuisce il traffico in arrivo su più istanze EC2. Se hai 2 web server, l'ELB manda il 50% delle richieste a uno e il 50% all'altro. Se un server cade, l'ELB smette di mandargli traffico e dirige tutto sull'altro. Serve sia per performance (distribuire il carico) che per resilienza (se uno cade, l'altro continua).

- **CloudFront** — è la CDN (Content Delivery Network) di AWS. Prende i tuoi contenuti (immagini, video, pagine web) e li copia nelle Edge Location in tutto il mondo. Quando un utente in Italia richiede un'immagine, la prende dall'Edge Location più vicina invece che dal server in Virginia. Risultato: caricamento molto più veloce.

- **Route 53** — è il servizio DNS di AWS. Traduce i nomi di dominio (es. www.miosito.com) in indirizzi IP. Offre anche routing intelligente: può mandare gli utenti al server più vicino, fare health check e redirigere il traffico se un server è giù.

- **Security Group** — è un firewall virtuale per le tue istanze EC2. Definisce quali porte e protocolli sono permessi in entrata e in uscita. Esempio: per un web server permetti HTTP (porta 80) e HTTPS (porta 443) in entrata, blocchi tutto il resto. È "stateful": se permetti il traffico in entrata, la risposta in uscita è automaticamente permessa.

### Sicurezza

- **IAM (Identity and Access Management)** — è il sistema di gestione degli accessi di AWS. Controlla CHI può fare COSA su quali risorse. Crei utenti, gruppi, ruoli e policy (regole). Esempio: l'utente "mario" appartiene al gruppo "developers" che ha una policy che permette di leggere S3 ma non di cancellare istanze EC2. Il principio fondamentale è "least privilege": dai a ognuno SOLO i permessi che gli servono, niente di più.

- **KMS (Key Management Service)** — è il servizio per gestire le chiavi di crittografia. Crea e gestisce le chiavi che usi per cifrare i tuoi dati (in S3, EBS, RDS, ecc.). Non devi preoccuparti di dove conservare le chiavi in modo sicuro: lo fa AWS per te.

- **CloudTrail** — registra TUTTE le chiamate API fatte nel tuo account AWS. Chi ha fatto cosa, quando, da dove. È il "registro delle attività" del tuo account. Fondamentale per audit, compliance e investigazione di incidenti di sicurezza.

### Messaging e Integrazione

- **SQS (Simple Queue Service)** — è una coda di messaggi. L'applicazione A mette un messaggio nella coda, l'applicazione B lo legge e lo processa quando è pronta. Serve per disaccoppiare i componenti: se B è giù o lento, i messaggi aspettano in coda senza perdere nulla. Esempio: un e-commerce mette gli ordini in coda, il sistema di elaborazione li processa uno alla volta.

- **SNS (Simple Notification Service)** — è un servizio di notifiche pub/sub (publish/subscribe). Un publisher manda un messaggio a un "topic", e tutti i subscriber di quel topic lo ricevono. Può mandare email, SMS, notifiche push, o triggerare Lambda. Esempio: quando l'inventario scende sotto una soglia, SNS manda un'email al responsabile magazzino.

### Infrastructure as Code

- **CloudFormation** — è il servizio per definire la tua infrastruttura come codice (template JSON o YAML). Descrivi cosa vuoi (2 istanze EC2, 1 database RDS, 1 load balancer) in un file, e CloudFormation crea tutto automaticamente. Se devi ricreare l'ambiente (disaster recovery, nuovo ambiente di test), lanci lo stesso template e hai tutto identico in minuti.

### Monitoring

- **CloudWatch** — è il servizio di monitoraggio di AWS. Raccoglie metriche (CPU, memoria, disco, rete) da tutte le tue risorse, mostra grafici, e può triggerare allarmi. Esempio: se la CPU di un'istanza supera l'80% per 5 minuti, CloudWatch può mandare un'email o lanciare un'azione di Auto Scaling.

---

## Cos'è il Well-Architected Framework

Il WAF è l'insieme di principi e best practice che AWS ha definito per progettare architetture cloud affidabili, sicure, efficienti e convenienti. È la bussola dell'esame SAA-C03: i 4 domini dell'esame corrispondono direttamente a 4 dei 6 pilastri del framework.

Il framework ti aiuta a valutare le tue architetture rispetto alle best practice e a identificare aree di miglioramento. Non è una checklist rigida, ma un modo di pensare critico alle decisioni architetturali.

---

## I 6 Pilastri

### 1. Operational Excellence

La capacità di supportare lo sviluppo, eseguire workload in modo efficace e migliorare continuamente i processi.

Design Principles:
- **Perform operations as code** — tratta l'infrastruttura come codice (CloudFormation, IaC)
- **Make frequent, small, reversible changes** — cambiamenti piccoli riducono il rischio
- **Refine operations procedures frequently** — rivedi e migliora i processi regolarmente
- **Anticipate failure** — progetta pensando a cosa può andare storto
- **Learn from all operational failures** — ogni incidente è un'opportunità di apprendimento

> Nell'esame SAA-C03 questo pilastro non ha un dominio dedicato, ma è trasversale a tutte le domande.

---

### 2. Security (→ Dominio 1 dell'esame, 30%)

La capacità di proteggere dati, sistemi e asset sfruttando le tecnologie cloud.

Design Principles:
- **Implement a strong identity foundation** — IAM con least privilege. Crea utenti, gruppi e ruoli appropriati. Usa MFA per il root account
- **Enable traceability** — monitora e audita tutto con CloudTrail. Attenzione: loggare tutto può aumentare i costi significativamente, logga ciò che serve
- **Apply security at all layers** — defense in depth: sicurezza a livello di account AWS, VPC, subnet, istanza e dentro l'istanza stessa
- **Automate security best practices** — codice sicuro, OS hardened, configurazioni automatizzate
- **Protect data in transit and at rest** — SSL/SSH per il transito, encryption AWS per i dati a riposo
- **Keep people away from data** — l'accesso ai dati deve essere programmatico (tramite app, API), non diretto. Protegge da danni accidentali e intenzionali (insider threat)
- **Prepare for security events** — notifiche rapide (CloudTrail + alarms) e un response plan pronto

Linee guida generali:
- Implementa IAM correttamente (MFA, least privilege, gruppi con policy)
- Detective controls (CloudTrail per monitorare le attività)
- Infrastructure protection (ogni account/ruolo accede solo a ciò che serve)
- Data protection (backup, recovery, encryption)
- Incident response plan (team pronto, procedure definite)

#### Shared Responsibility Model

Concetto fondamentale che esce spesso all'esame:

| AWS è responsabile di... | Tu sei responsabile di... |
|---|---|
| Sicurezza **del** cloud | Sicurezza **nel** cloud |
| Hardware fisico | Sistema operativo guest |
| Data center e strutture | Patch e aggiornamenti OS |
| Infrastruttura di rete | Configurazione firewall/security groups |
| Virtualizzazione | IAM (utenti, ruoli, policy) |
| | Encryption dei tuoi dati |
| | Sicurezza delle applicazioni |
| | Configurazione S3 bucket, database, ecc. |

> **Tip pratico da Kimiko**: Servono nuove security policy specifiche per il cloud. Le policy di sicurezza tradizionali on-premises spesso non coprono scenari cloud. Rivedi le policy aziendali e crea policy dedicate per cloud computing e cloud storage.

---

### 3. Reliability (→ Dominio 2 dell'esame, 26%)

La capacità di un workload di funzionare correttamente e consistentemente nel tempo.

Design Principles:
- **Test recovery procedures** — se non testi il recovery, non sai se funziona. Prova sempre a ripristinare da backup, lancia i template CloudFormation per verificare che funzionino
- **Automatically recover from failure** — usa CloudWatch per monitorare e triggerare azioni automatiche (es. lanciare nuove istanze quando quelle esistenti sono sovraccariche)
- **Scale horizontally** — decoupla l'applicazione in componenti separati invece di scalare verticalmente (più CPU/RAM). Scaling orizzontale = più istanze. Scaling verticale = istanza più potente
- **Stop guessing capacity** — non tirare a indovinare. Analizza l'utilizzo reale (performance monitor, log) e dimensiona di conseguenza
- **Manage change in automation** — scaling out/in, scaling up/down dei database RDS, tutto deve essere automatizzato. Se richiede intervento manuale, non è veramente resiliente

Concetti chiave:
- **Five nines (99.999%)** e **Four nines (99.99%)** — livelli di disponibilità target
- La resilienza DEVE essere automatica: recovery automatico, scaling automatico, backup automatici
- Resilienza ≠ Performance. Resilienza = il sistema è disponibile. Performance = il sistema risponde velocemente

---

### 4. Performance Efficiency (→ Dominio 3 dell'esame, 24%)

La capacità di usare le risorse computing in modo efficiente e mantenere quell'efficienza nel tempo.

Design Principles:
- **Democratize advanced technologies** — non reinventare la ruota. Usa i managed services (RDS invece di installare un DB su EC2, DynamoDB invece di scrivere file su S3). AWS ha già ottimizzato questi servizi per te
- **Go global in minutes** — deploy multi-region per avvicinare i server agli utenti. Riduce latenza, aumenta throughput
- **Use serverless architectures** — Lambda e API Gateway scalano meglio delle architetture server-based. Serverless scala automaticamente al livello necessario
- **Experiment more often** — il cloud rende economico testare. Puoi creare account, provare configurazioni diverse, senza comprare hardware. Sperimenta perché ora te lo puoi permettere
- **Mechanical sympathy** — usa la tecnologia giusta per il task giusto. Pensa al processo, ai task coinvolti, e scegli la soluzione AWS migliore per quel processo specifico (es. considera i data access patterns quando scegli database o storage)

#### Tipi di Storage e Performance

| Tipo | Servizio | Latenza | Throughput | Condivisione |
|---|---|---|---|---|
| Block Storage | EBS | Più bassa, consistente | Singolo (1 istanza) | Solo tramite l'istanza |
| File System | EFS | Bassa, consistente | Multiplo (N istanze) | Sì, multi-client |
| Object Storage | S3 | Bassa | Web-scale | Sì, molti client |
| Archival | Glacier | Minuti → ore | Alto (una volta rilasciato) | No, solo tu |

> **Regola d'oro**: la scelta dell'instance type giusto è il fattore più importante per la performance. Questo concetto si ripete per ogni sistema: database, web server, applicazioni. Classe giusta = performance giusta.

---

### 5. Cost Optimization (→ Dominio 4 dell'esame, 20%)

La capacità di eseguire sistemi che forniscono valore di business al costo più basso possibile.

Design Principles:
- **Adopt a consumption model** — paga solo per ciò che consumi. Se sei un ufficio con un turno solo, spegni i server la sera e riaccendili la mattina. Distingui tra servizi 24/7 (per i clienti) e servizi business-hours (per i dipendenti)
- **Measure overall efficiency** — monitora il valore di business che ogni sistema produce rispetto al suo costo. Se un dipartimento consuma il 30% dei costi AWS ma produce il 5% del valore, rivaluta
- **Stop spending money on data center operations** — AWS fa rack & stack per te. Non spendere per costruire data center per testare nuove soluzioni
- **Analyze and attribute expenditure** — traccia da dove vengono i costi, per dipartimento, per progetto. Usa i billing management tools di AWS
- **Use managed services to reduce cost of ownership** — RDS costa meno in ore-uomo rispetto a gestire un DB su EC2 (non devi gestire OS, patching, ecc.)

I 4 sotto-pilastri del cost optimization:
1. **Use cost-effective resources** — a volte un'istanza più potente (e costosa all'ora) è più economica perché finisce il lavoro prima
2. **Match supply with demand** — Auto Scaling per avere il numero giusto di server in ogni momento
3. **Expenditure awareness** — usa billing alerts per sapere quando superi una soglia
4. **Optimize over time** — l'ottimizzazione dei costi è un processo continuo. Più esperienza hai, meglio ottimizzi

---

### 6. Sustainability

La capacità di massimizzare l'efficienza e ridurre l'impatto ambientale.

Design Principles:
- Understand your impact
- Establish sustainability goals
- Maximize utilization
- Anticipate and adopt new, more efficient hardware and software offerings
- Use managed services
- Reduce the downstream impact of your cloud workloads

> Nell'esame SAA-C03 questo pilastro, come Operational Excellence, è trasversale.

---

## Mappatura Pilastri → Dominio Esame

| Pilastro WAF | Dominio SAA-C03 | Peso Esame |
|---|---|---|
| Security | Domain 1: Design Secure Architectures | **30%** |
| Reliability | Domain 2: Design Resilient Architectures | **26%** |
| Performance Efficiency | Domain 3: Design High-Performing Architectures | **24%** |
| Cost Optimization | Domain 4: Design Cost-Optimized Architectures | **20%** |
| Operational Excellence | Trasversale | — |
| Sustainability | Trasversale | — |

---

## Concetti Fondamentali Trasversali

### Cloud Economics: CapEx vs OpEx

| | CapEx (On-Premises) | OpEx (Cloud) |
|---|---|---|
| Modello | Acquisto anticipato hardware/software | Pay-as-you-go |
| Investimento iniziale | Alto | Minimo |
| Scalabilità | Costosa e complessa, rischio di over-provisioning | Facile e cost-effective, allineata alla domanda |
| Flessibilità | Limitata, lenta ad adattarsi | Ampia gamma di servizi, adattamento rapido |
| Gestione infrastruttura | Diretta (hardware, staff, elettricità, sicurezza fisica) | Delegata al provider |

### TCO (Total Cost of Ownership)

Il TCO è il costo totale di possesso su tutto il ciclo di vita. Include costi nascosti che spesso si dimenticano nel confronto cloud vs on-premises.

Esempio pratico dal PACKT (5 anni):

**On-premises:**
- Costo iniziale (hardware + licenze): $10,000
- Costi ricorrenti annui (manutenzione $2,000 + energia $500 + staff IT $3,000) × 5 = $27,500
- **TCO 5 anni = $37,500**

**Cloud:**
- Abbonamento mensile: $500 × 12 × 5 = $30,000
- **TCO 5 anni = $30,000**

> Il cloud vince di $7,500 in questo scenario, e non include i costi nascosti dell'on-premises (spazio fisico, raffreddamento, sicurezza fisica, formazione, downtime).

### ROI (Return on Investment)

ROI misura la redditività di un investimento: (profitto netto / costo totale).
- **TCO** = quanto spenderai (costo)
- **ROI** = quanto guadagnerai (beneficio)
- Usali insieme per un'analisi finanziaria completa

### Elasticity vs Scalability

- **Scalability** = posso crescere (aggiungere risorse)
- **Elasticity** = posso crescere E ridurmi (aggiungere E rimuovere risorse)
- Auto Scaling è elastico: scala out (aggiunge istanze) e scala in (rimuove istanze)
- Elastic Load Balancing è elastico: aggiungi e rimuovi nodi dal set

### High Availability vs Fault Tolerance

- **High Availability** = copie ridondanti pronte a subentrare. Se un componente cade, un altro prende il suo posto. Può esserci un breve downtime durante il failover
- **Fault Tolerance** = il sistema continua a funzionare anche durante il degrado di un componente. Rileva il problema e rerouta automaticamente. Zero downtime percepito

### Disaster Recovery — Le 4 Strategie

Dal più economico al più costoso:

| Strategia | Come funziona | RTO | RPO | Costo |
|---|---|---|---|---|
| **Backup & Restore** | Backup frequenti in location sicura, ripristino al bisogno | Più alto (ore) | Dipende dalla frequenza backup | Più basso |
| **Pilot Light** | Componenti core sempre attivi (es. DB con replica), il resto si avvia al bisogno | Medio | Minimo per i componenti core | Basso-Medio |
| **Warm Standby** | Ambiente ridotto ma funzionante, sempre in sync, da scalare in caso di disastro | Basso (minuti) | Minimo | Medio-Alto |
| **Multi-Site (Active-Active)** | Replica completa in configurazione active-active, basta redirigere il traffico | Più basso (secondi) | Quasi zero | Più alto |

> **RTO** (Recovery Time Objective) = quanto tempo puoi stare giù
> **RPO** (Recovery Point Objective) = quanti dati puoi permetterti di perdere

---

## Best Practice Architetturali (dal Dojo)

Queste best practice sono un riassunto potente di come pensare "cloud-native":

### Design for Failure
- Clustering: istanze extra pronte a subentrare
- Multi-AZ: istanze in data center diversi
- Backup: per gli scenari peggiori
- Account AWS alternativo come cold/warm site

### Disposable Resources
- Tratta i server come usa-e-getta, non come animali domestici
- Bootstrapping, Docker images, golden AMI per ricreare risorse velocemente
- Infrastructure as Code (CloudFormation) per rendere tutto riproducibile

### Loose Coupling
- **Well-Defined Interfaces** — componenti interagiscono solo tramite API (es. RESTful)
- **Service Discovery** — i microservizi devono essere trovabili senza conoscere la topologia di rete
- **Asynchronous Integration** — se non serve risposta immediata, usa uno storage intermedio durevole (SQS)
- **Distributed Systems Best Practices** — gestisci il fallimento dei componenti in modo graceful

### Services, Not Servers
- Preferisci managed services (RDS, DynamoDB, SQS) a soluzioni self-managed su EC2
- Serverless (Lambda) per event-driven e synchronous services senza gestire infrastruttura

### Removing Single Points of Failure
- **Standby redundancy** — failover su risorsa secondaria (usato per componenti stateful come DB relazionali)
- **Active redundancy** — richieste distribuite su più risorse, se una cade le altre assorbono il carico
- **Synchronous replication** — conferma la transazione solo dopo che è stata scritta su primario E replica (integrità massima)
- **Asynchronous replication** — disaccoppia primario e replica, introduce replication lag ma migliore performance
- **Quorum-based replication** — mix dei due, definisce un numero minimo di nodi per una write di successo

### Optimize for Cost
- **Right Sizing** — scegli il tipo e la dimensione giusta per il workload
- **Elasticity** — usa e rilascia risorse, non tenerle idle
- **Purchasing Options** — Reserved Instances, Spot Instances, Savings Plans

### Caching
- **Application Data Caching** — cache in-memory (ElastiCache) per dati frequentemente acceduti
- **Edge Caching** — CloudFront per servire contenuti da infrastruttura vicina agli utenti

---

## Scenario Pratico: Widget Makers (da Kimiko)

Kimiko presenta uno scenario reale di un'azienda ("Widget Makers") che deve migrare 5 sistemi al cloud. Per ogni pilastro, mostra le raccomandazioni concrete. Questo è oro per capire come applicare la teoria.

### L'azienda
Widget Makers ha 5 sistemi da migrare:
1. **Order Processing** — database SQL Server per gli ordini
2. **Inventory Management** — database MySQL per l'inventario
3. **Payroll** — database SQL Server per le buste paga
4. **User Data** — file condivisi sui server locali (~700MB per utente)
5. **Website** — WordPress su server interni

### Pilastro Reliability — Cosa fare

| Sistema | Raccomandazione |
|---|---|
| Order Processing | SQL Server → RDS managed instance + **Multi-AZ** |
| Inventory Management | MySQL → RDS managed instance + **Multi-AZ** (no clustering necessario) |
| Payroll | SQL Server → RDS + Multi-AZ + **Read Replica** (il payroll è intensivo in lettura durante l'elaborazione) |
| User Data | File condivisi → **S3 buckets** (resilienza intrinseca). Serve un tool di terze parti per mappare drive letter a S3 |
| Website | WordPress → **2 istanze dietro Elastic Load Balancer** (se una cade, l'altra continua) |

> **Insight chiave**: la read replica per il payroll è geniale. Il payroll gira ogni 1-2 settimane, fa molte letture intensive. La read replica evita di impattare il database principale durante l'elaborazione.

### Pilastro Performance — Cosa fare

| Sistema | Raccomandazione |
|---|---|
| Order Processing | Scegliere la **classe di istanza giusta** per memoria e CPU sufficienti |
| Inventory Management | Stessa cosa + automatizzare notifiche inventario con **SNS** + considerare CloudWatch per ordini automatici sotto soglia |
| Payroll | Classe giusta + processare payroll **solo dalla read replica** per performance migliori |
| User Data | **S3 bucket per dipartimento** per distribuire il carico + allarmi per utenti che superano 700MB |
| Website | Classe giusta + **EBS su SSD** (non magnetico) + ELB per load balancing tra i web server |

> **Tip ripetuto**: "Ensure instances are in a class providing sufficient memory and processing capabilities" — questo è IL pattern più importante per la performance. Classe giusta = performance giusta.

> **Tip spesso dimenticato**: quando migri al cloud, verifica che la **connessione internet** dell'azienda sia sufficiente. Puoi avere l'architettura AWS più performante del mondo, ma se hai 50 Mbps per 200 utenti, le performance saranno scarse.

### Pilastro Security — Cosa fare

| Sistema | Raccomandazione |
|---|---|
| Order Processing | IAM groups + policies per gestione DB + sicurezza interna del DB (permessi SQL) + sicurezza dell'app client |
| Inventory Management | IAM groups + policies + sicurezza interna DB (nessuno modifica inventario senza permessi) |
| Payroll | IAM groups + policies + **solo accounting accede alla read replica** + sicurezza interna DB |
| User Data | **S3 bucket policies** per dipartimento + **encryption at rest** + **SSL per i trasferimenti** |
| Website | Istanze con **ruoli IAM minimi** (no admin access, altrimenti una breach WordPress compromette tutto AWS) + **Security Groups** corretti (solo HTTP/HTTPS) + SG corretti sul VPC |

> **Insight critico**: se il web server gira con un ruolo admin e qualcuno sfrutta una vulnerabilità WordPress, può attaccare tutta l'infrastruttura AWS. Dai al web server SOLO i permessi che gli servono.

### Pilastro Cost Optimization — Cosa fare

| Sistema | Raccomandazione |
|---|---|
| Order Processing | Usa **managed database** (RDS) → meno ore-uomo di gestione |
| Inventory Management | Stessa cosa, managed database |
| Payroll | Managed database + **read replica attiva solo quando serve** (non tenerla accesa 24/7 se il payroll gira ogni 2 settimane) |
| User Data | **Monitorare** cosa gli utenti mettono nei bucket. Se caricano foto/video personali, i costi salgono e la performance cala |
| Website | **Classe giusta, non di più** (puoi sempre upgradare dopo) + monitorare accessi anomali (es. qualcuno sfrutta una vulnerabilità per hostare file pirata → costi di bandwidth alle stelle) |

> **Insight geniale**: la read replica del payroll si accende la sera prima dell'elaborazione, replica i dati durante la notte, il payroll gira la mattina, poi si spegne. Paghi poche ore ogni 2 settimane invece di 24/7.

---

## Riepilogo Veloce per l'Esame

- Il WAF ha **6 pilastri**, l'esame ne testa direttamente **4**
- **Security è il dominio più pesante** (30%) — IAM, encryption, defense in depth
- **Shared Responsibility**: AWS = sicurezza DEL cloud, Tu = sicurezza NEL cloud
- **Elasticity > Scalability**: elasticity = cresci E riduci
- **DR strategies**: Backup&Restore → Pilot Light → Warm Standby → Multi-Site (costo crescente, RTO/RPO decrescente)
- **Loose coupling** (SQS, SNS) previene cascading failures
- **Managed services** > self-managed (meno costi operativi, migliore performance)
- **Right-sizing** è fondamentale: classe giusta = performance giusta = costo giusto
- **Infrastructure as Code** (CloudFormation) per riproducibilità e disaster recovery
- **Consumption model**: paga solo quello che usi, spegni quello che non serve
