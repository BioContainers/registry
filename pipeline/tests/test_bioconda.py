from biocontainers_pipeline.sources import bioconda

META = '''{% set version = "1.19" %}
{% set name = "samtools" %}
package:
  name: {{ name }}
  version: {{ version }}
build:
  number: 0
about:
  home: http://www.htslib.org/
  license: MIT
  license_family: MIT
  doc_url: http://www.htslib.org/doc/
  dev_url: https://github.com/samtools/samtools
  summary: Tools for manipulating SAM/BAM/CRAM
  description: A longer paragraph describing samtools in detail.
extra:
  identifiers:
    - biotools:samtools
    - doi:10.1093/bioinformatics/btp352
  recipe-maintainers:
    - alice
    - bob
'''


def test_parse_meta_resolves_version_and_about():
    m = bioconda.parse_meta(META)
    assert m["version"] == "1.19"
    assert m["home"] == "http://www.htslib.org/"
    assert m["license"] == "MIT"
    assert m["summary"].startswith("Tools for manipulating")


def test_parse_meta_extracts_enrichment():
    m = bioconda.parse_meta(META)
    assert m["description"].startswith("A longer paragraph")
    assert m["doc_url"] == "http://www.htslib.org/doc/"
    assert m["dev_url"] == "https://github.com/samtools/samtools"
    assert m["license_family"] == "MIT"
    assert m["identifiers"] == ["biotools:samtools", "doi:10.1093/bioinformatics/btp352"]
    assert m["maintainers"] == ["alice", "bob"]


def test_parse_meta_tolerates_complex_jinja():
    text = 'package:\n  name: x\n  version: {{ version }}\nabout:\n  license: {{ lic|lower }}\n'
    m = bioconda.parse_meta(text)
    # unresolved jinja is blanked, not crashed
    assert m["version"] == ""
    assert m["license"] == ""
