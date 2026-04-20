# VPC Security - Security Groups, NACLs, VPC Endpoints

> Fonti: PACKT Cap.2 (p.119-127), PACKT Cap.12 (p.509-511), KIMIKO (p.208-224, p.282-285), DOJO (p.163-172)

---

## Cos'è un VPC

Come spiega il Dojo: *"Amazon VPC è una rete virtuale in cui server geograficamente distribuiti sono virtualmente connessi tra loro per formare una singola rete. Questa rete ha scope regionale — il tuo VPC può esistere solo all'interno di una Region AWS."*

Il Dojo chiarisce un punto importante sulla struttura fisica: un VPC non è limitato a un singolo data center. Può estendersi su più data center e Availability Zone all'interno di una Region. Una subnet deve risiedere interamente in una sola AZ, ma puoi avere più subnet nella stessa AZ.

Kimiko nel suo walkthrough pratico mostra i componenti del VPC nella console: subnets con indirizzi CIDR, route tables, Internet Gateway, egress-only Internet gateway, DHCP option sets, Elastic IP, NAT Gateways, Network ACLs e Security Groups. *"Tutti i componenti di networking cadono sotto il concetto di Virtual Private Cloud."*

### Default VPC vs Custom VPC (dal PACKT)

| Caratteristica | Default VPC | Custom VPC |
|---|---|---|
| Facilità d'uso | Pronto all'uso alla creazione dell'account; ideale per principianti | Richiede più setup iniziale e comprensione del networking AWS |
| Configurazione | Preconfigured con IP range, subnets, route tables, SG di default | Tu definisci ogni aspetto: IP ranges, subnets, route tables, SG |
| Sicurezza | Condiviso tra tutti gli account nella Region | Allineato alle tue policy di sicurezza e compliance |

> **Nota PACKT**: *"All production workloads should be placed in a custom VPC to ensure you maintain your security standards and controls."*

### Servizi che NON richiedono un VPC (dal Dojo)

Il Dojo elenca i servizi che non girano dentro un VPC:
1. **Amazon S3** — è una risorsa regionale, non può essere messa in una subnet
2. **Amazon DynamoDB**
3. **AWS Lambda** — anche se puoi configurare Lambda per connettersi a un VPC per accedere a risorse private

> Per connettere questi servizi al tuo VPC privatamente, usi **VPC Endpoints**.

---

## Security Groups (SG)

### Definizione e Caratteristiche

Il PACKT definisce i Security Groups come *"firewall stateful all'interno dei VPC AWS"*. Stateful significa che il SG ricorda che il traffico è stato autorizzato a passare in una direzione e quindi lascia passare la risposta nell'altra direzione — non devi definire regole speculari.

Kimiko spiega dove operano i SG con un esempio pratico nella console: *"Il security group si attacca alle network interface. Vai su un'istanza EC2, guarda i dettagli, trovi la virtual network interface, e lì vedi il security group assegnato."* Quindi il SG è un firewall stateful che si attacca alla network interface per controllare l'accesso in entrata e uscita dalla risorsa EC2.

| Proprietà | Dettaglio |
|---|---|
| Livello | Istanza (Network Interface / ENI) |
| Tipo | **Stateful** (PACKT, Kimiko) |
| Regole | Solo **Allow** — non puoi creare regole Deny |
| Default inbound | Tutto negato, tranne traffico da istanze con lo stesso SG di default (Dojo) |
| Default outbound | Tutto permesso (IPv4 e IPv6 se hai un CIDR IPv6) (Dojo) |
| Scope | Può agire su più subnet contemporaneamente (PACKT) |

### Stateful — Spiegazione Pratica (da Kimiko)

Kimiko lo spiega con chiarezza: *"Quando creiamo una regola inbound come permettere SSH sulla porta 22, non dobbiamo stressarci per la regola outbound appropriata perché sarà permessa automaticamente — il SG analizza il traffico in modo stateful."*

### SG di Default del VPC (dal Dojo)

Il Dojo specifica le regole del SG di default:
1. Permette traffico inbound **solo** da istanze assegnate allo stesso security group
2. Permette tutto il traffico outbound IPv4 (e IPv6 se applicabile)

### Hands-on: Configurazione SG nel Lab di Kimiko

Nel lab "Building a VPC", Kimiko mostra passo passo come configurare un SG:
1. Vai al SG di default del VPC creato (identificalo tramite le ultime cifre del VPC ID)
2. Aggiungi un nome tag (es. `SG_Sol_Arch`)
3. Modifica le inbound rules: permetti SSH da anywhere (`0.0.0.0/0`) e HTTPS da anywhere
4. *"In un ambiente di produzione, chiaramente non faresti questo. Dovresti limitare l'accesso al tuo management subnet. Ma nel lab, per testing, siamo pigri e permettiamo a tutti l'accesso SSH. Tieni presente che avranno comunque bisogno della key pair appropriata."*

---

## Network ACLs (NACLs)

### Definizione e Caratteristiche

Il PACKT definisce le NACLs come *"un livello aggiuntivo di sicurezza che opera a livello di subnet all'interno di un VPC AWS. Funzionano come filtri di pacchetti stateless, dando controllo granulare sul flusso di traffico in entrata e uscita dalle subnet."*

Kimiko spiega la differenza chiave: *"La NACL NON è stateful. Se permetti qualcosa inbound, assicurati di andare nell'outbound e permetterlo anche lì. Altrimenti, tipicamente avrai problemi."*

| Proprietà | Dettaglio |
|---|---|
| Livello | Subnet |
| Tipo | **Stateless** (PACKT, Kimiko) |
| Regole | **Allow e Deny** |
| Default | Permette tutto il traffico inbound e outbound (Dojo) |
| Regola asterisco | Ogni NACL include una regola non modificabile con numero `*` che nega tutto ciò che non matcha le altre regole (Dojo) |
| Valutazione | In ordine numerico (prima match vince) |

### NACL di Default (dal Dojo)

Il Dojo specifica:
1. Permette tutto il traffico inbound e outbound IPv4 (e IPv6 se applicabile)
2. Include una regola con numero asterisco (`*`) non modificabile e non rimovibile — se un pacchetto non matcha nessuna delle altre regole numerate, viene negato

### Uso Pratico delle NACLs (da Kimiko)

Kimiko mostra nella console che la NACL del suo VPC permette tutto il traffico inbound e outbound: *"Essenzialmente non sta facendo nulla. È associata a quelle subnet, ma non ha effetto restrittivo sul traffico. Ma tieni presente che sarebbe uno strumento molto prezioso da associare a subnet particolari per controllare i flussi di traffico."*

---

## Security Groups vs NACLs — Confronto

### Tabella dal PACKT

| Categoria | Security Groups | NACLs |
|---|---|---|
| **Scope** | Operano a livello di istanza, associati a singole istanze EC2. Controllano traffico inbound e outbound a livello di istanza | Operano a livello di subnet. Controllano traffico in entrata e uscita da intere subnet, influenzando tutte le istanze nella subnet |
| **Valutazione regole** | Stateful: se permetti traffico inbound da un IP specifico, il traffico outbound corrispondente è automaticamente permesso. Regole valutate indipendentemente per ogni istanza | Stateless: le regole sono valutate in base a criteri definiti, separatamente per inbound e outbound. Devono essere definite per entrambe le direzioni e valutate in ordine sequenziale |
| **Tipi di regole** | Permettono di specificare quali IP o altri SG possono comunicare con le istanze. Focus su allow/deny di sorgenti e destinazioni specifiche | Controllo fine-grained con regole basate su IP, range di porte e protocolli. Usate per requisiti di sicurezza di rete dettagliati |
| **Comportamento default** | Tutto il traffico inbound negato di default (tranne se esplicitamente permesso). Outbound permesso di default | Tutto il traffico inbound e outbound permesso di default. Regole custom devono essere create per restringere il traffico |

### Defense in Depth (da Kimiko)

Kimiko enfatizza il valore di usare entrambi insieme: *"Tra Network ACLs e Security Groups, possiamo davvero costruire quella che mi piace chiamare una strategia di defense in depth con le architetture AWS. Possiamo avere sicurezza fine-grained a più livelli dell'infrastruttura. Questo è sempre una grande idea perché ricorda, i criminali informatici cercheranno modi per entrare e vulnerabilità a vari livelli del modello OSI. Quando usiamo i diversi strumenti di sicurezza a più livelli, stiamo facendo una grande defense in depth. E molte volte l'attaccante si sposterà e cercherà qualche altro cliente AWS che non conosce le sue cose come te."*

### Uso Pratico dal PACKT Cap.12

Il PACKT (Cap.12) aggiunge un uso pratico delle NACLs: *"Customers can use NACLs to offer more precise controls and to provide a baseline that cannot be overridden by an SG. This is very useful for customers who have different teams working on VPC configuration, as using NACLs stops anyone from accidentally allowing wide access by misconfiguring an SG."*

> **Tip esame (PACKT Cap.12)**: *"A common question that can appear on the SAA-C03 exam is one that asks you to select the correct security group rule to accomplish a particular goal, so make sure you are familiar with the most common port numbers: 22 (SSH), 80 (HTTP), 443 (HTTPS), 3389 (RDP)."*

> **Tip esame (PACKT Cap.12)**: *"The CIDR notation 0.0.0.0/0 means everywhere. If you see this in an exam question or an answer, be careful. If the question states that they want the most secure rule, it is unlikely to be an answer containing 0.0.0.0/0."*

---

## NAT Gateway vs NAT Instance (dal Dojo)

Il Dojo fornisce un confronto dettagliato:

| Attributo | NAT Gateway | NAT Instance |
|---|---|---|
| **Disponibilità** | Altamente disponibile nella AZ in cui è creato. Per vera HA, crea un NAT GW in una public subnet per ogni private subnet/AZ ridondante | Non altamente disponibile. Serve uno script per gestire il failover |
| **Bandwidth** | Scala fino a 45 Gbps | Dipende dal tipo di istanza |
| **Manutenzione** | Gestito da AWS | Gestito da te (aggiornamenti software, patch OS) |
| **Costo** | Basato su numero di NAT GW, durata, e dati trasferiti | Basato su numero di istanze, durata, tipo/dimensione, storage. Può essere più economico |
| **Security Groups** | Non può essere associato a SG. Controlla traffico con NACLs | Può essere associato a uno o più SG |
| **Port forwarding** | Non supportato | Configurabile manualmente |
| **Bastion server** | Non supportato | Può essere usato come bastion server |

> **Nota Dojo**: *"Quando lanci un NAT Gateway o instance, devi metterli nelle public subnet, NON nelle private subnet. Sono letteralmente un gateway tra le tue public e private subnet."*

---

## VPC Endpoints (dal PACKT Cap.12 e Dojo)

Il Dojo spiega: *"Puoi configurare una connessione diretta per servizi come S3 e DynamoDB usando un VPC Endpoint. Questo permette connettività privata tra le tue istanze EC2 e altri servizi AWS senza che il traffico passi attraverso l'Internet pubblico."*

Il PACKT (Cap.12) è diretto: *"It is best practice to use VPC endpoints to connect to AWS services without your traffic leaving the AWS network to the public internet. This helps protect your network traffic."*

### Gateway Endpoint vs Interface Endpoint (dal PACKT Cap.12)

Il PACKT avverte: *"Remember that there are interface endpoints and gateway endpoints. Make sure you know the difference between the two as there is often a question that has both as options in the list of answers. If trying to connect to S3 or DynamoDB, it will be a gateway endpoint. If it is not one of those services, it will be an interface endpoint."*

| Tipo | Servizi | Costo | Come funziona |
|---|---|---|---|
| **Gateway Endpoint** | Solo **S3** e **DynamoDB** | Gratuito | Entry nella route table |
| **Interface Endpoint** | Quasi tutti gli altri servizi AWS | A pagamento | ENI con IP privato nella subnet |

---

## VPC Peering (dal Dojo)

Il Dojo descrive il VPC Peering come *"una soluzione comune per collegare due reti VPC insieme. La soluzione è semplice, efficace, e non costa nulla da configurare. Un altro vantaggio è che la connessione non è un single point of failure e non è un bottleneck di bandwidth."*

Passaggi per creare un VPC Peering (dal Dojo):
1. Nella console VPC, crea una peering request verso il VPC target
2. Indica se il target è nello stesso account o in un altro, e se nella stessa Region o no
3. **Il CIDR del target NON deve sovrapporsi** con il tuo VPC
4. Il VPC target accetta o rifiuta la richiesta
5. Se serve DNS resolution tra i due VPC, abilitala nelle impostazioni del peering
6. Una volta accettata, referenzia la connessione nelle route tables

### Transit Gateway (dal Dojo)

Il Dojo spiega quando usare Transit Gateway invece di VPC Peering: *"Con VPC Peering, puoi connettere solo due VPC insieme. Gestire multiple connessioni VPC Peering può essere molto problematico quando hai molti VPC interconnessi. Una soluzione migliore è usare AWS Transit Gateway. Richiede poco overhead di gestione e permette di creare soluzioni Site-to-Site VPN non possibili con VPC Peering."*

---

## Hands-on Challenge di Kimiko: Building a VPC

Kimiko propone una sfida pratica completa per costruire un VPC da zero:

1. **Crea un VPC** con nome tag `VPC_Solutions_Arch` e CIDR range `10.1.0.0/16`
2. **Crea una public subnet** con indirizzo `10.1.1.0/24` e nome tag specifico
3. **Crea un Internet Gateway** e attaccalo al VPC
4. **Crea una route table** con default route (`0.0.0.0/0`) che punta all'Internet Gateway
5. **Associa la subnet** alla route table
6. **Modifica il SG di default**: permetti SSH e HTTPS inbound da anywhere
7. **Lancia un'istanza Amazon Linux 2** nella subnet
8. **Testa la connettività** — se riesci a fare SSH all'istanza, hai completato la sfida
9. **Cancella tutte le risorse** create

> **Insight da Kimiko**: *"C'è un VPC creation wizard, ma una delle sfide che ho con quel wizard è che spesso ci scherma dai dettagli interni del VPC. E questo è problematico perché se ci facciamo schermare dai dettagli, molte volte non capiamo completamente i componenti funzionanti."*

> **Nota da Kimiko**: *"Questa è l'area dove vediamo la maggior parte delle domande di supporto tecnico riguardo AWS che non funziona correttamente. Così spesso è che lo studente o l'utente non capisce completamente i concetti di security group e network ACL."*

---

## Application Network Security (dal PACKT Cap.12)

Il PACKT Cap.12 riassume le best practice per la sicurezza di rete delle applicazioni:

- **Public subnet** per risorse public-facing (web frontend)
- **Private subnet** per risorse con dati (database, app server)
- **Internet Gateway vs NAT Gateway**: assicurati di capire la differenza
- **Direct Connect**: NON è cifrato di default. Puoi usare MACsec encryption o creare un tunnel VPN cifrato con IPsec. *"Direct Connect can take several months to implement, so if there is a requirement for the fastest possible solution, Direct Connect will not be the correct answer."*
- **VPC Endpoints**: best practice per connettersi a servizi AWS senza uscire dalla rete AWS

### Aggiungere CIDR Blocks al VPC (dal Dojo)

Il Dojo spiega che puoi espandere il tuo VPC aggiungendo CIDR blocks IPv4. Restrizioni da ricordare:
- Il CIDR block **non deve sovrapporsi** con CIDR esistenti nel VPC
- La dimensione permessa è tra `/28` e `/16`
- **Non puoi aumentare o diminuire** la dimensione di un CIDR block esistente
- Puoi dissociare CIDR secondari, ma **non puoi dissociare il CIDR primario**

---

## Scenari Tipici d'Esame

### Scenario 1: Bloccare un IP malevolo
**Domanda**: Un IP specifico sta attaccando le tue istanze. Come bloccarlo?

**Risposta**: Aggiungi una regola **Deny** nella **NACL** della subnet. I Security Groups non supportano regole Deny. (Concetto da PACKT e Kimiko)

### Scenario 2: Connettere EC2 a S3 privatamente
**Domanda**: Le istanze EC2 in una subnet privata devono accedere a S3 senza passare da internet.

**Risposta**: Crea un **Gateway Endpoint** per S3 (PACKT Cap.12: *"If trying to connect to S3 or DynamoDB, it will be a gateway endpoint"*).

### Scenario 3: Connettere molti VPC tra loro
**Domanda**: Hai 15 VPC che devono comunicare tra loro. Come gestire le connessioni?

**Risposta**: **Transit Gateway** (Dojo: *"Managing multiple VPC Peering connections can be very troublesome. A better solution would be to use AWS Transit Gateway."*)

### Scenario 4: Soluzione di connettività veloce
**Domanda**: Serve connettività tra on-premises e AWS il più velocemente possibile.

**Risposta**: **VPN** (non Direct Connect). PACKT Cap.12: *"Direct Connect can take several months to implement, so if there is a requirement for the fastest possible solution, Direct Connect will not be the correct answer."*

---

## Riepilogo Veloce per l'Esame

- **Security Groups**: stateful, solo Allow, a livello di istanza/ENI (PACKT, Kimiko)
- **NACLs**: stateless, Allow e Deny, a livello di subnet, ordine numerico (PACKT, Kimiko)
- **Bloccare un IP** → NACL (unico modo per fare Deny)
- **Defense in depth**: SG + NACL insieme per sicurezza a più livelli (Kimiko)
- **Porte da ricordare**: 22 (SSH), 80 (HTTP), 443 (HTTPS), 3389 (RDP) (PACKT Cap.12)
- **0.0.0.0/0 = everywhere**: se la domanda chiede "most secure", probabilmente non è la risposta (PACKT Cap.12)
- **Gateway Endpoint**: gratuito, solo S3 e DynamoDB (PACKT Cap.12)
- **Interface Endpoint**: a pagamento, quasi tutti gli altri servizi (PACKT Cap.12)
- **NAT Gateway**: managed, HA, fino a 45 Gbps, no SG. **NAT Instance**: self-managed, più economico, supporta SG e bastion (Dojo)
- **VPC Peering**: gratuito, solo 2 VPC, CIDR non devono sovrapporsi (Dojo)
- **Transit Gateway**: per molti VPC interconnessi, meno overhead (Dojo)
- **Direct Connect**: non cifrato di default, mesi per implementare (PACKT Cap.12)
- **Public subnet** per web, **private subnet** per dati (PACKT Cap.12)
