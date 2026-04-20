# Elastic Load Balancing e High Availability

> Fonti: PACKT Cap.6 (p.288-309), PACKT Cap.14 (p.570-574), KIMIKO (p.155-162), DOJO (p.182-190)

---

## Glossario: i servizi che incontrerai in questo documento

- **ELB (Elastic Load Balancer)** — il bilanciatore di carico di AWS. Distribuisce il traffico in arrivo su più istanze EC2 (o container, o Lambda). Se hai 3 web server, l'ELB manda le richieste equamente tra i tre. Se un server cade, l'ELB smette di mandargli traffico e dirige tutto sugli altri. Serve sia per performance (distribuire il carico) che per resilienza (se uno cade, gli altri continuano). Come un vigile urbano che dirige il traffico agli incroci.

- **ALB (Application Load Balancer)** — il tipo di ELB per applicazioni web (HTTP/HTTPS). Può fare routing intelligente basato sull'URL, sull'hostname, sugli header. Perfetto per microservizi. Usa algoritmo round-robin o least outstanding requests.

- **NLB (Network Load Balancer)** — il tipo di ELB per traffico TCP/UDP. Ultra-veloce (milioni di richieste/sec), fornisce **IP statici**. Per applicazioni gaming, IoT, o qualsiasi cosa non-HTTP.

- **GWLB (Gateway Load Balancer)** — il tipo di ELB per appliance di sicurezza di terze parti (firewall, IDS/IPS). Opera a Layer 3 (IP).

- **Target Group** — il gruppo di "destinazioni" (istanze, container, Lambda) a cui il load balancer invia il traffico. Definisce anche gli health check per verificare che le destinazioni siano sane.

- **Listener** — la "regola di ascolto" del load balancer. Definisce su quale porta ascoltare e come instradare le richieste. Può avere multiple regole con priorità.

- **Health Check** — un controllo periodico che il load balancer fa sulle destinazioni per verificare che siano vive e funzionanti. Se una destinazione non risponde, il LB smette di inviarle traffico. Come un medico che fa il giro delle corsie per controllare i pazienti.

---

## Overview del Load Balancing (dal PACKT)

Il PACKT spiega: *"Un load balancer si posiziona davanti ai tuoi server e instrada le richieste tra i server che gestisce secondo la sua configurazione. Assicura che le richieste vengano inviate solo a server sani e che quei server non siano sovraccaricati. I load balancer sono elementi chiave dell'infrastruttura per garantire alta disponibilità, ridondanza e flessibilità."*

### High Availability vs Redundancy (dal PACKT)

- **High Availability**: un'architettura che rimane disponibile la maggior parte del tempo (massimo uptime). Si ottiene rimuovendo single points of failure. Esempio: S3 ha un SLA di disponibilità del 99.9%
- **Redundancy**: come si ottiene la HA. Provisioning di copie extra dell'infrastruttura — se la prima fallisce, si passa alla seconda con impatto minimo

### ELB — Caratteristiche (dal PACKT)

Il PACKT spiega: *"ELB è, di default, un servizio elastico gestito da AWS. Ha ridondanza e alta disponibilità built-in. Sotto il cofano, ELB è in realtà diverse istanze che AWS gestisce, e il numero scala su e giù secondo il traffico. Non è il single point of failure che sembra a prima vista."*

ELB può bilanciare: **EC2 instances, container, Lambda functions**.

---

## Tipi di Load Balancer

### Confronto (dal PACKT Cap.14 e Dojo)

| Tipo | Protocollo | Routing | Quando usarlo |
|---|---|---|---|
| **ALB** | HTTP/HTTPS | Listener rules con priorità, **round robin** o **least outstanding requests** (Dojo) | Web app, microservizi, URL/host-based routing, WebSocket |
| **NLB** | TCP/UDP/TLS | **Flow hash algorithm** (protocol, source/dest IP, port, TCP sequence) — una connessione TCP resta sullo stesso target (Dojo) | Alto throughput, ultra-bassa latenza, **IP statici**, milioni di richieste/sec |
| **GWLB** | IP (Layer 3) | Per appliance di sicurezza di terze parti | Firewall, deep packet inspection, IDS/IPS (Dojo) |
| **CLB** | HTTP/HTTPS + TCP | Round robin (TCP), least outstanding requests (HTTP) | **Legacy** — AWS raccomanda di non usarlo (PACKT Cap.14) |

> **Tip esame (PACKT Cap.14)**: *"Per l'esame, il load balancer giusto molto probabilmente non sarà il CLB. I due differenziatori chiave tra ALB e NLB sono: protocolli supportati e supporto IP statici. HTTP/HTTPS → ALB. IP statici → NLB."*

### Target Groups e Listeners (dal PACKT)

**Target Groups**: gruppo di target (istanze, Lambda) a cui il LB invia traffico. Definisce anche gli health check — di default, ELB invia una richiesta ogni 30 secondi. Se il target è unhealthy, ELB smette di inviargli traffico.

**Listeners**: instradano le richieste secondo regole configurate. Ogni regola ha una priorità (numero più basso = priorità più alta).

### ELB Idle Timeout (dal Dojo)

Il Dojo spiega: *"Per ogni richiesta, il LB stabilisce due connessioni: una con il client e una con il target. L'idle timeout è il numero di secondi che una connessione deve inviare nuovi dati per restare attiva."*

- Default: **60 secondi** per ALB e CLB (modificabile fino a 4000 secondi)
- NLB: **350 secondi** (non modificabile)

> **Nota Dojo**: *"Se stai mantenendo una connessione attiva solo per aspettare una risposta da un processo lungo, dovresti considerare di refactorare l'applicazione per usare trasmissioni asincrone, o creare una pipeline per disaccoppiare la risposta dal load balancer."*

---

## Auto Scaling — Walkthrough Pratico di Kimiko

Kimiko mostra l'intero processo di Auto Scaling nella console con un demo live:

### Setup
1. **Crea una Launch Configuration**: scegli AMI (Ubuntu), instance type (t2.micro), storage (8 GB EBS), security group (SSH da anywhere)
2. **Crea un Auto Scaling Group**: usa la launch configuration, metti nel default VPC, scegli una subnet
3. **Configura la scaling policy**: scala dinamicamente tra **1 e 5 istanze**, basandosi su **average CPU utilization** con target del 5% (artificialmente basso per il demo) e warmup di 10 secondi

### Test Live
Kimiko si connette via SSH all'istanza e installa `stress`:
- Esegue `sudo stress --cpu 64 --timeout 20` per stressare la CPU
- Monitora nella console EC2 — dopo un po', nuove istanze vengono lanciate automaticamente
- *"Auto scaling davvero, davvero potente. E ricorda, quando la CPU torna sotto la soglia, le istanze extra verranno terminate automaticamente."*

> **Insight da Kimiko**: *"Puoi anche configurare notifiche SNS per essere avvisato degli eventi di auto scaling via email."*

---

## Health Checks — ELB vs Route 53 (dal Dojo)

Il Dojo confronta i due tipi di health check:

| Caratteristica | ELB Health Check | Route 53 Health Check |
|---|---|---|
| **Scopo** | Verifica se il target è disponibile per accettare traffico | Monitora lo stato del target di un record DNS |
| **Target** | Istanze, server, Lambda nel target group | EC2, server, servizi AWS con endpoint |
| **Azione su unhealthy** | Smette di inviare traffico al target | Può redirigere DNS verso un endpoint sano |

---

## ALB Listener Rule Conditions — In Profondità (dal Dojo)

Il Dojo descrive le condizioni che puoi aggiungere alle listener rules dell'ALB per creare routing avanzato sotto un singolo load balancer:

| Condizione | Cosa fa | Esempio |
|---|---|---|
| **host-header** | Routing basato sull'hostname (host-based routing). Supporta subdomini e top-level domain diversi | `api.example.com` → target group API, `www.example.com` → target group web |
| **path-pattern** | Routing basato sul path dell'URL (path-based routing). Case-sensitive | `/api/*` → target group API, `/images/*` → target group media |
| **http-header** | Routing basato su header HTTP (standard e custom). Case-insensitive | Header `X-Custom: mobile` → target group mobile |
| **http-request-method** | Routing basato sul metodo HTTP. Case-sensitive | `GET` → target group lettura, `POST` → target group scrittura |
| **query-string** | Routing basato su key/value nella query string. Case-insensitive | `?platform=mobile` → target group mobile |
| **source-ip** | Routing basato sull'IP sorgente (CIDR, IPv4 e IPv6) | IP interni → target group interno |

> **Nota Dojo**: *"Una listener rule può includere al massimo una condizione per host-header, http-request-method, path-pattern e source-ip; e una o più condizioni per http-header e query-string. Massimo 5 match evaluations per regola."*

---

## Health Checks — ELB vs Route 53 (dal Dojo)

Il Dojo confronta i due tipi di health check:

| Caratteristica | ELB Health Check | Route 53 Health Check |
|---|---|---|
| **Scopo** | Verifica se il target è disponibile per accettare traffico | Monitora lo stato del target di un record DNS |
| **Scope** | Target in multiple AZ ma **non cross-region** | Target **ovunque**, purché raggiungibili da Route 53 |
| **Frequenza** | Configurabile tra 5 e 300 secondi | Ogni 10 o 30 secondi |
| **Timeout** | Configurabile tra 2 e 60 secondi | Non configurabile |
| **Criterio healthy** | Soglia configurabile di check passati/falliti | Se >18% degli health checker riportano healthy → healthy |
| **Scopo primario** | HA e fault tolerance per i servizi | DNS failover routing |

> **Best practice Dojo**: *"Non c'è nessuna regola che dice che non puoi usare entrambi gli health check insieme. In effetti, è una pratica migliore usarli entrambi! ELB assicura che il traffico vada solo a target sani, Route 53 assicura che i record DNS puntino a endpoint raggiungibili."*

---

## Scenari Tipici d'Esame

### Scenario 1: Web app HTTP con routing per URL
**Domanda**: Un'applicazione web deve instradare `/api/*` a un set di server e `/static/*` a un altro.

**Risposta**: **ALB** con listener rules per URL-based routing (PACKT Cap.14).

### Scenario 2: Applicazione TCP con IP statici
**Domanda**: Un'applicazione richiede un load balancer con IP statici e supporto TCP.

**Risposta**: **NLB** — supporta TCP/UDP, fornisce IP statici (PACKT Cap.14, Dojo).

### Scenario 3: Scaling automatico su CPU
**Domanda**: L'applicazione deve scalare automaticamente quando la CPU supera il 70%.

**Risposta**: **Auto Scaling Group** con scaling policy basata su CPU utilization (Kimiko demo).

### Scenario 4: Connessioni lunghe al load balancer
**Domanda**: Le richieste al backend impiegano più di 60 secondi. Le connessioni vengono chiuse.

**Risposta**: Aumenta l'**idle timeout** dell'ALB (Dojo). Oppure refactora per comunicazione asincrona.

---

## Riepilogo Veloce per l'Esame

- **ALB**: HTTP/HTTPS, routing avanzato (URL/host), round robin o least outstanding requests (PACKT, Dojo)
- **NLB**: TCP/UDP/TLS, IP statici, ultra-bassa latenza, milioni req/sec, flow hash routing (PACKT, Dojo)
- **GWLB**: Layer 3, per appliance di sicurezza terze parti (Dojo)
- **CLB**: legacy, non usare (PACKT Cap.14)
- **HTTP → ALB, IP statici → NLB** (PACKT Cap.14)
- **Target Groups**: definiscono i target + health checks (ogni 30s default) (PACKT)
- **Listeners**: regole con priorità per instradamento (PACKT)
- **ELB è elastico e HA di default** — non è un single point of failure (PACKT)
- **Idle timeout**: 60s ALB/CLB (modificabile), 350s NLB (fisso) (Dojo)
- **ALB listener conditions**: host-header, path-pattern, http-header, http-request-method, query-string, source-ip (Dojo)
- **ELB health check**: 5-300s frequenza, scope multi-AZ. **Route 53 health check**: scope globale, DNS failover (Dojo)
- **Usa entrambi** ELB + Route 53 health check per massima resilienza (Dojo)
- **Launch template > launch configuration** per ASG (Dojo)
