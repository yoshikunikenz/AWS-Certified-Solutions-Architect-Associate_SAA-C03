#!/usr/bin/env python3
"""Generate comprehensive PDF study guides for AWS SAA-C03."""

from fpdf import FPDF
import os

class StudyGuidePDF(FPDF):
    def __init__(self, guide_title):
        super().__init__()
        self.guide_title = guide_title

    def header(self):
        if self.page_no() > 1:
            self.set_font('Helvetica', 'I', 9)
            self.set_text_color(150, 150, 150)
            self.cell(0, 8, f'AWS SAA-C03 | {self.guide_title}', align='R')
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Pagina {self.page_no()}/{{nb}}', align='C')

    def safe(self, text):
        r = {
            "\u2018":"'","\u2019":"'","\u201c":'"',"\u201d":'"',
            "\u2013":"-","\u2014":"-","\u2026":"...","\u2022":"-",
            "\u00e8":"e'","\u00e9":"e'","\u00e0":"a'","\u00f9":"u'",
            "\u00f2":"o'","\u00ec":"i'","\u20ac":"EUR","\u00e7":"c",
        }
        for k,v in r.items():
            text = text.replace(k,v)
        return text

    def add_cover(self, title, subtitle):
        self.add_page()
        self.ln(50)
        self.set_font('Helvetica', 'B', 32)
        self.set_text_color(255, 153, 0)
        self.cell(0, 15, 'AWS SAA-C03', align='C')
        self.ln(20)
        self.set_font('Helvetica', 'B', 24)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 12, self.safe(title), align='C')
        self.ln(10)
        self.set_font('Helvetica', '', 13)
        self.set_text_color(100, 100, 100)
        self.multi_cell(0, 8, self.safe(subtitle), align='C')
        self.ln(30)
        self.set_draw_color(255, 153, 0)
        self.set_line_width(1)
        self.line(60, self.get_y(), 150, self.get_y())
        self.ln(15)
        self.set_font('Helvetica', 'I', 11)
        self.set_text_color(130, 130, 130)
        self.cell(0, 8, 'Solutions Architect Associate', align='C')
        self.ln(8)
        self.cell(0, 8, 'Dispensa di Studio Approfondita', align='C')

    def write_content(self, text):
        for line in text.strip().split('\n'):
            sline = self.safe(line)
            stripped = sline.strip()
            if not stripped:
                self.ln(3)
                continue
            # Chapter title (## )
            if stripped.startswith('## '):
                self.add_page()
                self.set_font('Helvetica', 'B', 18)
                self.set_text_color(255, 153, 0)
                self.multi_cell(0, 10, stripped[3:])
                self.set_draw_color(255, 153, 0)
                self.set_line_width(0.6)
                self.line(10, self.get_y()+2, 200, self.get_y()+2)
                self.ln(8)
            # Section title (### )
            elif stripped.startswith('### '):
                self.ln(5)
                self.set_font('Helvetica', 'B', 13)
                self.set_text_color(50, 50, 50)
                self.multi_cell(0, 7, stripped[4:])
                self.ln(3)
            # Sub-section (#### )
            elif stripped.startswith('#### '):
                self.ln(3)
                self.set_font('Helvetica', 'BI', 11)
                self.set_text_color(80, 80, 80)
                self.multi_cell(0, 6, stripped[5:])
                self.ln(2)
            # Tip/exam box
            elif stripped.startswith('[TIP]') or stripped.startswith('[ESAME]'):
                self.ln(2)
                self.set_fill_color(255, 248, 230)
                self.set_draw_color(255, 153, 0)
                self.set_font('Helvetica', 'B', 10)
                self.set_text_color(180, 100, 0)
                tag = 'SUGGERIMENTO ESAME' if '[ESAME]' in stripped else 'TIP'
                content = stripped.replace('[TIP]','').replace('[ESAME]','').strip()
                y_before = self.get_y()
                self.set_x(15)
                self.multi_cell(180, 6, f'{tag}: {content}', border=1, fill=True)
                self.ln(3)
            # Bullet
            elif stripped.startswith('- '):
                self.set_font('Helvetica', '', 10)
                self.set_text_color(50, 50, 50)
                x = self.get_x()
                self.set_x(x + 5)
                self.cell(5, 6, '-')
                self.multi_cell(175, 6, stripped[2:])
                self.ln(1)
            # Numbered
            elif len(stripped) > 2 and stripped[0].isdigit() and stripped[1] in '.):':
                self.set_font('Helvetica', '', 10)
                self.set_text_color(50, 50, 50)
                self.set_x(self.get_x() + 3)
                self.multi_cell(185, 6, stripped)
                self.ln(1)
            # Normal paragraph
            else:
                self.set_font('Helvetica', '', 10)
                self.set_text_color(50, 50, 50)
                self.multi_cell(0, 6, stripped)
                self.ln(2)

def generate_pdf(filename, title, subtitle, content):
    pdf = StudyGuidePDF(title)
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_cover(title, subtitle)
    pdf.write_content(content)
    path = f'dispense/{filename}'
    pdf.output(path)
    print(f'  {path} ({pdf.page_no()} pagine)')

os.makedirs('dispense', exist_ok=True)

# ============================================================
# DISPENSA 1: STORAGE
# ============================================================
STORAGE = """
## Amazon S3: il cuore dello storage AWS

Amazon S3 (Simple Storage Service) e' probabilmente il servizio piu' importante di tutto l'ecosistema AWS, e sicuramente uno dei piu' presenti nell'esame SAA-C03. Si tratta di un servizio di object storage, il che significa che non funziona come un disco rigido tradizionale con file e cartelle, ma come un enorme contenitore di oggetti, ciascuno identificato da una chiave univoca all'interno di un bucket.

Ogni oggetto puo' avere una dimensione massima di 5TB, ma per upload superiori a 5GB e' obbligatorio usare il multipart upload, che spezza il file in parti caricate in parallelo. Questo e' un dettaglio che compare spesso nelle domande d'esame.

### Le classi di storage: quando usare quale

La scelta della classe di storage giusta e' uno degli argomenti piu' frequenti nell'esame. La logica di fondo e' semplice: piu' raramente accedi ai dati, meno paghi per lo storage, ma piu' paghi per il retrieval.

S3 Standard e' la classe predefinita. I dati sono replicati su almeno 3 Availability Zone, la disponibilita' e' del 99.99% e la durabilita' e' di 11 nove (99.999999999%). Usala quando accedi ai dati frequentemente e hai bisogno di bassa latenza.

S3 Intelligent-Tiering e' la scelta ideale quando non conosci il pattern di accesso dei tuoi dati. AWS sposta automaticamente gli oggetti tra un tier ad accesso frequente e uno ad accesso infrequente in base all'utilizzo reale. Non ci sono costi di retrieval, solo un piccolo costo di monitoraggio per oggetto. Nell'esame, quando la domanda dice "pattern di accesso imprevedibile" o "sconosciuto", Intelligent-Tiering e' quasi sempre la risposta giusta.

S3 Standard-IA (Infrequent Access) costa meno per lo storage rispetto a Standard, ma ha un costo per ogni retrieval. E' pensata per dati a cui accedi meno di una volta al mese ma che devono essere disponibili immediatamente quando servono. Attenzione: c'e' un minimo di 30 giorni di storage e un minimo di 128KB per oggetto.

S3 One Zone-IA e' identica a Standard-IA ma i dati risiedono in una sola AZ. Costa circa il 20% in meno. Usala solo per dati che puoi ricreare facilmente, come thumbnail, copie di backup secondarie o dati derivati. Se l'AZ ha un problema, perdi i dati.

[ESAME] Quando la domanda menziona "dati riproducibili" o "non critici" con accesso infrequente, la risposta e' spesso One Zone-IA.

### S3 Glacier: l'archivio a lungo termine

Le classi Glacier sono pensate per l'archiviazione a lungo termine, dove il costo di storage e' minimo ma il retrieval richiede tempo.

S3 Glacier Instant Retrieval offre retrieval in millisecondi, come Standard-IA, ma a un costo di storage ancora piu' basso. Ideale per dati acceduti una volta al trimestre, come archivi medici o dati di compliance.

S3 Glacier Flexible Retrieval (ex Glacier) offre tre velocita' di retrieval: Expedited (1-5 minuti), Standard (3-5 ore) e Bulk (5-12 ore, il piu' economico). Il minimo di storage e' 90 giorni.

S3 Glacier Deep Archive e' la classe piu' economica in assoluto. Il retrieval richiede 12 ore (Standard) o 48 ore (Bulk). Il minimo di storage e' 180 giorni. Pensala come il sostituto dei nastri magnetici.

[ESAME] Se la domanda parla di "compliance a 7 anni", "archivio legale" o "dati acceduti raramente", pensa a Glacier Deep Archive. Se serve accesso occasionale ma rapido, Glacier Instant Retrieval.

### Lifecycle Policies e Versioning

Le Lifecycle Policies permettono di automatizzare la transizione degli oggetti tra classi di storage. Ad esempio, puoi configurare una regola che sposta gli oggetti in Standard-IA dopo 30 giorni, in Glacier dopo 90 giorni e li cancella dopo 365 giorni. Questo e' fondamentale per ottimizzare i costi senza intervento manuale.

Il Versioning mantiene tutte le versioni di un oggetto. Quando sovrascrivi un file, la versione precedente non viene cancellata ma conservata. Quando cancelli un oggetto, S3 inserisce un "delete marker" ma le versioni precedenti restano. Il versioning e' un prerequisito per la Cross-Region Replication e per l'Object Lock.

[ESAME] Il versioning non puo' essere disabilitato una volta attivato, solo sospeso. Le versioni precedenti continuano a occupare spazio e a costare.

### Replica, Transfer Acceleration e accesso

Cross-Region Replication (CRR) copia automaticamente gli oggetti in un bucket in un'altra regione. E' utile per disaster recovery, compliance (dati in regioni specifiche) e riduzione della latenza per utenti globali. Richiede versioning abilitato su entrambi i bucket. La replica e' asincrona. Attenzione: gli oggetti esistenti prima dell'attivazione della replica NON vengono copiati automaticamente (serve S3 Batch Replication).

Same-Region Replication (SRR) funziona allo stesso modo ma nella stessa regione. Utile per aggregare log da piu' account o per mantenere copie in ambienti diversi (prod/test).

S3 Transfer Acceleration usa le edge location di CloudFront per velocizzare gli upload su lunghe distanze. Il client carica sulla edge location piu' vicina, e da li' i dati viaggiano sulla rete backbone di AWS fino al bucket. Nell'esame, quando si parla di "upload veloci da siti globali", Transfer Acceleration con multipart upload e' la risposta.

[ESAME] Transfer Acceleration + Multipart Upload e' la combinazione vincente per upload veloci da tutto il mondo verso un singolo bucket S3.

### Sicurezza e crittografia in S3

S3 offre diversi livelli di protezione. Le Bucket Policies sono documenti JSON che definiscono chi puo' fare cosa sul bucket. Sono lo strumento principale per il controllo degli accessi. Le ACL (Access Control Lists) sono un meccanismo piu' vecchio e meno flessibile, generalmente sconsigliato.

Per la crittografia server-side, ci sono tre opzioni: SSE-S3 usa chiavi gestite interamente da AWS ed e' il default dal gennaio 2023. SSE-KMS usa chiavi gestite tramite AWS KMS, il che ti da' un audit trail completo di chi ha usato la chiave e quando, oltre alla possibilita' di ruotare le chiavi. SSE-C ti permette di fornire la tua chiave ad ogni richiesta, e AWS la usa solo per criptare/decriptare senza conservarla.

I Pre-signed URLs permettono di dare accesso temporaneo a un oggetto privato. Generi un URL con una scadenza (da secondi a ore) e chiunque abbia quell'URL puo' scaricare (o caricare) l'oggetto fino alla scadenza. Molto usato per download di file da applicazioni web.

S3 Object Lock implementa il modello WORM (Write Once Read Many). In Governance Mode, solo utenti con permessi speciali possono modificare o cancellare gli oggetti. In Compliance Mode, nessuno puo' modificare o cancellare gli oggetti, nemmeno l'account root. Usato per requisiti di compliance normativa.

## Amazon EBS: block storage per EC2

Amazon EBS (Elastic Block Store) fornisce volumi di block storage che si collegano alle istanze EC2. A differenza di S3 che e' object storage, EBS funziona come un disco rigido virtuale: puoi formattarlo con un file system, installarci un sistema operativo, eseguire un database.

Un concetto fondamentale: un volume EBS esiste in una singola Availability Zone. Non puoi collegare un volume EBS in us-east-1a a un'istanza in us-east-1b. Per spostare dati tra AZ, devi creare uno snapshot e poi creare un nuovo volume dallo snapshot nell'altra AZ.

### Tipi di volume EBS

gp3 e' il volume SSD general purpose di nuova generazione. Offre 3000 IOPS e 125 MB/s di throughput come baseline, indipendentemente dalla dimensione. Puoi aumentare IOPS (fino a 16000) e throughput (fino a 1000 MB/s) in modo indipendente. E' il tipo di volume raccomandato per la maggior parte dei workload.

gp2 e' il predecessore di gp3. La differenza chiave e' che le IOPS sono legate alla dimensione del volume: 3 IOPS per GB, con un minimo di 100 IOPS e un massimo di 16000 IOPS. I volumi sotto i 1TB hanno un meccanismo di burst fino a 3000 IOPS. Nell'esame, se un'applicazione ha problemi di performance su gp2, la soluzione puo' essere aumentare la dimensione del volume (per ottenere piu' IOPS) o migrare a gp3.

io2 Block Express e' il top di gamma: fino a 256000 IOPS e 4000 MB/s. Pensato per database mission-critical come SAP HANA o Oracle. io1 e' la versione precedente con fino a 64000 IOPS. Entrambi supportano Multi-Attach, che permette di collegare lo stesso volume a piu' istanze EC2 nella stessa AZ (fino a 16 istanze). Questo e' utile per cluster di database che richiedono accesso condiviso allo storage.

st1 (Throughput Optimized HDD) e' un disco magnetico ottimizzato per letture sequenziali ad alto throughput. Ideale per big data, data warehouse, log processing. Non puo' essere usato come boot volume.

sc1 (Cold HDD) e' il tipo piu' economico. Per dati acceduti molto raramente. Nemmeno questo puo' essere boot volume.

[ESAME] Se la domanda parla di "database ad alte prestazioni" o "IOPS garantite", pensa a io2/io1. Se parla di "big data" o "throughput sequenziale", pensa a st1. Per tutto il resto, gp3.

### Snapshot e crittografia

Gli snapshot EBS sono backup incrementali salvati su S3 (ma non visibili nel tuo bucket). Solo i blocchi modificati dall'ultimo snapshot vengono copiati. Puoi copiare snapshot tra regioni per disaster recovery o per lanciare istanze in altre regioni.

La crittografia EBS usa AES-256 con chiavi KMS. Una volta creato un volume criptato, tutto e' criptato: dati a riposo, dati in transito tra istanza e volume, snapshot, e volumi creati dallo snapshot. Per criptare un volume esistente non criptato, devi: creare uno snapshot, copiare lo snapshot abilitando la crittografia, creare un nuovo volume dalla copia criptata.

## Amazon EFS: file system condiviso

Amazon EFS (Elastic File System) e' un file system NFS completamente gestito che puo' essere montato contemporaneamente da centinaia di istanze EC2 in diverse Availability Zone. Questa e' la differenza fondamentale rispetto a EBS: mentre EBS e' un disco collegato a una singola istanza in una singola AZ, EFS e' un file system di rete accessibile da ovunque nella regione.

EFS scala automaticamente da gigabyte a petabyte senza bisogno di provisioning. Paghi solo per lo spazio effettivamente utilizzato. Supporta il protocollo NFSv4.1, il che significa che funziona nativamente con istanze Linux ma NON con Windows (per Windows, usa FSx for Windows File Server).

Le performance mode sono due: General Purpose (la scelta predefinita, bassa latenza) e Max I/O (throughput piu' alto ma latenza leggermente superiore, per workload altamente paralleli come big data e media processing).

Per i throughput mode: Bursting scala il throughput in base alla dimensione del file system. Provisioned ti permette di specificare un throughput fisso indipendente dalla dimensione. Elastic (il piu' recente) scala automaticamente il throughput in base al carico.

EFS offre anche classi di storage: Standard e Infrequent Access (IA). Con una lifecycle policy, i file non acceduti per un periodo configurabile vengono spostati automaticamente in IA, riducendo i costi fino al 92%.

[ESAME] Quando la domanda richiede "storage condiviso tra piu' istanze EC2" o "file system accessibile da piu' AZ", la risposta e' EFS. Se le istanze sono Windows, la risposta e' FSx for Windows.

## Amazon FSx: file system specializzati

FSx for Windows File Server e' un file system Windows nativo completamente gestito. Supporta il protocollo SMB, si integra con Active Directory, supporta NTFS, DFS (Distributed File System) e puo' essere configurato in Multi-AZ per alta disponibilita'. E' la scelta giusta per qualsiasi workload Windows che richiede un file system condiviso: home directory, applicazioni .NET, SharePoint, SQL Server.

FSx for Lustre e' un file system parallelo ad altissime prestazioni, progettato per workload di High Performance Computing (HPC), machine learning e media processing. La caratteristica piu' importante per l'esame e' la sua integrazione nativa con S3: puoi "collegare" un bucket S3 a un file system Lustre, e Lustre presentera' gli oggetti S3 come file. Quando un'applicazione legge un file, Lustre lo carica automaticamente da S3. Quando scrive, i risultati possono essere sincronizzati su S3. Questo lo rende ideale per pipeline di elaborazione dati dove i dati di input sono su S3.

FSx for Lustre ha due modalita' di deployment: Scratch (storage temporaneo, nessuna replica, massime prestazioni, per elaborazioni brevi) e Persistent (dati replicati nella stessa AZ, per workload a lungo termine).

[ESAME] Se la domanda menziona "HPC", "machine learning" o "elaborazione dati da S3 ad alte prestazioni", la risposta e' FSx for Lustre. Se menziona "Windows", "SMB" o "Active Directory", e' FSx for Windows.

## Storage Gateway: il ponte verso il cloud

AWS Storage Gateway e' un servizio ibrido che collega il tuo ambiente on-premises allo storage cloud di AWS. Viene installato come appliance virtuale (VM) nel tuo data center e presenta lo storage cloud come se fosse storage locale.

S3 File Gateway espone un'interfaccia NFS o SMB che mappa direttamente su un bucket S3. I file scritti tramite il gateway vengono caricati su S3 come oggetti. Una cache locale mantiene i file acceduti di recente per garantire bassa latenza. E' la scelta ideale per migrare file share on-premises verso S3 mantenendo la compatibilita' con le applicazioni esistenti.

Volume Gateway offre volumi iSCSI. In modalita' Stored, i dati completi risiedono on-premises con snapshot asincroni su S3. In modalita' Cached, i dati primari sono su S3 con una cache locale per i dati frequenti. La modalita' Cached e' preferibile quando vuoi ridurre lo storage on-premises.

Tape Gateway emula una libreria di nastri virtuali (VTL) compatibile con i software di backup esistenti (Veeam, NetBackup, ecc.). I nastri virtuali vengono archiviati su S3 e possono essere spostati in Glacier per archiviazione a lungo termine. E' la soluzione per migrare i backup su nastro verso il cloud senza cambiare il software di backup.

[ESAME] Se la domanda parla di "migrare backup su nastro nel cloud", la risposta e' Tape Gateway. Se parla di "accesso NFS/SMB a S3 da on-premises", e' S3 File Gateway.

## Snow Family e DataSync: trasferimento dati massivo

La Snow Family e' una serie di dispositivi fisici per trasferire grandi quantita' di dati verso AWS quando la rete non e' sufficiente. La regola pratica: se il trasferimento via rete richiederebbe piu' di una settimana, considera Snow.

Snowcone e' il piu' piccolo: 8TB (HDD) o 14TB (SSD). Portatile, robusto, puo' essere spedito o portato a mano. Supporta anche edge computing con EC2 e IoT Greengrass.

Snowball Edge Storage Optimized offre 80TB di storage ed e' il dispositivo piu' comune per migrazioni dati. Snowball Edge Compute Optimized ha 42TB ma aggiunge capacita' di calcolo (CPU, GPU opzionale) per elaborazione locale.

Snowmobile e' letteralmente un container da camion con 100PB di capacita'. Per migrazioni su scala exabyte.

AWS DataSync e' un servizio di trasferimento dati automatizzato che funziona via rete (internet o Direct Connect). Trasferisce dati tra storage on-premises (NFS, SMB, HDFS) e servizi AWS (S3, EFS, FSx). E' fino a 10 volte piu' veloce degli strumenti open-source grazie a un protocollo ottimizzato. Include scheduling, verifica di integrita' e crittografia in transito.

[ESAME] Se c'e' una connessione internet/Direct Connect ad alta velocita', usa DataSync. Se la quantita' di dati e' enorme e la rete non basta, usa Snow Family. Se ogni sito ha gia' internet veloce e deve caricare su S3, usa S3 Transfer Acceleration.

## AWS Backup: gestione centralizzata dei backup

AWS Backup e' un servizio centralizzato per gestire i backup di praticamente tutti i servizi di storage e database AWS: EBS, RDS, Aurora, DynamoDB, EFS, FSx, EC2, S3. Definisci un Backup Plan con scheduling (ogni giorno, ogni settimana), retention (quanti giorni conservare) e regole di copia cross-region.

Vault Lock implementa il modello WORM per i backup: una volta bloccato, nessuno puo' cancellare i backup prima della scadenza della retention, nemmeno l'account root. Fondamentale per compliance normativa.

[ESAME] Quando la domanda chiede "soluzione centralizzata per backup di piu' servizi AWS" o "backup cross-region automatizzato", la risposta e' AWS Backup.
"""

print('Generazione dispense approfondite...\n')
generate_pdf('dispensa-01-Storage.pdf', 'Storage',
    'S3, EBS, EFS, FSx, Storage Gateway, Snow Family, DataSync, Backup', STORAGE)

# ============================================================
# DISPENSA 2: COMPUTE
# ============================================================
COMPUTE = """
## Amazon EC2: la spina dorsale del compute AWS

Amazon EC2 (Elastic Compute Cloud) e' il servizio di calcolo fondamentale di AWS. Ti permette di lanciare server virtuali (chiamati istanze) con il sistema operativo, la CPU, la memoria e lo storage che preferisci. Capire EC2 in profondita' e' essenziale per l'esame SAA-C03 perche' compare in quasi ogni scenario architetturale.

### Famiglie di istanze: scegliere quella giusta

Le istanze EC2 sono organizzate in famiglie, ciascuna ottimizzata per un tipo di workload specifico. Il nome di un'istanza segue il formato: famiglia + generazione + attributi + dimensione (es. m5.xlarge).

Le istanze General Purpose (serie M e T) offrono un bilanciamento tra CPU, memoria e rete. La serie T (T3, T4g) ha un meccanismo di crediti burst: accumula crediti quando la CPU e' sotto la baseline e li spende durante i picchi. Se i crediti si esauriscono, la performance cala. Questo le rende ideali per workload con utilizzo variabile come web server, ambienti di sviluppo e piccoli database. La serie M (M5, M6i, M7g) offre performance costanti senza burst, adatta per application server e backend.

Le istanze Compute Optimized (serie C) hanno il rapporto CPU/memoria piu' alto. Sono la scelta giusta per batch processing, encoding video, HPC, gaming server, machine learning inference e qualsiasi workload CPU-bound.

Le istanze Memory Optimized (serie R, X, z) hanno grandi quantita' di RAM. La serie R e' per database in-memory, cache distribuita e analytics real-time. La serie X ha ancora piu' memoria (fino a 4TB) per SAP HANA e database in-memory di grandi dimensioni.

Le istanze Storage Optimized (serie I, D, H) offrono alto throughput I/O verso storage locale (instance store). Ideali per database distribuiti come Cassandra, data warehouse e file system distribuiti come HDFS.

[ESAME] Quando la domanda descrive un workload, identifica se e' CPU-bound (C), memory-bound (R/X), storage-bound (I/D) o bilanciato (M/T). Questo ti guida verso la famiglia giusta.

### Modelli di acquisto: ottimizzare i costi

Questo e' uno degli argomenti piu' importanti dell'esame. AWS offre diversi modi per pagare le istanze EC2, e la scelta giusta puo' ridurre i costi fino al 90%.

On-Demand e' il modello predefinito: paghi al secondo (Linux) o all'ora (Windows) senza impegno. E' il piu' costoso ma il piu' flessibile. Usalo per workload imprevedibili, test, sviluppo o quando non puoi permetterti interruzioni.

Reserved Instances (RI) offrono sconti fino al 72% rispetto a On-Demand in cambio di un impegno di 1 o 3 anni. Le Standard RI sono legate a un tipo di istanza specifico e possono essere vendute sul Marketplace. Le Convertible RI permettono di cambiare tipo di istanza durante il periodo ma offrono uno sconto inferiore (fino al 54%). Puoi scegliere di pagare tutto anticipato (All Upfront, sconto massimo), parzialmente anticipato (Partial Upfront) o nulla anticipato (No Upfront, sconto minimo).

Savings Plans sono piu' flessibili delle RI. Ti impegni su una spesa oraria (es. $10/ora) per 1 o 3 anni. Compute Savings Plans si applicano a qualsiasi istanza EC2, Fargate e Lambda in qualsiasi regione. EC2 Instance Savings Plans sono legati a una famiglia di istanze in una regione specifica ma offrono uno sconto maggiore.

[ESAME] Se la domanda parla di "workload stabile e prevedibile per 3 anni", la risposta e' Reserved Instances o Savings Plans. Se chiede "massima flessibilita' con risparmio", Compute Savings Plans.

Spot Instances offrono sconti fino al 90% ma possono essere interrotte da AWS con 2 minuti di preavviso quando la capacita' e' necessaria. Sono perfette per workload fault-tolerant: batch processing, analisi dati, CI/CD, rendering, training di modelli ML. Non usarle mai per database o applicazioni stateful che non possono gestire interruzioni.

Una strategia comune e' combinare On-Demand o RI per il carico base con Spot per i picchi. Questo si implementa con un ASG che usa un mix di istanze On-Demand e Spot (Mixed Instances Policy).

Dedicated Hosts sono server fisici interamente dedicati a te. Il caso d'uso principale e' il BYOL (Bring Your Own License) per software con licenze legate al server fisico, come Oracle, SQL Server o Windows Server con licenze per-socket o per-core.

Dedicated Instances girano su hardware dedicato ma non hai controllo su quale server fisico. Meno costose dei Dedicated Hosts, utili quando hai requisiti di compliance che impediscono la condivisione dell'hardware.

### Placement Groups: controllare il posizionamento

I Placement Groups controllano come le istanze vengono distribuite sull'infrastruttura fisica.

Cluster posiziona tutte le istanze nella stessa rack (o rack adiacenti) nella stessa AZ. Offre la latenza di rete piu' bassa possibile e il throughput piu' alto (fino a 10 Gbps tra istanze). Usalo per HPC, applicazioni che richiedono comunicazione inter-nodo veloce. Il rischio e' che se la rack ha un problema, perdi tutte le istanze.

Spread distribuisce le istanze su hardware fisico diverso. Massimo 7 istanze per AZ per placement group. Ogni istanza e' su una rack separata con alimentazione e rete indipendenti. Usalo per applicazioni critiche dove vuoi massimizzare la disponibilita'.

Partition divide le istanze in partizioni logiche, ciascuna su rack separate. Fino a 7 partizioni per AZ, centinaia di istanze per partizione. Pensato per sistemi distribuiti come HDFS, HBase, Cassandra e Kafka che gestiscono la replica dei dati internamente.

[ESAME] "Bassa latenza tra istanze" = Cluster. "Massima disponibilita' per poche istanze critiche" = Spread. "Database distribuito" = Partition.

## Auto Scaling e Elastic Load Balancing

### Auto Scaling Group (ASG)

Un Auto Scaling Group gestisce automaticamente il numero di istanze EC2 in base alla domanda. Definisci una capacita' minima (il minimo di istanze sempre attive), una capacita' massima (il limite superiore) e una capacita' desiderata (il target attuale).

Le scaling policy determinano quando e come scalare. Target Tracking e' la piu' semplice: specifichi un target (es. "mantieni la CPU media al 50%") e ASG aggiunge o rimuove istanze per raggiungerlo. Step Scaling definisce azioni diverse per soglie diverse (es. "aggiungi 2 istanze se CPU > 70%, aggiungi 4 se CPU > 90%"). Scheduled Scaling scala in base a un calendario (es. "aggiungi 10 istanze ogni lunedi' alle 8:00"). Predictive Scaling usa il machine learning per analizzare i pattern storici e scalare in anticipo.

Il cooldown period e' il tempo di attesa dopo un'azione di scaling prima che ne possa avvenire un'altra. Serve a evitare oscillazioni (scaling su e giu' continuo). Il default e' 300 secondi.

L'ASG esegue health check per verificare che le istanze siano funzionanti. Puo' usare gli health check EC2 (l'istanza risponde ai check di sistema?) o gli health check ELB (l'applicazione risponde correttamente?). Le istanze che falliscono vengono terminate e sostituite automaticamente.

Il Launch Template definisce la configurazione delle nuove istanze: AMI, tipo di istanza, security group, key pair, user data, IAM role. E' il successore del Launch Configuration e supporta funzionalita' aggiuntive come il versioning e il mix di tipi di istanza.

[ESAME] Se la domanda chiede "come garantire che un'applicazione gestisca i picchi di traffico automaticamente", la risposta coinvolge quasi sempre ASG + ELB.

### Elastic Load Balancer (ELB)

L'Application Load Balancer (ALB) opera al Layer 7 (HTTP/HTTPS) ed e' il tipo piu' usato. Supporta routing basato sul path (/api/* verso un target group, /images/* verso un altro), routing basato sull'hostname (api.example.com verso un target, www.example.com verso un altro), e routing basato su header, query string o IP sorgente. I target possono essere istanze EC2, indirizzi IP, funzioni Lambda o container. ALB supporta sticky sessions (tramite cookie), WebSocket, HTTP/2 e gRPC. Si integra con WAF per la protezione da attacchi web e con Cognito per l'autenticazione.

Il Network Load Balancer (NLB) opera al Layer 4 (TCP/UDP/TLS). E' progettato per performance estreme: gestisce milioni di richieste al secondo con latenza ultra-bassa (microsecondi). Ogni NLB ha un IP statico per AZ (puoi anche assegnare Elastic IP). Usalo quando hai bisogno di performance massime, protocolli non-HTTP (es. gaming, IoT, VoIP), o quando i client devono connettersi a un IP fisso.

Il Gateway Load Balancer (GWLB) opera al Layer 3 ed e' progettato per inserire appliance di rete (firewall, IDS/IPS, deep packet inspection) nel flusso del traffico in modo trasparente. Usa il protocollo GENEVE per incapsulare il traffico.

[ESAME] "HTTP/HTTPS con routing avanzato" = ALB. "Performance massime, IP statico, TCP/UDP" = NLB. "Appliance di rete trasparenti" = GWLB.

Il Cross-Zone Load Balancing distribuisce il traffico uniformemente tra tutte le istanze registrate in tutte le AZ, indipendentemente dalla distribuzione del traffico tra le AZ. E' abilitato di default su ALB (gratuito) e disabilitato di default su NLB (a pagamento se abilitato).

## Container: ECS, EKS e Fargate

Amazon ECS (Elastic Container Service) e' l'orchestratore di container nativo di AWS. Gestisce il ciclo di vita dei container Docker: deployment, scaling, networking, service discovery. Una Task Definition e' il blueprint che descrive uno o piu' container: quale immagine usare, quanta CPU e memoria allocare, quali porte esporre, quali volumi montare. Un Service mantiene un numero desiderato di task in esecuzione e li integra con un load balancer.

ECS puo' funzionare in due modalita': EC2 launch type, dove gestisci tu le istanze EC2 che ospitano i container, e Fargate launch type, dove AWS gestisce l'infrastruttura e tu ti preoccupi solo dei container. Fargate e' la scelta serverless: paghi per le risorse (vCPU e memoria) usate dal container, senza gestire server.

Amazon EKS (Elastic Kubernetes Service) e' Kubernetes gestito da AWS. Se la tua organizzazione usa gia' Kubernetes o ha bisogno di portabilita' multi-cloud, EKS e' la scelta giusta. Supporta sia EC2 che Fargate come worker nodes.

[ESAME] Se la domanda menziona "Docker" o "container" senza specificare Kubernetes, pensa a ECS + Fargate. Se menziona "Kubernetes" o "portabilita'", pensa a EKS.

## AWS Lambda e il paradigma serverless

AWS Lambda e' il servizio di compute serverless di AWS. Carichi il tuo codice (una funzione), definisci un trigger (un evento che la attiva) e Lambda si occupa di tutto il resto: provisioning dei server, scaling, patching, alta disponibilita'. Paghi solo per il tempo di esecuzione effettivo, misurato in millisecondi.

Lambda ha alcuni limiti importanti da ricordare per l'esame: il timeout massimo e' 15 minuti (se il tuo processo richiede piu' tempo, Lambda non e' la scelta giusta), la memoria va da 128MB a 10GB (la CPU scala proporzionalmente alla memoria), e lo storage temporaneo in /tmp arriva fino a 10GB.

La concurrency e' il numero di esecuzioni simultanee. Il default e' 1000 per regione. La Reserved Concurrency riserva una quota per una funzione specifica (garantisce che abbia sempre capacita' ma limita anche il massimo). La Provisioned Concurrency mantiene un numero di istanze "calde" pronte a rispondere, eliminando il cold start (il ritardo della prima invocazione quando Lambda deve inizializzare un nuovo ambiente).

Lambda@Edge e CloudFront Functions permettono di eseguire codice ai margini della rete CDN di CloudFront. Lambda@Edge e' piu' potente (fino a 10 secondi, accesso a rete) ed e' utile per manipolazione di richieste/risposte, autenticazione, A/B testing. CloudFront Functions e' piu' leggera (sub-millisecondo, solo JavaScript) per manipolazioni semplici di header, URL rewriting, redirect.

[ESAME] Se il workload e' event-driven, dura meno di 15 minuti e non richiede stato persistente, Lambda e' quasi sempre la risposta. Se la domanda menziona "cold start" come problema, la soluzione e' Provisioned Concurrency.

## Elastic Beanstalk: PaaS su AWS

Elastic Beanstalk e' la soluzione Platform-as-a-Service di AWS. Carichi il tuo codice e Beanstalk si occupa di creare e gestire l'infrastruttura: istanze EC2, Auto Scaling Group, Load Balancer, e opzionalmente un database RDS. Supporta Java, .NET, PHP, Node.js, Python, Ruby, Go e Docker.

Beanstalk offre diversi metodi di deployment: All at once (veloce ma con downtime), Rolling (aggiorna un batch alla volta), Rolling with additional batch (aggiunge istanze prima di aggiornare per mantenere la capacita'), Immutable (crea un nuovo ASG con la nuova versione e poi fa swap), e Blue/Green (crea un ambiente completamente nuovo e usa Route 53 per switchare il traffico).

[ESAME] Beanstalk e' la risposta quando la domanda chiede "il modo piu' semplice per deployare un'applicazione web" o "ridurre la complessita' operativa" senza andare completamente serverless.
"""

generate_pdf('dispensa-02-Compute.pdf', 'Compute',
    'EC2, Auto Scaling, ELB, ECS, EKS, Fargate, Lambda, Beanstalk', COMPUTE)

# ============================================================
# DISPENSA 3: NETWORKING
# ============================================================
NETWORKING = """
## Amazon VPC: la tua rete privata nel cloud

Ogni volta che crei risorse in AWS, queste vivono all'interno di una Virtual Private Cloud (VPC). Una VPC e' una rete virtuale isolata che tu controlli completamente: definisci il range di indirizzi IP, crei subnet, configuri route table e gestisci i gateway. Capire la VPC in profondita' e' fondamentale per l'esame perche' quasi ogni scenario architetturale coinvolge decisioni di networking.

Una VPC e' regione-specifica e il suo range IP e' definito da un blocco CIDR (es. 10.0.0.0/16, che fornisce 65536 indirizzi). Puoi aggiungere blocchi CIDR secondari se hai bisogno di piu' indirizzi. All'interno della VPC, crei subnet in specifiche Availability Zone.

### Subnet pubbliche e private

Una subnet e' pubblica se la sua route table ha una route verso un Internet Gateway (IGW). L'Internet Gateway e' il componente che permette la comunicazione bidirezionale tra la VPC e internet. Ce n'e' uno solo per VPC ed e' altamente disponibile di default.

Una subnet e' privata se NON ha una route verso l'IGW. Le risorse in una subnet privata non sono raggiungibili da internet e non possono accedere a internet direttamente. Per permettere a queste risorse di accedere a internet (es. per scaricare aggiornamenti), si usa un NAT Gateway.

Il NAT Gateway e' un servizio managed che traduce gli indirizzi IP privati in un indirizzo IP pubblico per il traffico in uscita. E' unidirezionale: le risorse private possono raggiungere internet, ma internet non puo' raggiungere le risorse private. Il NAT Gateway risiede in una subnet pubblica e va creato in ogni AZ dove hai risorse che necessitano di accesso a internet, per garantire alta disponibilita'.

[ESAME] Architettura tipica: subnet pubblica con ALB e NAT Gateway, subnet privata con istanze EC2 e database. Le istanze private accedono a internet tramite il NAT Gateway per aggiornamenti, ma non sono raggiungibili dall'esterno.

### Security Groups e Network ACL

I Security Groups sono firewall stateful a livello di istanza (o piu' precisamente, a livello di interfaccia di rete). "Stateful" significa che se permetti il traffico in entrata, la risposta in uscita e' automaticamente permessa. Supportano solo regole ALLOW (non puoi creare regole DENY). Di default, un security group blocca tutto il traffico in entrata e permette tutto il traffico in uscita.

Una caratteristica potente dei Security Groups e' la possibilita' di referenziare altri Security Groups nelle regole. Ad esempio, puoi dire "permetti traffico sulla porta 3306 dal Security Group del web server". Questo e' molto piu' flessibile e sicuro che specificare indirizzi IP, perche' funziona indipendentemente dagli IP delle istanze.

Le Network ACL (NACL) sono firewall stateless a livello di subnet. "Stateless" significa che devi definire regole sia per il traffico in entrata che per quello in uscita esplicitamente. Supportano sia regole ALLOW che DENY, valutate in ordine numerico (la prima regola che corrisponde viene applicata). La NACL di default permette tutto il traffico. Le NACL custom negano tutto di default.

[ESAME] Se la domanda chiede "come bloccare un indirizzo IP specifico", la risposta e' NACL (perche' supporta regole DENY). I Security Groups non possono bloccare IP specifici, possono solo permettere.

### VPC Endpoints: accesso privato ai servizi AWS

Normalmente, quando un'istanza EC2 in una subnet privata deve accedere a S3 o DynamoDB, il traffico deve passare attraverso il NAT Gateway e internet. I VPC Endpoints eliminano questa necessita', permettendo l'accesso diretto ai servizi AWS attraverso la rete privata di AWS.

I Gateway Endpoints sono disponibili solo per S3 e DynamoDB. Sono gratuiti e funzionano aggiungendo una route nella route table della subnet. Sono la scelta predefinita per accedere a S3 e DynamoDB da subnet private.

Gli Interface Endpoints (powered by AWS PrivateLink) creano un'interfaccia di rete elastica (ENI) con un indirizzo IP privato nella tua subnet. Sono disponibili per la maggior parte dei servizi AWS e anche per servizi di terze parti. Hanno un costo orario e per GB di dati trasferiti. Possono essere acceduti da on-premises tramite VPN o Direct Connect.

[ESAME] Se la domanda chiede "come accedere a S3 da una subnet privata senza passare per internet", la risposta e' un Gateway Endpoint per S3. Se chiede accesso privato ad altri servizi, Interface Endpoint.

### VPC Peering e Flow Logs

VPC Peering crea una connessione diretta tra due VPC, permettendo alle risorse di comunicare usando indirizzi IP privati come se fossero nella stessa rete. Funziona tra VPC nello stesso account, in account diversi e anche in regioni diverse. Pero' il peering NON e' transitivo: se VPC A e' in peering con VPC B, e VPC B con VPC C, A e C non possono comunicare automaticamente. Per quello serve un Transit Gateway.

VPC Flow Logs catturano informazioni sul traffico IP che attraversa le interfacce di rete nella tua VPC. Puoi abilitarli a livello di VPC, subnet o singola interfaccia di rete. I log possono essere inviati a CloudWatch Logs o S3. Sono utili per troubleshooting di connettivita', analisi di sicurezza e compliance.

## Connettivita' ibrida: VPN e Direct Connect

### AWS Site-to-Site VPN

Una VPN Site-to-Site crea un tunnel IPsec criptato tra il tuo data center e la tua VPC attraverso internet. Lato AWS, configuri un Virtual Private Gateway (VGW) collegato alla VPC. Lato on-premises, configuri un Customer Gateway (che rappresenta il tuo dispositivo VPN).

AWS crea automaticamente due tunnel VPN per alta disponibilita' (ciascuno attraverso un endpoint diverso). La bandwidth massima e' circa 1.25 Gbps per tunnel. Il setup e' rapido (minuti) e il costo e' basso, il che la rende ideale per connettivita' immediata o come backup per Direct Connect.

### AWS Direct Connect

Direct Connect e' una connessione fisica dedicata tra il tuo data center e AWS, attraverso un partner di colocation. A differenza della VPN che passa per internet, Direct Connect offre bandwidth consistente (1 Gbps o 10 Gbps per connessioni dedicate, da 50 Mbps a 10 Gbps per connessioni hosted) e latenza prevedibile.

Il setup richiede settimane o mesi perche' coinvolge l'installazione fisica di cavi. Per questo motivo, molte architetture usano una VPN come connessione iniziale o di backup mentre Direct Connect viene provisionato.

Direct Connect NON e' criptato di default. Per aggiungere crittografia, puoi configurare una VPN IPsec sopra la connessione Direct Connect. Questo e' un dettaglio che compare spesso nell'esame.

Per accedere a VPC in piu' regioni da una singola connessione Direct Connect, usa un Direct Connect Gateway. Per la resilienza, configura due connessioni Direct Connect in location diverse.

[ESAME] "Connessione dedicata con latenza consistente" = Direct Connect. "Connessione rapida e criptata" = VPN. "Direct Connect con crittografia" = VPN over Direct Connect. "Backup per Direct Connect" = VPN Site-to-Site.

### AWS Transit Gateway

Transit Gateway e' un hub di rete regionale che semplifica la connettivita' tra VPC, VPN e Direct Connect. Invece di creare peering point-to-point tra ogni coppia di VPC (che diventa ingestibile con molte VPC), colleghi tutte le VPC al Transit Gateway e il routing e' automatico.

Transit Gateway supporta routing transitivo (a differenza del VPC Peering), route table multiple per segmentare il traffico, peering tra Transit Gateway in regioni diverse, e multicast. E' la soluzione per architetture hub-and-spoke con molte VPC.

[ESAME] Se la domanda descrive "molte VPC che devono comunicare tra loro" o "topologia hub-and-spoke", la risposta e' Transit Gateway.

## Amazon CloudFront: CDN globale

CloudFront e' la Content Delivery Network di AWS con oltre 400 edge location nel mondo. Quando un utente richiede un contenuto, CloudFront lo serve dalla edge location piu' vicina. Se il contenuto non e' in cache, lo recupera dall'origine (S3, ALB, EC2 o qualsiasi server HTTP) e lo memorizza per le richieste successive.

L'Origin Access Control (OAC) e' il meccanismo per garantire che un bucket S3 sia accessibile solo tramite CloudFront e non direttamente. Configuri una policy sul bucket che permette l'accesso solo all'identita' CloudFront.

I Cache Behaviors definiscono come CloudFront gestisce le richieste per path diversi. Ad esempio, puoi configurare /api/* per inoltrare sempre all'ALB senza cache, e /* per servire contenuti statici da S3 con cache lunga.

Le Signed URLs e i Signed Cookies permettono di distribuire contenuti privati. Una Signed URL da' accesso a un singolo file con una scadenza. I Signed Cookies danno accesso a piu' file (utile per streaming video o aree riservate di un sito).

Lambda@Edge permette di eseguire funzioni Lambda nelle edge location di CloudFront, intercettando le richieste e le risposte in quattro punti: viewer request, origin request, origin response, viewer response. Casi d'uso: autenticazione, A/B testing, manipolazione di header, redirect basati sulla geolocalizzazione.

[ESAME] "Ridurre la latenza per utenti globali" = CloudFront. "Accesso sicuro a S3 solo tramite CDN" = OAC. "Contenuti privati con scadenza" = Signed URLs.

## Amazon Route 53: DNS e routing intelligente

Route 53 e' il servizio DNS managed di AWS. Oltre alla risoluzione DNS standard, offre routing intelligente del traffico e health checking.

Il record Alias e' specifico di AWS e merita attenzione speciale. A differenza di un CNAME (che non puo' essere usato per il dominio apex, es. example.com), un Alias puo' puntare a risorse AWS (ELB, CloudFront, S3 website, ecc.) anche per il dominio apex. Le query Alias verso risorse AWS sono gratuite.

Le routing policy determinano come Route 53 risponde alle query DNS. Simple restituisce uno o piu' valori senza logica particolare. Weighted distribuisce il traffico in percentuale tra risorse diverse, perfetto per blue/green deployment graduali. Latency-based instrada verso la regione AWS con la latenza piu' bassa per l'utente. Failover implementa un pattern active-passive con health check. Geolocation instrada in base alla posizione geografica dell'utente (utile per compliance o contenuti localizzati). Geoproximity instrada in base alla distanza geografica con la possibilita' di usare un bias per spostare traffico. Multi-value e' come Simple ma con health check su ogni valore.

[ESAME] "Distribuzione graduale del traffico tra due versioni" = Weighted. "Utenti instradati alla regione piu' veloce" = Latency-based. "Failover automatico" = Failover con health check. "Utenti europei verso server europei" = Geolocation.

## AWS Global Accelerator

Global Accelerator e' spesso confuso con CloudFront nell'esame, ma ha uno scopo diverso. Fornisce due indirizzi IP anycast statici come punto di ingresso globale. Il traffico degli utenti entra nella rete AWS dalla edge location piu' vicina e viaggia sulla rete privata AWS (molto piu' veloce e affidabile di internet) fino all'endpoint nella regione di destinazione.

La differenza chiave con CloudFront: CloudFront e' un CDN che fa cache di contenuti HTTP/HTTPS. Global Accelerator non fa cache, ma ottimizza il percorso di rete per qualsiasi traffico TCP/UDP. Usa Global Accelerator per applicazioni non-HTTP (gaming, IoT, VoIP), quando hai bisogno di IP statici, o quando vuoi failover rapido tra regioni per applicazioni TCP.

[ESAME] "IP statici globali" o "applicazioni TCP/UDP con bassa latenza globale" = Global Accelerator. "Cache di contenuti web" = CloudFront.
"""

generate_pdf('dispensa-03-Networking.pdf', 'Networking',
    'VPC, Subnet, VPN, Direct Connect, Transit Gateway, CloudFront, Route 53, Global Accelerator', NETWORKING)

# ============================================================
# DISPENSA 4: DATABASES
# ============================================================
DATABASES = """
## Amazon RDS: database relazionali gestiti

Amazon RDS (Relational Database Service) elimina il lavoro operativo di gestire un database relazionale: provisioning hardware, patching, backup, replica. Tu ti concentri sullo schema e sulle query, AWS si occupa dell'infrastruttura.

RDS supporta sei engine: MySQL, PostgreSQL, MariaDB, Oracle, SQL Server e IBM Db2. La scelta dell'engine dipende dalle tue esigenze applicative e dalle licenze esistenti.

### Multi-AZ: alta disponibilita'

Multi-AZ crea una replica sincrona del database in un'altra Availability Zone. La replica standby NON e' accessibile per le letture: esiste solo per il failover. Se l'istanza primaria ha un problema, RDS esegue automaticamente il failover verso lo standby in 1-2 minuti. Il DNS endpoint rimane lo stesso, quindi l'applicazione non deve essere modificata.

Multi-AZ e' per alta disponibilita', non per performance. Se hai bisogno di scalare le letture, usa le Read Replicas.

### Read Replicas: scalare le letture

Le Read Replicas sono copie asincrone del database che puoi usare per le query di lettura. Puoi creare fino a 15 repliche per un database RDS. Ogni replica ha il suo endpoint DNS. L'applicazione deve essere modificata per inviare le letture alle repliche e le scritture al primario.

Le repliche possono essere nella stessa regione, in una regione diversa (Cross-Region Read Replica) o addirittura promosse a database standalone indipendente. La replica cross-region e' utile per disaster recovery e per ridurre la latenza per utenti in altre regioni.

[ESAME] "Migliorare le performance di lettura" = Read Replicas. "Alta disponibilita' con failover automatico" = Multi-AZ. Spesso la risposta corretta e' entrambi.

### Backup, crittografia e RDS Proxy

I backup automatici creano uno snapshot giornaliero e salvano i transaction log ogni 5 minuti. Questo permette il point-in-time recovery: puoi ripristinare il database a qualsiasi secondo negli ultimi 1-35 giorni (configurabile). Gli snapshot manuali persistono anche dopo la cancellazione del database.

La crittografia at-rest usa KMS e deve essere abilitata alla creazione del database. Non puoi criptare un database esistente direttamente: devi creare uno snapshot, copiarlo con crittografia abilitata, e ripristinare da quello.

RDS Proxy e' un servizio di connection pooling che si posiziona tra l'applicazione e il database. Mantiene un pool di connessioni aperte verso RDS, riducendo il tempo di failover del 66% e gestendo meglio i picchi di connessioni. E' particolarmente utile con Lambda, dove ogni invocazione potrebbe aprire una nuova connessione.

## Amazon Aurora: il database cloud-native

Aurora e' il database relazionale progettato da AWS specificamente per il cloud. E' compatibile con MySQL e PostgreSQL (puoi usare gli stessi driver e strumenti), ma l'architettura sottostante e' completamente diversa e offre performance fino a 5 volte superiori a MySQL e 3 volte superiori a PostgreSQL.

L'architettura di Aurora separa compute e storage. Lo storage e' distribuito su 3 AZ con 6 copie dei dati. Aurora puo' continuare a funzionare anche perdendo 2 copie per le scritture o 3 copie per le letture. Lo storage scala automaticamente da 10GB a 128TB senza intervento.

Aurora ha due tipi di endpoint: il Writer Endpoint punta sempre all'istanza primaria (per le scritture), il Reader Endpoint fa load balancing tra tutte le Read Replicas (fino a 15). Questo semplifica la configurazione dell'applicazione.

### Aurora Serverless e Global Database

Aurora Serverless v2 scala automaticamente la capacita' di calcolo in base al carico. La capacita' e' misurata in ACU (Aurora Capacity Units) e scala in incrementi di 0.5 ACU. Paghi per gli ACU effettivamente usati al secondo. E' ideale per workload imprevedibili, ambienti di sviluppo, e applicazioni con traffico intermittente.

Aurora Global Database replica i dati in fino a 5 regioni secondarie con un lag tipico inferiore a 1 secondo. In caso di disastro regionale, puoi promuovere una regione secondaria a primaria in meno di 1 minuto. E' la soluzione per disaster recovery cross-region con RPO e RTO minimi.

[ESAME] "Database relazionale con massime performance e disponibilita'" = Aurora. "Workload imprevedibile senza gestire capacita'" = Aurora Serverless. "Disaster recovery cross-region con RPO < 1 secondo" = Aurora Global Database.

## Amazon DynamoDB: NoSQL serverless

DynamoDB e' un database NoSQL key-value e document completamente serverless. Non ci sono server da gestire, la capacita' scala automaticamente, e la latenza e' single-digit millisecond a qualsiasi scala.

Ogni tabella ha una partition key (obbligatoria) che determina come i dati sono distribuiti. Puoi aggiungere una sort key per creare chiavi composite e permettere query range. La scelta delle chiavi e' critica per le performance: una partition key con alta cardinalita' distribuisce il carico uniformemente.

### Capacity modes e DAX

DynamoDB offre due modalita' di capacita'. On-Demand paga per ogni lettura e scrittura, senza provisioning. E' ideale per workload imprevedibili o nuove applicazioni. Provisioned definisce RCU (Read Capacity Units) e WCU (Write Capacity Units) in anticipo, con la possibilita' di abilitare auto-scaling. E' piu' economico per workload prevedibili.

DynamoDB Accelerator (DAX) e' una cache in-memory completamente compatibile con l'API DynamoDB. Riduce la latenza da millisecondi a microsecondi per le letture. L'applicazione punta a DAX invece che a DynamoDB, e DAX gestisce la cache in modo trasparente.

### Global Tables e Streams

Global Tables replica automaticamente una tabella DynamoDB in piu' regioni con un modello active-active: puoi scrivere in qualsiasi regione e le modifiche si propagano alle altre. Richiede DynamoDB Streams abilitato.

DynamoDB Streams cattura ogni modifica alla tabella (insert, update, delete) in un log ordinato. Puoi collegare una funzione Lambda che reagisce alle modifiche in tempo reale. Casi d'uso: trigger per elaborazioni, replica verso altri sistemi, audit log.

[ESAME] "Database NoSQL serverless con latenza garantita" = DynamoDB. "Cache per DynamoDB" = DAX. "Replica multi-region active-active" = Global Tables.

## ElastiCache: cache in-memory

ElastiCache offre due engine: Redis e Memcached. La scelta dipende dalle tue esigenze.

Redis supporta strutture dati avanzate (liste, set, sorted set, hash), persistence su disco, replica con failover automatico, cluster mode per sharding, pub/sub messaging e scripting Lua. E' la scelta per la maggior parte dei casi d'uso: session store, leaderboard, geospatial, caching complesso.

Memcached e' piu' semplice: puro key-value caching, multi-threaded, nessuna persistence o replica. E' la scelta quando hai bisogno solo di caching semplice e vuoi sfruttare il multi-threading.

Le strategie di caching piu' comuni sono Lazy Loading (carica in cache solo quando richiesto e non presente) e Write-Through (scrivi in cache ad ogni scrittura nel database). Lazy Loading puo' servire dati stale, Write-Through ha latenza di scrittura piu' alta.

[ESAME] "Cache con alta disponibilita' e persistence" = Redis. "Caching semplice multi-threaded" = Memcached.

## Amazon Redshift: data warehouse

Redshift e' un data warehouse colonnare basato su PostgreSQL, progettato per analytics su petabyte di dati. A differenza di RDS che e' ottimizzato per transazioni (OLTP), Redshift e' ottimizzato per query analitiche complesse su grandi volumi di dati (OLAP).

Redshift Spectrum permette di eseguire query su dati in S3 senza caricarli in Redshift. Puoi unire dati in Redshift con dati in S3 nella stessa query. Redshift Serverless scala automaticamente la capacita' senza gestire cluster.

Redshift NON e' Multi-AZ. Per alta disponibilita', usa cluster multi-nodo (i dati sono replicati tra i nodi) e snapshot automatici, che possono essere copiati in altre regioni.

[ESAME] "Analytics su petabyte di dati" = Redshift. "Query su dati in S3 senza caricarli" = Redshift Spectrum.
"""

generate_pdf('dispensa-04-Databases.pdf', 'Databases',
    'RDS, Aurora, DynamoDB, ElastiCache, Redshift', DATABASES)

# ============================================================
# DISPENSA 5: SECURITY
# ============================================================
SECURITY = """
## AWS IAM: il fondamento della sicurezza

IAM (Identity and Access Management) e' il servizio che controlla chi puo' fare cosa nel tuo account AWS. Ogni singola azione in AWS, che sia lanciare un'istanza EC2, leggere un oggetto da S3 o creare una tabella DynamoDB, passa attraverso IAM. Capire IAM in profondita' e' assolutamente essenziale per l'esame SAA-C03.

### Utenti, Gruppi e Ruoli

Un IAM User rappresenta una persona o un'applicazione che interagisce con AWS. Ogni utente puo' avere credenziali per la console (password) e/o credenziali programmatiche (access key ID + secret access key). La best practice e' non usare mai l'utente root per le operazioni quotidiane: crea un utente IAM con permessi di amministratore e usa quello.

I Groups sono raccolte di utenti. Quando assegni una policy a un gruppo, tutti gli utenti del gruppo ereditano quei permessi. Ad esempio, puoi creare un gruppo "Developers" con permessi su EC2 e S3, e un gruppo "DBAdmins" con permessi su RDS. Un utente puo' appartenere a piu' gruppi. I gruppi non possono contenere altri gruppi.

I Roles sono identita' temporanee che possono essere "assunte" da utenti, servizi AWS o entita' esterne. A differenza degli utenti, i ruoli non hanno credenziali permanenti: quando qualcuno assume un ruolo, riceve credenziali temporanee tramite STS (Security Token Service) che scadono dopo un periodo configurabile.

I casi d'uso piu' importanti dei ruoli per l'esame sono: EC2 Instance Role (permette a un'istanza EC2 di accedere ad altri servizi AWS senza dover memorizzare access key nel codice), Cross-Account Role (permette a utenti di un altro account AWS di accedere alle tue risorse), e Service-Linked Role (ruoli predefiniti che i servizi AWS usano per operare nel tuo account).

[ESAME] Se la domanda chiede "come permettere a un'istanza EC2 di accedere a S3 in modo sicuro", la risposta e' sempre un IAM Role associato all'istanza, MAI access key hardcoded nel codice o nell'istanza.

### Policy IAM: il linguaggio dei permessi

Le policy IAM sono documenti JSON che definiscono i permessi. Ogni policy contiene uno o piu' statement con questi elementi: Effect (Allow o Deny), Action (quali operazioni, es. s3:GetObject), Resource (su quali risorse, es. arn:aws:s3:::my-bucket/*), e opzionalmente Condition (condizioni aggiuntive, es. solo da un certo IP o solo con MFA).

Ci sono tre tipi di policy: AWS Managed Policies (create e mantenute da AWS, come AmazonS3ReadOnlyAccess), Customer Managed Policies (create da te, riutilizzabili tra utenti/gruppi/ruoli), e Inline Policies (incorporate direttamente in un singolo utente/gruppo/ruolo, non riutilizzabili).

La logica di valutazione delle policy segue un principio fondamentale: di default tutto e' negato (implicit deny). Se una policy concede un Allow, l'azione e' permessa. Ma se qualsiasi policy contiene un Deny esplicito, questo vince sempre su qualsiasi Allow. In sintesi: Explicit Deny > Allow > Implicit Deny.

I Permission Boundaries sono un meccanismo avanzato che definisce il massimo dei permessi che un utente o ruolo puo' avere. Anche se una policy concede un permesso, se il Permission Boundary non lo include, l'azione e' negata. Sono utili per delegare la creazione di ruoli senza rischiare escalation di privilegi.

### MFA e sicurezza dell'account

Multi-Factor Authentication (MFA) aggiunge un secondo fattore di autenticazione oltre alla password. AWS supporta dispositivi MFA virtuali (app come Google Authenticator), token hardware U2F (YubiKey) e token hardware TOTP. E' fortemente raccomandato abilitare MFA sull'account root e su tutti gli utenti con accesso alla console.

Puoi anche richiedere MFA nelle policy IAM usando la condizione aws:MultiFactorAuthPresent. Ad esempio, puoi permettere la cancellazione di oggetti S3 solo se l'utente ha completato l'autenticazione MFA.

[ESAME] Se la domanda chiede "come proteggere operazioni critiche come la cancellazione di risorse", la risposta spesso coinvolge una policy con condizione MFA.

### Service Control Policies (SCP)

Le SCP fanno parte di AWS Organizations e definiscono i limiti massimi di permessi per gli account o le Organizational Units (OU). Le SCP non concedono permessi: li limitano. Anche se un utente ha una policy che concede un'azione, se la SCP dell'account non la permette, l'azione e' negata.

Le SCP non si applicano al management account (l'account principale dell'organizzazione). Questo e' un dettaglio importante per l'esame.

[ESAME] "Impedire a tutti gli utenti di un account di usare una regione specifica" o "impedire la disabilitazione di CloudTrail" = SCP in AWS Organizations.

## Crittografia: KMS, CloudHSM e ACM

### AWS KMS: gestione centralizzata delle chiavi

AWS KMS (Key Management Service) e' il servizio centrale per la crittografia in AWS. Quasi tutti i servizi AWS che offrono crittografia (S3, EBS, RDS, DynamoDB, ecc.) si integrano con KMS per la gestione delle chiavi.

KMS gestisce Customer Master Keys (CMK), ora chiamate semplicemente KMS Keys. Ci sono tre tipi: AWS Managed Keys (create e gestite automaticamente da AWS per ogni servizio, con nome aws/s3, aws/ebs, ecc.), Customer Managed Keys (create e gestite da te, con pieno controllo su policy, rotazione e audit), e AWS Owned Keys (usate internamente da AWS, non visibili nel tuo account).

Le chiavi KMS possono essere simmetriche (AES-256, usate dalla maggior parte dei servizi AWS) o asimmetriche (RSA o ECC, per operazioni di encrypt/decrypt o sign/verify fuori da AWS). Le chiavi simmetriche non lasciano mai KMS in chiaro: le operazioni di crittografia avvengono all'interno del servizio.

Per criptare grandi quantita' di dati, KMS usa l'Envelope Encryption. Il processo e': chiami GenerateDataKey, KMS ti restituisce una data key in chiaro e una copia criptata della stessa. Usi la data key in chiaro per criptare i tuoi dati localmente, poi la scarti e conservi solo la versione criptata insieme ai dati. Per decriptare, invii la data key criptata a KMS che te la restituisce in chiaro.

La rotazione automatica delle chiavi e' disponibile per le Customer Managed Keys: ogni anno viene generata una nuova chiave crittografica, ma il key ID rimane lo stesso. I dati criptati con la vecchia chiave possono ancora essere decriptati.

Le Multi-Region Keys sono repliche della stessa chiave in piu' regioni. Hanno lo stesso materiale crittografico, quindi i dati criptati in una regione possono essere decriptati in un'altra senza dover ri-criptare. Utili per disaster recovery e applicazioni globali.

[ESAME] "Audit trail di chi ha usato una chiave di crittografia" = KMS con Customer Managed Key (CloudTrail registra ogni chiamata). "Crittografia con controllo completo sulle chiavi" = Customer Managed Key. "Crittografia di default senza gestione" = AWS Managed Key.

### AWS CloudHSM

CloudHSM fornisce Hardware Security Module dedicati nel cloud. A differenza di KMS dove AWS gestisce l'infrastruttura delle chiavi, con CloudHSM hai il controllo esclusivo: AWS non ha accesso alle tue chiavi. I moduli sono certificati FIPS 140-2 Level 3 (KMS e' Level 2).

CloudHSM e' la scelta quando hai requisiti di compliance stringenti che richiedono hardware dedicato, quando devi fare SSL/TLS offloading ad alte prestazioni, o quando usi Oracle Transparent Data Encryption (TDE). I cluster CloudHSM possono essere distribuiti su piu' AZ per alta disponibilita'.

[ESAME] "FIPS 140-2 Level 3" o "controllo esclusivo delle chiavi" o "Oracle TDE" = CloudHSM.

### AWS Certificate Manager (ACM)

ACM gestisce certificati SSL/TLS. Puoi richiedere certificati gratuiti emessi da Amazon o importare certificati di terze parti. I certificati emessi da ACM si rinnovano automaticamente.

ACM si integra nativamente con ALB, CloudFront, API Gateway e NLB. Per EC2, non puoi usare certificati ACM direttamente: devi importare il certificato manualmente sull'istanza.

[ESAME] "Certificato SSL gratuito con rinnovo automatico per un ALB" = ACM.

## Protezione delle applicazioni: WAF, Shield, Firewall Manager

### AWS WAF

AWS WAF (Web Application Firewall) protegge le applicazioni web da attacchi comuni come SQL injection, cross-site scripting (XSS), e bot malevoli. Si applica a CloudFront, ALB, API Gateway e AppSync.

WAF funziona con Web ACL (Access Control List) che contengono regole. Le regole possono essere: IP match (blocca o permetti IP specifici), geo match (blocca traffico da paesi specifici), rate-based (blocca IP che superano una soglia di richieste al secondo), string/regex match (cerca pattern nelle richieste), e size constraint (limita la dimensione delle richieste).

AWS fornisce Managed Rule Groups predefiniti che coprono le vulnerabilita' OWASP Top 10, la protezione da bot, e pattern di attacco noti. Puoi combinare regole managed con regole custom.

[ESAME] "Proteggere un'applicazione web da SQL injection" = WAF su ALB o CloudFront. "Bloccare IP che fanno troppe richieste" = WAF rate-based rule.

### AWS Shield

Shield protegge dagli attacchi DDoS (Distributed Denial of Service). Shield Standard e' gratuito e automaticamente attivo per tutti i clienti AWS. Protegge dagli attacchi piu' comuni a Layer 3 e Layer 4 (SYN flood, UDP reflection, ecc.).

Shield Advanced costa $3000 al mese e offre protezione avanzata per EC2, ELB, CloudFront, Global Accelerator e Route 53. Include: protezione DDoS a Layer 7, accesso al DDoS Response Team (DRT) di AWS 24/7, metriche e report avanzati, e cost protection (AWS rimborsa i costi di scaling causati da un attacco DDoS).

[ESAME] "Protezione DDoS avanzata con supporto 24/7" = Shield Advanced. "Protezione DDoS base" = Shield Standard (gia' incluso).

### AWS Firewall Manager

Firewall Manager permette di gestire centralmente le regole di sicurezza su piu' account in un'organizzazione AWS. Puoi definire policy di sicurezza per WAF, Shield Advanced, Security Groups e Network Firewall, e applicarle automaticamente a tutti gli account e le risorse.

[ESAME] "Gestire WAF rules su tutti gli account dell'organizzazione" = Firewall Manager.

## Rilevamento delle minacce: GuardDuty, Inspector, Macie

### Amazon GuardDuty

GuardDuty e' un servizio di threat detection intelligente che analizza continuamente diverse fonti di dati: CloudTrail Management Events, CloudTrail S3 Data Events, VPC Flow Logs, DNS Logs, e opzionalmente EKS Audit Logs e Lambda Network Activity.

Usando machine learning e threat intelligence, GuardDuty rileva attivita' sospette come: account compromessi (chiamate API da IP malevoli, disabilitazione di logging), istanze compromesse (comunicazione con server di command & control, crypto mining), e reconnaissance (scansione di porte, enumerazione di risorse).

I findings di GuardDuty possono essere inviati a EventBridge per attivare risposte automatiche. Ad esempio, puoi configurare una Lambda che isola automaticamente un'istanza compromessa modificando il suo Security Group.

[ESAME] "Rilevare attivita' sospette nell'account AWS" o "rilevare crypto mining su EC2" = GuardDuty.

### Amazon Inspector

Inspector esegue vulnerability assessment automatizzati su istanze EC2, immagini container in ECR e funzioni Lambda. Scansiona per vulnerabilita' note (CVE), problemi di network reachability e deviazioni dalle best practice.

Inspector assegna un severity score a ogni finding e suggerisce la remediation. Si integra con Security Hub per una vista centralizzata.

### Amazon Macie

Macie usa machine learning per scoprire e proteggere dati sensibili (PII, dati finanziari, credenziali) nei bucket S3. Classifica automaticamente i dati e genera alert quando rileva accessi anomali o configurazioni rischiose.

[ESAME] "Scoprire dati sensibili in S3" = Macie. "Vulnerability scanning su EC2 e container" = Inspector.

## Gestione delle identita': Cognito, IAM Identity Center

### Amazon Cognito

Cognito gestisce l'autenticazione e l'autorizzazione per applicazioni web e mobile. Ha due componenti principali.

User Pools sono directory di utenti. Gestiscono la registrazione, il login, il recupero password, e l'MFA. Supportano social login (Google, Facebook, Apple), SAML e OpenID Connect. Quando un utente si autentica, User Pool restituisce un JWT token che l'applicazione usa per le chiamate API.

Identity Pools (Federated Identities) forniscono credenziali AWS temporanee per accedere direttamente ai servizi AWS (S3, DynamoDB, ecc.). Possono autenticare utenti da User Pools, social providers, SAML, o anche utenti anonimi (guest access).

Il flusso tipico e': l'utente si autentica con User Pool, riceve un JWT token, lo presenta a Identity Pool, che restituisce credenziali AWS temporanee con permessi definiti da un IAM Role.

[ESAME] "Autenticazione per un'app mobile con social login" = Cognito User Pools. "Accesso diretto a S3 da un'app mobile" = Cognito Identity Pools. Spesso la risposta coinvolge entrambi.

### AWS IAM Identity Center (ex SSO)

IAM Identity Center fornisce Single Sign-On centralizzato per tutti gli account AWS nell'organizzazione e per applicazioni cloud di terze parti (Salesforce, Slack, ecc.). Si integra con Active Directory (on-premises o AWS Managed AD) e con identity provider SAML 2.0.

I Permission Sets definiscono i permessi che un utente ha in ogni account AWS. Puoi assegnare permission set diversi allo stesso utente per account diversi.

[ESAME] "SSO per accedere a piu' account AWS" = IAM Identity Center.

## Gestione dei segreti: Secrets Manager e Parameter Store

### AWS Secrets Manager

Secrets Manager e' progettato specificamente per gestire segreti come password di database, API key e token. La sua caratteristica distintiva e' la rotazione automatica: puo' ruotare automaticamente le credenziali di RDS, Redshift e DocumentDB senza downtime per l'applicazione.

Secrets Manager cripta i segreti con KMS e fornisce un'API per recuperarli programmaticamente. Le applicazioni non devono mai memorizzare segreti nel codice o nei file di configurazione.

### AWS Systems Manager Parameter Store

Parameter Store e' un key-value store per configurazioni e segreti. E' piu' semplice e meno costoso di Secrets Manager. I parametri possono essere String, StringList o SecureString (criptato con KMS).

Parameter Store supporta una gerarchia di parametri (es. /app/prod/db-password, /app/dev/db-password) e policy di accesso granulari tramite IAM. Non ha rotazione automatica nativa (devi implementarla tu con Lambda).

[ESAME] "Rotazione automatica delle credenziali del database" = Secrets Manager. "Configurazioni e segreti con costo minimo" = Parameter Store. Se la domanda non menziona la rotazione, Parameter Store e' spesso sufficiente.

## AWS Directory Service

AWS Managed Microsoft AD e' un Active Directory completo gestito da AWS. Supporta trust bidirezionale con AD on-premises, permettendo agli utenti on-premises di accedere a risorse AWS e viceversa. E' la scelta per workload che richiedono un AD completo (applicazioni .NET, SQL Server, SharePoint).

AD Connector e' un proxy che reindirizza le richieste di autenticazione al tuo AD on-premises. Non memorizza dati in cloud. E' la scelta quando vuoi usare il tuo AD esistente senza replicarlo in AWS.

Simple AD e' una directory standalone basata su Samba, per esigenze semplici e piccole (fino a 5000 utenti). Non supporta trust con altri AD.

[ESAME] "Estendere Active Directory on-premises in AWS" = AWS Managed Microsoft AD con trust. "Usare AD on-premises per autenticazione AWS senza replica" = AD Connector.
"""

print('  Security...')
generate_pdf('dispensa-05-Security.pdf', 'Security',
    'IAM, KMS, CloudHSM, ACM, WAF, Shield, GuardDuty, Inspector, Macie, Cognito', SECURITY)

# ============================================================
# DISPENSA 6: SERVERLESS & APPLICATION INTEGRATION
# ============================================================
SERVERLESS = """
## Amazon SQS: code di messaggi

Amazon SQS (Simple Queue Service) e' un servizio di message queuing completamente gestito che permette di disaccoppiare i componenti di un'applicazione. Un produttore invia messaggi alla coda, un consumatore li legge e li elabora. Se il consumatore e' temporaneamente non disponibile, i messaggi restano in coda fino a quando non viene ripristinato.

### Standard Queue vs FIFO Queue

Le Standard Queue offrono throughput praticamente illimitato e sono la scelta predefinita. Hanno due caratteristiche importanti da ricordare: at-least-once delivery (un messaggio potrebbe essere consegnato piu' di una volta, quindi il consumatore deve essere idempotente) e best-effort ordering (l'ordine dei messaggi non e' garantito).

Le FIFO Queue garantiscono che i messaggi siano consegnati esattamente una volta (exactly-once processing) e nell'ordine esatto in cui sono stati inviati. Il throughput e' limitato a 300 messaggi al secondo senza batching, o 3000 con batching. Il nome della coda deve terminare con .fifo.

Le FIFO Queue usano due concetti importanti: il Message Group ID raggruppa i messaggi che devono mantenere l'ordine tra loro (messaggi con group ID diversi possono essere elaborati in parallelo), e il Deduplication ID previene l'invio di messaggi duplicati in una finestra di 5 minuti.

[ESAME] "Ordine garantito dei messaggi" = FIFO Queue. "Throughput massimo" = Standard Queue. "Elaborazione esattamente una volta" = FIFO Queue.

### Visibility Timeout e Dead Letter Queue

Quando un consumatore legge un messaggio dalla coda, il messaggio non viene cancellato immediatamente ma diventa invisibile per un periodo chiamato Visibility Timeout (default 30 secondi). Se il consumatore elabora il messaggio con successo, lo cancella esplicitamente. Se il consumatore fallisce o va in timeout, il messaggio torna visibile e puo' essere elaborato da un altro consumatore.

Se un messaggio fallisce ripetutamente (il numero di tentativi e' configurabile con maxReceiveCount), viene spostato in una Dead Letter Queue (DLQ). La DLQ e' una coda separata dove puoi analizzare i messaggi problematici, fare debug e decidere come gestirli. E' una best practice configurare sempre una DLQ.

Il Long Polling riduce il numero di chiamate API vuote. Invece di ritornare immediatamente se la coda e' vuota, SQS aspetta fino a 20 secondi per un messaggio. Questo riduce i costi e migliora l'efficienza.

[ESAME] "Messaggi che falliscono ripetutamente" = Dead Letter Queue. "Ridurre le chiamate API a SQS" = Long Polling.

### SQS con Lambda e Auto Scaling

Lambda puo' essere configurato come consumatore di una coda SQS. Lambda poll automaticamente la coda e invoca la funzione per ogni batch di messaggi. Se l'elaborazione fallisce, i messaggi tornano visibili nella coda.

Per scalare consumatori EC2 in base alla lunghezza della coda, usa la metrica CloudWatch ApproximateNumberOfMessagesVisible come trigger per un Auto Scaling Group. Piu' messaggi in coda, piu' istanze vengono lanciate.

## Amazon SNS: pub/sub messaging

Amazon SNS (Simple Notification Service) implementa il pattern publish/subscribe. Un publisher invia un messaggio a un Topic, e SNS lo distribuisce a tutti i subscriber del topic. A differenza di SQS dove un messaggio viene elaborato da un solo consumatore, con SNS lo stesso messaggio raggiunge tutti i subscriber.

I subscriber possono essere: code SQS, funzioni Lambda, endpoint HTTP/HTTPS, email, SMS, e notifiche push mobile. Questo permette il pattern fan-out: un singolo evento puo' attivare elaborazioni multiple in parallelo.

Il pattern SNS + SQS fan-out e' molto comune: un messaggio viene pubblicato su un topic SNS che ha multiple code SQS come subscriber. Ogni coda riceve una copia del messaggio e puo' elaborarlo indipendentemente. Questo disaccoppia completamente il publisher dai consumatori.

SNS supporta anche FIFO Topics (solo con SQS FIFO come subscriber) e Message Filtering: ogni subscriber puo' definire una filter policy per ricevere solo i messaggi che corrispondono a certi attributi.

[ESAME] "Un evento deve attivare piu' elaborazioni in parallelo" = SNS fan-out. "Notificare piu' sistemi di un evento" = SNS Topic.

## Amazon EventBridge: event bus serverless

EventBridge (precedentemente CloudWatch Events) e' un event bus serverless che connette applicazioni usando eventi. E' l'evoluzione di SNS per architetture event-driven complesse.

EventBridge ha tre tipi di event bus: il Default Event Bus riceve eventi dai servizi AWS (un'istanza EC2 che cambia stato, un oggetto caricato su S3, ecc.), i Custom Event Bus ricevono eventi dalle tue applicazioni, e i Partner Event Bus ricevono eventi da applicazioni SaaS di terze parti (Zendesk, Datadog, Auth0, ecc.).

Le Rules definiscono quali eventi catturare (tramite pattern matching sul contenuto dell'evento) e dove inviarli (target). I target possono essere Lambda, SQS, SNS, Step Functions, Kinesis, e molti altri servizi AWS.

EventBridge ha funzionalita' avanzate che SNS non ha: Schema Registry (scopre e registra automaticamente la struttura degli eventi), Archive and Replay (archivia gli eventi e permette di riprodurli per debug o recovery), e Scheduler (cron e rate expressions per eventi schedulati).

[ESAME] "Reagire a eventi dei servizi AWS" = EventBridge. "Integrare eventi da applicazioni SaaS" = EventBridge Partner Event Bus. "Schedulare task periodici serverless" = EventBridge Scheduler.

## Amazon Kinesis: streaming di dati in tempo reale

Kinesis e' una famiglia di servizi per raccogliere, elaborare e analizzare dati in streaming in tempo reale.

### Kinesis Data Streams

Kinesis Data Streams e' il servizio core per l'ingestion di dati in streaming. I dati sono organizzati in Shards: ogni shard supporta 1 MB/sec in ingresso e 2 MB/sec in uscita. Aggiungi shard per aumentare la capacita'.

I dati restano nello stream per un periodo di retention (default 24 ore, massimo 365 giorni). Piu' consumatori possono leggere gli stessi dati indipendentemente. I consumatori possono essere applicazioni custom con Kinesis Client Library (KCL), funzioni Lambda, o Kinesis Data Analytics.

Enhanced Fan-Out permette a ogni consumatore di avere 2 MB/sec dedicati per shard (invece di condividere i 2 MB/sec tra tutti i consumatori). Usa un modello push invece di pull.

[ESAME] "Streaming di dati in tempo reale con elaborazione custom" = Kinesis Data Streams. "Piu' consumatori che leggono gli stessi dati" = Kinesis Data Streams.

### Kinesis Data Firehose

Firehose e' il modo piu' semplice per caricare dati in streaming verso destinazioni come S3, Redshift, OpenSearch e Splunk. E' completamente gestito: non devi gestire shard o capacita'.

Firehose puo' trasformare i dati in transito usando Lambda (es. convertire formato, arricchire dati) e puo' convertire il formato (es. JSON a Parquet). Il delivery e' near real-time con un buffer minimo di 60 secondi.

[ESAME] "Caricare dati in streaming su S3 automaticamente" = Kinesis Data Firehose. "Trasformare dati in streaming prima di salvarli" = Firehose con Lambda transformation.

### Kinesis Data Analytics

Kinesis Data Analytics permette di eseguire query SQL o applicazioni Apache Flink su dati in streaming. Puoi calcolare aggregazioni, rilevare anomalie e generare metriche in tempo reale.

[ESAME] "Analisi SQL su dati in streaming" = Kinesis Data Analytics.

## Amazon API Gateway

API Gateway e' un servizio completamente gestito per creare, pubblicare e gestire API. Funziona come "front door" per le tue applicazioni, gestendo autenticazione, throttling, caching e monitoring.

### Tipi di API

REST API e' il tipo piu' completo. Supporta caching delle risposte (per ridurre le chiamate al backend), throttling (10000 richieste/secondo di default, configurabile), API keys e usage plans (per limitare e monetizzare l'accesso), integrazione con WAF, e trasformazione di richieste/risposte con mapping templates.

HTTP API e' piu' semplice e costa circa il 70% in meno. E' ottimizzato per proxy verso Lambda e backend HTTP. Non supporta caching o trasformazioni complesse, ma e' sufficiente per molti casi d'uso.

WebSocket API supporta comunicazione bidirezionale in tempo reale. Il client mantiene una connessione persistente con API Gateway, che puo' inviare messaggi al client in qualsiasi momento. Ideale per chat, gaming, dashboard live.

### Autenticazione e autorizzazione

API Gateway supporta diversi metodi di autenticazione: IAM (per chiamate da altri servizi AWS o SDK), Lambda Authorizer (una funzione Lambda che valida un token custom e restituisce una policy IAM), e Cognito User Pools (valida JWT token emessi da Cognito).

### Deployment e stages

Le API vengono deployate in Stages (es. dev, staging, prod). Ogni stage ha il suo URL e puo' avere configurazioni diverse (throttling, caching, variabili di stage). Canary deployment permette di instradare una percentuale del traffico verso una nuova versione per testarla gradualmente.

[ESAME] "API REST con caching e throttling" = API Gateway REST API. "Proxy semplice verso Lambda con costo minimo" = HTTP API. "Comunicazione real-time bidirezionale" = WebSocket API.

## AWS Step Functions: orchestrazione di workflow

Step Functions permette di coordinare componenti distribuiti in workflow visuali. Definisci una state machine con stati che possono essere: Task (invoca Lambda, ECS, API, ecc.), Choice (branching condizionale), Parallel (esecuzione parallela), Wait (pausa), Map (iterazione su array), e altri.

### Standard vs Express Workflows

Standard Workflows possono durare fino a un anno, garantiscono exactly-once execution, e mantengono uno storico completo di ogni esecuzione. Sono ideali per workflow di lunga durata come approvazioni, orchestrazione di microservizi, e processi ETL.

Express Workflows durano massimo 5 minuti, hanno at-least-once execution, e sono ottimizzati per alto volume (oltre 100000 esecuzioni al secondo). Costano molto meno degli Standard. Ideali per elaborazione di eventi IoT, trasformazioni di dati ad alto throughput.

[ESAME] "Orchestrare piu' Lambda in sequenza con gestione degli errori" = Step Functions. "Workflow di approvazione con attesa di input umano" = Step Functions Standard. "Elaborazione ad alto volume di breve durata" = Step Functions Express.

## AWS AppSync: GraphQL gestito

AppSync e' un servizio gestito per creare API GraphQL. A differenza di REST dove ogni endpoint restituisce una struttura fissa, GraphQL permette al client di specificare esattamente quali dati vuole. AppSync si integra nativamente con DynamoDB, Lambda, RDS, OpenSearch e HTTP endpoints.

AppSync supporta subscriptions per aggiornamenti in tempo reale: il client si sottoscrive a certi eventi e riceve notifiche push quando i dati cambiano. Supporta anche offline sync per applicazioni mobile.

[ESAME] "API GraphQL gestita" = AppSync. "Sincronizzazione dati offline per app mobile" = AppSync con Amplify.
"""

print('  Serverless & Application Integration...')
generate_pdf('dispensa-06-Serverless.pdf', 'Serverless & Application Integration',
    'SQS, SNS, EventBridge, Kinesis, API Gateway, Step Functions', SERVERLESS)

# ============================================================
# DISPENSA 7: MONITORING, LOGGING & AUTOMATION
# ============================================================
MONITORING = """
## Amazon CloudWatch: il centro di osservabilita'

CloudWatch e' il servizio di monitoring e observability di AWS. Raccoglie metriche, log e eventi da praticamente tutti i servizi AWS e dalle tue applicazioni, permettendoti di monitorare lo stato dell'infrastruttura, rilevare anomalie e reagire automaticamente.

### Metriche: cosa puoi monitorare

Ogni servizio AWS invia automaticamente metriche a CloudWatch. Per EC2, le metriche predefinite includono CPUUtilization, NetworkIn/Out, DiskReadOps/WriteOps e StatusCheckFailed. Il monitoring di default e' ogni 5 minuti; abilitando Detailed Monitoring (a pagamento) ottieni metriche ogni 1 minuto.

Un dettaglio fondamentale per l'esame: la memoria RAM e lo spazio disco NON sono metriche predefinite di EC2. Per monitorarle, devi installare il CloudWatch Agent sull'istanza. L'agent raccoglie metriche a livello di sistema operativo (RAM, disco, processi, connessioni di rete) e puo' anche raccogliere log applicativi.

Le Custom Metrics ti permettono di inviare le tue metriche a CloudWatch tramite l'API PutMetricData. Puoi scegliere tra risoluzione standard (1 minuto) e high resolution (1 secondo). Utile per metriche applicative come il numero di utenti connessi, la dimensione della coda di elaborazione, o il tempo di risposta di un'API.

### Alarms: reagire automaticamente

Un CloudWatch Alarm monitora una metrica e esegue azioni quando supera una soglia. Gli stati possibili sono OK, ALARM e INSUFFICIENT_DATA. Le azioni possono essere: inviare una notifica SNS, eseguire un'azione di Auto Scaling (aggiungere o rimuovere istanze), o eseguire un'azione EC2 (stop, terminate, reboot, recover).

I Composite Alarms combinano piu' alarm con operatori AND e OR. Sono utili per ridurre il rumore: ad esempio, puoi creare un composite alarm che va in ALARM solo quando sia la CPU che la memoria superano le soglie, evitando falsi allarmi causati da picchi temporanei su una sola metrica.

[ESAME] "Monitorare la RAM di un'istanza EC2" = CloudWatch Agent + Custom Metric. "Scalare automaticamente quando la CPU supera il 70%" = CloudWatch Alarm + ASG Scaling Policy.

### CloudWatch Logs: raccolta e analisi dei log

CloudWatch Logs raccoglie e archivia log da molteplici fonti: istanze EC2 (tramite l'agent), funzioni Lambda (automaticamente), ECS, Route 53, VPC Flow Logs, CloudTrail, e molte altre. I log sono organizzati in Log Groups (un gruppo per applicazione/servizio) e Log Streams (un flusso per istanza/container).

La retention dei log e' configurabile: da 1 giorno a 10 anni, o mai (conservazione indefinita). Di default, i log non scadono mai, il che puo' generare costi significativi.

I Metric Filters estraggono metriche numeriche dai log. Ad esempio, puoi creare un filtro che conta quante volte appare la parola "ERROR" nei log e genera una metrica custom. Su questa metrica puoi poi creare un alarm.

CloudWatch Logs Insights e' un motore di query interattivo per analizzare i log. Usa un linguaggio di query dedicato per filtrare, aggregare e visualizzare i dati dei log. E' molto piu' potente della semplice ricerca testuale.

I Subscription Filters permettono di inviare i log in tempo reale verso altre destinazioni: Lambda (per elaborazione custom), Kinesis Data Streams (per analytics), Kinesis Data Firehose (per archiviazione su S3), o OpenSearch (per ricerca e visualizzazione).

[ESAME] "Contare gli errori nei log e creare un allarme" = Metric Filter + Alarm. "Analizzare i log con query" = Logs Insights. "Inviare log in tempo reale a S3" = Subscription Filter + Firehose.

### CloudWatch Dashboards e Synthetics

I Dashboards sono visualizzazioni personalizzabili di metriche e log. Possono includere metriche da regioni diverse e account diversi, fornendo una vista unificata dell'infrastruttura.

CloudWatch Synthetics crea "canary" che simulano le azioni degli utenti (navigazione web, chiamate API) a intervalli regolari. Se un canary fallisce, puoi ricevere un allarme prima che gli utenti reali siano impattati. Utile per monitorare endpoint, flussi di login, e disponibilita' di API.

## AWS CloudTrail: chi ha fatto cosa

CloudTrail registra ogni chiamata API effettuata nel tuo account AWS. Ogni evento include: chi ha fatto la chiamata (utente/ruolo), quale azione (API call), su quale risorsa, quando, da quale IP, e se ha avuto successo o meno. E' lo strumento fondamentale per audit, compliance e investigazione di incidenti di sicurezza.

### Tipi di eventi

Management Events registrano le operazioni di gestione sulle risorse: creare un bucket S3, lanciare un'istanza EC2, modificare un security group. Sono abilitati di default.

Data Events registrano le operazioni sui dati: leggere un oggetto da S3 (GetObject), invocare una funzione Lambda. NON sono abilitati di default perche' generano un volume molto alto di eventi. Devi abilitarli esplicitamente per i servizi che ti interessano.

Insights Events rilevano automaticamente attivita' anomale, come un improvviso aumento di chiamate API o un pattern di errori insolito. CloudTrail usa modelli statistici per stabilire una baseline e segnalare deviazioni.

### Trail e conservazione

Un Trail consegna gli eventi a un bucket S3 e/o a CloudWatch Logs. E' raccomandato creare un trail multi-region che cattura eventi da tutte le regioni. Per organizzazioni con piu' account, un Organization Trail cattura eventi da tutti gli account.

Nella console CloudTrail, gli eventi sono visibili per 90 giorni. Per conservazione a lungo termine, devi configurare un trail che salva su S3. La Log File Integrity Validation verifica che i file di log non siano stati modificati dopo la consegna, usando hash SHA-256.

[ESAME] "Chi ha cancellato un bucket S3?" = CloudTrail Management Events. "Chi ha letto un file specifico da S3?" = CloudTrail Data Events. "Conservare log di audit per 7 anni" = CloudTrail trail verso S3 con lifecycle policy verso Glacier.

## AWS Config: compliance e configurazione

AWS Config registra e valuta la configurazione delle risorse AWS nel tempo. Mentre CloudTrail ti dice chi ha fatto cosa, Config ti dice come era configurata una risorsa in un dato momento e se quella configurazione e' conforme alle tue regole.

### Config Rules

Le Config Rules valutano se le risorse sono conformi a regole specifiche. AWS fornisce oltre 200 Managed Rules predefinite, come: "tutti i bucket S3 devono avere la crittografia abilitata", "tutti i security group non devono permettere SSH da 0.0.0.0/0", "tutte le istanze EC2 devono avere un tag Environment".

Puoi anche creare Custom Rules usando funzioni Lambda per logica di valutazione personalizzata. Le regole possono essere valutate ad ogni cambiamento di configurazione o a intervalli periodici.

### Remediation e Aggregator

Quando una risorsa non e' conforme, Config puo' eseguire una Remediation automatica usando SSM Automation Documents. Ad esempio, se un bucket S3 non ha la crittografia abilitata, Config puo' automaticamente abilitarla.

L'Aggregator fornisce una vista multi-account e multi-region della compliance. Puoi vedere lo stato di conformita' di tutte le risorse in tutti gli account dell'organizzazione da un unico punto.

I Conformance Packs sono pacchetti di Config Rules e remediation actions raggruppati per framework di compliance (PCI-DSS, HIPAA, NIST, ecc.).

[ESAME] "Verificare che tutti i bucket S3 siano criptati" = Config Rule. "Correggere automaticamente risorse non conformi" = Config Remediation. "Vista compliance multi-account" = Config Aggregator.

## AWS Systems Manager: gestione operativa

Systems Manager (SSM) e' una suite di strumenti per la gestione operativa delle risorse AWS e on-premises. L'SSM Agent deve essere installato sulle istanze (e' preinstallato su Amazon Linux 2 e Windows Server) e l'istanza deve avere un IAM Role con i permessi necessari.

### Session Manager: accesso sicuro senza SSH

Session Manager permette di aprire una shell interattiva su un'istanza EC2 senza bisogno di SSH, bastion host, o porte aperte nel security group. La connessione passa attraverso l'SSM Agent e il servizio AWS. Tutte le sessioni sono registrate in CloudWatch Logs e/o S3 per audit.

Questo e' un enorme vantaggio di sicurezza: non devi gestire chiavi SSH, non devi aprire la porta 22, e hai un audit trail completo di ogni comando eseguito.

[ESAME] "Accesso sicuro a EC2 senza SSH e senza bastion host" = Session Manager.

### Run Command e Patch Manager

Run Command esegue comandi su flotte di istanze senza connettersi individualmente. Puoi usare documenti predefiniti (es. installare software, eseguire script) o crearne di custom. I risultati sono visibili nella console e possono essere inviati a S3 o CloudWatch Logs.

Patch Manager automatizza il patching del sistema operativo e delle applicazioni. Definisci una Patch Baseline (quali patch approvare) e una Maintenance Window (quando applicarle). Patch Manager scansiona le istanze, identifica le patch mancanti e le installa.

### Parameter Store e Automation

Parameter Store e' un key-value store per configurazioni e segreti (vedi sezione Security per i dettagli). Automation esegue workflow operativi predefiniti o custom: creare AMI, ridimensionare istanze, applicare patch, e molto altro.

## AWS CloudFormation: Infrastructure as Code

CloudFormation permette di definire l'intera infrastruttura AWS in template YAML o JSON. Invece di creare risorse manualmente dalla console, descrivi cosa vuoi in un template e CloudFormation crea tutto automaticamente, nell'ordine corretto, gestendo le dipendenze.

### Stack e operazioni

Uno Stack e' l'insieme di risorse create da un template. Puoi creare, aggiornare e cancellare stack. Quando aggiorni un template, CloudFormation calcola le differenze e applica solo le modifiche necessarie. Se qualcosa va storto durante la creazione o l'aggiornamento, CloudFormation esegue automaticamente il rollback allo stato precedente.

I Change Sets ti permettono di vedere in anteprima quali modifiche verranno applicate prima di eseguirle. Drift Detection rileva se qualcuno ha modificato manualmente le risorse dello stack.

### Funzionalita' avanzate

StackSets permettono di deployare lo stesso template su piu' account e regioni in un'organizzazione AWS. Nested Stacks permettono di riutilizzare template come componenti modulari. Cross-Stack References (Export/Import) permettono a uno stack di usare valori prodotti da un altro stack.

La DeletionPolicy controlla cosa succede a una risorsa quando lo stack viene cancellato: Delete (cancella la risorsa, default), Retain (mantieni la risorsa), Snapshot (crea uno snapshot prima di cancellare, per EBS, RDS, ecc.).

[ESAME] "Deployare la stessa infrastruttura in piu' regioni" = CloudFormation StackSets. "Proteggere un database dalla cancellazione accidentale dello stack" = DeletionPolicy: Retain o Snapshot.

## AWS CDK e altri strumenti IaC

AWS CDK (Cloud Development Kit) permette di definire l'infrastruttura usando linguaggi di programmazione come TypeScript, Python, Java e C#. Il CDK genera template CloudFormation sotto il cofano, ma offre un'esperienza di sviluppo piu' naturale con costrutti di alto livello, logica condizionale e riutilizzo del codice.

AWS SAM (Serverless Application Model) e' un'estensione di CloudFormation ottimizzata per applicazioni serverless. Semplifica la definizione di Lambda, API Gateway, DynamoDB e altri servizi serverless con una sintassi piu' concisa.

[ESAME] "Infrastructure as Code con template dichiarativi" = CloudFormation. "IaC con linguaggi di programmazione" = CDK. "IaC ottimizzato per serverless" = SAM.
"""

print('  Monitoring, Logging & Automation...')
generate_pdf('dispensa-07-Monitoring.pdf', 'Monitoring, Logging & Automation',
    'CloudWatch, CloudTrail, Config, Systems Manager, CloudFormation', MONITORING)

# ============================================================
# DISPENSA 8: COST OPTIMIZATION & WELL-ARCHITECTED
# ============================================================
COST_OPTIMIZATION = """
## Strumenti per la gestione dei costi

Ottimizzare i costi e' uno dei cinque pilastri del Well-Architected Framework e un argomento frequente nell'esame SAA-C03. AWS offre diversi strumenti per monitorare, analizzare e ridurre la spesa.

### AWS Cost Explorer

Cost Explorer e' lo strumento principale per visualizzare e analizzare i costi AWS. Mostra grafici della spesa nel tempo, suddivisa per servizio, account, regione, tag o altre dimensioni. Puoi creare report personalizzati e salvarli per consultazioni future.

La funzione Forecast usa i dati storici per prevedere la spesa futura. Rightsizing Recommendations analizza l'utilizzo delle istanze EC2 e suggerisce tipi di istanza piu' appropriati (piu' piccoli se sottoutilizzate, piu' grandi se sovraccariche). Savings Plans Recommendations suggerisce quali Savings Plans acquistare in base al tuo utilizzo.

[ESAME] "Analizzare i costi per servizio negli ultimi 6 mesi" = Cost Explorer. "Identificare istanze EC2 sovradimensionate" = Cost Explorer Rightsizing Recommendations.

### AWS Budgets

Budgets permette di impostare soglie di spesa e ricevere alert quando vengono superate. Puoi creare budget su costi, utilizzo, copertura di Reserved Instances e Savings Plans.

Gli alert possono essere configurati per notificare quando raggiungi una percentuale del budget (es. 80%) o quando la previsione indica che supererai il budget. Le notifiche vanno a SNS o email.

Budget Actions permettono di eseguire azioni automatiche quando un budget viene superato: applicare una SCP restrittiva, fermare istanze EC2, o disabilitare utenti IAM. Questo e' utile per ambienti di sviluppo o sandbox dove vuoi evitare spese incontrollate.

[ESAME] "Ricevere un alert quando la spesa supera $1000" = AWS Budgets. "Fermare automaticamente le istanze quando si supera il budget" = Budget Actions.

### AWS Cost and Usage Report (CUR)

Il Cost and Usage Report e' il report piu' dettagliato disponibile. Contiene ogni singolo addebito con tutti i dettagli: risorsa, operazione, pricing, tag, ecc. Viene consegnato a un bucket S3 in formato CSV o Parquet.

CUR e' troppo dettagliato per essere letto direttamente. Si usa con strumenti di analytics come Athena (query SQL su S3), QuickSight (visualizzazione), o Redshift (data warehouse) per analisi approfondite.

### AWS Trusted Advisor

Trusted Advisor analizza il tuo account e fornisce raccomandazioni su cinque categorie: Cost Optimization (risorse inutilizzate, istanze sottoutilizzate), Performance (limiti di servizio, configurazioni subottimali), Security (permessi troppo aperti, MFA non abilitato), Fault Tolerance (backup mancanti, risorse non distribuite su AZ), e Service Limits (utilizzo vicino ai limiti).

Con il piano di supporto Basic, hai accesso solo a un sottoinsieme di check (principalmente security). Con Business o Enterprise Support, hai accesso a tutti i check e puoi usare l'API per automazione.

[ESAME] "Identificare risorse inutilizzate per ridurre i costi" = Trusted Advisor Cost Optimization. "Verificare che MFA sia abilitato su root" = Trusted Advisor Security.

### AWS Compute Optimizer

Compute Optimizer usa machine learning per analizzare l'utilizzo di EC2, Auto Scaling Groups, Lambda e EBS, e raccomandare configurazioni ottimali. A differenza di Cost Explorer Rightsizing che guarda solo EC2, Compute Optimizer copre piu' servizi e fornisce raccomandazioni piu' dettagliate.

## Strategie di risparmio

### Reserved Instances e Savings Plans

Per workload stabili e prevedibili, Reserved Instances e Savings Plans offrono sconti significativi rispetto a On-Demand.

Le Reserved Instances (RI) sono legate a un tipo di istanza specifico in una regione specifica. Standard RI offrono lo sconto massimo (fino al 72%) ma non possono essere modificate. Convertible RI offrono uno sconto inferiore (fino al 66%) ma permettono di cambiare tipo di istanza, sistema operativo e tenancy durante il periodo.

I Savings Plans sono piu' flessibili. Compute Savings Plans si applicano a qualsiasi utilizzo EC2, Fargate e Lambda in qualsiasi regione, offrendo fino al 66% di sconto. EC2 Instance Savings Plans sono legati a una famiglia di istanze in una regione specifica ma offrono uno sconto maggiore (fino al 72%).

La scelta tra RI e Savings Plans dipende dalla prevedibilita' del tuo workload. Se sai esattamente quali istanze userai per 1-3 anni, le RI Standard offrono il massimo risparmio. Se hai bisogno di flessibilita', i Savings Plans sono preferibili.

[ESAME] "Massimo risparmio per workload EC2 stabile e prevedibile" = Reserved Instances Standard o EC2 Instance Savings Plan. "Risparmio con flessibilita' su tipo di istanza e regione" = Compute Savings Plan.

### Spot Instances

Le Spot Instances offrono sconti fino al 90% ma possono essere interrotte da AWS con 2 minuti di preavviso quando la capacita' e' necessaria. Sono ideali per workload fault-tolerant: batch processing, big data analytics, CI/CD, rendering, training di modelli ML.

Le Spot Fleet e gli EC2 Fleet permettono di lanciare un mix di istanze Spot e On-Demand, specificando la capacita' desiderata e lasciando che AWS scelga i tipi di istanza piu' economici disponibili.

[ESAME] "Ridurre i costi per batch processing che puo' tollerare interruzioni" = Spot Instances.

### Altre strategie

S3 Lifecycle Policies spostano automaticamente gli oggetti verso classi di storage piu' economiche (Standard-IA, Glacier) in base all'eta'. Questo puo' ridurre drasticamente i costi di storage per dati acceduti raramente.

Elimina le risorse inutilizzate: volumi EBS non collegati, Elastic IP non associati, snapshot vecchi, load balancer senza target. Trusted Advisor e Cost Explorer aiutano a identificarle.

Usa servizi serverless (Lambda, Fargate, DynamoDB On-Demand) per workload variabili. Paghi solo per l'utilizzo effettivo invece di pagare per capacita' provisionata che potrebbe restare inutilizzata.

## AWS Organizations e governance multi-account

### Struttura e Consolidated Billing

AWS Organizations permette di gestire centralmente piu' account AWS. Gli account sono organizzati in una gerarchia con Organizational Units (OU). Il Management Account (ex Master Account) e' l'account principale che crea e gestisce l'organizzazione.

Consolidated Billing aggrega la fatturazione di tutti gli account in un'unica fattura. Questo non e' solo una comodita' amministrativa: permette di beneficiare dei volume discounts (piu' usi, meno paghi per unita') e di condividere Reserved Instances e Savings Plans tra gli account.

### Service Control Policies (SCP)

Le SCP definiscono i permessi massimi per gli account o le OU. Non concedono permessi, li limitano. Anche se un utente ha una policy IAM che permette un'azione, se la SCP dell'account non la permette, l'azione e' negata.

Casi d'uso comuni: impedire l'uso di regioni non approvate, impedire la disabilitazione di CloudTrail o GuardDuty, impedire la creazione di utenti IAM con accesso programmatico, forzare l'uso di certi tipi di istanze.

Le SCP non si applicano al Management Account. Questo e' intenzionale per evitare di bloccarsi fuori, ma significa che il Management Account dovrebbe essere usato solo per la gestione dell'organizzazione, non per workload.

[ESAME] "Impedire a tutti gli account di usare la regione ap-southeast-1" = SCP. "Impedire la cancellazione dei log CloudTrail" = SCP.

### AWS Control Tower

Control Tower automatizza il setup e la governance di un ambiente multi-account seguendo le best practice AWS. Crea una Landing Zone con account predefiniti (Log Archive, Audit), OU predefinite, e guardrails (regole di governance).

I Guardrails sono di due tipi: Preventive (implementati come SCP, impediscono azioni non conformi) e Detective (implementati come Config Rules, rilevano configurazioni non conformi).

Account Factory automatizza la creazione di nuovi account con configurazioni standardizzate. Quando un team ha bisogno di un nuovo account, lo richiede tramite Service Catalog e Account Factory lo crea con tutte le configurazioni di governance gia' applicate.

[ESAME] "Setup automatizzato di un ambiente multi-account con best practice" = Control Tower. "Creare nuovi account con configurazioni standardizzate" = Account Factory.

## Disaster Recovery

Il disaster recovery (DR) e' la capacita' di ripristinare i sistemi dopo un evento catastrofico. AWS offre diverse strategie con trade-off tra costo e tempo di recovery.

### RPO e RTO

RPO (Recovery Point Objective) e' la quantita' massima di dati che puoi permetterti di perdere, misurata in tempo. Se il tuo RPO e' 1 ora, devi avere backup almeno ogni ora.

RTO (Recovery Time Objective) e' il tempo massimo che puoi permetterti di restare offline. Se il tuo RTO e' 4 ore, devi essere in grado di ripristinare i sistemi entro 4 ore dal disastro.

### Strategie di DR (dal meno al piu' costoso)

Backup and Restore e' la strategia piu' semplice ed economica. Fai backup regolari su S3 (possibilmente in un'altra regione) e, in caso di disastro, ripristini l'infrastruttura dai backup. RPO: ore (dipende dalla frequenza dei backup). RTO: ore (tempo per ripristinare). Costo: basso (solo storage dei backup).

Pilot Light mantiene i componenti core sempre attivi nella regione di DR, tipicamente il database con replica continua. L'infrastruttura di compute (EC2, ASG) e' definita ma non attiva. In caso di disastro, avvii l'infrastruttura e scali alla capacita' necessaria. RPO: minuti (replica del database). RTO: decine di minuti (tempo per avviare e scalare). Costo: medio-basso.

Warm Standby mantiene una versione ridotta dell'ambiente sempre in esecuzione nella regione di DR. Tutti i componenti sono attivi ma con capacita' minima. In caso di disastro, scali alla capacita' piena. RPO: secondi (replica sincrona o quasi). RTO: minuti (solo scaling). Costo: medio.

Multi-Site / Hot Standby mantiene l'ambiente completo attivo in entrambe le regioni, con traffico distribuito tra le due (active-active). In caso di disastro in una regione, tutto il traffico va all'altra. RPO: near zero. RTO: near zero (solo tempo di failover DNS). Costo: alto (paghi per due ambienti completi).

[ESAME] "DR con costo minimo per un'applicazione non critica" = Backup and Restore. "DR con RTO di pochi minuti per un'applicazione critica" = Warm Standby o Multi-Site. "RPO near zero" = replica sincrona (Aurora Global Database, DynamoDB Global Tables).

### Servizi AWS per DR

Route 53 Failover routing rileva quando l'endpoint primario non e' healthy e instrada il traffico verso l'endpoint di DR. Aurora Global Database replica i dati in regioni secondarie con lag inferiore a 1 secondo e permette promozione in meno di 1 minuto. S3 Cross-Region Replication replica gli oggetti in un'altra regione. DynamoDB Global Tables fornisce replica active-active multi-region.

## Well-Architected Framework

Il Well-Architected Framework e' un insieme di best practice per progettare e operare sistemi affidabili, sicuri, efficienti e cost-effective nel cloud. Si basa su sei pilastri.

Operational Excellence si concentra sull'esecuzione e il monitoraggio dei sistemi per fornire valore di business. Include: operazioni as code (CloudFormation, CDK), cambiamenti piccoli e frequenti, anticipare i fallimenti, imparare dagli incidenti.

Security protegge informazioni, sistemi e asset. Include: identity management forte (IAM, MFA), tracciabilita' (CloudTrail, Config), sicurezza a tutti i livelli (VPC, Security Groups, WAF), protezione dei dati (crittografia, backup).

Reliability assicura che un sistema funzioni correttamente e si riprenda dai fallimenti. Include: recovery automatico (Auto Scaling, Multi-AZ), scaling orizzontale, gestione dei cambiamenti (blue/green deployment), test di recovery.

Performance Efficiency usa le risorse di computing in modo efficiente. Include: selezione del tipo di risorsa giusto, monitoraggio delle performance, trade-off informati (es. caching vs freshness).

Cost Optimization evita spese non necessarie. Include: adottare un modello di consumo (pay for what you use), misurare l'efficienza, eliminare sprechi, usare servizi managed.

Sustainability minimizza l'impatto ambientale. Include: comprendere l'impatto, stabilire obiettivi di sostenibilita', massimizzare l'utilizzo, usare servizi managed.

Il Well-Architected Tool nella console AWS ti permette di valutare i tuoi workload rispetto alle best practice dei sei pilastri e ricevere raccomandazioni per migliorare.

[ESAME] Le domande spesso descrivono uno scenario e chiedono quale principio del Well-Architected Framework viene violato o quale soluzione lo rispetta meglio. Familiarizza con i concetti chiave di ogni pilastro.
"""

print('  Cost Optimization & Well-Architected...')
generate_pdf('dispensa-08-CostOptimization.pdf', 'Cost Optimization & Well-Architected',
    'Cost Explorer, Budgets, Trusted Advisor, Organizations, Control Tower, DR', COST_OPTIMIZATION)

print('\nTutte le 8 dispense sono state generate nella cartella "dispense/"')
