# CloudFront, Route 53, Global Accelerator

> Fonti: PACKT Cap.6 (p.277-309), PACKT Cap.14 (p.569-577), KIMIKO (p.225-233), DOJO (p.173-181, p.191-203, p.271, p.275)

---

## Glossario: i servizi che incontrerai in questo documento

- **Route 53** — il servizio DNS di AWS. Traduce i nomi di dominio (es. www.miosito.com) in indirizzi IP. Il nome viene dalla porta TCP/UDP 53 usata dal protocollo DNS. Offre anche routing intelligente: può mandare gli utenti al server più vicino, fare health check e redirigere il traffico se un server è giù. Puoi registrare domini direttamente in Route 53.

- **CloudFront** — la CDN (Content Delivery Network) di AWS. Prende i tuoi contenuti (immagini, video, pagine web) e li copia nelle Edge Location in tutto il mondo. Quando un utente in Italia richiede un'immagine, la prende dall'Edge Location più vicina invece che dal server in Virginia. Risultato: caricamento molto più veloce. Come avere copie del tuo menu in ogni filiale del ristorante invece di far chiamare tutti la sede centrale.

- **Global Accelerator** — un servizio che migliora le performance delle applicazioni globali instradando il traffico attraverso la rete privata di AWS (invece che attraverso internet pubblico). Fornisce **IP statici** come punto di ingresso fisso. A differenza di CloudFront che cacha contenuti, Global Accelerator ottimizza il **percorso di rete**. Funziona con TCP e UDP, non solo HTTP.

- **ALB (Application Load Balancer)** — il bilanciatore di carico per applicazioni web. Opera a livello HTTP/HTTPS (Layer 7). Può instradare il traffico basandosi sull'URL, sull'hostname, sugli header HTTP. Perfetto per microservizi dove diverse URL vanno a diversi backend.

- **NLB (Network Load Balancer)** — il bilanciatore di carico per traffico TCP/UDP (Layer 4). Ultra-veloce, gestisce milioni di richieste al secondo con latenza bassissima. Fornisce **IP statici**. Perfetto per applicazioni gaming, IoT, o qualsiasi cosa che non sia HTTP.

- **Edge Location** — mini data center sparsi in tutto il mondo (ce ne sono centinaia). Usati da CloudFront per cachare contenuti e da Lambda@Edge per eseguire codice vicino agli utenti.

---

## Amazon Route 53

### Panoramica (dal PACKT Cap.14 e Kimiko)

Il PACKT Cap.14 descrive Route 53 come *"un servizio DNS scalabile che gestisce la risoluzione dei nomi di dominio per le applicazioni. Offre funzionalità di routing basate su latenza, health check e posizione geografica per garantire alta disponibilità e performance ottimali."*

Kimiko mostra il servizio nella console: *"Saresti in difficoltà a trovare qualcosa che non puoi fare con Route 53. È davvero impressionante. Puoi registrare domini, fare traffic management, availability monitoring, traffic policies, risolvere per i tuoi VPC interni e outbound."*

### Registrazione Domini e Hosted Zone (da Kimiko)

Kimiko mostra il processo pratico:
1. Registri un dominio direttamente in Route 53
2. Route 53 crea automaticamente una **hosted zone** con record NS (name server) e SOA (start of authority)
3. Puoi modificare i name server se necessario (es. per usare CloudFlare)
4. Crei record DNS: A, AAAA, CNAME, MX, TXT, ecc.

### Routing Policies (da Kimiko e Dojo)

Kimiko mostra le opzioni di routing: *"Quando crei un record, puoi fare simple routing, weighted, geolocation — puoi costruire intelligenza in come DNS instraderà il traffico."*

| Policy | Cosa fa |
|---|---|
| **Simple** | Routing base, nessuna logica speciale |
| **Weighted** | Distribuisce traffico in percentuali tra endpoint |
| **Latency-based** | Instrada verso l'endpoint con la latenza più bassa |
| **Geolocation** | Instrada basandosi sulla posizione geografica dell'utente |
| **Failover** | Instrada verso un endpoint primario, failover su secondario se il primario è unhealthy |

### Alias Records (da Kimiko)

Kimiko mostra una feature potente: *"Quando crei un record, puoi fare alias a tutti i tipi di componenti AWS — puoi puntare ad altri servizi AWS con questa entry DNS. Questo è fantastico."*

> **Tip esame (da Kimiko)**: *"L'esame è noto per fare domande di DNS standard — come 'a cosa serve un record MX?' Assicurati di conoscere i tipi di record DNS base."*

---

## Amazon CloudFront

### Panoramica (dal PACKT Cap.14 e Kimiko)

Il PACKT Cap.14 descrive CloudFront come *"una content delivery network (CDN) che cacha e distribuisce contenuti da una rete di edge location distribuite globalmente. Servendo contenuti da location più vicine agli utenti finali, CloudFront riduce la latenza e migliora i tempi di caricamento."*

Kimiko spiega il concetto: *"Oltre alle Region e alle AZ, ci sono le edge location posizionate strategicamente. CloudFront è un'opportunità di caching per le tue risorse chiave e usa queste edge location. Questo è come puoi davvero assicurarti che l'accesso alle risorse per i tuoi clienti sia ad altissima velocità."*

### Tipi di Distribuzione (da Kimiko)

Kimiko mostra nella console:
- **Web distribution**: per distribuire contenuti web
- **RTMP distribution**: per velocizzare la distribuzione di file media in streaming

### Pricing (da Kimiko)

Kimiko mostra le opzioni di pricing:
- **Free tier** (primo anno): 50 GB data transfer out + 2 milioni di richieste HTTP/HTTPS al mese
- **On-demand**: *"Se sei negli USA/Canada e fai solo 10 TB al mese, spendi meno di un dollaro — circa 8.5 centesimi. Può essere molto, molto conveniente."*
- **Commitment pricing**: per 10+ TB/mese, contatta AWS per prezzi scontati

### Integrazione con altri servizi (dal PACKT Cap.14)

Il PACKT Cap.14 nota: *"CloudFront si integra con Amazon S3 per lo storage dei contenuti e AWS Lambda per serverless computing, permettendo di implementare logica custom e processing all'edge. Questo riduce la necessità che i dati viaggino avanti e indietro tra i tuoi origin server e gli utenti finali."*

---

## AWS Global Accelerator

### Panoramica (dal PACKT Cap.14)

Il PACKT Cap.14 descrive: *"AWS Global Accelerator migliora le performance e la disponibilità delle applicazioni globali instradando il traffico utente attraverso l'estesa rete globale di AWS. Fornisce indirizzi IP statici e dirige il traffico verso la edge location AWS più vicina, riducendo la latenza."*

### CloudFront vs Global Accelerator (dal Dojo)

Il Dojo fornisce il confronto chiave:

| Caratteristica | CloudFront | Global Accelerator |
|---|---|---|
| **IP** | IP dinamici che cambiano | **IP statici** come entry point fisso |
| **Pricing** | Basato su data transfer out e richieste HTTP | Fee oraria fissa + DT-Premium |
| **Edge Locations** | Usa edge location per **cachare contenuti** | Usa edge location per trovare il **pathway ottimale** verso l'endpoint regionale più vicino |
| **Protocolli** | Progettato per **HTTP/HTTPS** | Per **HTTP e non-HTTP** (TCP, UDP) |

> **Regola per l'esame**: CloudFront per contenuti web/HTTP. Global Accelerator per applicazioni TCP/UDP non-HTTP o quando servono IP statici.

---

## Latency-Based Routing vs CloudFront (dal Dojo)

Il Dojo fornisce un confronto dettagliato:

| Aspetto | Route 53 Latency-Based Routing | CloudFront |
|---|---|---|
| **Infrastruttura** | Richiede applicazioni deployate in **più Region** | Basta una singola Region + CloudFront cacha nelle edge location. **Può risparmiare molto denaro** |
| **Contenuto** | Serve sempre il **contenuto più recente** (importante per dati real-time) | Cacha contenuti statici e dinamici secondo le regole di caching. Se non abiliti caching, CloudFront non riduce la latenza |
| **Usi aggiuntivi** | Combinabile con weighted routing per HA globale, analytics per region | Geo restriction, Lambda@Edge per computing all'edge, integrazione WAF anti-DDoS, custom error pages |

> **Nota Dojo**: *"Non c'è nessuna regola che dice che non puoi usare entrambe le tecnologie insieme."*

---

## Load Balancer — Quale Scegliere (dal PACKT Cap.14)

Il PACKT Cap.14 fornisce linee guida chiare:

| Load Balancer | Protocollo | Quando usarlo |
|---|---|---|
| **ALB** | HTTP/HTTPS | Web application, microservizi, URL-based routing, host-based routing, WebSocket |
| **NLB** | TCP/UDP | Alto throughput, bassa latenza, **IP statici**, applicazioni high-performance |
| **CLB** | HTTP/HTTPS + TCP | Legacy — **improbabile sia la risposta corretta** nell'esame |

> **Tip esame (PACKT Cap.14)**: *"Per l'esame, il load balancer giusto molto probabilmente non sarà il CLB. AWS raccomanda di non usarlo. I due differenziatori chiave tra ALB e NLB sono i protocolli supportati e il supporto IP statici. Se l'applicazione è web con HTTP/HTTPS → ALB. Se richiede IP statici → NLB."*

---

## Network Architecture Best Practices (dal PACKT Cap.14)

### Scalabilità
- Distribuisci risorse su **multiple AZ** per HA e fault tolerance
- **Public subnet** per risorse con accesso internet (web server, LB)
- **Private subnet** per risorse interne (app server, database)

### Connettività Globale e Ibrida
- **Global Accelerator**: per applicazioni globali, routing ottimizzato, IP statici
- **Direct Connect**: connessione dedicata on-premises ↔ AWS, latenza più bassa e performance più consistenti dell'internet

### Ridondanza e Failover
- ELB su multiple AZ — se una AZ diventa indisponibile, il traffico viene instradato alle istanze sane nelle altre AZ

### Placement delle Risorse
- Deploy in Region/AZ **geograficamente vicine** agli utenti
- Per applicazioni globali, usa Global Accelerator per dirigere il traffico alla edge location più vicina

> **Tip esame (PACKT Cap.14)**: *"Potresti ricevere una domanda sulla migliore location per deployare infrastruttura, data la posizione geografica fornita nella domanda."*

### Monitoring (dal PACKT Cap.14)
- **CloudWatch**: metriche di rete (latenza, throughput), allarmi
- **X-Ray**: tracing e analisi di richieste di rete, identificazione bottleneck
- **VPC Flow Logs**: cattura e analisi traffico nel VPC

---

## Scenari Tipici d'Esame

### Scenario 1: Ridurre latenza per utenti globali
**Domanda**: Gli utenti in Asia sperimentano alta latenza accedendo a un'applicazione hostata in us-east-1.

**Risposta**: **CloudFront** per cachare contenuti nelle edge location vicine agli utenti asiatici (PACKT Cap.14, Kimiko).

### Scenario 2: Applicazione TCP con IP statici
**Domanda**: Un'applicazione gaming TCP richiede IP statici e bassa latenza globale.

**Risposta**: **Global Accelerator** — IP statici, supporta TCP/UDP, routing ottimizzato (Dojo).

### Scenario 3: Web application con routing avanzato
**Domanda**: Un'applicazione web deve instradare richieste basandosi sull'URL path.

**Risposta**: **ALB** — supporta URL-based routing e host-based routing (PACKT Cap.14).

### Scenario 4: Failover DNS
**Domanda**: Se il server primario va giù, il traffico deve essere automaticamente rediretto al server secondario.

**Risposta**: **Route 53 con failover routing policy** + health checks (Kimiko).

### Scenario 5: Contenuti real-time vs cachati
**Domanda**: L'applicazione serve dati real-time che cambiano continuamente. Come ridurre la latenza globale?

**Risposta**: **Route 53 latency-based routing** con applicazione in più Region (Dojo: *"Latency-based routing always delivers the latest content. CloudFront caches content."*).

---

## Riepilogo Veloce per l'Esame

- **Route 53**: DNS scalabile, routing policies (simple/weighted/latency/geolocation/failover), alias a servizi AWS (PACKT, Kimiko)
- **CloudFront**: CDN, cacha contenuti nelle edge location, riduce latenza, integra con S3/Lambda/WAF (PACKT, Kimiko)
- **Global Accelerator**: IP statici, routing ottimizzato via rete AWS, per TCP/UDP non-HTTP (PACKT, Dojo)
- **CloudFront = HTTP/caching, Global Accelerator = TCP-UDP/IP statici** (Dojo)
- **ALB = HTTP/HTTPS + routing avanzato, NLB = TCP-UDP + IP statici, CLB = legacy (non usare)** (PACKT Cap.14)
- **Latency routing**: serve contenuto più recente, richiede multi-Region. **CloudFront**: cacha, basta una Region (Dojo)
- **Direct Connect**: connessione dedicata on-premises, latenza più bassa, ma mesi per implementare (PACKT)
- **Multi-AZ**: distribuisci risorse per HA. Public subnet per web, private per dati (PACKT Cap.14)
- **Monitoring**: CloudWatch (metriche), X-Ray (tracing), VPC Flow Logs (traffico) (PACKT Cap.14)
- **Pricing CloudFront**: free tier 50GB/mese, on-demand molto economico per volumi bassi (Kimiko)
