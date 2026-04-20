# Encryption, KMS and Secrets Management

> Sources: PACKT Ch.10 (p.443-449), PACKT Ch.12 (p.511-514), KIMIKO (p.292-298), DOJO (p.211-214, p.283)

---

## Encryption Fundamentals

PACKT introduces encryption as *"un aspetto fondamentale della sicurezza dei dati, che trasforma i dati in un formato sicuro illeggibile per utenti non autorizzati. Questo processo è cruciale per proteggere informazioni sensibili da accessi non autorizzati e garantire l'integrità dei dati."*

### Encryption at Rest (from PACKT)

Protects data stored on AWS services such as S3, RDS and EBS. PACKT specifies the behavior of each service:

| Service | Encryption at Rest | Notes |
|---|---|---|
| **S3** | By default with S3-managed key | Supports SSE-S3, SSE-KMS, SSE-C, and client-side |
| **EBS** | Must be configured | Also encrypts snapshots |
| **RDS** | Must be configured | Also encrypts backups, read replicas and snapshots |
| **DynamoDB** | Automatic with AWS-owned keys | If you don't provide a KMS key |
| **Lambda** | Automatic for environment variables | Also deployment packages and layer archives |
| **Redshift** | Supports encryption with KMS | Must be configured |

> **PACKT Note**: *"It is recommended that encryption be enabled wherever possible."*

PACKT distinguishes between **client-side encryption** (you encrypt data before sending it to AWS — maximum control because data is encrypted throughout the entire transfer) and **server-side encryption** (AWS encrypts data once stored).

### Encryption in Transit (from PACKT)

Protects data while traveling over the network. PACKT lists best practices:

- **Use HTTPS endpoints** where possible to protect data with TLS
- **Use AWS PrivateLink** for private access to AWS services from your VPC
- **Use AWS Direct Connect** for secure connections with the on-premises environment (encryptable with IPsec)
- **SSL/TLS Certificates**: PACKT explains that TLS is the more modern protocol. When you connect to a secure site, the server presents the certificate to prove its authenticity

### AWS Certificate Manager — ACM (from PACKT)

PACKT describes ACM as the service that *"semplifica il provisioning, la gestione e il deploy di certificati SSL/TLS, che proteggono le comunicazioni di rete e verificano l'identità di siti web e risorse interne."*

Key characteristics:
- You can request **public and private** certificates
- **Automatic renewal** for continuous security without manual intervention
- Deploy with: **CloudFront, Elastic Load Balancing, API Gateway**
- Public certificates from ACM are **free**
- **AWS Private Certificate Authority (CA)** for private certificates for internal applications

> **Exam tip (PACKT Ch.12)**: *"Make sure you are familiar with how key policies work in KMS. You may be presented with an exam question that shows you a key policy and asks you to pick the correct answer about who can use or access the key."*

---

## AWS KMS — Key Management Service

### Overview (from PACKT and Dojo)

PACKT describes KMS as the service for *"creare, gestire e controllare chiavi crittografiche attraverso un'ampia gamma di servizi AWS."*

The Dojo adds an important technical detail: *"KMS è un servizio gestito che funziona quasi come CloudHSM. Sotto il cofano, KMS usa anche hardware security modules. Ma a differenza di CloudHSM, questo servizio ha accesso multi-tenant, il che significa che condividi l'HSM con altri tenant o clienti AWS."*

Key features (from PACKT):
- **Centralized key management** — manage keys for various AWS services from a single location
- **Key policies and IAM integration** — define permissions and access controls
- **Automatic key rotation** — to improve security
- **Auditing and logging** — monitor key usage with CloudTrail

### Key Types (from Dojo)

The Dojo provides the most detailed classification of CMKs (Customer Master Keys):

| Type | Who manages | Control | Notes |
|---|---|---|---|
| **Customer managed** | You | Full control: key policies, IAM policies, grants, enable/disable, rotation, tags, aliases, scheduling deletion | Maximum flexibility |
| **AWS managed** | AWS | You cannot manage, rotate, or change key policies. The service that creates them uses them on your behalf | Created automatically when you enable encryption on a service |
| **AWS owned** | AWS | You cannot view, use, track, or audit them | Used internally by AWS across multiple accounts |

The Dojo also specifies encryption types:
- **Symmetric** — AES 256-bit key used for encryption AND decryption
- **Asymmetric** — RSA key pair for encryption/decryption OR signing/verification (not both), or ECC pair for signing/verification

> **Dojo Note**: *"Symmetric CMKs and the private keys of asymmetric CMKs never leave AWS KMS unencrypted."*

### Envelope Encryption (from Dojo)

The Dojo explains the mechanism: *"AWS KMS usa envelope encryption, che è la pratica di cifrare i tuoi dati in chiaro con una data key; e poi cifrare quella data key usando un'altra chiave, chiamata master key."*

Important detail from the Dojo: *"Una CMK può essere usata per cifrare piccole quantità di dati (fino a 4096 byte). Se devi cifrare contenuti più grandi, usa la CMK per generare, cifrare e decifrare le data keys che vengono poi usate per cifrare i tuoi dati. Le data keys possono cifrare dati di qualsiasi dimensione e formato, inclusi dati in streaming."*

> **Dojo Note**: *"AWS KMS non salva né gestisce le data keys, e non puoi usare KMS per cifrare o decifrare con le data keys. AWS KMS gestisce solo le CMK."*

### Kimiko's Hands-on Walkthrough: Creating and Using a KMS Key

Kimiko shows the complete process in the console:

1. **View existing keys**: in the KMS console you see AWS managed keys (for Lambda, Redshift, Lightsail, etc.) and customer managed keys
2. **Create a key**: choose symmetric (for bulk data encryption, e.g. S3 bucket) or asymmetric (for authentication). Kimiko creates a symmetric key with alias `sample_symmetric_S3`
3. **Define key administrators**: who can manage the key administratively, including whether they can delete it
4. **Define who can use the key**: select IAM users or roles
5. **Review the automatically generated key policy**
6. **Use the key with S3**: go to bucket properties → Default encryption → choose AWS KMS → paste the custom key ARN

> **Insight from Kimiko**: *"Quando cifri un bucket con una chiave custom, devi modificare la bucket policy per lavorare con le impostazioni di encryption. Le put request senza informazioni di encryption verranno rifiutate se hai bucket policies che rifiutano tali richieste."*

### Key Rotation (from Dojo)

The Dojo provides the most complete details on rotation:

Advantages of automatic rotation:
1. The CMK properties (key ID, key ARN, region, policies, permissions) **do not change** when the key is rotated
2. **You don't need to change** applications or aliases that reference the CMK ID or ARN
3. AWS KMS rotates the CMK **automatically every year** — you don't need to remember or schedule the update

Limitations: automatic rotation is **not available** for:
- Asymmetric CMKs
- CMKs in custom key stores
- CMKs with imported key material

> **Dojo Note**: *"KMS salva il vecchio materiale crittografico così può essere usato per decifrare dati che ha cifrato. KMS non cancella nessun materiale ruotato finché non cancelli la CMK."*

### Key Deletion (from Kimiko)

Kimiko shows an important practical detail: *"Quando vuoi cancellare una chiave, devi schedulare la cancellazione. Questo è un bel safeguard contro la cancellazione di una chiave di cui hai disperatamente bisogno. Devi aspettare un minimo di 7 giorni prima che la chiave venga cancellata. Mentre è in pending deletion, puoi cancellare la cancellazione e reimplementare l'accesso alle risorse cifrate."*

---

## CloudHSM (from Dojo)

The Dojo provides the most detailed comparison between KMS and CloudHSM:

### When to Use KMS (from Dojo)

*"Le CMK di AWS KMS sono salvate in hardware security modules (HSM) validati FIPS che KMS gestisce (tenancy condivisa tra clienti AWS)."*

### When to Use CloudHSM (from Dojo)

*"Se preferisci gestire i tuoi HSM per salvare le chiavi in KMS, o se richiedi FIPS 140-2 Level 3, puoi usare AWS CloudHSM."*

The Dojo lists specific use cases for CloudHSM:
- **SSL/TLS offload** — you can offload cryptographic processing for HTTPS sessions to your CloudHSM module (not possible with KMS). This reduces the computational load on your servers
- **Protect private keys** for an issuing Certificate Authority (CA)
- **Transparent Data Encryption** for Oracle databases

### Custom Key Store (from Dojo)

The Dojo describes when to use a custom key store with CloudHSM:
1. Key material **cannot be stored in a shared environment**
2. Key material must be subject to a **secondary, independent audit path**
3. You need the ability to **immediately remove** key material from AWS KMS
4. HSMs must be certified **FIPS 140-2 Level 3**

> **Dojo Note**: custom key stores do not support creating asymmetric CMKs, and you cannot enable automatic rotation. Rotation must be done manually by creating new keys and remapping aliases.

---

## AWS Secrets Manager (from PACKT)

PACKT describes Secrets Manager as *"un servizio fully managed progettato per semplificare e migliorare la sicurezza della gestione di informazioni sensibili nel tuo ambiente AWS."*

### Key Characteristics (from PACKT)

- **Secure storage**: secrets are encrypted at rest using AWS KMS
- **Fine-grained IAM policies**: customize access controls
- **Automatic rotation**: automate rotation of secrets such as database passwords and API keys
- **Version control**: maintains a history of previous secret versions for audit and traceability
- **Logging with CloudTrail**: all interactions and API calls are logged
- **Integration with CloudFormation**: define and manage secrets as IaC resources

### Secret Rotation (from PACKT)

PACKT specifies two rotation modes:

| Mode | How it works | Supported services |
|---|---|---|
| **Managed rotation** | Secrets Manager configures and manages the rotation | Amazon Aurora, Amazon ECS, Amazon RDS, Amazon Redshift |
| **Lambda function rotation** | A Lambda function updates the secret and the service that uses it | Any service |

> **PACKT Note**: *"Per Aurora, RDS e Redshift, la managed rotation può ruotare solo le credenziali del master user o admin. Per qualsiasi altra rotazione di credenziali utente, si deve usare la Lambda function rotation."*

### Secrets Manager vs Parameter Store (from PACKT)

PACKT notes: *"C'è un servizio comparabile in Systems Manager chiamato Parameter Store. Parameter Store permette di salvare vari valori in chiaro necessari per diversi task di automazione, inclusi segreti che possono essere cifrati. Tuttavia, una distinzione significativa è nelle capacità di rotazione dei segreti. A differenza di Secrets Manager, Parameter Store non ha rotazione nativa."*

---

## Data Security Controls (from PACKT Ch.12)

PACKT Ch.12 summarizes data security controls for the exam in two categories:

### Controlling Data

- **Data access**: use IAM to restrict who can access managed database services. For self-hosted databases on EC2, configure authentication yourself and store passwords in **Secrets Manager**
- **The biggest problem**: *"Companies will often think deeply about how to mitigate malicious threats to their data, but the biggest problem facing their data is human error. A simple mistake can wipe out an entire database in seconds."*
- **RPO**: *"Pay attention to the exam question to work out whether an RPO has been defined and work backward from that."*
- **RTO**: *"If you store all of your data in cold storage, it can take several hours to restore your data."*
- **Data retention**: familiarize yourself with lifecycle policies in S3 and Intelligent-Tiering
- **Protection from accidental deletion**: S3 Versioning, S3 Object Lock, MFA delete, RDS database delete protection

### Encrypting Data (from PACKT Ch.12)

- *"Data should be encrypted throughout its life cycle. Encrypted at rest using AWS KMS and encrypted in transit using TLS and a certificate stored in ACM."*
- When managing your own keys in KMS, *"remember to ensure that you are locking down the key so that it can only be used and managed by the principals and applications that need access to it."*
- **Key rotation**: can be automated in KMS
- **Certificate renewal**: certificates have a limited validity and must be renewed. Know the process in ACM

---

## Example Questions from Kimiko

Kimiko proposes example questions at the end of the security section:

1. **Which IAM object is recommended for inter-service communication?** → **Role** (not user, not MFA, not group). Roles are not for interactive login, but for allowing one service to communicate with another service with the appropriate permissions.

2. **Which AWS service specializes in preventing DDoS attacks?** → **AWS Shield** (two versions: Standard included, Advanced paid for large implementations).

> **Tip from Kimiko**: *"Sii consapevole del servizio KMS e sei garantito di avere una o due domande su questo nel tuo ambiente di esame di certificazione."*

---

## Typical Exam Scenarios

### Scenario 1: Encrypt Large Data with KMS
**Question**: You need to encrypt 10GB files with KMS. How?

**Answer**: Use **envelope encryption** (Dojo). The CMK can only encrypt up to 4096 bytes. For larger data, use the CMK to generate a data key, then use the data key to encrypt the data.

### Scenario 2: FIPS 140-2 Level 3
**Question**: The company requires FIPS 140-2 Level 3 for key management.

**Answer**: **CloudHSM** (Dojo: *"If you require FIPS 140-2 Level 3, you may use AWS CloudHSM"*). KMS is multi-tenant and FIPS 140-2 Level 2.

### Scenario 3: Automatic DB Credential Rotation
**Question**: RDS database credentials must be rotated automatically.

**Answer**: **Secrets Manager** with managed rotation (PACKT). Parameter Store does not have native rotation.

### Scenario 4: SSL/TLS Processing Offload
**Question**: You want to reduce the SSL/TLS processing load on your web servers.

**Answer**: **CloudHSM** (Dojo: *"You can offload SSL/TLS cryptographic processing for HTTPS sessions to your CloudHSM module, which cannot be done on AWS KMS"*).

### Scenario 5: Key Policy on the Exam
**Question**: You are shown a key policy and asked who can use the key.

**Answer**: Read the key policy carefully (PACKT Ch.12: *"You may be presented with an exam question that shows you a key policy and asks you to pick the correct answer about who can use or access the key"*).

---

## Quick Recap for the Exam

- **Encryption at rest**: KMS for most services. S3 encrypts by default, EBS/RDS must be configured (PACKT)
- **Encryption in transit**: TLS/SSL with ACM certificates (free for AWS services) (PACKT)
- **KMS**: multi-tenant, FIPS 140-2 Level 2, centralized key management (Dojo)
- **CloudHSM**: single-tenant, FIPS 140-2 Level 3, SSL/TLS offload, Oracle TDE (Dojo)
- **CMK types**: Customer managed (full control), AWS managed (managed by AWS), AWS owned (invisible) (Dojo)
- **Envelope encryption**: CMK encrypts the data key, data key encrypts the data. CMK max 4096 bytes directly (Dojo)
- **Key rotation**: automatic every year for customer managed keys, not available for asymmetric/imported/custom key store (Dojo)
- **Key deletion**: minimum 7-day wait, cancellable during pending (Kimiko)
- **Secrets Manager**: automatic rotation (managed for Aurora/RDS/Redshift master user, Lambda for others) (PACKT)
- **Parameter Store**: similar but without native rotation (PACKT)
- **ACM**: free SSL certificates for CloudFront/ELB/API GW, automatic renewal (PACKT)
- **Data protection**: S3 Versioning + Object Lock + MFA delete for deletion protection (PACKT Ch.12)
- **Human error > malicious threats**: the biggest problem for data is human error (PACKT Ch.12)
