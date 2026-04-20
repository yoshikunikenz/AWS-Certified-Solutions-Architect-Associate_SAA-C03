# Data Ingestion & Analytics - Redshift, Kinesis, Glue, Athena

> Fonti: PACKT Cap.7 (p.354-377), PACKT Cap.14 (p.578-583), KIMIKO (p.25-33, p.255-266), DOJO (p.238-243, p.264-265, p.274)

---

## Glossario: i servizi che incontrerai in questo documento

- **Kinesis** — il servizio per processare dati in streaming in tempo reale. Pensalo come un fiume di dati che scorre continuamente (click degli utenti, log dei server, dati IoT) e tu puoi "pescare" da questo fiume per analizzare i dati mentre arrivano. Ha 4 varianti: Data Streams (streaming raw), Firehose (caricamento automatico), Analytics (SQL su streaming), Video Streams.

- **Athena** — un servizio per fare query SQL direttamente sui file salvati in S3, senza dover caricare i dati in un database. Serverless — non c'è nulla da configurare. Paghi solo per i dati scansionati. Come poter fare ricerche in un archivio di documenti senza doverli prima catalogare in un database.

- **Glue** — il servizio ETL (Extract, Transform, Load) di AWS. Estrae dati da varie fonti, li trasforma nel formato che ti serve, e li carica nella destinazione. Ha anche un **Data Catalog** che è come un indice di tutti i tuoi dati — sa dove sono, che formato hanno, e come accedervi.

- **Redshift** — il data warehouse di AWS per analytics su petabyte di dati. Usa SQL. Non è per operazioni quotidiane (quello è RDS/Aurora), ma per analisi complesse su grandi volumi di dati storici. Come la differenza tra il registro di cassa giornaliero e il report annuale delle vendite.

- **EMR (Elastic MapReduce)** — una piattaforma per eseguire framework di big data come Apache Spark, Hive e Presto su cluster gestiti da AWS. Per chi ha bisogno di processare enormi quantità di dati con strumenti open source.

- **QuickSight** — il servizio di Business Intelligence (BI) di AWS. Crea dashboard interattive e visualizzazioni dai tuoi dati. Come Tableau o Power BI, ma serverless e integrato con tutti i servizi AWS.

- **Lake Formation** — semplifica la creazione di un data lake (un repository centralizzato dove salvi tutti i dati, strutturati e non, a qualsiasi scala). Gestisce sicurezza, accesso e governance dei dati.

- **MSK (Managed Streaming for Apache Kafka)** — Apache Kafka gestito da AWS. Per chi già usa Kafka per processare dati in streaming e vuole portarlo nel cloud senza gestire l'infrastruttura.

---

## Panoramica

Il PACKT introduce: *"Analytics su AWS è una gamma estremamente ampia di strumenti e servizi per aiutare le organizzazioni a raccogliere, salvare, processare e analizzare dati. AWS offre soluzioni per data lake, data warehousing, analytics real-time e machine learning."*

Kimiko aggiunge: *"Ci sono diversi servizi in AWS davvero focalizzati sull'analytics. È importante capire cosa possono fare per te. Come architetto AWS, vogliamo capire cosa possono fare e quando potremmo usarli."*

---

## Amazon Redshift (dal PACKT)

Il PACKT descrive Redshift come *"un servizio di data warehouse fully managed, a scala petabyte, progettato per analisi ad alte performance di dati strutturati e semi-strutturati. Permette di eseguire query analitiche complesse su dataset massivi, usando strumenti SQL e applicazioni BI."*

### Capacity Management (dal PACKT)

- **Provisioned clusters**: selezioni node type e numero basato sui requisiti
- **Elastic resize**: aggiustamento rapido della capacità compute
- **Classic resize**: per cambiamenti più significativi
- **Concurrency scaling**: aggiunge capacità transitoria automaticamente per spike di query
- **Redshift Serverless**: gestione automatica della capacità

### Redshift Spectrum (dal PACKT)

Il PACKT descrive Redshift Spectrum come una feature che *"permette di eseguire query direttamente su dati salvati in S3 senza doverli caricare in Redshift. Questo è particolarmente utile per analizzare grandi volumi di dati che non devono essere permanentemente salvati nel data warehouse."*

---

## Amazon Kinesis (dal PACKT e Dojo)

### I 4 Tipi di Kinesis (dal Dojo)

| Servizio | Cosa fa |
|---|---|
| **Kinesis Data Streams** | Streaming real-time di big data. I dati sono mantenuti nello stream per il periodo di retention. I consumer possono scegliere quali chunk consumare e **riprodurre messaggi** nello stesso ordine |
| **Kinesis Video Streams** | Streaming di video in tempo reale |
| **Kinesis Data Firehose** | Cattura, trasforma e carica immediatamente dati streaming nei target consumer (S3, Redshift, Elasticsearch) |
| **Kinesis Data Analytics** | Esegui query SQL immediatamente sui dati in streaming |

### Kinesis vs SQS (dal Dojo)

Il Dojo fornisce il confronto chiave:

| Caratteristica | Kinesis | SQS |
|---|---|---|
| **Velocità** | Real-time, latenza molto bassa | Alto throughput ma non veloce come Kinesis |
| **Consumer** | **Multipli consumer** possono processare lo stesso stream contemporaneamente | **Un solo consumer** processa un singolo messaggio |
| **Ordine** | Dati salvati nell'ordine di arrivo | Standard: best-effort ordering. FIFO: ordine garantito |
| **Replay** | I consumer possono **riprodurre messaggi** nello stesso ordine | No replay — dopo il polling il messaggio diventa invisibile, poi va cancellato manualmente |
| **Scaling** | Devi avere abbastanza **shard** nello stream | Non superare il limite di throughput API |
| **Features** | Built-in big data, analytics, ETL | At-least-once (Standard) o exactly-once (FIFO) |
| **Librerie** | Servono Kinesis libraries | Basta AWS API o SDK |

> **Regola per l'esame**: Kinesis per streaming real-time con multipli consumer e replay. SQS per decoupling di applicazioni con singolo consumer.

---

## Amazon Athena (dal PACKT e Kimiko)

### Panoramica (dal PACKT)

Il PACKT descrive Athena come *"un servizio di query interattivo che permette di analizzare dati direttamente in Amazon S3 usando SQL standard. Athena è serverless, quindi non c'è infrastruttura da gestire, e paghi solo per le query che esegui."*

### Walkthrough di Kimiko

Kimiko mostra Athena nella console: *"Athena è un servizio di query interattivo che rende facile analizzare dati in Amazon S3 usando SQL standard. Athena è serverless — non c'è infrastruttura da configurare o gestire. Puoi iniziare a fare query immediatamente."*

Kimiko spiega il processo:
1. Definisci una tabella che punta ai dati in S3
2. Scrivi query SQL standard
3. I risultati vengono restituiti in secondi
4. Paghi solo per i dati scansionati dalle query

> **Tip da Kimiko**: *"Athena è perfetto quando hai dati in S3 e vuoi analizzarli senza dover caricare nulla in un database."*

---

## AWS Glue (dal PACKT e Kimiko)

### Panoramica (dal PACKT)

Il PACKT descrive Glue come *"un servizio ETL (Extract, Transform, Load) fully managed che semplifica la preparazione e il caricamento dei dati per l'analytics. Glue scopre e cataloga automaticamente i dati da varie fonti, li trasforma, e li carica in data store target."*

### Glue Data Catalog (dal PACKT)

Il PACKT spiega: *"Il Glue Data Catalog è un repository centralizzato di metadati che salva informazioni sulle fonti dati, le trasformazioni e i target. Funziona come un indice per i tuoi dati, rendendo facile scoprire e gestire i dataset."*

### Kimiko su Glue

Kimiko commenta: *"AWS Glue è uno dei miei strumenti preferiti in AWS. È un servizio ETL fully managed. Puoi usarlo per preparare e trasformare i dati per l'analytics."*

---

## Amazon EMR — Elastic MapReduce (dal PACKT)

Il PACKT descrive EMR come *"una piattaforma di big data cloud che permette di processare grandi quantità di dati usando framework open source come Apache Spark, Apache Hive e Presto. EMR semplifica l'esecuzione di framework di big data su AWS, gestendo il provisioning, la configurazione e il tuning dei cluster."*

---

## Amazon QuickSight (dal PACKT)

Il PACKT descrive QuickSight come *"un servizio di business intelligence (BI) serverless che permette di creare e pubblicare dashboard interattive. QuickSight si integra con varie fonti dati AWS, inclusi S3, RDS, Redshift e Athena."*

---

## AWS Lake Formation (dal PACKT)

Il PACKT descrive Lake Formation come *"un servizio che semplifica la configurazione di un data lake sicuro. Un data lake è un repository centralizzato che permette di salvare tutti i dati strutturati e non strutturati a qualsiasi scala."*

---

## Amazon MSK — Managed Streaming for Apache Kafka (dal PACKT)

Il PACKT descrive MSK come *"un servizio fully managed per Apache Kafka che semplifica la costruzione e l'esecuzione di applicazioni che usano Apache Kafka per processare dati in streaming."*

---

## Servizi di Ricerca (da Kimiko)

Kimiko esplora i servizi di ricerca nella console:

### CloudSearch
*"Utile quando hai molti dati offline che vuoi portare in un repository centrale e renderli ricercabili. Puoi cercarli usando API."*

### Elasticsearch Service (ora OpenSearch)
*"La differenza tra CloudSearch e Elasticsearch è che CloudSearch non si espande tanto quanto Elasticsearch. 'Elastic' nel nome ti dice che può crescere e ridursi come ne hai bisogno — come un elastico."*

### Data Pipeline (da Kimiko)
*"Orchestrazione per workflow guidati dai dati. Definiamo data node (S3, DynamoDB, Redshift, database relazionali), scheduliamo attività di compute, attiviamo la pipeline e la monitoriamo."*

---

## Data Ingestion ad Alte Performance (dal PACKT Cap.14)

Il PACKT Cap.14 riassume le strategie per l'esame:

### Streaming Data
- **Kinesis Data Streams**: per ingestione real-time di grandi volumi di dati
- **Kinesis Data Firehose**: per caricamento automatico in S3, Redshift, o OpenSearch
- **Amazon MSK**: per applicazioni Apache Kafka

### Batch Data
- **AWS Glue**: ETL per preparare e caricare dati
- **AWS Batch**: per job di elaborazione batch su larga scala

### Query e Analytics
- **Athena**: query SQL su dati in S3, serverless, pay-per-query
- **Redshift**: data warehouse per query complesse su dataset massivi
- **Redshift Spectrum**: query su dati in S3 senza caricarli in Redshift
- **QuickSight**: dashboard BI interattive

---

## Scenari Tipici d'Esame

### Scenario 1: Analizzare log in S3 senza database
**Domanda**: Hai terabyte di log in S3 e vuoi analizzarli con SQL senza caricarli in un database.

**Risposta**: **Amazon Athena** — query SQL serverless direttamente su S3 (PACKT, Kimiko).

### Scenario 2: Streaming real-time con multipli consumer
**Domanda**: Dati IoT in streaming devono essere processati da più applicazioni contemporaneamente in real-time.

**Risposta**: **Kinesis Data Streams** — multipli consumer, replay, real-time (Dojo).

### Scenario 3: Caricare streaming data in S3 automaticamente
**Domanda**: Dati in streaming devono essere automaticamente trasformati e caricati in S3.

**Risposta**: **Kinesis Data Firehose** — cattura, trasforma e carica automaticamente (Dojo).

### Scenario 4: Data warehouse per analytics complesse
**Domanda**: L'azienda ha petabyte di dati strutturati da analizzare con query SQL complesse.

**Risposta**: **Amazon Redshift** (PACKT).

### Scenario 5: ETL per preparare dati
**Domanda**: Dati da diverse fonti devono essere estratti, trasformati e caricati in un data lake.

**Risposta**: **AWS Glue** — ETL fully managed con Data Catalog (PACKT, Kimiko).

### Scenario 6: Query su dati in S3 da Redshift
**Domanda**: Vuoi eseguire query su dati in S3 dal tuo cluster Redshift senza caricarli.

**Risposta**: **Redshift Spectrum** (PACKT).

---

## Riepilogo Veloce per l'Esame

- **Redshift**: data warehouse petabyte-scale, SQL, BI. Serverless o provisioned. Spectrum per query su S3 (PACKT)
- **Kinesis Data Streams**: streaming real-time, multipli consumer, replay, shard-based (Dojo)
- **Kinesis Firehose**: caricamento automatico streaming → S3/Redshift/OpenSearch (Dojo)
- **Kinesis Analytics**: SQL su dati in streaming (Dojo)
- **Kinesis vs SQS**: Kinesis = real-time, multipli consumer, replay. SQS = decoupling, singolo consumer (Dojo)
- **Athena**: query SQL serverless su S3, pay-per-query (PACKT, Kimiko)
- **Glue**: ETL fully managed + Data Catalog per metadati (PACKT, Kimiko)
- **EMR**: big data con Spark/Hive/Presto su cluster gestiti (PACKT)
- **QuickSight**: dashboard BI serverless (PACKT)
- **Lake Formation**: setup semplificato di data lake sicuro (PACKT)
- **MSK**: Apache Kafka gestito per streaming (PACKT)
- **CloudSearch**: ricerca su dati offline. **OpenSearch**: ricerca elastica su larga scala (Kimiko)
