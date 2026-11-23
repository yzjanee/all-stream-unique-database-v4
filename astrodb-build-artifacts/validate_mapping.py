"""Validate all_streams_unique.fits against schema.yaml using the schema-match mapping."""
import json, re, sys
import numpy as np, yaml
from astropy.table import Table

meta = json.load(open("astrodb-build-artifacts/astrodb-parse-result.json"))
t = Table.read(meta["file_path"], format=meta["format"])
schema = yaml.safe_load(open("schema.yaml"))
fields = {tb["name"]: {c["name"]: {"datatype": c["datatype"], "nullable": c.get("nullable", True), "length": c.get("length")}
          for c in tb["columns"]} for tb in schema["tables"]}

rows = []
for line in open("astrodb-build-artifacts/all_streams_unique-schema-match.md"):
    m = re.match(r"\| `([^`]+)` \|[^|]*\|[^|]*\| (\w+) \| `([^`]+)` \| ([^|]+) \|", line)
    if m and m.group(2) != "—" and m.group(3) != "—":
        rows.append((m.group(1), m.group(2), m.group(3)))

compat = {"string": "SUa", "char": "SUa", "text": "SUa", "double": "f", "float": "f",
          "int": "i", "long": "i", "short": "i", "boolean": "b", "timestamp": "MSU"}
out = []
for col, table, field in rows:
    r = {"col": col, "table": table, "field": field}
    if col not in t.colnames:
        r["error"] = "column not in data"; out.append(r); continue
    c = t[col]; kind = c.dtype.kind
    if kind == "f":
        nulls = int(np.isnan(np.asarray(c)).sum())
    else:
        vals = np.char.strip(np.asarray(c).astype(str)) if kind in "SU" else None
        nulls = int((vals == "").sum()) if vals is not None else 0
    if getattr(c, "mask", None) is not None and np.any(c.mask):
        nulls = max(nulls, int(np.sum(c.mask)))
    r.update(dtype=str(c.dtype.newbyteorder("=")), nulls=nulls, total=len(c))
    f = fields.get(table, {}).get(field)
    if f is None:
        r["error"] = "field not in schema.yaml"
    else:
        r.update(expected=f["datatype"], nullable=f["nullable"],
                 compatible=kind in compat.get(f["datatype"], ""))
    out.append(r)
json.dump(out, sys.stdout, indent=1)
