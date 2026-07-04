from biocontainers_pipeline.sources import bioconda

META = '''{% set version = "1.19" %}
package:
  name: samtools
  version: {{ version }}
about:
  home: http://www.htslib.org/
  license: MIT
  summary: Tools for manipulating SAM/BAM/CRAM
'''


def test_parse_meta_reads_about_block():
    m = bioconda.parse_meta(META)
    assert m["home"] == "http://www.htslib.org/"
    assert m["license"] == "MIT"
    assert m["summary"].startswith("Tools for manipulating")
