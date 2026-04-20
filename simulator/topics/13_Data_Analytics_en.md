# Data Ingestion & Analytics - Redshift, Kinesis, Glue, Athena

> Sources: PACKT Ch.7 (p.354-377), PACKT Ch.14 (p.578-583), KIMIKO (p.25-33, p.255-266), DOJO (p.238-243, p.264-265, p.274)

---

## Glossary: the services you will encounter in this document

- **Kinesis** — the service for processing streaming data in real time. Think of it as a river of data flowing continuously (user clicks, server logs, IoT data) and you can "fish" from this river to analyze data as it arrives. It has 4 variants: Data Streams (raw streaming), Firehose (automatic loading), Analytics (SQL on streaming), Video Streams.

- **Athena** — a service for running SQL queries directly on files stored in S3, without having to load the data into a database. Serverless — there's nothing to configure. You only pay for the data scanned. Like being able to search through a document archive without first cataloging them in a database.

- **Glue** — AWS's ETL (Extract, Transform, Load) service. Extracts data from various sources, transforms it into the format you need, and loads it into the destination. It also has a **Data Catalog** which is like an index of all your data — it knows where they are, what format they have, and how to access them.

- **Redshift** — AWS's data warehouse for analytics on petabytes of data. Uses SQL. It's not for daily operations (that's RDS/Aurora), but for complex analysis on large volumes of historical data. Like the difference between the daily cash register and the annual sales report.

- **EMR (Elastic MapReduce)** — a platform for running big data frameworks like Apache Spark, Hive, and Presto on AWS-managed clusters. For those who need to process huge amounts of data with open source tools.

- **QuickSight** — AWS's Business Intelligence (BI) service. Creates interactive dashboards and visualizations from your data. Like Tableau or Power BI, but serverless and integrated with all AWS services.

- **Lake Formation** — simplifies the creation of a data lake (a centralized repository where you store all data, structured and unstructured, at any scale). Manages data security, access, and governance.

- **MSK (Managed Streaming for Apache Kafka)** — Apache Kafka managed by AWS. For those who already use Kafka for streaming data processing and want to bring it to the cloud without managing the infrastructure.

---

## Overview

PACKT introduces: *"Analytics su AWS è una gamma estremamente ampia di strumenti e servizi per aiutare le organizzazioni a raccogliere, salvare, processare e analizzare dati. AWS offre soluzioni per data lake, data warehousing, analytics real-time e machine learning."*

Kimiko adds: *"Ci sono diversi servizi in AWS davvero focalizzati sull'analytics. È importante capire cosa possono fare per te. Come architetto AWS, vogliamo capire cosa possono fare e quando potremmo usarli."*

---

## Amazon Redshift (from PACKT)

PACKT describes Redshift as *"un servizio di data warehouse fully managed, a scala petabyte, progettato per analisi ad alte performance di dati strutturati e semi-strutturati. Permette di eseguire query analitiche complesse su dataset massivi, usando strumenti SQL e applicazioni BI."*

### Capacity Management (from PACKT)

- **Provisioned clusters**: select node type and number based on requirements
- **Elastic resize**: rapid compute capacity adjustment
- **Classic resize**: for more significant changes
- **Concurrency scaling**: automatically adds transient capacity for query spikes
- **Redshift Serverless**: automatic capacity management

### Redshift Spectrum (from PACKT)

PACKT describes Redshift Spectrum as a feature that *"permette di eseguire query direttamente su dati salvati in S3 senza doverli caricare in Redshift. Questo è particolarmente utile per analizzare grandi volumi di dati che non devono essere permanentemente salvati nel data warehouse."*

---

## Amazon Kinesis (from PACKT and Dojo)

### The 4 Types of Kinesis (from Dojo)

| Service | What it does |
|---|---|
| **Kinesis Data Streams** | Real-time big data streaming. Data is kept in the stream for the retention period. Consumers can choose which chunks to consume and **replay messages** in the same order |
| **Kinesis Video Streams** | Real-time video streaming |
| **Kinesis Data Firehose** | Captures, transforms, and immediately loads streaming data into target consumers (S3, Redshift, Elasticsearch) |
| **Kinesis Data Analytics** | Run SQL queries immediately on streaming data |

### Kinesis vs SQS (from Dojo)

The Dojo provides the key comparison:

| Feature | Kinesis | SQS |
|---|---|---|
| **Speed** | Real-time, very low latency | High throughput but not as fast as Kinesis |
| **Consumer** | **Multiple consumers** can process the same stream simultaneously | **A single consumer** processes a single message |
| **Order** | Data saved in arrival order | Standard: best-effort ordering. FIFO: guaranteed order |
| **Replay** | Consumers can **replay messages** in the same order | No replay — after polling the message becomes invisible, then must be manually deleted |
| **Scaling** | You need enough **shards** in the stream | Don't exceed the API throughput limit |
| **Features** | Built-in big data, analytics, ETL | At-least-once (Standard) or exactly-once (FIFO) |
| **Libraries** | Kinesis libraries required | AWS API or SDK is enough |

> **Exam rule**: Kinesis for real-time streaming with multiple consumers and replay. SQS for application decoupling with a single consumer.

---

## Amazon Athena (from PACKT and Kimiko)

### Overview (from PACKT)

PACKT describes Athena as *"un servizio di query interattivo che permette di analizzare dati direttamente in Amazon S3 usando SQL standard. Athena è serverless, quindi non c'è infrastruttura da gestire, e paghi solo per le query che esegui."*

### Kimiko's Walkthrough

Kimiko shows Athena in the console: *"Athena è un servizio di query interattivo che rende facile analizzare dati in Amazon S3 usando SQL standard. Athena è serverless — non c'è infrastruttura da configurare o gestire. Puoi iniziare a fare query immediatamente."*

Kimiko explains the process:
1. Define a table that points to data in S3
2. Write standard SQL queries
3. Results are returned in seconds
4. You only pay for the data scanned by queries

> **Tip from Kimiko**: *"Athena è perfetto quando hai dati in S3 e vuoi analizzarli senza dover caricare nulla in un database."*

---

## AWS Glue (from PACKT and Kimiko)

### Overview (from PACKT)

PACKT describes Glue as *"un servizio ETL (Extract, Transform, Load) fully managed che semplifica la preparazione e il caricamento dei dati per l'analytics. Glue scopre e cataloga automaticamente i dati da varie fonti, li trasforma, e li carica in data store target."*

### Glue Data Catalog (from PACKT)

PACKT explains: *"Il Glue Data Catalog è un repository centralizzato di metadati che salva informazioni sulle fonti dati, le trasformazioni e i target. Funziona come un indice per i tuoi dati, rendendo facile scoprire e gestire i dataset."*

### Kimiko on Glue

Kimiko comments: *"AWS Glue è uno dei miei strumenti preferiti in AWS. È un servizio ETL fully managed. Puoi usarlo per preparare e trasformare i dati per l'analytics."*

---

## Amazon EMR — Elastic MapReduce (from PACKT)

PACKT describes EMR as *"una piattaforma di big data cloud che permette di processare grandi quantità di dati usando framework open source come Apache Spark, Apache Hive e Presto. EMR semplifica l'esecuzione di framework di big data su AWS, gestendo il provisioning, la configurazione e il tuning dei cluster."*

---

## Amazon QuickSight (from PACKT)

PACKT describes QuickSight as *"un servizio di business intelligence (BI) serverless che permette di creare e pubblicare dashboard interattive. QuickSight si integra con varie fonti dati AWS, inclusi S3, RDS, Redshift e Athena."*

---

## AWS Lake Formation (from PACKT)

PACKT describes Lake Formation as *"un servizio che semplifica la configurazione di un data lake sicuro. Un data lake è un repository centralizzato che permette di salvare tutti i dati strutturati e non strutturati a qualsiasi scala."*

---

## Amazon MSK — Managed Streaming for Apache Kafka (from PACKT)

PACKT describes MSK as *"un servizio fully managed per Apache Kafka che semplifica la costruzione e l'esecuzione di applicazioni che usano Apache Kafka per processare dati in streaming."*

---

## Search Services (from Kimiko)

Kimiko explores search services in the console:

### CloudSearch
*"Utile quando hai molti dati offline che vuoi portare in un repository centrale e renderli ricercabili. Puoi cercarli usando API."*

### Elasticsearch Service (now OpenSearch)
*"La differenza tra CloudSearch e Elasticsearch è che CloudSearch non si espande tanto quanto Elasticsearch. 'Elastic' nel nome ti dice che può crescere e ridursi come ne hai bisogno — come un elastico."*

### Data Pipeline (from Kimiko)
*"Orchestrazione per workflow guidati dai dati. Definiamo data node (S3, DynamoDB, Redshift, database relazionali), scheduliamo attività di compute, attiviamo la pipeline e la monitoriamo."*

---

## High-Performance Data Ingestion (from PACKT Ch.14)

PACKT Ch.14 summarizes the strategies for the exam:

### Streaming Data
- **Kinesis Data Streams**: for real-time ingestion of large data volumes
- **Kinesis Data Firehose**: for automatic loading into S3, Redshift, or OpenSearch
- **Amazon MSK**: for Apache Kafka applications

### Batch Data
- **AWS Glue**: ETL to prepare and load data
- **AWS Batch**: for large-scale batch processing jobs

### Query and Analytics
- **Athena**: SQL queries on S3 data, serverless, pay-per-query
- **Redshift**: data warehouse for complex queries on massive datasets
- **Redshift Spectrum**: queries on S3 data without loading them into Redshift
- **QuickSight**: interactive BI dashboards

---

## Typical Exam Scenarios

### Scenario 1: Analyze logs in S3 without a database
**Question**: You have terabytes of logs in S3 and want to analyze them with SQL without loading them into a database.

**Answer**: **Amazon Athena** — serverless SQL queries directly on S3 (PACKT, Kimiko).

### Scenario 2: Real-time streaming with multiple consumers
**Question**: IoT streaming data must be processed by multiple applications simultaneously in real-time.

**Answer**: **Kinesis Data Streams** — multiple consumers, replay, real-time (Dojo).

### Scenario 3: Load streaming data into S3 automatically
**Question**: Streaming data must be automatically transformed and loaded into S3.

**Answer**: **Kinesis Data Firehose** — captures, transforms, and loads automatically (Dojo).

### Scenario 4: Data warehouse for complex analytics
**Question**: The company has petabytes of structured data to analyze with complex SQL queries.

**Answer**: **Amazon Redshift** (PACKT).

### Scenario 5: ETL to prepare data
**Question**: Data from various sources must be extracted, transformed, and loaded into a data lake.

**Answer**: **AWS Glue** — fully managed ETL with Data Catalog (PACKT, Kimiko).

### Scenario 6: Query S3 data from Redshift
**Question**: You want to run queries on S3 data from your Redshift cluster without loading them.

**Answer**: **Redshift Spectrum** (PACKT).

---

## Quick Recap for the Exam

- **Redshift**: petabyte-scale data warehouse, SQL, BI. Serverless or provisioned. Spectrum for S3 queries (PACKT)
- **Kinesis Data Streams**: real-time streaming, multiple consumers, replay, shard-based (Dojo)
- **Kinesis Firehose**: automatic streaming loading → S3/Redshift/OpenSearch (Dojo)
- **Kinesis Analytics**: SQL on streaming data (Dojo)
- **Kinesis vs SQS**: Kinesis = real-time, multiple consumers, replay. SQS = decoupling, single consumer (Dojo)
- **Athena**: serverless SQL queries on S3, pay-per-query (PACKT, Kimiko)
- **Glue**: fully managed ETL + Data Catalog for metadata (PACKT, Kimiko)
- **EMR**: big data with Spark/Hive/Presto on managed clusters (PACKT)
- **QuickSight**: serverless BI dashboards (PACKT)
- **Lake Formation**: simplified secure data lake setup (PACKT)
- **MSK**: managed Apache Kafka for streaming (PACKT)
- **CloudSearch**: search on offline data. **OpenSearch**: elastic search at large scale (Kimiko)
