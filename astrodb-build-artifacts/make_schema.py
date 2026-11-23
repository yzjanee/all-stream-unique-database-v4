"""Build all_streams_unique_v4 schema from the template schema.yaml + the schema-match mapping."""
import copy, yaml
s = yaml.safe_load(open("schema.yaml"))
keep = ["Publications","Telescopes","Instruments","PhotometryFilters","RegimeList","AssociationList",
        "ParameterList","Sources","Names","Photometry","Parallaxes","RadialVelocities","Associations",
        "ProperMotions","ModeledParameters"]
s["name"] = "all_streams_unique_v4"; s["@id"] = "#all_streams_unique_v4"
s["description"] = ("Unique Gaia DR3 stellar stream members (80,162 rows, 80,135 stars, 92 streams) from "
                    "Ibata et al. 2024 and associated works.")
s["tables"] = [t for t in s["tables"] if t["name"] in keep]
ids = {"#"+t["name"] for t in s["tables"]} | {c["@id"] for t in s["tables"] for c in t["columns"]}
for t in s["tables"]:
    for con in t.get("constraints", []):
        for r in con.get("referencedColumns", []):
            assert r in ids, f"{t['name']} FK points at removed {r}"
    if t["name"] == "ProperMotions":
        i = [c["name"] for c in t["columns"]].index("pm_dec_error_lower") + 1
        t["columns"].insert(i, {"name": "pmra_pmdec_corr", "@id": "#ProperMotions.pmra_pmdec_corr",
            "datatype": "double", "description": "Correlation coefficient between pm_ra and pm_dec (Gaia DR3 pmra_pmdec_corr)",
            "ivoa:ucd": "stat.correlation"})
    if t["name"] == "ModeledParameters":
        t["primaryKey"] = ["#ModeledParameters.source", "#ModeledParameters.parameter", "#ModeledParameters.reference"]
yaml.safe_dump(s, open("astrodb-build-artifacts/all_streams_unique_v4-schema.yaml", "w"), sort_keys=False, allow_unicode=True, width=120)
print(len(s["tables"]), "tables,", sum(len(t["columns"]) for t in s["tables"]), "columns")
