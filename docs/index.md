# txdb

This package provides a Python interface to access and manipulate genome annotations, implemented in the Bioconductor [GenomicFeatures](https://bioconductor.org/packages/GenomicFeatures) package. It allows users to interact with `TxDb` SQLite databases to extract genomic features such as transcripts, exons, CDS, and promoters as `GenomicRanges` objects. It also includes a registry system to easily download and cache standard TxDb databases.

## Install

To get started, install the package from [PyPI](https://pypi.org/project/txdb/)

```bash
pip install txdb
```

## Contents

```{toctree}
:maxdepth: 2

Overview <readme>
Contributions & Help <contributing>
License <license>
Authors <authors>
Changelog <changelog>
Module Reference <api/modules>
```

## Indices and tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`

[Sphinx]: http://www.sphinx-doc.org/
[Markdown]: https://daringfireball.net/projects/markdown/
[reStructuredText]: http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
[MyST]: https://myst-parser.readthedocs.io/en/latest/
