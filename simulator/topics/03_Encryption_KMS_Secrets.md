# Encryption, KMS e Secrets Management

> Fonti: PACKT Cap.10 (p.443-449), PACKT Cap.12 (p.511-514), KIMIKO (p.292-298), DOJO (p.211-214, p.283)

---

## Encryption Fundamentals

Il PACKT introduce l'encryption come *"un aspetto fondamentale della sicurezza dei dati, che trasforma i dati in un formato sicuro illeggibile per utenti non autorizzati. Questo processo è cruciale per proteggere informazioni sensibili da accessi non autorizzati e garantire l'integrità dei dati."*

### Encryption at Rest (dal PACKT)

Protegge i dati salvati su servizi AWS come S3, RDS e EBS. Il PACKT specifica il comportamento di ogni servizio:

| Servizio | Encryption at Rest | Note |
|---|---|---|
| **S3** | Di default con chiave S3-managed | Supporta SSE-S3, SSE-KMS, SSE-C, e client-side |
| **EBS** | Deve essere configurata | Cifra anche gli snapshot |
| **RDS** | Deve essere configurata | Cifra anche backup, read replica e snapshot |
| **DynamoDB** | Automatica con AWS-owned keys | Se non fornisci una chiave KMS |
| **Lambda** | Automatica per environment variables | Anche deployment packages e layer archives |
| **Redshift** | Supporta encryption con KMS | Deve essere configurata |

> **Nota PACKT**: *"It is recommended that encryption be enabled wherever possible."*

Il PACKT distingue tra **client-side encryption** (cifri i dati prima di inviarli ad AWS — massimo controllo perché i dati sono cifrati durante tutto il trasferimento) e **server-side encryption** (AWS cifra i dati una volta salvati).

### Encryption in Transit (dal PACKT)

Protegge i dati mentre viaggiano sulla rete. Il PACKT elenca le best practice:

- **Usa endpoint HTTPS** dove possibile per proteggere i dati con TLS
- **Usa AWS PrivateLink** per accesso privato ai servizi AWS dal tuo VPC
- **Usa AWS Direct Connect** per connessioni sicure con l'ambiente on-premises (cifrabile con IPsec)
- **Certificati SSL/TLS**: il PACKT spiega che TLS è il protocollo più moderno. Quando ti connetti a un sito sicuro, il server presenta il certificato per provare la sua autenticità

### AWS Certificate Manager — ACM (dal PACKT)

Il PACKT descrive ACM come il servizio che *"semplifica il provisioning, la gestione e il deploy di certificati SSL/TLS, che proteggono le comunicazioni di rete e verificano l'identità di siti web e risorse interne."*

Caratteristiche chiave:
- Puoi richiedere certificati **pubblici e privati**
- **Rinnovo automatico** per sicurezza continua senza intervento manuale
- Deploy con: **CloudFront, Elastic Load Balancing, API Gateway**
- I certificati pubblici da ACM sono **gratuiti**
- **AWS Private Certificate Authority (CA)** per certificati privati per applicazioni interne

> **Tip esame (PACKT Cap.12)**: *"Make sure you are familiar with how key policies work in KMS. You may be presented with an exam question that shows you a key policy and asks you to pick the correct answer about who can use or access the key."*

---

## AWS KMS — Key Management Service

### Panoramica (dal PACKT e Dojo)

Il PACKT descrive KMS come il servizio per *"creare, gestire e controllare chiavi crittografiche attraverso un'ampia gamma di servizi AWS."*

Il Dojo aggiunge un dettaglio tecnico importante: *"KMS è un servizio gestito che funziona quasi come CloudHSM. Sotto il cofano, KMS usa anche hardware security modules. Ma a differenza di CloudHSM, questo servizio ha accesso multi-tenant, il che significa che condividi l'HSM con altri tenant o clienti AWS."*

Funzionalità chiave (dal PACKT):
- **Gestione centralizzata delle chiavi** — gestisci chiavi per vari servizi AWS da un'unica posizione
- **Key policies e integrazione IAM** — definisci permessi e controlli di accesso
- **Rotazione automatica delle chiavi** — per migliorare la sicurezza
- **Auditing e logging** — monitora l'uso delle chiavi con CloudTrail

### Tipi di Chiavi (dal Dojo)

Il Dojo fornisce la classificazione più dettagliata delle CMK (Customer Master Keys):

| Tipo | Chi gestisce | Controllo | Note |
|---|---|---|---|
| **Customer managed** | Tu | Pieno controllo: key policies, IAM policies, grants, abilitazione/disabilitazione, rotazione, tag, alias, scheduling deletion | Massima flessibilità |
| **AWS managed** | AWS | Non puoi gestirle, ruotarle, o cambiare le key policies. Il servizio che le crea le usa per tuo conto | Create automaticamente quando abiliti encryption su un servizio |
| **AWS owned** | AWS | Non puoi visualizzarle, usarle, tracciarle o auditarle | Usate internamente da AWS in più account |

Il Dojo specifica anche i tipi di encryption:
- **Symmetric** — chiave AES a 256 bit usata per encryption E decryption
- **Asymmetric** — coppia di chiavi RSA per encryption/decryption O signing/verification (non entrambi), oppure coppia ECC per signing/verification

> **Nota Dojo**: *"Symmetric CMKs and the private keys of asymmetric CMKs never leave AWS KMS unencrypted."*

### Envelope Encryption (dal Dojo)

Il Dojo spiega il meccanismo: *"AWS KMS usa envelope encryption, che è la pratica di cifrare i tuoi dati in chiaro con una data key; e poi cifrare quella data key usando un'altra chiave, chiamata master key."*

Dettaglio importante dal Dojo: *"Una CMK può essere usata per cifrare piccole quantità di dati (fino a 4096 byte). Se devi cifrare contenuti più grandi, usa la CMK per generare, cifrare e decifrare le data keys che vengono poi usate per cifrare i tuoi dati. Le data keys possono cifrare dati di qualsiasi dimensione e formato, inclusi dati in streaming."*

> **Nota Dojo**: *"AWS KMS non salva né gestisce le data keys, e non puoi usare KMS per cifrare o decifrare con le data keys. AWS KMS gestisce solo le CMK."*

### Walkthrough Pratico di Kimiko: Creare e Usare una Chiave KMS

Kimiko mostra il processo completo nella console:

1. **Visualizza le chiavi esistenti**: nella console KMS vedi le AWS managed keys (per Lambda, Redshift, Lightsail, ecc.) e le customer managed keys
2. **Crea una chiave**: scegli symmetric (per bulk encryption di dati, es. S3 bucket) o asymmetric (per autenticazione). Kimiko crea una chiave simmetrica con alias `sample_symmetric_S3`
3. **Definisci i key administrators**: chi può gestire la chiave amministrativamente, incluso se possono cancellarla
4. **Definisci chi può usare la chiave**: seleziona utenti o ruoli IAM
5. **Rivedi la key policy** generata automaticamente
6. **Usa la chiave con S3**: vai nelle proprietà del bucket → Default encryption → scegli AWS KMS → incolla l'ARN della chiave custom

> **Insight da Kimiko**: *"Quando cifri un bucket con una chiave custom, devi modificare la bucket policy per lavorare con le impostazioni di encryption. Le put request senza informazioni di encryption verranno rifiutate se hai bucket policies che rifiutano tali richieste."*

### Key Rotation (dal Dojo)

Il Dojo fornisce i dettagli più completi sulla rotazione:

Vantaggi della rotazione automatica:
1. Le proprietà della CMK (key ID, key ARN, region, policies, permissions) **non cambiano** quando la chiave viene ruotata
2. **Non devi cambiare** applicazioni o alias che riferiscono al CMK ID o ARN
3. AWS KMS ruota la CMK **automaticamente ogni anno** — non devi ricordare o schedulare l'aggiornamento

Limitazioni: la rotazione automatica **non è disponibile** per:
- CMK asimmetriche
- CMK in custom key stores
- CMK con key material importato

> **Nota Dojo**: *"KMS salva il vecchio materiale crittografico così può essere usato per decifrare dati che ha cifrato. KMS non cancella nessun materiale ruotato finché non cancelli la CMK."*

### Cancellazione delle Chiavi (da Kimiko)

Kimiko mostra un dettaglio pratico importante: *"Quando vuoi cancellare una chiave, devi schedulare la cancellazione. Questo è un bel safeguard contro la cancellazione di una chiave di cui hai disperatamente bisogno. Devi aspettare un minimo di 7 giorni prima che la chiave venga cancellata. Mentre è in pending deletion, puoi cancellare la cancellazione e reimplementare l'accesso alle risorse cifrate."*

---

## CloudHSM (dal Dojo)

Il Dojo fornisce il confronto più dettagliato tra KMS e CloudHSM:

### Quando Usare KMS (dal Dojo)

*"Le CMK di AWS KMS sono salvate in hardware security modules (HSM) validati FIPS che KMS gestisce (tenancy condivisa tra clienti AWS)."*

### Quando Usare CloudHSM (dal Dojo)

*"Se preferisci gestire i tuoi HSM per salvare le chiavi in KMS, o se richiedi FIPS 140-2 Level 3, puoi usare AWS CloudHSM."*

Il Dojo elenca i casi d'uso specifici per CloudHSM:
- **Offload SSL/TLS** — puoi scaricare il processing crittografico per sessioni HTTPS sul tuo modulo CloudHSM (non possibile con KMS). Questo alleggerisce il carico computazionale sui tuoi server
- **Proteggere chiavi private** per una Certificate Authority (CA) emittente
- **Transparent Data Encryption** per database Oracle

### Custom Key Store (dal Dojo)

Il Dojo descrive quando usare un custom key store con CloudHSM:
1. Il key material **non può essere salvato in un ambiente condiviso**
2. Il key material deve essere soggetto a un **audit path secondario e indipendente**
3. Hai bisogno della capacità di **rimuovere immediatamente** il key material da AWS KMS
4. Gli HSM devono essere certificati **FIPS 140-2 Level 3**

> **Nota Dojo**: i custom key stores non supportano la creazione di CMK asimmetriche, e non puoi abilitare la rotazione automatica. La rotazione deve essere fatta manualmente creando nuove chiavi e rimappando gli alias.

---

## AWS Secrets Manager (dal PACKT)

Il PACKT descrive Secrets Manager come *"un servizio fully managed progettato per semplificare e migliorare la sicurezza della gestione di informazioni sensibili nel tuo ambiente AWS."*

### Caratteristiche Chiave (dal PACKT)

- **Secure storage**: i segreti sono cifrati at rest usando AWS KMS
- **Fine-grained IAM policies**: personalizza i controlli di accesso
- **Rotazione automatica**: automatizza la rotazione di segreti come password database e API keys
- **Version control**: mantiene una storia delle versioni precedenti dei segreti per audit e tracciabilità
- **Logging con CloudTrail**: tutte le interazioni e API calls sono loggate
- **Integrazione con CloudFormation**: definisci e gestisci segreti come risorse IaC

### Rotazione dei Segreti (dal PACKT)

Il PACKT specifica due modalità di rotazione:

| Modalità | Come funziona | Servizi supportati |
|---|---|---|
| **Managed rotation** | Secrets Manager configura e gestisce la rotazione | Amazon Aurora, Amazon ECS, Amazon RDS, Amazon Redshift |
| **Lambda function rotation** | Una Lambda function aggiorna il segreto e il servizio che lo usa | Qualsiasi servizio |

> **Nota PACKT**: *"Per Aurora, RDS e Redshift, la managed rotation può ruotare solo le credenziali del master user o admin. Per qualsiasi altra rotazione di credenziali utente, si deve usare la Lambda function rotation."*

### Secrets Manager vs Parameter Store (dal PACKT)

Il PACKT nota: *"C'è un servizio comparabile in Systems Manager chiamato Parameter Store. Parameter Store permette di salvare vari valori in chiaro necessari per diversi task di automazione, inclusi segreti che possono essere cifrati. Tuttavia, una distinzione significativa è nelle capacità di rotazione dei segreti. A differenza di Secrets Manager, Parameter Store non ha rotazione nativa."*

---

## Data Security Controls (dal PACKT Cap.12)

Il PACKT Cap.12 riassume i controlli di sicurezza dei dati per l'esame in due categorie:

### Controlling Data

- **Accesso ai dati**: usa IAM per restringere chi può accedere ai servizi database gestiti. Per database self-hosted su EC2, configura l'autenticazione tu stesso e salva le password in **Secrets Manager**
- **Il problema più grande**: *"Companies will often think deeply about how to mitigate malicious threats to their data, but the biggest problem facing their data is human error. A simple mistake can wipe out an entire database in seconds."*
- **RPO**: *"Pay attention to the exam question to work out whether an RPO has been defined and work backward from that."*
- **RTO**: *"If you store all of your data in cold storage, it can take several hours to restore your data."*
- **Data retention**: familiarizzati con lifecycle policies in S3 e Intelligent-Tiering
- **Protezione da cancellazione accidentale**: S3 Versioning, S3 Object Lock, MFA delete, RDS database delete protection

### Encrypting Data (dal PACKT Cap.12)

- *"Data should be encrypted throughout its life cycle. Encrypted at rest using AWS KMS and encrypted in transit using TLS and a certificate stored in ACM."*
- Quando gestisci le tue chiavi in KMS, *"remember to ensure that you are locking down the key so that it can only be used and managed by the principals and applications that need access to it."*
- **Rotazione delle chiavi**: può essere automatizzata in KMS
- **Rinnovo certificati**: i certificati hanno una validità limitata e devono essere rinnovati. Conosci il processo in ACM

---

## Domande Esempio da Kimiko

Kimiko propone domande di esempio alla fine della sezione security:

1. **Quale oggetto IAM è raccomandato per la comunicazione inter-servizio?** → **Ruolo** (non utente, non MFA, non gruppo). I ruoli non sono per login interattivo, ma per permettere a un servizio di comunicare con un altro servizio con i permessi appropriati.

2. **Quale servizio AWS è specializzato nella prevenzione di attacchi DDoS?** → **AWS Shield** (due versioni: Standard incluso, Advanced a pagamento per implementazioni grandi).

> **Tip da Kimiko**: *"Sii consapevole del servizio KMS e sei garantito di avere una o due domande su questo nel tuo ambiente di esame di certificazione."*

---

## Scenari Tipici d'Esame

### Scenario 1: Cifrare dati grandi con KMS
**Domanda**: Devi cifrare file da 10GB con KMS. Come?

**Risposta**: Usa **envelope encryption** (Dojo). La CMK può cifrare solo fino a 4096 byte. Per dati più grandi, usa la CMK per generare una data key, poi usa la data key per cifrare i dati.

### Scenario 2: FIPS 140-2 Level 3
**Domanda**: L'azienda richiede FIPS 140-2 Level 3 per la gestione delle chiavi.

**Risposta**: **CloudHSM** (Dojo: *"If you require FIPS 140-2 Level 3, you may use AWS CloudHSM"*). KMS è multi-tenant e FIPS 140-2 Level 2.

### Scenario 3: Rotazione automatica credenziali DB
**Domanda**: Le credenziali del database RDS devono essere ruotate automaticamente.

**Risposta**: **Secrets Manager** con managed rotation (PACKT). Parameter Store non ha rotazione nativa.

### Scenario 4: Offload SSL/TLS processing
**Domanda**: Vuoi alleggerire il carico di processing SSL/TLS dai tuoi web server.

**Risposta**: **CloudHSM** (Dojo: *"You can offload SSL/TLS cryptographic processing for HTTPS sessions to your CloudHSM module, which cannot be done on AWS KMS"*).

### Scenario 5: Key policy nell'esame
**Domanda**: Ti viene mostrata una key policy e ti chiedono chi può usare la chiave.

**Risposta**: Leggi attentamente la key policy (PACKT Cap.12: *"You may be presented with an exam question that shows you a key policy and asks you to pick the correct answer about who can use or access the key"*).

---

## Riepilogo Veloce per l'Esame

- **Encryption at rest**: KMS per la maggior parte dei servizi. S3 cifra di default, EBS/RDS devono essere configurati (PACKT)
- **Encryption in transit**: TLS/SSL con certificati ACM (gratuiti per servizi AWS) (PACKT)
- **KMS**: multi-tenant, FIPS 140-2 Level 2, gestione centralizzata chiavi (Dojo)
- **CloudHSM**: single-tenant, FIPS 140-2 Level 3, offload SSL/TLS, Oracle TDE (Dojo)
- **CMK types**: Customer managed (pieno controllo), AWS managed (gestite da AWS), AWS owned (invisibili) (Dojo)
- **Envelope encryption**: CMK cifra la data key, data key cifra i dati. CMK max 4096 byte direttamente (Dojo)
- **Key rotation**: automatica ogni anno per customer managed keys, non disponibile per asymmetric/imported/custom key store (Dojo)
- **Cancellazione chiavi**: minimo 7 giorni di attesa, cancellabile durante il pending (Kimiko)
- **Secrets Manager**: rotazione automatica (managed per Aurora/RDS/Redshift master user, Lambda per altri) (PACKT)
- **Parameter Store**: simile ma senza rotazione nativa (PACKT)
- **ACM**: certificati SSL gratuiti per CloudFront/ELB/API GW, rinnovo automatico (PACKT)
- **Data protection**: S3 Versioning + Object Lock + MFA delete per protezione da cancellazione (PACKT Cap.12)
- **Human error > malicious threats**: il problema più grande per i dati è l'errore umano (PACKT Cap.12)
