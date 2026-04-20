# AWS Organizations e Multi-Account Strategy

> Fonti: PACKT Cap.11 (p.466-472), KIMIKO (p.301-302)

---

## Perché Multi-Account?

Il PACKT spiega il contesto: *"Man mano che ti allontani da una piccola piattaforma AWS verso una più grande, probabilmente avrai diversi account da gestire. Magari stai centralizzando i log in un account, o magari hai un account per tutto il networking ingress e egress. Man mano che guadagni più account, applicare controlli diventa complesso."*

---

## AWS Organizations (dal PACKT)

Il PACKT descrive Organizations come il servizio per *"creare e gestire più account AWS, configurare policy organizzative e controllare l'accesso alle risorse AWS."*

### Struttura Organizzativa

Gli account sono strutturati in **Organizational Units (OU)**. Il PACKT spiega: *"Le OU ti permettono di raggruppare i tuoi account secondo funzioni di business, team, o qualsiasi struttura logica abbia senso per la tua piattaforma."*

Il PACKT fornisce un esempio visivo della struttura:

```
Root Account (management + billing consolidato)
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

Limiti importanti (dal PACKT):
- Puoi annidare OU fino a **5 livelli** di profondità
- Massimo **1,000 OU** per organizzazione
- Limite default di **10 account** (soft limit, aumentabile a migliaia)

### Consolidated Billing (da Kimiko)

Kimiko spiega il problema che Organizations risolve: *"Per molto tempo c'era una sfida con AWS, nell'area del billing. Potevi ritrovarti con un sacco di account AWS diversi nella tua azienda, e non c'era un modo facile per configurare il consolidated billing in self-service."*

Kimiko mostra il processo: *"Vai in AWS Organizations con il tuo root account — vuoi essere il main account dell'organizzazione. Poi invii inviti agli altri indirizzi email che rappresentano gli altri root account. Riceveranno un'email, cliccheranno accept, e saranno parte dell'organizzazione."*

> **Nota da Kimiko**: *"Il master account può dettare quali servizi possono essere acceduti dagli altri root account nell'organizzazione."*

> **Avvertimento da Kimiko**: *"Ci può essere un po' di latenza nell'attesa che le modifiche di configurazione abbiano effetto. Non sorprenderti se devi controllare dopo un'ora per assicurarti che le impostazioni si siano propagate correttamente."*

---

## Service Control Policies — SCP (dal PACKT)

Il PACKT descrive le SCP come *"policy di permessi che ti permettono di definire i permessi massimi consentiti per gli account nella tua organizzazione."*

### Esempio Pratico dal PACKT

Il PACKT fornisce un esempio concreto — una SCP che restringe gli utenti a poter lanciare solo istanze `t2.micro`:

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

### Regole Chiave delle SCP (dal PACKT)

- **Non concedono permessi** — forniscono solo restrizioni o guardrail sulle azioni che gli utenti possono eseguire
- Possono essere applicate a un **account specifico** o a una **OU** (tutti gli account nella OU ereditano la restrizione)
- Le **priorità dei permessi** rimangono le stesse di IAM: *"Se un permesso è negato a qualsiasi livello, è bloccato per quell'account, anche se l'amministratore locale concede accesso più ampio"*
- Puoi anche applicare **management policies** per definire policy di tagging e backup su tutta la piattaforma

---

## AWS Control Tower (dal PACKT)

### Landing Zone

Il PACKT descrive il concetto core: *"Al centro di AWS Control Tower c'è il concetto di 'landing zone' — un ambiente AWS pre-configurato e baseline che include account separati per diversi workload, team o business unit, tutti con un set di guardrail pre-costruiti."*

Il PACKT spiega che Control Tower è un **orchestratore** che usa diversi servizi AWS:
- **AWS Organizations** per il provisioning degli account
- **AWS Service Catalog** per il deploy dell'infrastruttura di rete
- **AWS IAM Identity Center** per il deploy consistente dei ruoli IAM tra account

### Struttura Iniziale

Quando crei un deployment Control Tower:
- Viene creata un'organizzazione AWS con due OU: **Security** (obbligatoria) e **Sandbox** (opzionale)
- Nella Security OU vengono creati due account: **Audit** e **Log Archive**
- Puoi poi creare altre OU come desideri

### Guardrails (dal PACKT)

| Tipo | Come funziona | Implementazione |
|---|---|---|
| **Preventive** | Impediscono azioni che non conformano alle tue policy | **SCP** |
| **Detective** | Monitorano le risorse e rilevano quando non conformano più alle policy. Alcuni supportano auto-remediation (es. rimuovere accesso pubblico a un bucket S3) | **AWS Config** |

Il PACKT specifica i livelli:
- **Mandatory**: deployati con ogni account, non disabilitabili
- **Strongly recommended**: best practice AWS
- **Elective**: opzionali, per requisiti specifici

### Account Factory (dal PACKT)

Il PACKT descrive Account Factory per automatizzare il provisioning di nuovi account: *"Definisci un blueprint che delinea quali risorse devono essere deployate in un nuovo account e poi usi questo blueprint durante la creazione dell'account per deployare le risorse. Questo elimina molto del lavoro pesante."*

> **Tip esame (PACKT)**: *"Non dovrai sapere esattamente quali guardrail sono mandatory e quali no, ma capire la differenza tra guardrail preventive e detective e i servizi sottostanti (SCP e AWS Config) sarà utile."*

---

## Scenari Tipici d'Esame

### Scenario 1: Limitare i tipi di istanza
**Domanda**: Vuoi che nessun account nell'organizzazione possa lanciare istanze più grandi di t3.small.

**Risposta**: **SCP** con Deny su `ec2:RunInstances` con condizione `StringNotEquals` sul tipo di istanza (esempio diretto dal PACKT).

### Scenario 2: Nuovo ambiente multi-account con governance
**Domanda**: L'azienda sta migrando al cloud e vuole un ambiente multi-account con governance automatica.

**Risposta**: **AWS Control Tower** — crea la landing zone, configura account base, applica guardrail (PACKT).

### Scenario 3: Consolidated billing
**Domanda**: L'azienda ha 20 account AWS e vuole una fattura unica con sconti volume.

**Risposta**: **AWS Organizations con consolidated billing** (Kimiko: *"Tutti gli account roll up per il consolidated billing"*).

### Scenario 4: Rilevare bucket S3 pubblici e rimediare automaticamente
**Domanda**: Vuoi che i bucket S3 resi pubblici vengano automaticamente resi privati.

**Risposta**: **Control Tower con guardrail detective** implementato con AWS Config e auto-remediation (PACKT: *"For some detective guardrails, you can auto-remediate resolution, for example, by removing public access to an S3 bucket"*).

---

## Riepilogo Veloce per l'Esame

- **Organizations**: gestione centralizzata multi-account, OU per raggruppare account, consolidated billing (PACKT, Kimiko)
- **SCP**: definiscono permessi massimi, NON concedono permessi, Deny vince sempre (PACKT)
- **SCP su OU**: tutti gli account nella OU ereditano la restrizione (PACKT)
- **Limiti**: max 1000 OU, 5 livelli di nesting, 10 account default (soft limit) (PACKT)
- **Control Tower**: landing zone pre-configurata, usa Organizations + Service Catalog + IAM Identity Center (PACKT)
- **Guardrail preventive**: SCP. **Guardrail detective**: AWS Config (PACKT)
- **Account Factory**: blueprint per provisioning automatizzato di nuovi account (PACKT)
- **Consolidated billing**: fattura unica, sconti volume aggregati (Kimiko)
- **Latenza propagazione**: le modifiche possono richiedere tempo per propagarsi (Kimiko)
