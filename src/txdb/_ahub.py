"""This list of TxDB resources was generated from AnnotationHub. (credits to Lori Shepherd).

Code to generate:

```bash
wget https://annotationhub.bioconductor.org/metadata/annotationhub.sqlite3
sqlite3 annotationhub.sqlite3
```

```sql
SELECT
    r.title,
    r.rdatadateadded,
    lp.location_prefix || rp.rdatapath AS full_rdatapath
FROM resources r
LEFT JOIN location_prefixes lp
    ON r.location_prefix_id = lp.id
LEFT JOIN rdatapaths rp
    ON rp.resource_id = r.id
WHERE r.title LIKE 'TxDb%.sqlite';
```

Note: we only keep the latest version of these files.

"""

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"

TXDB_CONFIG = {
    "TxDb.Athaliana.BioMart.plantsmart22": {
        "release_date": "2016-12-22",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.4/TxDb.Athaliana.BioMart.plantsmart22.sqlite",
    },
    "TxDb.Athaliana.BioMart.plantsmart25": {
        "release_date": "2016-12-22",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.4/TxDb.Athaliana.BioMart.plantsmart25.sqlite",
    },
    "TxDb.Athaliana.BioMart.plantsmart28": {
        "release_date": "2016-12-22",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.4/TxDb.Athaliana.BioMart.plantsmart28.sqlite",
    },
    "TxDb.Btaurus.UCSC.bosTau8.refGene": {
        "release_date": "2020-10-20",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.12/TxDb.Btaurus.UCSC.bosTau8.refGene.sqlite",
    },
    "TxDb.Celegans.UCSC.ce11.refGene": {
        "release_date": "2019-05-01",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.9/TxDb.Celegans.UCSC.ce11.refGene.sqlite",
    },
    "TxDb.Celegans.UCSC.ce6.ensGene": {
        "release_date": "2016-12-22",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.4/TxDb.Celegans.UCSC.ce6.ensGene.sqlite",
    },
    "TxDb.Cfamiliaris.UCSC.canFam3.refGene": {
        "release_date": "2020-10-20",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.12/TxDb.Cfamiliaris.UCSC.canFam3.refGene.sqlite",
    },
    "TxDb.Dmelanogaster.UCSC.dm3.ensGene": {
        "release_date": "2016-12-22",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.4/TxDb.Dmelanogaster.UCSC.dm3.ensGene.sqlite",
    },
    "TxDb.Dmelanogaster.UCSC.dm6.ensGene": {
        "release_date": "2020-10-20",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.12/TxDb.Dmelanogaster.UCSC.dm6.ensGene.sqlite",
    },
    "TxDb.Drerio.UCSC.danRer10.refGene": {
        "release_date": "2019-05-01",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.9/TxDb.Drerio.UCSC.danRer10.refGene.sqlite",
    },
    "TxDb.Ggallus.UCSC.galGal4.refGene": {
        "release_date": "2020-10-20",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.12/TxDb.Ggallus.UCSC.galGal4.refGene.sqlite",
    },
    "TxDb.Hsapiens.BioMart.igis": {
        "release_date": "2016-12-22",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.4/TxDb.Hsapiens.BioMart.igis.sqlite",
    },
    "TxDb.Hsapiens.UCSC.hg18.knownGene": {
        "release_date": "2016-12-22",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.4/TxDb.Hsapiens.UCSC.hg18.knownGene.sqlite",
    },
    "TxDb.Hsapiens.UCSC.hg19.knownGene": {
        "release_date": "2025-10-29",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.22/TxDb.Hsapiens.UCSC.hg19.knownGene.sqlite",
    },
    "TxDb.Hsapiens.UCSC.hg19.lincRNAsTranscripts": {
        "release_date": "2016-12-22",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.4/TxDb.Hsapiens.UCSC.hg19.lincRNAsTranscripts.sqlite",
    },
    "TxDb.Hsapiens.UCSC.hg38.knownGene": {
        "release_date": "2025-10-29",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.22/TxDb.Hsapiens.UCSC.hg38.knownGene.sqlite",
    },
    "TxDb.Hsapiens.UCSC.hg38.refGene": {
        "release_date": "2024-04-02",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.19/TxDb.Hsapiens.UCSC.hg38.refGene.sqlite",
    },
    "TxDb.Mmulatta.UCSC.rheMac3.refGene": {
        "release_date": "2020-10-20",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.12/TxDb.Mmulatta.UCSC.rheMac3.refGene.sqlite",
    },
    "TxDb.Mmulatta.UCSC.rheMac8.refGene": {
        "release_date": "2020-10-20",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.12/TxDb.Mmulatta.UCSC.rheMac8.refGene.sqlite",
    },
    "TxDb.Mmulatta.UCSC.rheMac10.refGene": {
        "release_date": "2021-10-08",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.14/TxDb.Mmulatta.UCSC.rheMac10.refGene.sqlite",
    },
    "TxDb.Mmusculus.UCSC.mm10.ensGene": {
        "release_date": "2016-12-22",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.4/TxDb.Mmusculus.UCSC.mm10.ensGene.sqlite",
    },
    "TxDb.Mmusculus.UCSC.mm10.knownGene": {
        "release_date": "2019-05-01",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.9/TxDb.Mmusculus.UCSC.mm10.knownGene.sqlite",
    },
    "TxDb.Mmusculus.UCSC.mm39.refGene": {
        "release_date": "2024-04-02",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.19/TxDb.Mmusculus.UCSC.mm39.refGene.sqlite",
    },
    "TxDb.Mmusculus.UCSC.mm39.knownGene": {
        "release_date": "2025-03-11",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.21/TxDb.Mmusculus.UCSC.mm39.knownGene.sqlite",
    },
    "TxDb.Mmusculus.UCSC.mm9.knownGene": {
        "release_date": "2016-12-22",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.4/TxDb.Mmusculus.UCSC.mm9.knownGene.sqlite",
    },
    "TxDb.Ptroglodytes.UCSC.panTro4.refGene": {
        "release_date": "2020-04-27",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.11/TxDb.Ptroglodytes.UCSC.panTro4.refGene.sqlite",
    },
    "TxDb.Ptroglodytes.UCSC.panTro5.refGene": {
        "release_date": "2020-04-27",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.11/TxDb.Ptroglodytes.UCSC.panTro5.refGene.sqlite",
    },
    "TxDb.Ptroglodytes.UCSC.panTro6.refGene": {
        "release_date": "2019-10-29",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.10/TxDb.Ptroglodytes.UCSC.panTro6.refGene.sqlite",
    },
    "TxDb.Rnorvegicus.BioMart.igis": {
        "release_date": "2016-12-22",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.4/TxDb.Rnorvegicus.BioMart.igis.sqlite",
    },
    "TxDb.Rnorvegicus.UCSC.rn4.ensGene": {
        "release_date": "2016-12-22",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.4/TxDb.Rnorvegicus.UCSC.rn4.ensGene.sqlite",
    },
    "TxDb.Rnorvegicus.UCSC.rn5.refGene": {
        "release_date": "2020-04-27",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.11/TxDb.Rnorvegicus.UCSC.rn5.refGene.sqlite",
    },
    "TxDb.Rnorvegicus.UCSC.rn6.refGene": {
        "release_date": "2019-05-01",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.9/TxDb.Rnorvegicus.UCSC.rn6.refGene.sqlite",
    },
    "TxDb.Rnorvegicus.UCSC.rn6.ncbiRefSeq": {
        "release_date": "2020-10-20",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.12/TxDb.Rnorvegicus.UCSC.rn6.ncbiRefSeq.sqlite",
    },
    "TxDb.Rnorvegicus.UCSC.rn7.refGene": {
        "release_date": "2022-04-18",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.15/TxDb.Rnorvegicus.UCSC.rn7.refGene.sqlite",
    },
    "TxDb.Scerevisiae.UCSC.sacCer2.sgdGene": {
        "release_date": "2016-12-22",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.4/TxDb.Scerevisiae.UCSC.sacCer2.sgdGene.sqlite",
    },
    "TxDb.Scerevisiae.UCSC.sacCer3.sgdGene": {
        "release_date": "2016-12-22",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.4/TxDb.Scerevisiae.UCSC.sacCer3.sgdGene.sqlite",
    },
    "TxDb.Sscrofa.UCSC.susScr3.refGene": {
        "release_date": "2020-04-27",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.11/TxDb.Sscrofa.UCSC.susScr3.refGene.sqlite",
    },
    "TxDb.Sscrofa.UCSC.susScr11.refGene": {
        "release_date": "2020-04-27",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.11/TxDb.Sscrofa.UCSC.susScr11.refGene.sqlite",
    },
    "TxDb.Ggallus.UCSC.galGal5.refGene": {
        "release_date": "2020-04-27",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.11/TxDb.Ggallus.UCSC.galGal5.refGene.sqlite",
    },
    "TxDb.Ggallus.UCSC.galGal6.refGene": {
        "release_date": "2019-10-29",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.10/TxDb.Ggallus.UCSC.galGal6.refGene.sqlite",
    },
    "TxDb.Cfamiliaris.UCSC.canFam4.refGene": {
        "release_date": "2021-10-08",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.14/TxDb.Cfamiliaris.UCSC.canFam4.refGene.sqlite",
    },
    "TxDb.Cfamiliaris.UCSC.canFam5.refGene": {
        "release_date": "2021-10-08",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.14/TxDb.Cfamiliaris.UCSC.canFam5.refGene.sqlite",
    },
    "TxDb.Cfamiliaris.UCSC.canFam6.refGene": {
        "release_date": "2023-04-06",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.17/TxDb.Cfamiliaris.UCSC.canFam6.refGene.sqlite",
    },
    "TxDb.Celegans.UCSC.ce11.ensGene": {
        "release_date": "2022-04-18",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.15/TxDb.Celegans.UCSC.ce11.ensGene.sqlite",
    },
    "TxDb.Drerio.UCSC.danRer11.refGene": {
        "release_date": "2019-05-01",
        "url": "https://mghp.osn.xsede.org/bir190004-bucket01/AnnotationHub/ucsc/standard/3.9/TxDb.Drerio.UCSC.danRer11.refGene.sqlite",
    },
}
