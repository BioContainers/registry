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
  summary: Tools for manipulating SAM/BAM/CRAM
'''


def test_parse_meta_resolves_version_and_about():
    m = bioconda.parse_meta(META)
    assert m["version"] == "1.19"
    assert m["home"] == "http://www.htslib.org/"
    assert m["license"] == "MIT"
    assert m["summary"].startswith("Tools for manipulating")


def test_parse_meta_tolerates_complex_jinja():
    text = 'package:\n  name: x\n  version: {{ version }}\nabout:\n  license: {{ lic|lower }}\n'
    m = bioconda.parse_meta(text)
    # unresolved jinja is blanked, not crashed
    assert m["version"] == ""
    assert m["license"] == ""
