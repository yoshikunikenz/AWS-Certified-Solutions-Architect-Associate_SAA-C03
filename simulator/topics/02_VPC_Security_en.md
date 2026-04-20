# VPC Security - Security Groups, NACLs, VPC Endpoints

> Sources: PACKT Ch.2 (p.119-127), PACKT Ch.12 (p.509-511), KIMIKO (p.208-224, p.282-285), DOJO (p.163-172)

---

## What is a VPC

As the Dojo explains: *"Amazon VPC è una rete virtuale in cui server geograficamente distribuiti sono virtualmente connessi tra loro per formare una singola rete. Questa rete ha scope regionale — il tuo VPC può esistere solo all'interno di una Region AWS."*

The Dojo clarifies an important point about the physical structure: a VPC is not limited to a single data center. It can span multiple data centers and Availability Zones within a Region. A subnet must reside entirely in a single AZ, but you can have multiple subnets in the same AZ.

Kimiko in her hands-on walkthrough shows the VPC components in the console: subnets with CIDR addresses, route tables, Internet Gateway, egress-only Internet gateway, DHCP option sets, Elastic IP, NAT Gateways, Network ACLs and Security Groups. *"Tutti i componenti di networking cadono sotto il concetto di Virtual Private Cloud."*

### Default VPC vs Custom VPC (from PACKT)

| Feature | Default VPC | Custom VPC |
|---|---|---|
| Ease of use | Ready to use at account creation; ideal for beginners | Requires more initial setup and understanding of AWS networking |
| Configuration | Preconfigured with IP range, subnets, route tables, default SG | You define every aspect: IP ranges, subnets, route tables, SG |
| Security | Shared among all accounts in the Region | Aligned with your security and compliance policies |

> **PACKT Note**: *"All production workloads should be placed in a custom VPC to ensure you maintain your security standards and controls."*

### Services that DO NOT Require a VPC (from Dojo)

The Dojo lists services that do not run inside a VPC:
1. **Amazon S3** — it is a regional resource, it cannot be placed in a subnet
2. **Amazon DynamoDB**
3. **AWS Lambda** — although you can configure Lambda to connect to a VPC to access private resources

> To connect these services to your VPC privately, you use **VPC Endpoints**.

---

## Security Groups (SG)

### Definition and Characteristics

PACKT defines Security Groups as *"firewall stateful all'interno dei VPC AWS"*. Stateful means the SG remembers that traffic was authorized to pass in one direction and therefore allows the response in the other direction — you don't need to define mirror rules.

Kimiko explains where SGs operate with a hands-on example in the console: *"Il security group si attacca alle network interface. Vai su un'istanza EC2, guarda i dettagli, trovi la virtual network interface, e lì vedi il security group assegnato."* So the SG is a stateful firewall that attaches to the network interface to control inbound and outbound access to the EC2 resource.

| Property | Detail |
|---|---|
| Level | Instance (Network Interface / ENI) |
| Type | **Stateful** (PACKT, Kimiko) |
| Rules | **Allow** only — you cannot create Deny rules |
| Default inbound | All denied, except traffic from instances with the same default SG (Dojo) |
| Default outbound | All allowed (IPv4 and IPv6 if you have an IPv6 CIDR) (Dojo) |
| Scope | Can act across multiple subnets simultaneously (PACKT) |

### Stateful — Practical Explanation (from Kimiko)

Kimiko explains it clearly: *"Quando creiamo una regola inbound come permettere SSH sulla porta 22, non dobbiamo stressarci per la regola outbound appropriata perché sarà permessa automaticamente — il SG analizza il traffico in modo stateful."*

### Default VPC Security Group (from Dojo)

The Dojo specifies the default SG rules:
1. Allows inbound traffic **only** from instances assigned to the same security group
2. Allows all outbound IPv4 traffic (and IPv6 if applicable)

### Hands-on: SG Configuration in Kimiko's Lab

In the "Building a VPC" lab, Kimiko shows step by step how to configure a SG:
1. Go to the default SG of the created VPC (identify it by the last digits of the VPC ID)
2. Add a name tag (e.g. `SG_Sol_Arch`)
3. Edit the inbound rules: allow SSH from anywhere (`0.0.0.0/0`) and HTTPS from anywhere
4. *"In un ambiente di produzione, chiaramente non faresti questo. Dovresti limitare l'accesso al tuo management subnet. Ma nel lab, per testing, siamo pigri e permettiamo a tutti l'accesso SSH. Tieni presente che avranno comunque bisogno della key pair appropriata."*

---

## Network ACLs (NACLs)

### Definition and Characteristics

PACKT defines NACLs as *"un livello aggiuntivo di sicurezza che opera a livello di subnet all'interno di un VPC AWS. Funzionano come filtri di pacchetti stateless, dando controllo granulare sul flusso di traffico in entrata e uscita dalle subnet."*

Kimiko explains the key difference: *"La NACL NON è stateful. Se permetti qualcosa inbound, assicurati di andare nell'outbound e permetterlo anche lì. Altrimenti, tipicamente avrai problemi."*

| Property | Detail |
|---|---|
| Level | Subnet |
| Type | **Stateless** (PACKT, Kimiko) |
| Rules | **Allow and Deny** |
| Default | Allows all inbound and outbound traffic (Dojo) |
| Asterisk rule | Every NACL includes a non-modifiable rule numbered `*` that denies everything that doesn't match the other rules (Dojo) |
| Evaluation | In numerical order (first match wins) |

### Default NACL (from Dojo)

The Dojo specifies:
1. Allows all inbound and outbound IPv4 traffic (and IPv6 if applicable)
2. Includes a rule numbered asterisk (`*`) that is non-modifiable and non-removable — if a packet doesn't match any of the other numbered rules, it is denied

### Practical Use of NACLs (from Kimiko)

Kimiko shows in the console that her VPC's NACL allows all inbound and outbound traffic: *"Essenzialmente non sta facendo nulla. È associata a quelle subnet, ma non ha effetto restrittivo sul traffico. Ma tieni presente che sarebbe uno strumento molto prezioso da associare a subnet particolari per controllare i flussi di traffico."*

---

## Security Groups vs NACLs — Comparison

### Table from PACKT

| Category | Security Groups | NACLs |
|---|---|---|
| **Scope** | Operate at instance level, associated with individual EC2 instances. Control inbound and outbound traffic at instance level | Operate at subnet level. Control inbound and outbound traffic for entire subnets, affecting all instances in the subnet |
| **Rule evaluation** | Stateful: if you allow inbound traffic from a specific IP, the corresponding outbound traffic is automatically allowed. Rules evaluated independently for each instance | Stateless: rules are evaluated based on defined criteria, separately for inbound and outbound. Must be defined for both directions and evaluated in sequential order |
| **Rule types** | Allow specifying which IPs or other SGs can communicate with instances. Focus on allow/deny of specific sources and destinations | Fine-grained control with rules based on IP, port ranges and protocols. Used for detailed network security requirements |
| **Default behavior** | All inbound traffic denied by default (unless explicitly allowed). Outbound allowed by default | All inbound and outbound traffic allowed by default. Custom rules must be created to restrict traffic |

### Defense in Depth (from Kimiko)

Kimiko emphasizes the value of using both together: *"Tra Network ACLs e Security Groups, possiamo davvero costruire quella che mi piace chiamare una strategia di defense in depth con le architetture AWS. Possiamo avere sicurezza fine-grained a più livelli dell'infrastruttura. Questo è sempre una grande idea perché ricorda, i criminali informatici cercheranno modi per entrare e vulnerabilità a vari livelli del modello OSI. Quando usiamo i diversi strumenti di sicurezza a più livelli, stiamo facendo una grande defense in depth. E molte volte l'attaccante si sposterà e cercherà qualche altro cliente AWS che non conosce le sue cose come te."*

### Practical Use from PACKT Ch.12

PACKT (Ch.12) adds a practical use of NACLs: *"Customers can use NACLs to offer more precise controls and to provide a baseline that cannot be overridden by an SG. This is very useful for customers who have different teams working on VPC configuration, as using NACLs stops anyone from accidentally allowing wide access by misconfiguring an SG."*

> **Exam tip (PACKT Ch.12)**: *"A common question that can appear on the SAA-C03 exam is one that asks you to select the correct security group rule to accomplish a particular goal, so make sure you are familiar with the most common port numbers: 22 (SSH), 80 (HTTP), 443 (HTTPS), 3389 (RDP)."*

> **Exam tip (PACKT Ch.12)**: *"The CIDR notation 0.0.0.0/0 means everywhere. If you see this in an exam question or an answer, be careful. If the question states that they want the most secure rule, it is unlikely to be an answer containing 0.0.0.0/0."*

---

## NAT Gateway vs NAT Instance (from Dojo)

The Dojo provides a detailed comparison:

| Attribute | NAT Gateway | NAT Instance |
|---|---|---|
| **Availability** | Highly available in the AZ where it is created. For true HA, create a NAT GW in a public subnet for each redundant private subnet/AZ | Not highly available. A script is needed to handle failover |
| **Bandwidth** | Scales up to 45 Gbps | Depends on instance type |
| **Maintenance** | Managed by AWS | Managed by you (software updates, OS patches) |
| **Cost** | Based on number of NAT GWs, duration, and data transferred | Based on number of instances, duration, type/size, storage. Can be cheaper |
| **Security Groups** | Cannot be associated with SG. Control traffic with NACLs | Can be associated with one or more SGs |
| **Port forwarding** | Not supported | Manually configurable |
| **Bastion server** | Not supported | Can be used as a bastion server |

> **Dojo Note**: *"Quando lanci un NAT Gateway o instance, devi metterli nelle public subnet, NON nelle private subnet. Sono letteralmente un gateway tra le tue public e private subnet."*

---

## VPC Endpoints (from PACKT Ch.12 and Dojo)

The Dojo explains: *"Puoi configurare una connessione diretta per servizi come S3 e DynamoDB usando un VPC Endpoint. Questo permette connettività privata tra le tue istanze EC2 e altri servizi AWS senza che il traffico passi attraverso l'Internet pubblico."*

PACKT (Ch.12) is direct: *"It is best practice to use VPC endpoints to connect to AWS services without your traffic leaving the AWS network to the public internet. This helps protect your network traffic."*

### Gateway Endpoint vs Interface Endpoint (from PACKT Ch.12)

PACKT warns: *"Remember that there are interface endpoints and gateway endpoints. Make sure you know the difference between the two as there is often a question that has both as options in the list of answers. If trying to connect to S3 or DynamoDB, it will be a gateway endpoint. If it is not one of those services, it will be an interface endpoint."*

| Type | Services | Cost | How it works |
|---|---|---|---|
| **Gateway Endpoint** | Only **S3** and **DynamoDB** | Free | Entry in the route table |
| **Interface Endpoint** | Almost all other AWS services | Paid | ENI with private IP in the subnet |

---

## VPC Peering (from Dojo)

The Dojo describes VPC Peering as *"una soluzione comune per collegare due reti VPC insieme. La soluzione è semplice, efficace, e non costa nulla da configurare. Un altro vantaggio è che la connessione non è un single point of failure e non è un bottleneck di bandwidth."*

Steps to create a VPC Peering (from Dojo):
1. In the VPC console, create a peering request to the target VPC
2. Indicate whether the target is in the same account or another, and whether in the same Region or not
3. **The target CIDR must NOT overlap** with your VPC
4. The target VPC accepts or rejects the request
5. If DNS resolution between the two VPCs is needed, enable it in the peering settings
6. Once accepted, reference the connection in the route tables

### Transit Gateway (from Dojo)

The Dojo explains when to use Transit Gateway instead of VPC Peering: *"Con VPC Peering, puoi connettere solo due VPC insieme. Gestire multiple connessioni VPC Peering può essere molto problematico quando hai molti VPC interconnessi. Una soluzione migliore è usare AWS Transit Gateway. Richiede poco overhead di gestione e permette di creare soluzioni Site-to-Site VPN non possibili con VPC Peering."*

---

## Kimiko's Hands-on Challenge: Building a VPC

Kimiko proposes a complete hands-on challenge to build a VPC from scratch:

1. **Create a VPC** with name tag `VPC_Solutions_Arch` and CIDR range `10.1.0.0/16`
2. **Create a public subnet** with address `10.1.1.0/24` and a specific name tag
3. **Create an Internet Gateway** and attach it to the VPC
4. **Create a route table** with a default route (`0.0.0.0/0`) pointing to the Internet Gateway
5. **Associate the subnet** with the route table
6. **Modify the default SG**: allow SSH and HTTPS inbound from anywhere
7. **Launch an Amazon Linux 2 instance** in the subnet
8. **Test connectivity** — if you can SSH into the instance, you've completed the challenge
9. **Delete all created resources**

> **Insight from Kimiko**: *"C'è un VPC creation wizard, ma una delle sfide che ho con quel wizard è che spesso ci scherma dai dettagli interni del VPC. E questo è problematico perché se ci facciamo schermare dai dettagli, molte volte non capiamo completamente i componenti funzionanti."*

> **Note from Kimiko**: *"Questa è l'area dove vediamo la maggior parte delle domande di supporto tecnico riguardo AWS che non funziona correttamente. Così spesso è che lo studente o l'utente non capisce completamente i concetti di security group e network ACL."*

---

## Application Network Security (from PACKT Ch.12)

PACKT Ch.12 summarizes best practices for application network security:

- **Public subnet** for public-facing resources (web frontend)
- **Private subnet** for resources with data (database, app server)
- **Internet Gateway vs NAT Gateway**: make sure you understand the difference
- **Direct Connect**: NOT encrypted by default. You can use MACsec encryption or create an encrypted VPN tunnel with IPsec. *"Direct Connect can take several months to implement, so if there is a requirement for the fastest possible solution, Direct Connect will not be the correct answer."*
- **VPC Endpoints**: best practice for connecting to AWS services without leaving the AWS network

### Adding CIDR Blocks to the VPC (from Dojo)

The Dojo explains that you can expand your VPC by adding IPv4 CIDR blocks. Restrictions to remember:
- The CIDR block **must not overlap** with existing CIDRs in the VPC
- The allowed size is between `/28` and `/16`
- **You cannot increase or decrease** the size of an existing CIDR block
- You can disassociate secondary CIDRs, but **you cannot disassociate the primary CIDR**

---

## Typical Exam Scenarios

### Scenario 1: Block a Malicious IP
**Question**: A specific IP is attacking your instances. How do you block it?

**Answer**: Add a **Deny** rule in the subnet's **NACL**. Security Groups do not support Deny rules. (Concept from PACKT and Kimiko)

### Scenario 2: Connect EC2 to S3 Privately
**Question**: EC2 instances in a private subnet need to access S3 without going through the internet.

**Answer**: Create a **Gateway Endpoint** for S3 (PACKT Ch.12: *"If trying to connect to S3 or DynamoDB, it will be a gateway endpoint"*).

### Scenario 3: Connect Many VPCs Together
**Question**: You have 15 VPCs that need to communicate with each other. How do you manage the connections?

**Answer**: **Transit Gateway** (Dojo: *"Managing multiple VPC Peering connections can be very troublesome. A better solution would be to use AWS Transit Gateway."*)

### Scenario 4: Fast Connectivity Solution
**Question**: You need connectivity between on-premises and AWS as quickly as possible.

**Answer**: **VPN** (not Direct Connect). PACKT Ch.12: *"Direct Connect can take several months to implement, so if there is a requirement for the fastest possible solution, Direct Connect will not be the correct answer."*

---

## Quick Recap for the Exam

- **Security Groups**: stateful, Allow only, at instance/ENI level (PACKT, Kimiko)
- **NACLs**: stateless, Allow and Deny, at subnet level, numerical order (PACKT, Kimiko)
- **Block an IP** → NACL (only way to Deny)
- **Defense in depth**: SG + NACL together for multi-layer security (Kimiko)
- **Ports to remember**: 22 (SSH), 80 (HTTP), 443 (HTTPS), 3389 (RDP) (PACKT Ch.12)
- **0.0.0.0/0 = everywhere**: if the question asks "most secure", it's probably not the answer (PACKT Ch.12)
- **Gateway Endpoint**: free, S3 and DynamoDB only (PACKT Ch.12)
- **Interface Endpoint**: paid, almost all other services (PACKT Ch.12)
- **NAT Gateway**: managed, HA, up to 45 Gbps, no SG. **NAT Instance**: self-managed, cheaper, supports SG and bastion (Dojo)
- **VPC Peering**: free, only 2 VPCs, CIDRs must not overlap (Dojo)
- **Transit Gateway**: for many interconnected VPCs, less overhead (Dojo)
- **Direct Connect**: not encrypted by default, months to implement (PACKT Ch.12)
- **Public subnet** for web, **private subnet** for data (PACKT Ch.12)
