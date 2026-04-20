# AWS Organizations and Multi-Account Strategy

> Sources: PACKT Ch.11 (p.466-472), KIMIKO (p.301-302)

---

## Why Multi-Account?

PACKT explains the context: *"Man mano che ti allontani da una piccola piattaforma AWS verso una più grande, probabilmente avrai diversi account da gestire. Magari stai centralizzando i log in un account, o magari hai un account per tutto il networking ingress e egress. Man mano che guadagni più account, applicare controlli diventa complesso."*

---

## AWS Organizations (from PACKT)

PACKT describes Organizations as the service for *"creare e gestire più account AWS, configurare policy organizzative e controllare l'accesso alle risorse AWS."*

### Organizational Structure

Accounts are structured into **Organizational Units (OU)**. PACKT explains: *"Le OU ti permettono di raggruppare i tuoi account secondo funzioni di business, team, o qualsiasi struttura logica abbia senso per la tua piattaforma."*

PACKT provides a visual example of the structure:

```
Root Account (management + consolidated billing)
│
├── OU: Security
│   ├── Account: Audit
│   └── Account: Log Archive
│
└── OU: Workload
    ├── OU: Project X
    │   ├── Account: ...
    │   └── Account: ...
    └── OU: Project Y
        └── Account: ...
```

Important limits (from PACKT):
- You can nest OUs up to **5 levels** deep
- Maximum **1,000 OUs** per organization
- Default limit of **10 accounts** (soft limit, can be increased to thousands)

### Consolidated Billing (from Kimiko)

Kimiko explains the problem that Organizations solves: *"Per molto tempo c'era una sfida con AWS, nell'area del billing. Potevi ritrovarti con un sacco di account AWS diversi nella tua azienda, e non c'era un modo facile per configurare il consolidated billing in self-service."*

Kimiko shows the process: *"Vai in AWS Organizations con il tuo root account — vuoi essere il main account dell'organizzazione. Poi invii inviti agli altri indirizzi email che rappresentano gli altri root account. Riceveranno un'email, cliccheranno accept, e saranno parte dell'organizzazione."*

> **Note from Kimiko**: *"Il master account può dettare quali servizi possono essere acceduti dagli altri root account nell'organizzazione."*

> **Warning from Kimiko**: *"Ci può essere un po' di latenza nell'attesa che le modifiche di configurazione abbiano effetto. Non sorprenderti se devi controllare dopo un'ora per assicurarti che le impostazioni si siano propagate correttamente."*

---

## Service Control Policies — SCP (from PACKT)

PACKT describes SCPs as *"policy di permessi che ti permettono di definire i permessi massimi consentiti per gli account nella tua organizzazione."*

### Practical Example from PACKT

PACKT provides a concrete example — an SCP that restricts users to only launching `t2.micro` instances:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "RequireSmallInstanceType",
            "Effect": "Deny",
            "Action": "ec2:RunInstances",
            "Resource": ["arn:aws:ec2:*:*:instance/*"],
            "Condition": {
                "StringNotEquals": {
                    "ec2:InstanceType": "t2.micro"
                }
            }
        }
    ]
}
```

### Key SCP Rules (from PACKT)

- **They do not grant permissions** — they only provide restrictions or guardrails on actions users can perform
- Can be applied to a **specific account** or to an **OU** (all accounts in the OU inherit the restriction)
- **Permission priorities** remain the same as IAM: *"Se un permesso è negato a qualsiasi livello, è bloccato per quell'account, anche se l'amministratore locale concede accesso più ampio"*
- You can also apply **management policies** to define tagging and backup policies across the entire platform

---

## AWS Control Tower (from PACKT)

### Landing Zone

PACKT describes the core concept: *"Al centro di AWS Control Tower c'è il concetto di 'landing zone' — un ambiente AWS pre-configurato e baseline che include account separati per diversi workload, team o business unit, tutti con un set di guardrail pre-costruiti."*

PACKT explains that Control Tower is an **orchestrator** that uses several AWS services:
- **AWS Organizations** for account provisioning
- **AWS Service Catalog** for network infrastructure deployment
- **AWS IAM Identity Center** for consistent IAM role deployment across accounts

### Initial Structure

When you create a Control Tower deployment:
- An AWS organization is created with two OUs: **Security** (mandatory) and **Sandbox** (optional)
- Two accounts are created in the Security OU: **Audit** and **Log Archive**
- You can then create additional OUs as desired

### Guardrails (from PACKT)

| Type | How it works | Implementation |
|---|---|---|
| **Preventive** | Prevent actions that do not conform to your policies | **SCP** |
| **Detective** | Monitor resources and detect when they no longer conform to policies. Some support auto-remediation (e.g. removing public access from an S3 bucket) | **AWS Config** |

PACKT specifies the levels:
- **Mandatory**: deployed with every account, cannot be disabled
- **Strongly recommended**: AWS best practices
- **Elective**: optional, for specific requirements

### Account Factory (from PACKT)

PACKT describes Account Factory for automating new account provisioning: *"Definisci un blueprint che delinea quali risorse devono essere deployate in un nuovo account e poi usi questo blueprint durante la creazione dell'account per deployare le risorse. Questo elimina molto del lavoro pesante."*

> **Exam tip (PACKT)**: *"Non dovrai sapere esattamente quali guardrail sono mandatory e quali no, ma capire la differenza tra guardrail preventive e detective e i servizi sottostanti (SCP e AWS Config) sarà utile."*

---

## Typical Exam Scenarios

### Scenario 1: Limit Instance Types
**Question**: You want no account in the organization to be able to launch instances larger than t3.small.

**Answer**: **SCP** with Deny on `ec2:RunInstances` with `StringNotEquals` condition on instance type (direct example from PACKT).

### Scenario 2: New Multi-Account Environment with Governance
**Question**: The company is migrating to the cloud and wants a multi-account environment with automated governance.

**Answer**: **AWS Control Tower** — creates the landing zone, configures base accounts, applies guardrails (PACKT).

### Scenario 3: Consolidated Billing
**Question**: The company has 20 AWS accounts and wants a single invoice with volume discounts.

**Answer**: **AWS Organizations with consolidated billing** (Kimiko: *"Tutti gli account roll up per il consolidated billing"*).

### Scenario 4: Detect Public S3 Buckets and Auto-Remediate
**Question**: You want S3 buckets made public to be automatically made private.

**Answer**: **Control Tower with detective guardrail** implemented with AWS Config and auto-remediation (PACKT: *"For some detective guardrails, you can auto-remediate resolution, for example, by removing public access to an S3 bucket"*).

---

## Quick Recap for the Exam

- **Organizations**: centralized multi-account management, OUs to group accounts, consolidated billing (PACKT, Kimiko)
- **SCP**: define maximum permissions, do NOT grant permissions, Deny always wins (PACKT)
- **SCP on OU**: all accounts in the OU inherit the restriction (PACKT)
- **Limits**: max 1000 OUs, 5 nesting levels, 10 accounts default (soft limit) (PACKT)
- **Control Tower**: pre-configured landing zone, uses Organizations + Service Catalog + IAM Identity Center (PACKT)
- **Preventive guardrails**: SCP. **Detective guardrails**: AWS Config (PACKT)
- **Account Factory**: blueprint for automated new account provisioning (PACKT)
- **Consolidated billing**: single invoice, aggregated volume discounts (Kimiko)
- **Propagation latency**: changes may take time to propagate (Kimiko)
