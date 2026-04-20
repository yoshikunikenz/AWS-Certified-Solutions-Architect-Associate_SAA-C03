# CloudFront, Route 53, Global Accelerator

> Sources: PACKT Ch.6 (p.277-309), PACKT Ch.14 (p.569-577), KIMIKO (p.225-233), DOJO (p.173-181, p.191-203, p.271, p.275)

---

## Glossary: the services you will encounter in this document

- **Route 53** — AWS's DNS service. Translates domain names (e.g. www.mysite.com) into IP addresses. The name comes from TCP/UDP port 53 used by the DNS protocol. It also offers intelligent routing: it can send users to the nearest server, perform health checks, and redirect traffic if a server is down. You can register domains directly in Route 53.

- **CloudFront** — AWS's CDN (Content Delivery Network). Takes your content (images, videos, web pages) and copies it to Edge Locations around the world. When a user in Italy requests an image, it's served from the nearest Edge Location instead of the server in Virginia. Result: much faster loading. Like having copies of your menu at every restaurant branch instead of making everyone call headquarters.

- **Global Accelerator** — a service that improves global application performance by routing traffic through AWS's private network (instead of the public internet). Provides **static IPs** as a fixed entry point. Unlike CloudFront which caches content, Global Accelerator optimizes the **network path**. Works with TCP and UDP, not just HTTP.

- **ALB (Application Load Balancer)** — the load balancer for web applications. Operates at the HTTP/HTTPS level (Layer 7). Can route traffic based on URL, hostname, HTTP headers. Perfect for microservices where different URLs go to different backends.

- **NLB (Network Load Balancer)** — the load balancer for TCP/UDP traffic (Layer 4). Ultra-fast, handles millions of requests per second with very low latency. Provides **static IPs**. Perfect for gaming applications, IoT, or anything that isn't HTTP.

- **Edge Location** — mini data centers spread around the world (there are hundreds). Used by CloudFront to cache content and by Lambda@Edge to run code close to users.

---

## Amazon Route 53

### Overview (from PACKT Ch.14 and Kimiko)

PACKT Ch.14 describes Route 53 as *"un servizio DNS scalabile che gestisce la risoluzione dei nomi di dominio per le applicazioni. Offre funzionalità di routing basate su latenza, health check e posizione geografica per garantire alta disponibilità e performance ottimali."*

Kimiko shows the service in the console: *"Saresti in difficoltà a trovare qualcosa che non puoi fare con Route 53. È davvero impressionante. Puoi registrare domini, fare traffic management, availability monitoring, traffic policies, risolvere per i tuoi VPC interni e outbound."*

### Domain Registration and Hosted Zone (from Kimiko)

Kimiko shows the practical process:
1. Register a domain directly in Route 53
2. Route 53 automatically creates a **hosted zone** with NS (name server) and SOA (start of authority) records
3. You can modify the name servers if needed (e.g. to use CloudFlare)
4. Create DNS records: A, AAAA, CNAME, MX, TXT, etc.

### Routing Policies (from Kimiko and Dojo)

Kimiko shows the routing options: *"Quando crei un record, puoi fare simple routing, weighted, geolocation — puoi costruire intelligenza in come DNS instraderà il traffico."*

| Policy | What it does |
|---|---|
| **Simple** | Basic routing, no special logic |
| **Weighted** | Distributes traffic in percentages across endpoints |
| **Latency-based** | Routes to the endpoint with the lowest latency |
| **Geolocation** | Routes based on the user's geographic location |
| **Failover** | Routes to a primary endpoint, fails over to secondary if primary is unhealthy |

### Alias Records (from Kimiko)

Kimiko shows a powerful feature: *"Quando crei un record, puoi fare alias a tutti i tipi di componenti AWS — puoi puntare ad altri servizi AWS con questa entry DNS. Questo è fantastico."*

> **Exam tip (from Kimiko)**: *"L'esame è noto per fare domande di DNS standard — come 'a cosa serve un record MX?' Assicurati di conoscere i tipi di record DNS base."*

---

## Amazon CloudFront

### Overview (from PACKT Ch.14 and Kimiko)

PACKT Ch.14 describes CloudFront as *"una content delivery network (CDN) che cacha e distribuisce contenuti da una rete di edge location distribuite globalmente. Servendo contenuti da location più vicine agli utenti finali, CloudFront riduce la latenza e migliora i tempi di caricamento."*

Kimiko explains the concept: *"Oltre alle Region e alle AZ, ci sono le edge location posizionate strategicamente. CloudFront è un'opportunità di caching per le tue risorse chiave e usa queste edge location. Questo è come puoi davvero assicurarti che l'accesso alle risorse per i tuoi clienti sia ad altissima velocità."*

### Distribution Types (from Kimiko)

Kimiko shows in the console:
- **Web distribution**: for distributing web content
- **RTMP distribution**: for speeding up streaming media file distribution

### Pricing (from Kimiko)

Kimiko shows the pricing options:
- **Free tier** (first year): 50 GB data transfer out + 2 million HTTP/HTTPS requests per month
- **On-demand**: *"Se sei negli USA/Canada e fai solo 10 TB al mese, spendi meno di un dollaro — circa 8.5 centesimi. Può essere molto, molto conveniente."*
- **Commitment pricing**: for 10+ TB/month, contact AWS for discounted prices

### Integration with Other Services (from PACKT Ch.14)

PACKT Ch.14 notes: *"CloudFront si integra con Amazon S3 per lo storage dei contenuti e AWS Lambda per serverless computing, permettendo di implementare logica custom e processing all'edge. Questo riduce la necessità che i dati viaggino avanti e indietro tra i tuoi origin server e gli utenti finali."*

---

## AWS Global Accelerator

### Overview (from PACKT Ch.14)

PACKT Ch.14 describes: *"AWS Global Accelerator migliora le performance e la disponibilità delle applicazioni globali instradando il traffico utente attraverso l'estesa rete globale di AWS. Fornisce indirizzi IP statici e dirige il traffico verso la edge location AWS più vicina, riducendo la latenza."*

### CloudFront vs Global Accelerator (from Dojo)

The Dojo provides the key comparison:

| Feature | CloudFront | Global Accelerator |
|---|---|---|
| **IP** | Dynamic IPs that change | **Static IPs** as a fixed entry point |
| **Pricing** | Based on data transfer out and HTTP requests | Fixed hourly fee + DT-Premium |
| **Edge Locations** | Uses edge locations to **cache content** | Uses edge locations to find the **optimal pathway** to the nearest regional endpoint |
| **Protocols** | Designed for **HTTP/HTTPS** | For **HTTP and non-HTTP** (TCP, UDP) |

> **Exam rule**: CloudFront for web/HTTP content. Global Accelerator for non-HTTP TCP/UDP applications or when static IPs are needed.

---

## Latency-Based Routing vs CloudFront (from Dojo)

The Dojo provides a detailed comparison:

| Aspect | Route 53 Latency-Based Routing | CloudFront |
|---|---|---|
| **Infrastructure** | Requires applications deployed in **multiple Regions** | Just a single Region + CloudFront caches at edge locations. **Can save a lot of money** |
| **Content** | Always serves the **most recent content** (important for real-time data) | Caches static and dynamic content according to caching rules. If you don't enable caching, CloudFront doesn't reduce latency |
| **Additional uses** | Combinable with weighted routing for global HA, per-region analytics | Geo restriction, Lambda@Edge for edge computing, WAF anti-DDoS integration, custom error pages |

> **Dojo note**: *"Non c'è nessuna regola che dice che non puoi usare entrambe le tecnologie insieme."*

---

## Load Balancer — Which to Choose (from PACKT Ch.14)

PACKT Ch.14 provides clear guidelines:

| Load Balancer | Protocol | When to use it |
|---|---|---|
| **ALB** | HTTP/HTTPS | Web applications, microservices, URL-based routing, host-based routing, WebSocket |
| **NLB** | TCP/UDP | High throughput, low latency, **static IPs**, high-performance applications |
| **CLB** | HTTP/HTTPS + TCP | Legacy — **unlikely to be the correct answer** on the exam |

> **Exam tip (PACKT Ch.14)**: *"Per l'esame, il load balancer giusto molto probabilmente non sarà il CLB. AWS raccomanda di non usarlo. I due differenziatori chiave tra ALB e NLB sono i protocolli supportati e il supporto IP statici. Se l'applicazione è web con HTTP/HTTPS → ALB. Se richiede IP statici → NLB."*

---

## Network Architecture Best Practices (from PACKT Ch.14)

### Scalability
- Distribute resources across **multiple AZs** for HA and fault tolerance
- **Public subnet** for resources with internet access (web servers, LBs)
- **Private subnet** for internal resources (app servers, databases)

### Global and Hybrid Connectivity
- **Global Accelerator**: for global applications, optimized routing, static IPs
- **Direct Connect**: dedicated on-premises ↔ AWS connection, lower latency and more consistent performance than the internet

### Redundancy and Failover
- ELB across multiple AZs — if one AZ becomes unavailable, traffic is routed to healthy instances in other AZs

### Resource Placement
- Deploy in Regions/AZs **geographically close** to users
- For global applications, use Global Accelerator to direct traffic to the nearest edge location

> **Exam tip (PACKT Ch.14)**: *"Potresti ricevere una domanda sulla migliore location per deployare infrastruttura, data la posizione geografica fornita nella domanda."*

### Monitoring (from PACKT Ch.14)
- **CloudWatch**: network metrics (latency, throughput), alarms
- **X-Ray**: tracing and analysis of network requests, bottleneck identification
- **VPC Flow Logs**: capture and analyze VPC traffic

---

## Typical Exam Scenarios

### Scenario 1: Reduce latency for global users
**Question**: Users in Asia experience high latency accessing an application hosted in us-east-1.

**Answer**: **CloudFront** to cache content at edge locations near Asian users (PACKT Ch.14, Kimiko).

### Scenario 2: TCP application with static IPs
**Question**: A TCP gaming application requires static IPs and low global latency.

**Answer**: **Global Accelerator** — static IPs, supports TCP/UDP, optimized routing (Dojo).

### Scenario 3: Web application with advanced routing
**Question**: A web application needs to route requests based on URL path.

**Answer**: **ALB** — supports URL-based routing and host-based routing (PACKT Ch.14).

### Scenario 4: DNS failover
**Question**: If the primary server goes down, traffic must be automatically redirected to the secondary server.

**Answer**: **Route 53 with failover routing policy** + health checks (Kimiko).

### Scenario 5: Real-time vs cached content
**Question**: The application serves real-time data that changes continuously. How to reduce global latency?

**Answer**: **Route 53 latency-based routing** with application in multiple Regions (Dojo: *"Latency-based routing always delivers the latest content. CloudFront caches content."*).

---

## Quick Recap for the Exam

- **Route 53**: scalable DNS, routing policies (simple/weighted/latency/geolocation/failover), alias to AWS services (PACKT, Kimiko)
- **CloudFront**: CDN, caches content at edge locations, reduces latency, integrates with S3/Lambda/WAF (PACKT, Kimiko)
- **Global Accelerator**: static IPs, optimized routing via AWS network, for non-HTTP TCP/UDP (PACKT, Dojo)
- **CloudFront = HTTP/caching, Global Accelerator = TCP-UDP/static IPs** (Dojo)
- **ALB = HTTP/HTTPS + advanced routing, NLB = TCP-UDP + static IPs, CLB = legacy (don't use)** (PACKT Ch.14)
- **Latency routing**: serves most recent content, requires multi-Region. **CloudFront**: caches, just one Region needed (Dojo)
- **Direct Connect**: dedicated on-premises connection, lower latency, but months to implement (PACKT)
- **Multi-AZ**: distribute resources for HA. Public subnet for web, private for data (PACKT Ch.14)
- **Monitoring**: CloudWatch (metrics), X-Ray (tracing), VPC Flow Logs (traffic) (PACKT Ch.14)
- **CloudFront pricing**: free tier 50GB/month, on-demand very cheap for low volumes (Kimiko)
