# IAM - Identity and Access Management

> Fonti: PACKT Cap.3 (p.156-185), PACKT Cap.12 (p.502-517), KIMIKO (p.275-281), DOJO (p.204-210)

---

## Cos'è IAM

IAM è il servizio web di AWS che gestisce in modo sicuro il controllo e l'accesso alle risorse AWS. Come spiega il Dojo, ha due funzioni primarie evidenti dal nome: gestire l'**identità** dei tuoi utenti (autenticazione) e fornire la **gestione degli accessi** alle risorse e servizi del tuo account (autorizzazione).

Caratteristiche fondamentali:
- **Globale** — IAM non è legato a una Region. Un utente IAM creato una volta è disponibile in tutte le Region
- **Gratuito** — non paghi per creare utenti, gruppi, ruoli o policy
- **Eventually consistent** — le modifiche alle policy si propagano rapidamente ma non istantaneamente

---

## I Componenti di IAM

### Root Account

Quando crei un account AWS, il primo utente che esiste automaticamente è il **root user** (Dojo). Come dice Kimiko nel suo walkthrough pratico: *"Il root user è l'account amministratore 'godlike' del sistema. Può fare qualsiasi cosa. Dovremmo loggarci con questo account solo quando dobbiamo fare le poche operazioni che un normale account admin AWS non può fare"* — ad esempio cambiare le informazioni di billing associate all'account.

Best practice per il root account (da PACKT Cap.12):
- **Non usarlo mai per le operazioni quotidiane** — il PACKT è esplicito: *"This root user should not be used for everyday tasks, and only used in the case of an emergency"*
- **Abilita MFA** — Kimiko mostra nella console che il security status di IAM segnala se MFA non è attivo sul root account
- **Non creare access key per il root** — se le crei, cancellale
- **Proteggi le credenziali fisicamente** — il PACKT suggerisce addirittura di scrivere la password e conservarla in una cassaforte fisica

> **Tip esame (PACKT Cap.12)**: *"A common question topic that features on the AWS SAA-C03 exam is around the root user. The key thing to remember is that the root user should never be used as a normal IAM user."*

### Users (Utenti)

Il PACKT paragona gli utenti IAM ai singoli dipendenti di un'azienda. Ogni utente ha un'identità unica all'interno di AWS e può ricevere accesso a vari servizi e risorse.

Ogni utente può avere:
- **Console access** — username + password per la AWS Management Console
- **Programmatic access** — Access Key ID + Secret Access Key per CLI, SDK, API
- **Entrambi**

Come mostra Kimiko nel suo walkthrough: quando crei un utente, decidi se può avere accesso programmatico ad AWS e/o accesso alla Management Console, e puoi impostare una password custom o auto-generata che l'utente dovrà cambiare al primo login.

Il Dojo aggiunge un esempio pratico importante: *"Hai un nuovo Solutions Architect che ha bisogno solo di accesso ai template CloudFormation. Dopo aver creato un utente IAM, quali permessi dovresti dare senza compromettere la sicurezza? Come minimo, dovresti aggiungere l'utente a un gruppo IAM con una policy che permette solo azioni CloudFormation."* Se gli dai PowerUserAccess o AdministratorAccess, è un rischio di sicurezza. Se gli dai le credenziali del root user, stai mettendo in pericolo l'intera infrastruttura cloud.

### Groups (Gruppi)

Il PACKT paragona i gruppi ai dipartimenti di un'azienda, dove ogni dipartimento ha un certo set di permessi basato sulla funzione lavorativa.

Regole dei gruppi:
- Un utente può appartenere a **più gruppi**
- I gruppi **non possono contenere altri gruppi** (niente nesting)
- Le policy attaccate al gruppo si applicano a **tutti** gli utenti del gruppo

Kimiko mostra il processo pratico nella console: quando crei un utente, puoi aggiungerlo a un gruppo (modo scalabile), aggiungere permessi direttamente, o copiarli da un utente esistente. Nel suo esempio, crea un gruppo "S3 admin" con la policy `AmazonS3FullAccess` e ci aggiunge l'utente "student2".

Il PACKT (Cap.12) sottolinea il vantaggio operativo: *"By placing users in a group and applying a policy to that same group, you can implement restrictions to hundreds of users in one action, saving you vast amounts of operational overhead."*

### Roles (Ruoli)

Il PACKT descrive i ruoli come posizioni lavorative all'interno di un'azienda, equipaggiate con set di permessi specifici. La differenza chiave rispetto agli utenti: i ruoli usano **credenziali di sicurezza temporanee**, non permanenti.

Kimiko chiarisce un punto che confonde spesso gli studenti: *"I ruoli NON sono per gli utenti che fanno login. Sono per le risorse che interagiscono con altre risorse."* Nel suo esempio: un'istanza EC2 che deve leggere da un bucket S3 → assegni il ruolo "EasyToReadS3" all'istanza EC2, e questa usa il ruolo per presentare i permessi appropriati a S3.

Il Dojo aggiunge dettagli tecnici importanti sull'uso dei ruoli con EC2: *"Per Amazon EC2, puoi usare l'instance profile per passare un ruolo IAM specifico alla tua istanza EC2. Questi ruoli IAM attaccati alla tua istanza possono essere visualizzati nei metadata EC2"* — con il comando `curl http://169.254.169.254/latest/meta-data/iam/info`.

#### Casi d'uso principali dei ruoli (dal PACKT)

| Caso d'uso | Descrizione |
|---|---|
| **EC2 Instance Role** | Un'istanza EC2 che deve accedere a S3 → le assegni un ruolo con permessi S3 |
| **Cross-Account Access** | Un'applicazione deve accedere a risorse in un altro account → configuri cross-account access con ruoli |
| **Identity Federation** | Utenti con identità esterne (corporate directory, app mobile/web) assumono un ruolo per accedere temporaneamente ad AWS |
| **Service Role** | Un servizio AWS (es. Lambda) che deve accedere ad altri servizi |

> **Tip esame (PACKT Cap.12)**: *"It is best practice to configure federation and IAM roles to grant temporary credentials to your AWS accounts"* piuttosto che usare utenti IAM con credenziali permanenti.

---

## Policies (Policy)

Le policy sono documenti JSON che definiscono i permessi. Il PACKT le descrive come *"i regolamenti che definiscono chi è autorizzato a fare cosa"*.

### Struttura di una Policy

Il PACKT fornisce questo esempio commentato — una policy che permette di listare tutti i bucket S3 e leggere oggetti da un bucket specifico:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:ListAllMyBuckets",
            "Resource": "arn:aws:s3:::*"
        },
        {
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::AWSExamBucket/*"
        }
    ]
}
```

Il Dojo dettaglia la struttura con precisione:

- **Effect** — `Allow` o `Deny`. Di default, gli utenti IAM non hanno permesso di fare nulla, quindi tutte le richieste sono implicitamente negate. Un Allow esplicito sovrascrive il default. Un Deny esplicito sovrascrive qualsiasi Allow.
- **Action** — le azioni API specifiche che stai concedendo o negando
- **Resource** — la risorsa interessata, specificata tramite ARN o wildcard `*`
- **Condition** — opzionale, per controllo granulare

### Condizioni nelle Policy (dal Dojo)

Il Dojo elenca le condizioni che devi conoscere per l'esame:

| Condizione | Cosa fa |
|---|---|
| `StringEquals` | Matching esatto di stringa, case sensitive |
| `StringNotEquals` | Opposto di StringEquals |
| `StringLike` | Matching esatto ma ignora il case |
| `StringNotLike` | Opposto di StringLike |
| `Bool` | Restringe accesso basato su valori true/false |
| `IpAddress` | Matching di un IP o range specifico |
| `NotIpAddress` | Tutti gli IP tranne quello specificato |
| `ArnEquals`, `ArnLike` | Matching di ARN |
| `Null` | Verifica se una condition key è presente al momento dell'autorizzazione |

> Puoi aggiungere `IfExists` alla fine di qualsiasi operatore (tranne Null) — es. `StringLikeIfExists`.

### Tipi di Policy

Il PACKT distingue tra managed policies (create e gestite da AWS o dall'utente) e inline policies (attaccate direttamente a un utente, gruppo o ruolo).

Il Dojo approfondisce con la distinzione fondamentale:

| Tipo | Dove si attacca | Caratteristica |
|---|---|---|
| **Identity-based** | Utenti, Gruppi, Ruoli | Definisce cosa può fare l'identità |
| **Resource-based** | Risorse (S3, SQS, ecc.) | Include un campo **Principal** per specificare chi può accedere |
| **AWS Managed** | Predefinite da AWS | Policy pronte all'uso (es. `AmazonS3FullAccess`) |
| **Customer Managed** | Create da te | Policy personalizzate |
| **Inline** | Incorporate in un utente/gruppo/ruolo | Per permessi specifici di una singola entità |

Il Dojo fornisce un esempio concreto di resource-based policy su S3 con condizione IP:

```json
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {"AWS": "arn:aws:iam::123456789000:role/EC2RoleToAccessS3"},
        "Action": ["s3:GetObject", "s3:GetObjectVersion"],
        "Resource": ["arn:aws:s3:::EXAMPLE-BUCKET/*"],
        "Condition": {
            "ForAnyValue:StringEquals": {
                "NotIpAddress": {"aws:SourceIp": "10.10.0.0/24"}
            }
        }
    }]
}
```

> **Nota Dojo**: Resource-based policies e resource-level permissions sono due cose diverse. Le resource-based policies includono un elemento `Principal` per specificare quali identità IAM possono accedere alla risorsa. Le resource-level permissions si riferiscono alla capacità di usare ARN per specificare risorse individuali in una policy.

### IAM DB Authentication (dal Dojo)

Il Dojo menziona una feature importante: **IAM DB Authentication per Amazon RDS e Aurora**. Questa feature permette di usare IAM per gestire centralmente l'accesso alle risorse database, eliminando la necessità di gestire l'accesso utente individualmente su ogni istanza DB. Migliora anche la sicurezza delle applicazioni su EC2 perché non devi salvare la password del database — usi l'instance profile per connetterti a RDS.

### Uso di IAM con altri servizi (dal Dojo)

| Servizio | Come usa IAM |
|---|---|
| **EC2** | Instance profile per passare un ruolo IAM all'istanza |
| **S3** | Bucket policy per concedere accesso cross-account |
| **DynamoDB** | IAM policy per permettere put/update/delete su tabelle specifiche |
| **SQS** | Access policy per controllare accesso esterno alla coda |
| **RDS/Aurora** | IAM DB Authentication per accesso centralizzato |

---

## Logica di Valutazione delle Policy

Questo è FONDAMENTALE per l'esame. Il Dojo fornisce la spiegazione più completa con 4 livelli di valutazione:

### Il Processo (dal Dojo)

Quando un principal invia una richiesta ad AWS:
1. AWS **autentica** il principal
2. AWS processa le informazioni nella richiesta per determinare quali policy si applicano
3. AWS **valuta tutti i tipi di policy**, che influenzano l'ordine di valutazione
4. AWS processa le policy per determinare se la richiesta è permessa o negata

### Le 4 Regole di Valutazione (dal Dojo)

1. Se si applicano **solo identity-based policies**: AWS cerca almeno un Allow esplicito e verifica che non ci sia un Deny esplicito
2. Se si applicano **sia resource-based che identity-based policies**: AWS cerca un Allow in tutte le policy e verifica che non ci sia un Deny esplicito
3. Se c'è una **permissions boundary**: l'entità può eseguire solo le azioni permesse sia dalle identity-based policies che dalla boundary. Un deny implicito nella boundary NON limita i permessi concessi da una resource-based policy
4. Se c'è una **SCP di AWS Organizations**: identity-based e resource-based policies concedono permessi solo se anche la SCP permette l'azione. Se sono presenti sia boundary che SCP, allora boundary + SCP + identity-based policy devono TUTTE permettere l'azione senza deny esplicito

### Riepilogo della Logica (dal Dojo)

- Di default, tutte le richieste sono **implicitamente negate**. Il root user ha accesso completo di default
- Un **Allow esplicito** in una identity-based o resource-based policy sovrascrive il default
- Se è presente una **permissions boundary, SCP, o session policy**, potrebbe sovrascrivere l'Allow con un deny implicito
- Un **Deny esplicito** in qualsiasi policy sovrascrive qualsiasi Allow

> **Nota PACKT Cap.12**: *"If an action is explicitly denied in one policy and explicitly allowed in another, and both policies are attached to an IAM principal, the deny policy will always take precedence."*

---

## Permission Boundaries

Il PACKT spiega le permission boundaries come un metodo per impostare i **permessi massimi** che un utente o ruolo IAM può avere, agendo come guardrail nella struttura dei permessi dell'organizzazione.

Il Dojo definisce: *"Una permissions boundary è una feature avanzata per usare una managed policy per impostare i permessi massimi che una identity-based policy può concedere a un'entità IAM. La boundary prende precedenza su una identity policy, quindi anche se i tuoi utenti attaccano privilegi Administrator ai loro account, non potranno eseguire azioni oltre quanto stabilito nella boundary."*

### Hands-on Lab del PACKT: David e la Permission Boundary

Il PACKT presenta un lab pratico completo che illustra perfettamente come funzionano le permission boundaries:

**Scenario**: David è nuovo nel team infrastruttura. Ha bisogno di accesso a certi servizi AWS, ma deve essere limitato per non lanciare accidentalmente servizi costosi.

**Passaggi**:
1. **Crea un gruppo** "Operators"
2. **Crea l'utente** David con accesso alla Management Console, aggiungilo al gruppo Operators
3. **Crea una custom policy** `EC2_S3_OperatorsPolicy`: Allow su tutti i servizi EC2 e S3, ma Deny su `RunInstances` e `TerminateInstances`
4. **Crea una permission boundary** `UserBoundary` con questa policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "ec2:*",
            "Resource": "*"
        },
        {
            "Effect": "Deny",
            "Action": "*",
            "NotResource": "arn:aws:ec2:*:*:instance/*"
        }
    ]
}
```

5. **Attacca la boundary** a David

**Risultato del test** (nel Policy Simulator):
- Tutte le azioni S3 sono **DENIED** — anche se David ha una policy che gli dà accesso S3, la permission boundary permette solo azioni EC2
- Se rimuovi la boundary nel simulatore, le azioni S3 tornano Allow

> **Insight PACKT**: *"Even though he had an inline policy attached that gave those permissions [S3], he was unable to access S3"* — la boundary limita i permessi massimi, non concede permessi.

### Caso d'uso pratico delle Boundaries (dal PACKT)

Il PACKT descrive uno scenario aziendale: un'organizzazione con più team di developer, ognuno responsabile di deploy e gestione di applicazioni AWS. Ogni team può creare e gestire le proprie risorse (EC2, S3, Lambda), ma vuoi assicurarti che nessun developer possa concedersi permessi eccessivi (come accesso admin) che potrebbero portare a rischi di sicurezza o costi imprevisti. Le permission boundaries bloccano la possibilità di concedersi privilegi aggiuntivi.

Il Dojo aggiunge: *"Quando hai utenti che lavorano su diversi progetti e ambienti, può essere difficile tenere traccia dei permessi necessari. A volte sarebbe più veloce lasciare che gli utenti attacchino le policy di cui hanno bisogno ai loro ruoli IAM. Questo può causare problemi di sicurezza. Puoi trovare un compromesso creando IAM permissions boundaries."*

---

## Identity Providers e Federation

### SAML 2.0 Federation (dal PACKT)

Il PACKT descrive il processo completo di federated access:

1. **Configura un IdP esterno** (Active Directory, Google, o qualsiasi servizio che supporta SAML 2.0) — questo IdP gestisce i login e le identità fuori da AWS
2. **Crea un IAM identity provider** nella console AWS che si connette all'IdP esterno — fornisci i dettagli dell'IdP e carica un metadata file
3. **Crea ruoli IAM** che gli utenti assumeranno quando fanno login — questi ruoli definiscono le azioni permesse in AWS
4. **Configura una trust policy** per ogni ruolo, specificando che solo utenti autenticati dal tuo IdP possono usare questi ruoli
5. **L'utente fa login** attraverso l'IdP esterno con le sue credenziali esistenti
6. **L'IdP fornisce un'asserzione SAML** — un security token con informazioni sull'utente
7. **AWS usa l'asserzione SAML** per determinare quale ruolo IAM l'utente può assumere
8. **L'utente scambia l'asserzione** per credenziali AWS temporanee

> **Nota PACKT**: le credenziali temporanee scadono. Quando succede, l'utente deve fare login di nuovo attraverso l'IdP.

### Best Practice per la Federation (dal PACKT)

Il PACKT (Cap.12) è chiaro: *"The best practice is to use federated identities and IAM roles, granting individuals temporary credentials. This can be done using supported identity providers such as Google and Facebook, or using an existing identity directory such as Amazon Cognito or Azure AD/Entra ID. Once you have configured your identity store, you will use AWS STS to authenticate and temporarily assume a role."*

---

## RBAC — Role-Based Access Control (dal PACKT Cap.12)

Il PACKT dedica una sezione specifica alla strategia RBAC:

*"When creating a robust RBAC strategy, it is important to define clear responsibilities for your roles. The worst thing that you could do is give admin permissions to everyone."*

Esempio pratico dal PACKT:
- **DevOps engineer**: ha bisogno di write access a CodeBuild e S3, ma NON ha bisogno di accesso a EKS o SageMaker
- **Data scientist**: ha bisogno solo di accesso a SageMaker

→ Crei due ruoli separati: uno per DevOps (solo S3 + CodeBuild) e uno per data scientist (solo SageMaker).

Il PACKT menziona anche il **role switching**: un individuo potrebbe avere accesso a diversi ruoli. Ad esempio, un'organizzazione potrebbe spostare tutte le azioni IAM in un ruolo separato per assicurarsi che gli individui non possano concedersi permessi extra. Per usare questo altro ruolo, l'individuo usa il role switching per assumere un altro ruolo.

---

## IAM Access Analyzer (dal PACKT)

Il PACKT descrive Access Analyzer come uno strumento che aiuta a identificare le risorse nel tuo account che sono condivise con entità esterne o che non sono in uso e quindi non seguono il principio di least privilege.

Dettagli importanti dal PACKT:
- **È regionale** — devi creare un audit run per ogni Region in cui operi
- **Controlla anche le Region non usate** — *"It is also worthwhile running it for all regions that you have access to, even if you do not use them for deployments, as hackers or bad actors can exploit these unused regions to operate unseen"*
- **Usa i tag** — il PACKT raccomanda di aggiungere tag a tutti i ruoli e policy IAM come best practice. *"Most hackers will not follow any tagging requirements, as they need to operate as quickly as possible, and using tagging allows those roles and policies to be found and removed more quickly"*

---

## IAM Policy Simulator (dal PACKT)

Il Policy Simulator permette di simulare come le policy IAM funzioneranno in pratica, senza applicarle in un ambiente live. Il PACKT lo descrive come particolarmente utile per amministratori e professionisti della sicurezza.

Caratteristiche chiave:
- Simula permessi per qualsiasi utente, gruppo o ruolo IAM
- Mostra se ogni azione sarebbe Allow o Deny
- Utile per testare nuove policy o modifiche prima di applicarle
- Accessibile via link esterno: `https://policysim.aws.amazon.com/`

> Nel hands-on lab del PACKT, il Policy Simulator viene usato per verificare che David non possa accedere a S3 a causa della permission boundary.

---

## IAM at Scale (dal PACKT Cap.12)

Il PACKT dedica una sezione a come gestire IAM quando la piattaforma AWS cresce:

*"As your AWS platform grows and begins to have more and more accounts, remember to leverage tools to simplify the management of IAM across your platform. Make use of SCPs to implement guardrails across your AWS organization and use Control Tower to ensure IAM roles and policies are standardized across your accounts."*

---

## Hands-on Challenge di Kimiko

Kimiko propone una sfida pratica:

1. **Crea un gruppo IAM** con il nome tag "IAM Group R.D.S.R.O."
2. **Assegna al gruppo** una policy che permette accesso read-only a RDS
3. **Crea un utente IAM** e assicurati che sia membro del gruppo creato
4. **L'utente deve avere** solo accesso alla Management Console (no programmatic access)
5. **Quando hai finito**, cancella tutte le risorse create
6. **Accetta i default** per qualsiasi impostazione non esplicitamente specificata

> **Tip da Kimiko**: *"Whenever possible, create those groups and those user accounts for your engineers. Really try and focus on an approach that has them operate with the least privilege as much as possible. And of course, avoid the use of the root account."*

---

## Scenari Tipici d'Esame

### Scenario 1: Accesso EC2 a S3 (dal Dojo)
**Domanda**: Un'applicazione su EC2 deve caricare dati su S3. Come configurare l'accesso?

**Risposta**: Usa l'**instance profile** per passare un ruolo IAM specifico all'istanza EC2. Il ruolo avrà una policy che permette le azioni S3 necessarie. Non salvare mai credenziali nel codice.

### Scenario 2: Nuovo dipendente con accesso limitato (dal Dojo)
**Domanda**: Un nuovo Solutions Architect ha bisogno solo di accesso a CloudFormation. Cosa fare?

**Risposta**: Crea un utente IAM, aggiungilo a un gruppo con una policy che permette **solo** azioni CloudFormation. NON dare PowerUserAccess o AdministratorAccess.

### Scenario 3: Developer che non devono auto-concedersi admin (dal PACKT)
**Domanda**: I developer devono poter creare risorse ma non devono potersi concedere permessi admin. Come?

**Risposta**: Usa **permission boundaries**. Permetti ai developer di creare ruoli, ma ogni ruolo deve avere una boundary che limita i permessi massimi.

### Scenario 4: Accesso cross-account (dal PACKT Cap.12)
**Domanda**: Un'applicazione deve accedere a risorse in un altro account (es. account di logging centralizzato).

**Risposta**: Configura **cross-account access** con ruoli IAM, restringendo le azioni e i permessi che l'applicazione può eseguire e in quali account.

### Scenario 5: Accesso database sicuro (dal Dojo)
**Domanda**: Come migliorare la sicurezza dell'accesso al database RDS da istanze EC2?

**Risposta**: Usa **IAM DB Authentication** per RDS/Aurora. Non devi salvare la password del database — usi l'instance profile dell'EC2 per connetterti a RDS.

---

## Riepilogo Veloce per l'Esame

- **Root account**: MFA obbligatorio, non usarlo mai per operazioni quotidiane (PACKT, Kimiko)
- **Least privilege**: dai SOLO i permessi necessari (tutte le fonti)
- **Gruppi**: usa i gruppi per gestire i permessi, non attaccare policy direttamente agli utenti (Kimiko, PACKT)
- **Ruoli > Utenti** per applicazioni e servizi: i ruoli sono per risorse che interagiscono con altre risorse (Kimiko), mai access key nel codice
- **Instance profile**: il modo per attaccare un ruolo a EC2, credenziali visibili nei metadata (Dojo)
- **Deny esplicito vince sempre** su Allow (PACKT, Dojo)
- **4 livelli di valutazione**: identity policy → resource policy → permission boundary → SCP (Dojo)
- **Permission boundary**: limita il massimo dei permessi, non concede permessi (PACKT lab con David)
- **Federation**: SAML 2.0 per enterprise, Cognito per web/mobile, STS per credenziali temporanee (PACKT)
- **RBAC**: definisci ruoli chiari per funzione lavorativa, mai admin a tutti (PACKT Cap.12)
- **IAM DB Authentication**: per RDS/Aurora, elimina la necessità di salvare password (Dojo)
- **Access Analyzer**: regionale, controlla anche Region non usate, usa i tag per trovare ruoli sospetti (PACKT)
- **Policy Simulator**: testa le policy prima di applicarle, accessibile via `policysim.aws.amazon.com` (PACKT)
- **IAM at Scale**: usa SCP + Control Tower per standardizzare IAM su più account (PACKT Cap.12)
