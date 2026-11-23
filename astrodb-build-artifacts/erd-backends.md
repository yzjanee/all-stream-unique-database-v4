Backend availability
  builtin-mermaid        AVAILABLE   (pyyaml only - always works)
  d2 binary              missing     not required; https://d2lang.com
  mermaid-cli (mmdc)     missing     not required; npx -y @mermaid-js/mermaid-cli
  npx                    available   /usr/local/bin/npx
  graphviz `dot`         missing     NOT required by this skill
  plantuml               missing     not supported by this skill; see references/backends.md
  java                   available   /usr/bin/java
  eralchemy >=1.7        missing     optional; uv add "eralchemy[graphviz]"
  eralchemy2             missing     DEPRECATED, merged into eralchemy 1.5+; do not install
  paracelsus             missing     optional; uv add paracelsus
  mermaidx               missing     optional; renders mermaid without node or graphviz
  sqlalchemy             available   only needed by the SQLAlchemy-based backends
  lsst-felis             available   only needed by the SQLAlchemy-based backends
  graphviz (python)      missing     needs the system graphviz binary as well
  pydot                  missing     needs the system graphviz binary as well
  sqlalchemy-schemadisplay missing     optional; needs system graphviz

RECOMMENDATION: builtin-mermaid - no installs needed.
No image renderer found on PATH. None is required - Mermaid text is the deliverable.
