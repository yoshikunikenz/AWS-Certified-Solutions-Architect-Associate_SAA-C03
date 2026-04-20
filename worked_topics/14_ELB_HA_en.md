# Elastic Load Balancing and High Availability

> Sources: PACKT Ch.6 (p.288-309), PACKT Ch.14 (p.570-574), KIMIKO (p.155-162), DOJO (p.182-190)

---

## Glossary: the services you will encounter in this document

- **ELB (Elastic Load Balancer)** — the AWS load balancer. It distributes incoming traffic across multiple EC2 instances (or containers, or Lambda). If you have 3 web servers, the ELB sends requests evenly among the three. If a server goes down, the ELB stops sending it traffic and directs everything to the others. It serves both for performance (distributing the load) and for resilience (if one goes down, the others continue). Like a traffic officer directing traffic at intersections.

- **ALB (Application Load Balancer)** — the type of ELB for web applications (HTTP/HTTPS). It can do intelligent routing based on URL, hostname, or headers. Perfect for microservices. Uses round-robin or least outstanding requests algorithm.

- **NLB (Network Load Balancer)** — the type of ELB for TCP/UDP traffic. Ultra-fast (millions of requests/sec), provides **static IPs**. For gaming applications, IoT, or anything non-HTTP.

- **GWLB (Gateway Load Balancer)** — the type of ELB for third-party security appliances (firewall, IDS/IPS). Operates at Layer 3 (IP).

- **Target Group** — the group of "destinations" (instances, containers, Lambda) to which the load balancer sends traffic. It also defines health checks to verify that destinations are healthy.

- **Listener** — the "listening rule" of the load balancer. It defines which port to listen on and how to route requests. It can have multiple rules with priorities.

- **Health Check** — a periodic check that the load balancer performs on destinations to verify they are alive and functioning. If a destination doesn't respond, the LB stops sending it traffic. Like a doctor making rounds to check on patients.

---

## Load Balancing Overview (from PACKT)

PACKT explains: *"Un load balancer si posiziona davanti ai tuoi server e instrada le richieste tra i server che gestisce secondo la sua configurazione. Assicura che le richieste vengano inviate solo a server sani e che quei server non siano sovraccaricati. I load balancer sono elementi chiave dell'infrastruttura per garantire alta disponibilità, ridondanza e flessibilità."*

### High Availability vs Redundancy (from PACKT)

- **High Availability**: an architecture that remains available most of the time (maximum uptime). Achieved by removing single points of failure. Example: S3 has an availability SLA of 99.9%
- **Redundancy**: how you achieve HA. Provisioning extra copies of infrastructure — if the first fails, you switch to the second with minimal impact

### ELB — Features (from PACKT)

PACKT explains: *"ELB è, di default, un servizio elastico gestito da AWS. Ha ridondanza e alta disponibilità built-in. Sotto il cofano, ELB è in realtà diverse istanze che AWS gestisce, e il numero scala su e giù secondo il traffico. Non è il single point of failure che sembra a prima vista."*

ELB can balance: **EC2 instances, containers, Lambda functions**.

---

## Types of Load Balancers

### Comparison (from PACKT Ch.14 and Dojo)

| Type | Protocol | Routing | When to use |
|---|---|---|---|
| **ALB** | HTTP/HTTPS | Listener rules with priority, **round robin** or **least outstanding requests** (Dojo) | Web apps, microservices, URL/host-based routing, WebSocket |
| **NLB** | TCP/UDP/TLS | **Flow hash algorithm** (protocol, source/dest IP, port, TCP sequence) — a TCP connection stays on the same target (Dojo) | High throughput, ultra-low latency, **static IPs**, millions of requests/sec |
| **GWLB** | IP (Layer 3) | For third-party security appliances | Firewall, deep packet inspection, IDS/IPS (Dojo) |
| **CLB** | HTTP/HTTPS + TCP | Round robin (TCP), least outstanding requests (HTTP) | **Legacy** — AWS recommends not using it (PACKT Ch.14) |

> **Exam tip (PACKT Ch.14)**: *"Per l'esame, il load balancer giusto molto probabilmente non sarà il CLB. I due differenziatori chiave tra ALB e NLB sono: protocolli supportati e supporto IP statici. HTTP/HTTPS → ALB. IP statici → NLB."*

### Target Groups and Listeners (from PACKT)

**Target Groups**: group of targets (instances, Lambda) to which the LB sends traffic. Also defines health checks — by default, ELB sends a request every 30 seconds. If the target is unhealthy, ELB stops sending it traffic.

**Listeners**: route requests according to configured rules. Each rule has a priority (lower number = higher priority).

### ELB Idle Timeout (from Dojo)

Dojo explains: *"Per ogni richiesta, il LB stabilisce due connessioni: una con il client e una con il target. L'idle timeout è il numero di secondi che una connessione deve inviare nuovi dati per restare attiva."*

- Default: **60 seconds** for ALB and CLB (adjustable up to 4000 seconds)
- NLB: **350 seconds** (not adjustable)

> **Dojo Note**: *"Se stai mantenendo una connessione attiva solo per aspettare una risposta da un processo lungo, dovresti considerare di refactorare l'applicazione per usare trasmissioni asincrone, o creare una pipeline per disaccoppiare la risposta dal load balancer."*

---

## Auto Scaling — Kimiko's Hands-On Walkthrough

Kimiko shows the entire Auto Scaling process in the console with a live demo:

### Setup
1. **Create a Launch Configuration**: choose AMI (Ubuntu), instance type (t2.micro), storage (8 GB EBS), security group (SSH from anywhere)
2. **Create an Auto Scaling Group**: use the launch configuration, place in the default VPC, choose a subnet
3. **Configure the scaling policy**: scale dynamically between **1 and 5 instances**, based on **average CPU utilization** with a target of 5% (artificially low for the demo) and a warmup of 10 seconds

### Live Test
Kimiko connects via SSH to the instance and installs `stress`:
- Runs `sudo stress --cpu 64 --timeout 20` to stress the CPU
- Monitors in the EC2 console — after a while, new instances are launched automatically
- *"Auto scaling davvero, davvero potente. E ricorda, quando la CPU torna sotto la soglia, le istanze extra verranno terminate automaticamente."*

> **Insight from Kimiko**: *"Puoi anche configurare notifiche SNS per essere avvisato degli eventi di auto scaling via email."*

---

## Health Checks — ELB vs Route 53 (from Dojo)

Dojo compares the two types of health checks:

| Feature | ELB Health Check | Route 53 Health Check |
|---|---|---|
| **Purpose** | Verifies if the target is available to accept traffic | Monitors the status of a DNS record's target |
| **Target** | Instances, servers, Lambda in the target group | EC2, servers, AWS services with endpoints |
| **Action on unhealthy** | Stops sending traffic to the target | Can redirect DNS to a healthy endpoint |

---

## ALB Listener Rule Conditions — In Depth (from Dojo)

Dojo describes the conditions you can add to ALB listener rules to create advanced routing under a single load balancer:

| Condition | What it does | Example |
|---|---|---|
| **host-header** | Routing based on hostname (host-based routing). Supports subdomains and different top-level domains | `api.example.com` → API target group, `www.example.com` → web target group |
| **path-pattern** | Routing based on URL path (path-based routing). Case-sensitive | `/api/*` → API target group, `/images/*` → media target group |
| **http-header** | Routing based on HTTP headers (standard and custom). Case-insensitive | Header `X-Custom: mobile` → mobile target group |
| **http-request-method** | Routing based on HTTP method. Case-sensitive | `GET` → read target group, `POST` → write target group |
| **query-string** | Routing based on key/value in the query string. Case-insensitive | `?platform=mobile` → mobile target group |
| **source-ip** | Routing based on source IP (CIDR, IPv4 and IPv6) | Internal IPs → internal target group |

> **Dojo Note**: *"Una listener rule può includere al massimo una condizione per host-header, http-request-method, path-pattern e source-ip; e una o più condizioni per http-header e query-string. Massimo 5 match evaluations per regola."*

---

## Health Checks — ELB vs Route 53 (from Dojo)

Dojo compares the two types of health checks:

| Feature | ELB Health Check | Route 53 Health Check |
|---|---|---|
| **Purpose** | Verifies if the target is available to accept traffic | Monitors the status of a DNS record's target |
| **Scope** | Targets in multiple AZs but **not cross-region** | Targets **anywhere**, as long as reachable from Route 53 |
| **Frequency** | Configurable between 5 and 300 seconds | Every 10 or 30 seconds |
| **Timeout** | Configurable between 2 and 60 seconds | Not configurable |
| **Healthy criteria** | Configurable threshold of passed/failed checks | If >18% of health checkers report healthy → healthy |
| **Primary purpose** | HA and fault tolerance for services | DNS failover routing |

> **Dojo Best practice**: *"Non c'è nessuna regola che dice che non puoi usare entrambi gli health check insieme. In effetti, è una pratica migliore usarli entrambi! ELB assicura che il traffico vada solo a target sani, Route 53 assicura che i record DNS puntino a endpoint raggiungibili."*

---

## Typical Exam Scenarios

### Scenario 1: HTTP web app with URL routing
**Question**: A web application needs to route `/api/*` to one set of servers and `/static/*` to another.

**Answer**: **ALB** with listener rules for URL-based routing (PACKT Ch.14).

### Scenario 2: TCP application with static IPs
**Question**: An application requires a load balancer with static IPs and TCP support.

**Answer**: **NLB** — supports TCP/UDP, provides static IPs (PACKT Ch.14, Dojo).

### Scenario 3: Automatic scaling on CPU
**Question**: The application must scale automatically when CPU exceeds 70%.

**Answer**: **Auto Scaling Group** with scaling policy based on CPU utilization (Kimiko demo).

### Scenario 4: Long connections to the load balancer
**Question**: Backend requests take more than 60 seconds. Connections are being closed.

**Answer**: Increase the ALB **idle timeout** (Dojo). Or refactor for asynchronous communication.

---

## Quick Review for the Exam

- **ALB**: HTTP/HTTPS, advanced routing (URL/host), round robin or least outstanding requests (PACKT, Dojo)
- **NLB**: TCP/UDP/TLS, static IPs, ultra-low latency, millions req/sec, flow hash routing (PACKT, Dojo)
- **GWLB**: Layer 3, for third-party security appliances (Dojo)
- **CLB**: legacy, don't use (PACKT Ch.14)
- **HTTP → ALB, static IPs → NLB** (PACKT Ch.14)
- **Target Groups**: define targets + health checks (every 30s default) (PACKT)
- **Listeners**: rules with priority for routing (PACKT)
- **ELB is elastic and HA by default** — it's not a single point of failure (PACKT)
- **Idle timeout**: 60s ALB/CLB (adjustable), 350s NLB (fixed) (Dojo)
- **ALB listener conditions**: host-header, path-pattern, http-header, http-request-method, query-string, source-ip (Dojo)
- **ELB health check**: 5-300s frequency, multi-AZ scope. **Route 53 health check**: global scope, DNS failover (Dojo)
- **Use both** ELB + Route 53 health checks for maximum resilience (Dojo)
- **Launch template > launch configuration** for ASG (Dojo)
