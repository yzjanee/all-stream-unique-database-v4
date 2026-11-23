"""Ingest all_streams_unique.fits into Sources and Names (astrodb-ingest-02-sources)."""
import sys, logging
from astropy.table import Table
from astrodb_utils.loaders import build_db_from_json
from astrodb_utils.sources import ingest_source, ingest_name

SAVE_DB = True           # user confirmed 2026-11-23 after clean dry run
LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else None  # rows to try (dry-run sample)
DATA = "../all-stream-unique-database-v2/all_streams_unique.fits"

REF = {"Awad2024": "Awad24", "Bonaca2020": "Bona20", "Chandra2022": "Chan22",
       "Ferguson2022": "Ferg22", "Grillmair2019": "Gril19", "Grillmair2022": "Gril22",
       "Huang2019": "Huan19", "Ibata2024": "Ibat24", "Koposov2023": "Kopo23",
       "Li2021": "Li__21", "Shipp2019": "Ship19", "Shipp2020": "Ship20",
       "Vasiliev2021": "Vasi21", "Yang2022": "Yang22", "Yang2023": "Yang23"}

logging.getLogger("astrodb_utils").setLevel(logging.WARNING)
db = build_db_from_json(settings_file="database.toml")
t = Table.read(DATA)
seen, ok, dup, fail = set(), 0, 0, []
for row in t[:LIMIT]:
    sid = str(row["source_id"])
    if sid in seen:
        dup += 1
        continue
    seen.add(sid)
    refs = [REF[r.strip()] for r in str(row["reference"]).split(",")]
    name = f"Gaia DR3 {sid}"
    try:
        ingest_source(db, name, refs[0], ra=float(row["ra"]), dec=float(row["dec"]),
                      epoch=2016.0, other_reference=",".join(refs[1:]) or None,
                      search_db=False, use_simbad=False, raise_error=True)
        ingest_name(db, source=name, other_name=sid, raise_error=True)
        ok += 1
    except Exception as e:
        fail.append((name, str(e)[:120]))

print(f"ingested={ok} skipped_duplicates={dup} failed={len(fail)}")
for f in fail[:10]:
    print("FAIL", f)
if SAVE_DB and not fail:
    db.save_database("data/")
    print("Saved to data/")
