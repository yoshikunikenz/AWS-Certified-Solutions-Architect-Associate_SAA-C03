# Decoupling (SQS, SNS, EventBridge) e Serverless (Lambda, Step Functions)

> Fonti: PACKT Cap.9 (p.413-436), PACKT Cap.13 (p.534-543), KIMIKO (p.140-154), DOJO (p.95-99, p.228-237)

---

## Glossario: i servizi che incontrerai in questo documento

- **SQS (Simple Queue Service)** — una coda di messaggi. L'applicazione A mette un messaggio nella coda, l'applicazione B lo legge e lo processa quando è pronta. Serve per disaccoppiare i componenti: se B è giù o lento, i messaggi aspettano in coda senza perdere nulla. Come la coda al banco della posta: i clienti prendono il numerino e aspettano, l'impiegato li serve uno alla volta quando è libero.

- **SNS (Simple Notification Service)** — un servizio di notifiche pub/sub (publish/subscribe). Un publisher manda un messaggio a un "topic", e TUTTI i subscriber di quel topic lo ricevono. Può mandare email, SMS, notifiche push, o triggerare Lambda e SQS. Come un altoparlante in un aeroporto: un annuncio, tutti i passeggeri lo sentono.

- **EventBridge** — un event bus serverless che connette applicazioni usando eventi. A differenza di SNS (one-to-many), EventBridge è **many-to-many**: molte sorgenti di eventi possono triggerare molte destinazioni, con regole di filtraggio sofisticate. Come un centralino telefonico intelligente che instrada le chiamate in base al contenuto.

- **Lambda** — il servizio serverless di AWS. Scrivi il tuo codice, lo carichi, e AWS lo esegue quando succede qualcosa (un evento). Non devi gestire nessun server. Paghi solo per il tempo effettivo di esecuzione (millisecondi). Scala automaticamente. Timeout massimo: 15 minuti. Come un cameriere a chiamata: arriva solo quando lo chiami, lavora, e se ne va.

- **Step Functions** — un servizio per orchestrare workflow complessi che coinvolgono multiple Lambda functions (o altri servizi). Definisci un flusso con passi sequenziali, paralleli, condizionali, retry e error handling. Come un diagramma di flusso che si esegue da solo.

- **API Gateway** — un servizio per creare, pubblicare e gestire API REST e WebSocket. Fa da "porta d'ingresso" per le tue applicazioni serverless. Gestisce autenticazione, throttling, caching delle risposte, e monitoring. Come il portiere di un palazzo che controlla chi entra, gestisce la coda, e ricorda le risposte alle domande frequenti.

- **Decoupling** — il principio di progettare i componenti di un'architettura in modo che possano funzionare indipendentemente l'uno dall'altro. Se un componente cade, gli altri continuano a funzionare. L'opposto di un sistema "monolitico" dove tutto è collegato e se un pezzo si rompe, tutto si ferma.

---

## Decoupling — Concetti (da Kimiko)

Kimiko introduce: *"Decoupling si riferisce a componenti della nostra architettura che possono operare senza consapevolezza o dipendenza da altri componenti. Ci piace chiamarlo loose decoupling. I componenti in un'architettura disaccoppiata sono come black box — possono fare il loro lavoro senza preoccuparsi di cosa fanno gli altri componenti."*

### Synchronous vs Asynchronous Decoupling (da Kimiko)

- **Synchronous**: i componenti devono essere sempre disponibili. Non è veramente "loose". Esempio: load balancing tra due istanze in AZ diverse — entrambe devono essere vive
- **Asynchronous (loose)**: i componenti possono andare offline. I messaggi vengono messi in coda e consegnati quando il componente torna online. *"Questo è quello che vogliamo targetizzare"*

### Esempio Pratico di Kimiko

Kimiko descrive un'architettura disaccoppiata per un servizio di closed captioning:
1. L'utente carica un video tramite un frontend → il video va in un **bucket S3**
2. Un messaggio **SQS** viene generato con la location del video e la lingua desiderata
3. Qualsiasi istanza EC2 disponibile nel pool prende il messaggio e fa il captioning
4. Quando finisce, mette il video in un altro bucket S3 e genera un messaggio SQS di completamento

*"Con questa soluzione disaccoppiata, abbiamo grandi opzioni per aggiungere, rimuovere, mantenere istanze EC2 nel pool senza impattare l'architettura complessiva."*

---

## Amazon SQS — Simple Queue Service

### Panoramica (da Kimiko e Dojo)

Kimiko mostra SQS nella console e spiega i due tipi di coda:

| Tipo | Caratteristiche |
|---|---|
| **Standard Queue** | *"Incredibilmente veloce. Supporta un numero quasi illimitato di transazioni per secondo per API action. Ma i messaggi possono arrivare in ordine diverso da quello di invio"* (Kimiko) |
| **FIFO Queue** | *"Buon throughput, ma garantisce delivery first-in-first-out perfetto e exactly-once processing. La duplicazione non viene introdotta"* (Kimiko). Il nome deve terminare con `.fifo` |

### Visibility Timeout (da Kimiko)

Kimiko spiega un parametro critico: *"Il default visibility timeout è il numero di secondi in cui il messaggio sarà invisibile ad altri potenziali consumer della coda, dopo che qualcuno lo prende. Questo assicura che non abbiamo multiple istanze EC2 che vanno a prendere lo stesso messaggio inutilmente."*

- Default: **30 secondi**
- Puoi ridurlo se sai che il processing è veloce (es. 5 secondi)
- Se il timeout scade e il messaggio non è stato cancellato, diventa di nuovo visibile per un altro consumer

### Walkthrough SQS di Kimiko

Kimiko crea una FIFO queue nella console:
1. Crea la coda con nome `test.fifo`
2. Invia un messaggio con body, message group ID, deduplication ID, e attributi custom
3. Fa polling per i messaggi e visualizza i dettagli
4. Mostra come purgare la coda

### SQS dal Dojo

Il Dojo aggiunge dettagli importanti:
- **Standard**: at-least-once delivery (possibili duplicati)
- **FIFO**: exactly-once processing, max **300 messaggi/secondo** (o 3000 con batching)
- **Dead Letter Queue (DLQ)**: coda dove finiscono i messaggi che non possono essere processati dopo N tentativi
- **Long Polling**: riduce il numero di risposte vuote e i costi — il consumer aspetta fino a quando un messaggio è disponibile (fino a 20 secondi)

---

## Amazon SNS — Simple Notification Service

### Panoramica (da Kimiko)

Kimiko mostra SNS nella console: *"SNS è il servizio di notifica. Ci aiuta a notificare altri componenti di eventi."*

### Modello Pub/Sub (dal Dojo)

Il Dojo spiega: *"SNS è un servizio di messaggistica pub/sub fully managed. Un publisher invia un messaggio a un topic SNS, e tutti i subscriber di quel topic ricevono il messaggio."*

Subscriber supportati:
- **SQS queues** — per processing asincrono
- **Lambda functions** — per processing serverless
- **HTTP/HTTPS endpoints** — per webhook
- **Email/SMS** — per notifiche umane
- **Mobile push** — per notifiche app

### SNS + SQS Fan-Out Pattern (dal Dojo)

Il Dojo descrive il pattern fan-out: un messaggio pubblicato su un topic SNS viene automaticamente inviato a multiple code SQS subscriber. Ogni coda processa il messaggio indipendentemente. Questo è il pattern per distribuire un evento a più consumer.

---

## Amazon EventBridge

### Dal PACKT Cap.13

Il PACKT posiziona EventBridge nel contesto del decoupling: *"SQS è comunicazione one-to-one, SNS è comunicazione one-to-many, EventBridge è comunicazione many-to-many."*

EventBridge è un event bus serverless che connette applicazioni usando eventi da:
- Servizi AWS (EC2 state change, S3 upload, ecc.)
- Applicazioni SaaS di terze parti
- Applicazioni custom

---

## AWS Lambda (dal PACKT e Dojo)

### Panoramica (dal Dojo)

Il Dojo descrive Lambda: *"AWS Lambda è un servizio di compute serverless che ti permette di eseguire codice senza provisionare o gestire server. Lambda esegue il tuo codice solo quando necessario e scala automaticamente."*

Caratteristiche chiave dal Dojo:
- **Event-driven**: eseguito in risposta a eventi (S3 upload, API Gateway request, SQS message, DynamoDB stream, ecc.)
- **Scaling automatico**: scala da zero a migliaia di esecuzioni concorrenti
- **Pay per use**: paghi solo per il tempo di esecuzione (millisecondi) e il numero di richieste
- **Timeout massimo**: **15 minuti** per esecuzione
- **Memoria**: da 128 MB a 10 GB
- **Stateless**: non mantiene stato tra esecuzioni. Per stato, usa S3 o DynamoDB
- **Linguaggi supportati**: Node.js, Python, Java, C#, Go, Ruby, PowerShell, e custom runtime

### Lambda Concurrency (dal Dojo)

Il Dojo spiega:
- **Reserved concurrency**: garantisce un numero di esecuzioni concorrenti per una funzione
- **Provisioned concurrency**: mantiene istanze "calde" per eliminare cold start
- **Account limit**: 1000 esecuzioni concorrenti di default (soft limit)

---

## AWS Step Functions (dal PACKT Cap.13)

Il PACKT descrive: *"Quando hai diverse Lambda functions da coordinare, considera Step Functions piuttosto che disaccoppiare con SQS. Questo ti dà più controllo sul processo di chaining delle Lambda e logica per cambiare cosa succede dopo senza bisogno di una Lambda intermediaria."*

---

## API Gateway (da Kimiko)

Kimiko introduce: *"L'API Gateway ti permette di prendere la tua API e scalarla così che sia disponibile in tutto il mondo."*

Il PACKT Cap.13 aggiunge: *"API Gateway caching cacha le risposte API — se la stessa richiesta arriva di nuovo, la risposta viene dalla cache."*

### Lambda Concurrency — In Profondità (dal Dojo)

Il Dojo spiega: *"Concurrency è il numero di richieste che la tua funzione sta servendo in un dato momento. Di default, il tuo account AWS ha un limite di 1000 esecuzioni Lambda concorrenti per Region. Tutte le tue funzioni Lambda contano contro questo limite."*

| Tipo | Come funziona |
|---|---|
| **Reserved concurrency** | Pool di richieste riservato per una specifica funzione. *"Una funzione non può utilizzare la reserved concurrency di un'altra funzione, quindi altre funzioni non possono impedire alla tua di scalare"* |
| **Provisioned concurrency** | Inizializza un numero di ambienti di esecuzione pronti a rispondere senza cold start. *"Utile per funzioni che devono rispondere immediatamente"* |

> **Nota Dojo**: *"Entrambi i piani possono essere usati insieme, ma la provisioned concurrency non può superare la reserved concurrency massima."*

### Lambda Memory e Timeout (dal Dojo)

Il Dojo fornisce dettagli specifici:
- **Memoria**: da 128 MB a 10,240 MB in incrementi di 1 MB. *"A 1,769 MB, una funzione ha l'equivalente di un vCPU"*
- **Timeout**: default 3 secondi, massimo **900 secondi (15 minuti)**
- **CPU**: allocata proporzionalmente alla memoria configurata
- **Billing**: addebitato per ogni 1ms di esecuzione × memoria allocata

> **Nota Dojo**: *"Non allocare il massimo di memoria e timeout per tutte le funzioni — allocare grandi quantità di memoria quando non serve aumenta i costi. Scegli le impostazioni ottimali con qualche test run e metriche CloudWatch."*

### Lambda@Edge (dal Dojo)

Il Dojo descrive Lambda@Edge: *"Una feature di CloudFront che ti permette di eseguire codice Lambda alle edge location nel mondo. Non c'è infrastruttura da mantenere o deployare."*

Trigger supportati:
- **Viewer request**: dopo che CloudFront riceve una richiesta dall'utente
- **Origin request**: prima che CloudFront inoltri la richiesta all'origin
- **Origin response**: dopo che CloudFront riceve la risposta dall'origin
- **Viewer response**: prima che CloudFront inoltri la risposta all'utente

Supporta solo **Node.js e Python**.

---

## Scenari Tipici d'Esame

### Scenario 1: Disaccoppiare web tier da processing tier
**Domanda**: Il web server riceve richieste di elaborazione che richiedono tempo. Come disaccoppiare?

**Risposta**: **SQS** — il web server mette i messaggi in coda, i worker li processano quando disponibili (Kimiko esempio closed captioning).

### Scenario 2: Notificare più sistemi di un evento
**Domanda**: Quando un ordine viene creato, devi notificare il sistema di inventario, il sistema di fatturazione e il sistema di spedizione.

**Risposta**: **SNS** con topic "OrderCreated" e 3 subscriber (SQS queues per ogni sistema) — pattern fan-out (Dojo).

### Scenario 3: Coordinare multiple Lambda
**Domanda**: Un workflow richiede l'esecuzione sequenziale di 5 Lambda functions con logica condizionale.

**Risposta**: **Step Functions** (PACKT Cap.13: *"Considera Step Functions piuttosto che SQS per coordinare Lambda"*).

### Scenario 4: Processing che non deve perdere messaggi
**Domanda**: I messaggi devono essere processati esattamente una volta, nell'ordine di arrivo.

**Risposta**: **SQS FIFO** — exactly-once processing, ordine garantito (Kimiko, Dojo).

### Scenario 5: Event-driven con molte sorgenti
**Domanda**: Devi reagire a eventi da servizi AWS, applicazioni SaaS e applicazioni custom.

**Risposta**: **EventBridge** — many-to-many, event bus serverless (PACKT Cap.13).

### Scenario 6: Funzione che gira per 30 minuti
**Domanda**: Un job di elaborazione richiede 30 minuti. Può usare Lambda?

**Risposta**: **No** — Lambda ha un timeout massimo di 15 minuti (Dojo). Usa EC2, ECS/Fargate, o AWS Batch.

---

## Riepilogo Veloce per l'Esame

- **SQS**: coda messaggi, 1:1, Standard (fast, at-least-once) vs FIFO (ordered, exactly-once) (Kimiko, Dojo)
- **SNS**: pub/sub, 1:many, topic con subscriber (SQS, Lambda, HTTP, email, SMS) (Dojo)
- **EventBridge**: event bus, many:many, eventi da AWS/SaaS/custom (PACKT Cap.13)
- **SQS = 1:1, SNS = 1:many, EventBridge = many:many** — regola chiave per l'esame (PACKT Cap.13)
- **Fan-out**: SNS topic → multiple SQS queues (Dojo)
- **Visibility timeout**: tempo in cui il messaggio è invisibile dopo il pickup. Default 30s (Kimiko)
- **DLQ**: per messaggi che falliscono dopo N tentativi (Dojo)
- **Long Polling**: riduce costi e risposte vuote in SQS (Dojo)
- **Lambda**: serverless, event-driven, max 15 min, stateless, pay per ms × memoria (Dojo)
- **Lambda memory**: 128MB-10GB, CPU proporzionale. A 1,769MB = 1 vCPU (Dojo)
- **Lambda concurrency**: 1000 default/Region. Reserved (garantita per funzione), Provisioned (no cold start) (Dojo)
- **Lambda@Edge**: codice Lambda alle edge location CloudFront, solo Node.js/Python (Dojo)
- **Step Functions**: per coordinare multiple Lambda con logica condizionale (PACKT Cap.13)
- **API Gateway**: scala API globalmente, supporta caching delle risposte (Kimiko, PACKT)
- **Loose coupling (async) > tight coupling (sync)** — target sempre il decoupling asincrono (Kimiko)
