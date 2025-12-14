[![PyPI-Server](https://img.shields.io/pypi/v/txdb.svg)](https://pypi.org/project/txdb/)
![Unit tests](https://github.com/BiocPy/txdb/actions/workflows/run-tests.yml/badge.svg)

# TxDb

This package provides a Python interface to access and manipulate genome annotations, implemented in the Bioconductor [GenomicFeatures](https://bioconductor.org/packages/GenomicFeatures) package. It allows users to interact with `TxDb` SQLite databases to extract genomic features such as transcripts, exons, CDS, and promoters as [GenomicRanges](https://github.com/biocpy/genomicranges) objects. It also includes a registry system to easily download and cache standard TxDb annotation files.

## Install

To get started, install the package from [PyPI](https://pypi.org/project/txdb/)

```bash
pip install txdb
```

## Usage

### Using TxDbRegistry

The TxDbRegistry provides easy access to hosted TxDb databases in [AnnotationHub](https://bioconductor.org/packages/release/bioc/html/AnnotationHub.html).

```python
from txdb import TxDbRegistry

# Initialize registry
registry = TxDbRegistry()

# List available databases
print(registry.list_txdb())

# Load a specific database (downloads and caches it automatically)
# Example: hg38 knownGene
txdb = registry.load_db("TxDb.Hsapiens.UCSC.hg38.knownGene")

# Access features
transcripts = txdb.transcripts()
print(transcripts)
```

    ## OUTPUT
    GenomicRanges with 412044 ranges and 3 metadata columns
                        seqnames          ranges          strand   _tx_id           tx_name tx_type
                        <str>       <IRanges> <ndarray[int8]>   <list>            <list>  <list>
        [0]                chr1   11121 - 14413               + |      1 ENST00000832824.1    None
        [1]                chr1   11125 - 14405               + |      2 ENST00000832825.1    None
        [2]                chr1   11410 - 14413               + |      3 ENST00000832826.1    None
                            ...             ...             ... |    ...               ...     ...
    [412041] chrX_MU273397v1_alt 314193 - 316302               - | 412042 ENST00000710030.1    None
    [412042] chrX_MU273397v1_alt 314813 - 315236               - | 412043 ENST00000710216.1    None
    [412043] chrX_MU273397v1_alt 324527 - 324923               - | 412044 ENST00000710031.1    None
    ------
    seqinfo(711 sequences): chr1 chr2 chr3 ... chrX_MU273395v1_alt chrX_MU273396v1_alt chrX_MU273397v1_alt

### Using a Local TxDb File

If you have a local SQLite file (e.g., generated from R), you can load it directly.

```python
from txdb import TxDb

txdb = TxDb("path/to/custom_txdb.sqlite")

# Extract exons
exons = txdb.exons()

# Extract promoters (2kb upstream)
promoters = txdb.promoters(upstream=2000, downstream=200)

# Filter for a specific chromosome
chr1_tx = txdb.transcripts(filter={"tx_chrom": "chr1"})
```

Check out the documentation for all supported extractors from TxDB files.

<!-- biocsetup-notes -->

## Note

This project has been set up using [BiocSetup](https://github.com/biocpy/biocsetup)
and [PyScaffold](https://pyscaffold.org/).
