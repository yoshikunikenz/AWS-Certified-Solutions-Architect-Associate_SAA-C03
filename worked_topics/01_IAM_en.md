# IAM - Identity and Access Management

> Sources: PACKT Ch.3 (p.156-185), PACKT Ch.12 (p.502-517), KIMIKO (p.275-281), DOJO (p.204-210)

---

## What is IAM

IAM is the AWS web service that securely manages control and access to AWS resources. As the Dojo explains, it has two primary functions evident from its name: managing the **identity** of your users (authentication) and providing **access management** to your account's resources and services (authorization).

Key characteristics:
- **Global** — IAM is not tied to a Region. An IAM user created once is available across all Regions
- **Free** — you don't pay to create users, groups, roles, or policies
- **Eventually consistent** — policy changes propagate quickly but not instantaneously

---

## IAM Components

### Root Account

When you create an AWS account, the first user that automatically exists is the **root user** (Dojo). As Kimiko says in her practical walkthrough: *"Il root user è l'account amministratore 'godlike' del sistema. Può fare qualsiasi cosa. Dovremmo loggarci con questo account solo quando dobbiamo fare le poche operazioni che un normale account admin AWS non può fare"* — for example, changing the billing information associated with the account.

Best practices for the root account (from PACKT Ch.12):
- **Never use it for everyday operations** — PACKT is explicit: *"This root user should not be used for everyday tasks, and only used in the case of an emergency"*
- **Enable MFA** — Kimiko shows in the console that the IAM security status flags if MFA is not active on the root account
- **Don't create access keys for root** — if you create them, delete them
- **Physically protect the credentials** — PACKT even suggests writing down the password and storing it in a physical safe

> **Exam tip (PACKT Ch.12)**: *"A common question topic that features on the AWS SAA-C03 exam is around the root user. The key thing to remember is that the root user should never be used as a normal IAM user."*

### Users

PACKT compares IAM users to individual employees in a company. Each user has a unique identity within AWS and can receive access to various services and resources.

Each user can have:
- **Console access** — username + password for the AWS Management Console
- **Programmatic access** — Access Key ID + Secret Access Key for CLI, SDK, API
- **Both**

As Kimiko shows in her walkthrough: when you create a user, you decide whether they can have programmatic access to AWS and/or access to the Management Console, and you can set a custom or auto-generated password that the user will need to change at first login.

The Dojo adds an important practical example: *"Hai un nuovo Solutions Architect che ha bisogno solo di accesso ai template CloudFormation. Dopo aver creato un utente IAM, quali permessi dovresti dare senza compromettere la sicurezza? Come minimo, dovresti aggiungere l'utente a un gruppo IAM con una policy che permette solo azioni CloudFormation."* If you give them PowerUserAccess or AdministratorAccess, it's a security risk. If you give them the root user credentials, you're putting the entire cloud infrastructure at risk.

### Groups

PACKT compares groups to departments in a company, where each department has a certain set of permissions based on job function.

Group rules:
- A user can belong to **multiple groups**
- Groups **cannot contain other groups** (no nesting)
- Policies attached to the group apply to **all** users in the group

Kimiko shows the practical process in the console: when you create a user, you can add them to a group (scalable approach), add permissions directly, or copy them from an existing user. In her example, she creates an "S3 admin" group with the `AmazonS3FullAccess` policy and adds the user "student2" to it.

PACKT (Ch.12) highlights the operational advantage: *"By placing users in a group and applying a policy to that same group, you can implement restrictions to hundreds of users in one action, saving you vast amounts of operational overhead."*

### Roles

PACKT describes roles as job positions within a company, equipped with specific sets of permissions. The key difference from users: roles use **temporary security credentials**, not permanent ones.

Kimiko clarifies a point that often confuses students: *"I ruoli NON sono per gli utenti che fanno login. Sono per le risorse che interagiscono con altre risorse."* In her example: an EC2 instance that needs to read from an S3 bucket → you assign the "EasyToReadS3" role to the EC2 instance, and it uses the role to present the appropriate permissions to S3.

The Dojo adds important technical details about using roles with EC2: *"Per Amazon EC2, puoi usare l'instance profile per passare un ruolo IAM specifico alla tua istanza EC2. Questi ruoli IAM attaccati alla tua istanza possono essere visualizzati nei metadata EC2"* — with the command `curl http://169.254.169.254/latest/meta-data/iam/info`.

#### Main Role Use Cases (from PACKT)

| Use Case | Description |
|---|---|
| **EC2 Instance Role** | An EC2 instance that needs to access S3 → you assign it a role with S3 permissions |
| **Cross-Account Access** | An application needs to access resources in another account → you configure cross-account access with roles |
| **Identity Federation** | Users with external identities (corporate directory, mobile/web app) assume a role to temporarily access AWS |
| **Service Role** | An AWS service (e.g., Lambda) that needs to access other services |

> **Exam tip (PACKT Ch.12)**: *"It is best practice to configure federation and IAM roles to grant temporary credentials to your AWS accounts"* rather than using IAM users with permanent credentials.

---

## Policies

Policies are JSON documents that define permissions. PACKT describes them as *"the regulations that define who is authorized to do what"*.

### Policy Structure

PACKT provides this commented example — a policy that allows listing all S3 buckets and reading objects from a specific bucket:

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

The Dojo details the structure precisely:

- **Effect** — `Allow` or `Deny`. By default, IAM users have no permission to do anything, so all requests are implicitly denied. An explicit Allow overrides the default. An explicit Deny overrides any Allow.
- **Action** — the specific API actions you are granting or denying
- **Resource** — the affected resource, specified via ARN or wildcard `*`
- **Condition** — optional, for granular control

### Policy Conditions (from Dojo)

The Dojo lists the conditions you need to know for the exam:

| Condition | What it does |
|---|---|
| `StringEquals` | Exact string matching, case sensitive |
| `StringNotEquals` | Opposite of StringEquals |
| `StringLike` | Exact matching but ignores case |
| `StringNotLike` | Opposite of StringLike |
| `Bool` | Restricts access based on true/false values |
| `IpAddress` | Matches a specific IP or range |
| `NotIpAddress` | All IPs except the specified one |
| `ArnEquals`, `ArnLike` | ARN matching |
| `Null` | Checks if a condition key is present at the time of authorization |

> You can add `IfExists` to the end of any operator (except Null) — e.g., `StringLikeIfExists`.

### Policy Types

PACKT distinguishes between managed policies (created and managed by AWS or the user) and inline policies (attached directly to a user, group, or role).

The Dojo goes deeper with the fundamental distinction:

| Type | Where it attaches | Characteristic |
|---|---|---|
| **Identity-based** | Users, Groups, Roles | Defines what the identity can do |
| **Resource-based** | Resources (S3, SQS, etc.) | Includes a **Principal** field to specify who can access |
| **AWS Managed** | Predefined by AWS | Ready-to-use policies (e.g., `AmazonS3FullAccess`) |
| **Customer Managed** | Created by you | Custom policies |
| **Inline** | Embedded in a user/group/role | For permissions specific to a single entity |

The Dojo provides a concrete example of a resource-based policy on S3 with an IP condition:

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

> **Dojo Note**: Resource-based policies and resource-level permissions are two different things. Resource-based policies include a `Principal` element to specify which IAM identities can access the resource. Resource-level permissions refer to the ability to use ARNs to specify individual resources in a policy.

### IAM DB Authentication (from Dojo)

The Dojo mentions an important feature: **IAM DB Authentication for Amazon RDS and Aurora**. This feature allows you to use IAM to centrally manage access to database resources, eliminating the need to manage user access individually on each DB instance. It also improves the security of applications on EC2 because you don't have to store the database password — you use the instance profile to connect to RDS.

### Using IAM with Other Services (from Dojo)

| Service | How it uses IAM |
|---|---|
| **EC2** | Instance profile to pass an IAM role to the instance |
| **S3** | Bucket policy to grant cross-account access |
| **DynamoDB** | IAM policy to allow put/update/delete on specific tables |
| **SQS** | Access policy to control external access to the queue |
| **RDS/Aurora** | IAM DB Authentication for centralized access |

---

## Policy Evaluation Logic

This is FUNDAMENTAL for the exam. The Dojo provides the most comprehensive explanation with 4 levels of evaluation:

### The Process (from Dojo)

When a principal sends a request to AWS:
1. AWS **authenticates** the principal
2. AWS processes the information in the request to determine which policies apply
3. AWS **evaluates all policy types**, which influence the evaluation order
4. AWS processes the policies to determine whether the request is allowed or denied

### The 4 Evaluation Rules (from Dojo)

1. If **only identity-based policies** apply: AWS looks for at least one explicit Allow and verifies there is no explicit Deny
2. If **both resource-based and identity-based policies** apply: AWS looks for an Allow across all policies and verifies there is no explicit Deny
3. If there is a **permissions boundary**: the entity can only perform actions allowed by both the identity-based policies and the boundary. An implicit deny in the boundary does NOT limit permissions granted by a resource-based policy
4. If there is an **AWS Organizations SCP**: identity-based and resource-based policies grant permissions only if the SCP also allows the action. If both boundary and SCP are present, then boundary + SCP + identity-based policy must ALL allow the action without an explicit deny

### Evaluation Logic Summary (from Dojo)

- By default, all requests are **implicitly denied**. The root user has full access by default
- An **explicit Allow** in an identity-based or resource-based policy overrides the default
- If a **permissions boundary, SCP, or session policy** is present, it may override the Allow with an implicit deny
- An **explicit Deny** in any policy overrides any Allow

> **PACKT Ch.12 Note**: *"If an action is explicitly denied in one policy and explicitly allowed in another, and both policies are attached to an IAM principal, the deny policy will always take precedence."*

---

## Permission Boundaries

PACKT explains permission boundaries as a method for setting the **maximum permissions** that an IAM user or role can have, acting as guardrails in the organization's permission structure.

The Dojo defines: *"Una permissions boundary è una feature avanzata per usare una managed policy per impostare i permessi massimi che una identity-based policy può concedere a un'entità IAM. La boundary prende precedenza su una identity policy, quindi anche se i tuoi utenti attaccano privilegi Administrator ai loro account, non potranno eseguire azioni oltre quanto stabilito nella boundary."*

### PACKT Hands-on Lab: David and the Permission Boundary

PACKT presents a complete hands-on lab that perfectly illustrates how permission boundaries work:

**Scenario**: David is new to the infrastructure team. He needs access to certain AWS services, but must be limited so he doesn't accidentally launch expensive services.

**Steps**:
1. **Create a group** "Operators"
2. **Create the user** David with Management Console access, add him to the Operators group
3. **Create a custom policy** `EC2_S3_OperatorsPolicy`: Allow on all EC2 and S3 services, but Deny on `RunInstances` and `TerminateInstances`
4. **Create a permission boundary** `UserBoundary` with this policy:

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

5. **Attach the boundary** to David

**Test result** (in the Policy Simulator):
- All S3 actions are **DENIED** — even though David has a policy that gives him S3 access, the permission boundary only allows EC2 actions
- If you remove the boundary in the simulator, S3 actions return to Allow

> **PACKT Insight**: *"Even though he had an inline policy attached that gave those permissions [S3], he was unable to access S3"* — the boundary limits maximum permissions, it does not grant permissions.

### Practical Use Case for Boundaries (from PACKT)

PACKT describes a corporate scenario: an organization with multiple developer teams, each responsible for deploying and managing AWS applications. Each team can create and manage their own resources (EC2, S3, Lambda), but you want to ensure no developer can grant themselves excessive permissions (like admin access) that could lead to security risks or unexpected costs. Permission boundaries block the ability to grant additional privileges.

The Dojo adds: *"Quando hai utenti che lavorano su diversi progetti e ambienti, può essere difficile tenere traccia dei permessi necessari. A volte sarebbe più veloce lasciare che gli utenti attacchino le policy di cui hanno bisogno ai loro ruoli IAM. Questo può causare problemi di sicurezza. Puoi trovare un compromesso creando IAM permissions boundaries."*

---

## Identity Providers and Federation

### SAML 2.0 Federation (from PACKT)

PACKT describes the complete federated access process:

1. **Configure an external IdP** (Active Directory, Google, or any service that supports SAML 2.0) — this IdP manages logins and identities outside of AWS
2. **Create an IAM identity provider** in the AWS console that connects to the external IdP — provide the IdP details and upload a metadata file
3. **Create IAM roles** that users will assume when they log in — these roles define the allowed actions in AWS
4. **Configure a trust policy** for each role, specifying that only users authenticated by your IdP can use these roles
5. **The user logs in** through the external IdP with their existing credentials
6. **The IdP provides a SAML assertion** — a security token with user information
7. **AWS uses the SAML assertion** to determine which IAM role the user can assume
8. **The user exchanges the assertion** for temporary AWS credentials

> **PACKT Note**: temporary credentials expire. When that happens, the user must log in again through the IdP.

### Best Practices for Federation (from PACKT)

PACKT (Ch.12) is clear: *"The best practice is to use federated identities and IAM roles, granting individuals temporary credentials. This can be done using supported identity providers such as Google and Facebook, or using an existing identity directory such as Amazon Cognito or Azure AD/Entra ID. Once you have configured your identity store, you will use AWS STS to authenticate and temporarily assume a role."*

---

## RBAC — Role-Based Access Control (from PACKT Ch.12)

PACKT dedicates a specific section to the RBAC strategy:

*"When creating a robust RBAC strategy, it is important to define clear responsibilities for your roles. The worst thing that you could do is give admin permissions to everyone."*

Practical example from PACKT:
- **DevOps engineer**: needs write access to CodeBuild and S3, but does NOT need access to EKS or SageMaker
- **Data scientist**: needs only access to SageMaker

→ You create two separate roles: one for DevOps (only S3 + CodeBuild) and one for data scientist (only SageMaker).

PACKT also mentions **role switching**: an individual might have access to different roles. For example, an organization might move all IAM actions into a separate role to ensure individuals cannot grant themselves extra permissions. To use this other role, the individual uses role switching to assume another role.

---

## IAM Access Analyzer (from PACKT)

PACKT describes Access Analyzer as a tool that helps identify resources in your account that are shared with external entities or that are not in use and therefore don't follow the principle of least privilege.

Important details from PACKT:
- **It's regional** — you must create an audit run for each Region you operate in
- **Also checks unused Regions** — *"It is also worthwhile running it for all regions that you have access to, even if you do not use them for deployments, as hackers or bad actors can exploit these unused regions to operate unseen"*
- **Use tags** — PACKT recommends adding tags to all IAM roles and policies as a best practice. *"Most hackers will not follow any tagging requirements, as they need to operate as quickly as possible, and using tagging allows those roles and policies to be found and removed more quickly"*

---

## IAM Policy Simulator (from PACKT)

The Policy Simulator allows you to simulate how IAM policies will work in practice, without applying them in a live environment. PACKT describes it as particularly useful for administrators and security professionals.

Key features:
- Simulates permissions for any IAM user, group, or role
- Shows whether each action would be Allow or Deny
- Useful for testing new policies or changes before applying them
- Accessible via external link: `https://policysim.aws.amazon.com/`

> In the PACKT hands-on lab, the Policy Simulator is used to verify that David cannot access S3 due to the permission boundary.

---

## IAM at Scale (from PACKT Ch.12)

PACKT dedicates a section to managing IAM as the AWS platform grows:

*"As your AWS platform grows and begins to have more and more accounts, remember to leverage tools to simplify the management of IAM across your platform. Make use of SCPs to implement guardrails across your AWS organization and use Control Tower to ensure IAM roles and policies are standardized across your accounts."*

---

## Kimiko's Hands-on Challenge

Kimiko proposes a practical challenge:

1. **Create an IAM group** with the name tag "IAM Group R.D.S.R.O."
2. **Assign the group** a policy that allows read-only access to RDS
3. **Create an IAM user** and make sure they are a member of the created group
4. **The user must have** only Management Console access (no programmatic access)
5. **When finished**, delete all created resources
6. **Accept defaults** for any settings not explicitly specified

> **Tip from Kimiko**: *"Whenever possible, create those groups and those user accounts for your engineers. Really try and focus on an approach that has them operate with the least privilege as much as possible. And of course, avoid the use of the root account."*

---

## Typical Exam Scenarios

### Scenario 1: EC2 Access to S3 (from Dojo)
**Question**: An application on EC2 needs to upload data to S3. How do you configure access?

**Answer**: Use the **instance profile** to pass a specific IAM role to the EC2 instance. The role will have a policy that allows the necessary S3 actions. Never store credentials in code.

### Scenario 2: New Employee with Limited Access (from Dojo)
**Question**: A new Solutions Architect needs only access to CloudFormation. What do you do?

**Answer**: Create an IAM user, add them to a group with a policy that allows **only** CloudFormation actions. Do NOT give PowerUserAccess or AdministratorAccess.

### Scenario 3: Developers Who Must Not Self-Grant Admin (from PACKT)
**Question**: Developers need to create resources but must not be able to grant themselves admin permissions. How?

**Answer**: Use **permission boundaries**. Allow developers to create roles, but every role must have a boundary that limits maximum permissions.

### Scenario 4: Cross-Account Access (from PACKT Ch.12)
**Question**: An application needs to access resources in another account (e.g., centralized logging account).

**Answer**: Configure **cross-account access** with IAM roles, restricting the actions and permissions the application can execute and in which accounts.

### Scenario 5: Secure Database Access (from Dojo)
**Question**: How do you improve the security of RDS database access from EC2 instances?

**Answer**: Use **IAM DB Authentication** for RDS/Aurora. You don't need to store the database password — you use the EC2 instance profile to connect to RDS.

---

## Quick Recap for the Exam

- **Root account**: MFA mandatory, never use it for everyday operations (PACKT, Kimiko)
- **Least privilege**: give ONLY the necessary permissions (all sources)
- **Groups**: use groups to manage permissions, don't attach policies directly to users (Kimiko, PACKT)
- **Roles > Users** for applications and services: roles are for resources that interact with other resources (Kimiko), never access keys in code
- **Instance profile**: the way to attach a role to EC2, credentials visible in metadata (Dojo)
- **Explicit Deny always wins** over Allow (PACKT, Dojo)
- **4 evaluation levels**: identity policy → resource policy → permission boundary → SCP (Dojo)
- **Permission boundary**: limits the maximum permissions, does not grant permissions (PACKT lab with David)
- **Federation**: SAML 2.0 for enterprise, Cognito for web/mobile, STS for temporary credentials (PACKT)
- **RBAC**: define clear roles by job function, never admin for everyone (PACKT Ch.12)
- **IAM DB Authentication**: for RDS/Aurora, eliminates the need to store passwords (Dojo)
- **Access Analyzer**: regional, also checks unused Regions, use tags to find suspicious roles (PACKT)
- **Policy Simulator**: test policies before applying them, accessible via `policysim.aws.amazon.com` (PACKT)
- **IAM at Scale**: use SCP + Control Tower to standardize IAM across multiple accounts (PACKT Ch.12)
