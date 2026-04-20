# Decoupling (SQS, SNS, EventBridge) and Serverless (Lambda, Step Functions)

> Sources: PACKT Ch.9 (p.413-436), PACKT Ch.13 (p.534-543), KIMIKO (p.140-154), DOJO (p.95-99, p.228-237)

---

## Glossary: the services you will encounter in this document

- **SQS (Simple Queue Service)** — a message queue. Application A puts a message in the queue, application B reads it and processes it when ready. It serves to decouple components: if B is down or slow, messages wait in the queue without losing anything. Like the queue at the post office counter: customers take a number and wait, the clerk serves them one at a time when free.

- **SNS (Simple Notification Service)** — a pub/sub (publish/subscribe) notification service. A publisher sends a message to a "topic", and ALL subscribers of that topic receive it. It can send emails, SMS, push notifications, or trigger Lambda and SQS. Like a loudspeaker in an airport: one announcement, all passengers hear it.

- **EventBridge** — a serverless event bus that connects applications using events. Unlike SNS (one-to-many), EventBridge is **many-to-many**: many event sources can trigger many destinations, with sophisticated filtering rules. Like an intelligent telephone switchboard that routes calls based on content.

- **Lambda** — the AWS serverless service. You write your code, upload it, and AWS runs it when something happens (an event). You don't have to manage any servers. You pay only for the actual execution time (milliseconds). It scales automatically. Maximum timeout: 15 minutes. Like an on-call waiter: arrives only when you call, works, and leaves.

- **Step Functions** — a service for orchestrating complex workflows involving multiple Lambda functions (or other services). You define a flow with sequential, parallel, conditional steps, retry and error handling. Like a flowchart that executes itself.

- **API Gateway** — a service for creating, publishing, and managing REST and WebSocket APIs. It acts as the "front door" for your serverless applications. It handles authentication, throttling, response caching, and monitoring. Like the doorman of a building who checks who enters, manages the queue, and remembers answers to frequently asked questions.

- **Decoupling** — the principle of designing architecture components so they can operate independently of each other. If one component goes down, the others continue to work. The opposite of a "monolithic" system where everything is connected and if one piece breaks, everything stops.

---

## Decoupling — Concepts (from Kimiko)

Kimiko introduces: *"Decoupling si riferisce a componenti della nostra architettura che possono operare senza consapevolezza o dipendenza da altri componenti. Ci piace chiamarlo loose decoupling. I componenti in un'architettura disaccoppiata sono come black box — possono fare il loro lavoro senza preoccuparsi di cosa fanno gli altri componenti."*

### Synchronous vs Asynchronous Decoupling (from Kimiko)

- **Synchronous**: components must always be available. Not truly "loose". Example: load balancing between two instances in different AZs — both must be alive
- **Asynchronous (loose)**: components can go offline. Messages are queued and delivered when the component comes back online. *"Questo è quello che vogliamo targetizzare"*

### Kimiko's Practical Example

Kimiko describes a decoupled architecture for a closed captioning service:
1. The user uploads a video through a frontend → the video goes to an **S3 bucket**
2. An **SQS** message is generated with the video location and desired language
3. Any available EC2 instance in the pool picks up the message and does the captioning
4. When finished, it puts the video in another S3 bucket and generates an SQS completion message

*"Con questa soluzione disaccoppiata, abbiamo grandi opzioni per aggiungere, rimuovere, mantenere istanze EC2 nel pool senza impattare l'architettura complessiva."*

---

## Amazon SQS — Simple Queue Service

### Overview (from Kimiko and Dojo)

Kimiko shows SQS in the console and explains the two queue types:

| Type | Features |
|---|---|
| **Standard Queue** | *"Incredibilmente veloce. Supporta un numero quasi illimitato di transazioni per secondo per API action. Ma i messaggi possono arrivare in ordine diverso da quello di invio"* (Kimiko) |
| **FIFO Queue** | *"Buon throughput, ma garantisce delivery first-in-first-out perfetto e exactly-once processing. La duplicazione non viene introdotta"* (Kimiko). The name must end with `.fifo` |

### Visibility Timeout (from Kimiko)

Kimiko explains a critical parameter: *"Il default visibility timeout è il numero di secondi in cui il messaggio sarà invisibile ad altri potenziali consumer della coda, dopo che qualcuno lo prende. Questo assicura che non abbiamo multiple istanze EC2 che vanno a prendere lo stesso messaggio inutilmente."*

- Default: **30 seconds**
- You can reduce it if you know processing is fast (e.g., 5 seconds)
- If the timeout expires and the message hasn't been deleted, it becomes visible again for another consumer

### Kimiko's SQS Walkthrough

Kimiko creates a FIFO queue in the console:
1. Creates the queue with name `test.fifo`
2. Sends a message with body, message group ID, deduplication ID, and custom attributes
3. Polls for messages and views the details
4. Shows how to purge the queue

### SQS from Dojo

Dojo adds important details:
- **Standard**: at-least-once delivery (possible duplicates)
- **FIFO**: exactly-once processing, max **300 messages/second** (or 3000 with batching)
- **Dead Letter Queue (DLQ)**: queue where messages that can't be processed after N attempts end up
- **Long Polling**: reduces the number of empty responses and costs — the consumer waits until a message is available (up to 20 seconds)

---

## Amazon SNS — Simple Notification Service

### Overview (from Kimiko)

Kimiko shows SNS in the console: *"SNS è il servizio di notifica. Ci aiuta a notificare altri componenti di eventi."*

### Pub/Sub Model (from Dojo)

Dojo explains: *"SNS è un servizio di messaggistica pub/sub fully managed. Un publisher invia un messaggio a un topic SNS, e tutti i subscriber di quel topic ricevono il messaggio."*

Supported subscribers:
- **SQS queues** — for asynchronous processing
- **Lambda functions** — for serverless processing
- **HTTP/HTTPS endpoints** — for webhooks
- **Email/SMS** — for human notifications
- **Mobile push** — for app notifications

### SNS + SQS Fan-Out Pattern (from Dojo)

Dojo describes the fan-out pattern: a message published to an SNS topic is automatically sent to multiple subscriber SQS queues. Each queue processes the message independently. This is the pattern for distributing an event to multiple consumers.

---

## Amazon EventBridge

### From PACKT Ch.13

PACKT positions EventBridge in the decoupling context: *"SQS è comunicazione one-to-one, SNS è comunicazione one-to-many, EventBridge è comunicazione many-to-many."*

EventBridge is a serverless event bus that connects applications using events from:
- AWS services (EC2 state change, S3 upload, etc.)
- Third-party SaaS applications
- Custom applications

---

## AWS Lambda (from PACKT and Dojo)

### Overview (from Dojo)

Dojo describes Lambda: *"AWS Lambda è un servizio di compute serverless che ti permette di eseguire codice senza provisionare o gestire server. Lambda esegue il tuo codice solo quando necessario e scala automaticamente."*

Key features from Dojo:
- **Event-driven**: executed in response to events (S3 upload, API Gateway request, SQS message, DynamoDB stream, etc.)
- **Automatic scaling**: scales from zero to thousands of concurrent executions
- **Pay per use**: you pay only for execution time (milliseconds) and number of requests
- **Maximum timeout**: **15 minutes** per execution
- **Memory**: from 128 MB to 10 GB
- **Stateless**: doesn't maintain state between executions. For state, use S3 or DynamoDB
- **Supported languages**: Node.js, Python, Java, C#, Go, Ruby, PowerShell, and custom runtime

### Lambda Concurrency (from Dojo)

Dojo explains:
- **Reserved concurrency**: guarantees a number of concurrent executions for a function
- **Provisioned concurrency**: keeps "warm" instances to eliminate cold starts
- **Account limit**: 1000 concurrent executions by default (soft limit)

---

## AWS Step Functions (from PACKT Ch.13)

PACKT describes: *"Quando hai diverse Lambda functions da coordinare, considera Step Functions piuttosto che disaccoppiare con SQS. Questo ti dà più controllo sul processo di chaining delle Lambda e logica per cambiare cosa succede dopo senza bisogno di una Lambda intermediaria."*

---

## API Gateway (from Kimiko)

Kimiko introduces: *"L'API Gateway ti permette di prendere la tua API e scalarla così che sia disponibile in tutto il mondo."*

PACKT Ch.13 adds: *"API Gateway caching cacha le risposte API — se la stessa richiesta arriva di nuovo, la risposta viene dalla cache."*

### Lambda Concurrency — In Depth (from Dojo)

Dojo explains: *"Concurrency è il numero di richieste che la tua funzione sta servendo in un dato momento. Di default, il tuo account AWS ha un limite di 1000 esecuzioni Lambda concorrenti per Region. Tutte le tue funzioni Lambda contano contro questo limite."*

| Type | How it works |
|---|---|
| **Reserved concurrency** | Request pool reserved for a specific function. *"Una funzione non può utilizzare la reserved concurrency di un'altra funzione, quindi altre funzioni non possono impedire alla tua di scalare"* |
| **Provisioned concurrency** | Initializes a number of execution environments ready to respond without cold start. *"Utile per funzioni che devono rispondere immediatamente"* |

> **Dojo Note**: *"Entrambi i piani possono essere usati insieme, ma la provisioned concurrency non può superare la reserved concurrency massima."*

### Lambda Memory and Timeout (from Dojo)

Dojo provides specific details:
- **Memory**: from 128 MB to 10,240 MB in 1 MB increments. *"A 1,769 MB, una funzione ha l'equivalente di un vCPU"*
- **Timeout**: default 3 seconds, maximum **900 seconds (15 minutes)**
- **CPU**: allocated proportionally to configured memory
- **Billing**: charged per 1ms of execution × allocated memory

> **Dojo Note**: *"Non allocare il massimo di memoria e timeout per tutte le funzioni — allocare grandi quantità di memoria quando non serve aumenta i costi. Scegli le impostazioni ottimali con qualche test run e metriche CloudWatch."*

### Lambda@Edge (from Dojo)

Dojo describes Lambda@Edge: *"Una feature di CloudFront che ti permette di eseguire codice Lambda alle edge location nel mondo. Non c'è infrastruttura da mantenere o deployare."*

Supported triggers:
- **Viewer request**: after CloudFront receives a request from the user
- **Origin request**: before CloudFront forwards the request to the origin
- **Origin response**: after CloudFront receives the response from the origin
- **Viewer response**: before CloudFront forwards the response to the user

Supports only **Node.js and Python**.

---

## Typical Exam Scenarios

### Scenario 1: Decouple web tier from processing tier
**Question**: The web server receives processing requests that take a long time. How to decouple?

**Answer**: **SQS** — the web server puts messages in the queue, workers process them when available (Kimiko closed captioning example).

### Scenario 2: Notify multiple systems of an event
**Question**: When an order is created, you need to notify the inventory system, the billing system, and the shipping system.

**Answer**: **SNS** with "OrderCreated" topic and 3 subscribers (SQS queues for each system) — fan-out pattern (Dojo).

### Scenario 3: Coordinate multiple Lambda functions
**Question**: A workflow requires sequential execution of 5 Lambda functions with conditional logic.

**Answer**: **Step Functions** (PACKT Ch.13: *"Considera Step Functions piuttosto che SQS per coordinare Lambda"*).

### Scenario 4: Processing that must not lose messages
**Question**: Messages must be processed exactly once, in order of arrival.

**Answer**: **SQS FIFO** — exactly-once processing, guaranteed order (Kimiko, Dojo).

### Scenario 5: Event-driven with many sources
**Question**: You need to react to events from AWS services, SaaS applications, and custom applications.

**Answer**: **EventBridge** — many-to-many, serverless event bus (PACKT Ch.13).

### Scenario 6: Function that runs for 30 minutes
**Question**: A processing job requires 30 minutes. Can it use Lambda?

**Answer**: **No** — Lambda has a maximum timeout of 15 minutes (Dojo). Use EC2, ECS/Fargate, or AWS Batch.

---

## Quick Review for the Exam

- **SQS**: message queue, 1:1, Standard (fast, at-least-once) vs FIFO (ordered, exactly-once) (Kimiko, Dojo)
- **SNS**: pub/sub, 1:many, topic with subscribers (SQS, Lambda, HTTP, email, SMS) (Dojo)
- **EventBridge**: event bus, many:many, events from AWS/SaaS/custom (PACKT Ch.13)
- **SQS = 1:1, SNS = 1:many, EventBridge = many:many** — key rule for the exam (PACKT Ch.13)
- **Fan-out**: SNS topic → multiple SQS queues (Dojo)
- **Visibility timeout**: time the message is invisible after pickup. Default 30s (Kimiko)
- **DLQ**: for messages that fail after N attempts (Dojo)
- **Long Polling**: reduces costs and empty responses in SQS (Dojo)
- **Lambda**: serverless, event-driven, max 15 min, stateless, pay per ms × memory (Dojo)
- **Lambda memory**: 128MB-10GB, CPU proportional. At 1,769MB = 1 vCPU (Dojo)
- **Lambda concurrency**: 1000 default/Region. Reserved (guaranteed per function), Provisioned (no cold start) (Dojo)
- **Lambda@Edge**: Lambda code at CloudFront edge locations, Node.js/Python only (Dojo)
- **Step Functions**: to coordinate multiple Lambda with conditional logic (PACKT Ch.13)
- **API Gateway**: scales APIs globally, supports response caching (Kimiko, PACKT)
- **Loose coupling (async) > tight coupling (sync)** — always target asynchronous decoupling (Kimiko)
