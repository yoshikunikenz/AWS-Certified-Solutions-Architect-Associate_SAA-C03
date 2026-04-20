# WAF, Shield and Network Firewall

> Sources: PACKT Ch.10 (p.455-458), PACKT Ch.12 (p.507-509), KIMIKO (p.286-291), DOJO (p.215-216, p.281)

---

## AWS WAF — Web Application Firewall

### Overview

PACKT describes WAF as *"un servizio di web application firewall che aiuta a proteggere le applicazioni web e le API da attacchi web comuni. È progettato per fornire una soluzione di sicurezza completa per chiunque ospiti le proprie applicazioni web sul cloud AWS."*

The Dojo adds: *"Puoi usare AWS WAF per creare regole custom che bloccano pattern di attacco comuni, come SQL injection e attacchi cross-site scripting."*

### What It Protects

Kimiko explains it in her walkthrough: *"Configuriamo WAF per proteggere le nostre CloudFront distributions, Application Load Balancers e/o Amazon API Gateways."*

The Dojo confirms the integration: WAF is tightly integrated with **Amazon CloudFront, Application Load Balancer (ALB), Amazon API Gateway and AWS AppSync**.

### Pricing (from Kimiko)

Kimiko shows the pricing in the console and comments on it: *"Che esempio incredibilmente granulare di pricing con AWS. Nella vita reale, in ambienti on-premises tradizionali, potremmo dover spendere centinaia di migliaia di dollari per equipaggiamento upfront per avere questo livello di protezione."*

- $5 per Web ACL per month (prorated hourly)
- $1 per rule per month
- $0.60 per million requests processed

### Rule Statements (from Dojo)

The Dojo provides the complete table of available match statements:

| Match Statement | Use case |
|---|---|
| **Geographic match** | Allow or block web requests based on country of origin. If you use CloudFront's geo restriction to block a country, requests from that country are blocked and not forwarded to WAF |
| **IP set match** | Inspect the IP of a request against a set of IPs and ranges you want to allow or block |
| **Label match** | Inspect the request for labels added by other rules in the same Web ACL |
| **Regex pattern set** | Match regex patterns against a specific component of the web request |
| **Size constraint** | Compare the size of a request component against a constraint in bytes |
| **SQLi attack** | Inspect for malicious SQL code in a web request |
| **String match** | Search for a matching string in a web request component |
| **XSS scripting attack** | Inspect for cross-site scripting attacks in a web request |
| **Rate-based** | Track the rate of requests from each source IP and trigger an action on IPs that exceed a limit. You can use this rule type to place a temporary block on requests from an IP that sends excessive requests |

### Kimiko's Hands-on Walkthrough: Creating a Web ACL

Kimiko shows the process in the console:
1. Create a Web ACL with a name and CloudWatch metric name
2. Select the Region (e.g. US East)
3. Add rules — you can create your own or use **managed rule groups**
4. Kimiko chooses the AWS **Core Rule Set**: *"Generalmente applicabile alle applicazioni web. Fornisce protezione contro lo sfruttamento di un'ampia gamma di vulnerabilità, incluse quelle descritte nelle pubblicazioni OWASP."*
5. Note the **capacity**: you cannot exceed 1500 Web ACL Rule Capacity Units
6. The default action for requests that don't match any rule: **Allow**
7. Associate AWS resources (CloudFront distributions, API Gateways, ALB)

> **Note from Kimiko**: *"C'è ancora il WAF Classic disponibile, ma non riesco a immaginare di usarlo alla luce del nuovo e migliorato Web Application Firewall."*

---

## AWS Shield

### Shield Standard vs Shield Advanced

PACKT explains: *"AWS Shield offre due livelli di servizio: AWS Shield Standard è fornito senza costi aggiuntivi a tutti i clienti AWS e offre protezione base contro attacchi DDoS, mentre AWS Shield Advanced fornisce capacità di mitigazione DDoS più complete, incluso accesso a team dedicati di risposta DDoS e analytics avanzate, per un canone mensile."*

Kimiko adds from the console: *"AWS Shield Standard è la protezione DDoS distribuita che viene fatta contro il tuo account automaticamente. Stai già ottenendo quel beneficio automaticamente. Ma per $3,000 al mese più costi aggiuntivi di data transfer, puoi attivare AWS Shield Advanced, che ti darà feature molto più granulari, più supporto e più visibilità nella protezione DDoS."*

### Complete Comparison (from Dojo)

| Feature | AWS WAF | AWS Shield Basic | AWS Shield Advanced |
|---|---|---|---|
| **Protection** | Monitors HTTP/HTTPS requests. Protects from SQL injection, XSS, rate-limiting, bad bots | Protection against common L3/L4 attacks (SYN/UDP floods, reflection attacks, DDoS). Works with IPv4 and IPv6 | Additional protections against more sophisticated and larger attacks. Near real-time notifications of suspected DDoS incidents. Advanced mitigation techniques and routing |
| **Integration** | CloudFront, ALB, API Gateway, AppSync | Most AWS resources are automatically integrated and protected | EC2, ELB, CloudFront, Global Accelerator, Route 53 |
| **Pricing** | Based on number of Web ACLs, rules per ACL, and web requests received | Free, automatically enabled for all AWS customers | $3,000/month per organization + data transfer costs for protected resources |
| **DDoS Response Team** | No | No | Yes (with Business or Enterprise support plan) |

### DDoS Protection — Strategies (from PACKT Ch.12)

PACKT Ch.12 lists strategies for protecting against DDoS:

1. **Scalable architectures**: *"Il motivo principale per cui DDoS ha successo è che l'applicazione si blocca quando le sue risorse sono completamente utilizzate. Se la tua applicazione è scalabile, può scalare per soddisfare la domanda inaspettata."* Caveat: it can be incredibly expensive. Put guardrails to limit how much the infrastructure can scale. Use Route 53 for failover and CloudFront to distribute traffic.

2. **AWS Shield Standard**: *"Automaticamente abilitato per tutti i clienti AWS senza costi aggiuntivi. Mitiga attacchi DDoS base e comuni facendo scrubbing di pacchetti malevoli e attività di scaling."*

3. **Block malicious traffic**: AWS Network Firewall and AWS WAF

> **Exam tip (PACKT Ch.12)**: *"Make sure you understand the difference between each of the security services. Learn which ones can actually perform mitigations and which ones are more about detection."*

### SQL Injection (from PACKT Ch.12)

PACKT Ch.12 explains: *"SQL injection funziona inviando una query SQL malevola al tuo database backend tramite il frontend web. Nel peggiore dei casi, può risultare nella perdita del tuo database."*

Protections:
1. **Sanitize inputs** — check query length, special characters, wildcards (good practice but unlikely on the exam)
2. **AWS WAF** — *"WAF allows you to create match conditions to identify malicious SQL code. This will likely be the correct answer for any question asking about the right way to prevent SQL injection in the exam."*

---

## AWS Firewall Manager (from Kimiko)

Kimiko shows Firewall Manager in the console: *"Una grande idea da Amazon per darci gestione centralizzata di tutte quelle regole firewall che potrebbero essere sparse nei nostri diversi account e nelle nostre diverse applicazioni."*

Cost: **$100/month per policy** configured for centralized management.

Prerequisites (from Kimiko):
1. The account must be a member of **AWS Organizations** ✓
2. The account must be the **AWS Firewall Manager administrator**
3. **AWS Config** must be configured for the account/region

> **Note from Kimiko**: *"Il Firewall Manager dipende direttamente da AWS Organizations, AWS Config e l'account administrator appropriato. Devi soddisfare tutte e tre le condizioni."*

---

## Key Exam Tips

### WAF vs Shield — How to Choose (from PACKT)

PACKT provides an explicit exam note:

> *"When deciding between Shield or WAF as the correct answer, look for whether the question is specifically asking for DDoS protection. If yes, Shield is probably the correct answer. If the question is more concerned about things such as SQL injection or XSS, then WAF is likely to be the correct answer. In reality, though, both should be used to provide a holistic security approach."*

### Kimiko's Insight on Cloud Security

Kimiko concludes with an important reflection: *"Quando sento panico riguardo alla sicurezza con un passaggio al cloud pubblico come AWS, certo, dobbiamo essere preoccupati per la sicurezza, ma se facciamo i compiti, se impariamo a usare questi strumenti, se li configuriamo correttamente, scommetto che quando guardiamo di nuovo attentamente le nostre architetture, scopriremo che abbiamo guadagnato molto in sicurezza. Non abbiamo perso nell'area della sicurezza, abbiamo guadagnato parecchio."*

---

## Typical Exam Scenarios

### Scenario 1: SQL Injection Protection
**Question**: The web application is vulnerable to SQL injection. How do you protect it?

**Answer**: **AWS WAF** with match conditions to identify malicious SQL code (PACKT Ch.12: *"This will likely be the correct answer for any question asking about the right way to prevent SQL injection"*).

### Scenario 2: DDoS Attack
**Question**: The application is under a DDoS attack. How do you protect it?

**Answer**: **Shield** for DDoS (PACKT: *"If the question is specifically asking for DDoS protection, Shield is probably the correct answer"*). Shield Standard is already active for free. For advanced protection with DRT: Shield Advanced.

### Scenario 3: Rate Limit Requests per IP
**Question**: A bot is making too many requests to your API.

**Answer**: **WAF with rate-based rule** (Dojo: *"Tracks the rate of requests of each originating IP addresses, and triggers a rule action on IPs with rates that go over a limit"*).

### Scenario 4: Block Traffic from a Specific Country
**Question**: The application must be accessible only from Italy.

**Answer**: **WAF with geographic match** (Dojo: *"Allows you to allow or block web requests based on country of origin"*).

### Scenario 5: Centralized Rule Management Across Multiple Accounts
**Question**: The organization has 50 AWS accounts and wants to apply the same WAF rules to all of them.

**Answer**: **AWS Firewall Manager** (Kimiko: centralized management, requires Organizations + Config + admin account).

---

## Quick Recap for the Exam

- **WAF**: Layer 7 protection (SQLi, XSS, bot, rate limiting), works with ALB/CloudFront/API GW/AppSync (PACKT, Dojo)
- **Shield Standard**: free, automatic for everyone, basic L3/L4 DDoS protection (PACKT, Kimiko)
- **Shield Advanced**: $3,000/month, DRT, near real-time notifications, advanced mitigation (Dojo, Kimiko)
- **WAF pricing**: $5/Web ACL + $1/rule + $0.60/million requests (Kimiko)
- **DDoS → Shield, SQLi/XSS → WAF** (PACKT exam note)
- **Rate-based rules**: to limit requests per IP, anti-DDoS L7, anti-bot (Dojo)
- **Geo match**: to block/allow traffic by country (Dojo)
- **Core Rule Set**: OWASP protection out-of-the-box (Kimiko)
- **Firewall Manager**: centralized multi-account management, requires Organizations + Config (Kimiko)
- **Both WAF + Shield** for a holistic security approach (PACKT)
