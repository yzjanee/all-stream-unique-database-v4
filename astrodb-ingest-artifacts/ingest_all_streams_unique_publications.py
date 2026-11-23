"""Ingest the 15 stream-membership papers cited in all_streams_unique.fits into Publications.

Also removes the astrodb-template demo publications that nothing in v4 uses, and the
template's demo AssociationList row (TW Hydra Association). Keeps Cohe03, Cutr03, Wrig10 and
Gaia23 because template Telescopes/Instruments rows reference them.

Run from the repo root:
    uv run --python 3.13 --with astrodb-utils python astrodb-ingest-artifacts/ingest_all_streams_unique_publications.py
"""
import logging

from sqlalchemy import delete
from astrodb_utils import build_db_from_json
from astrodb_utils.publications import ingest_publication, find_publication, check_ads_token

logging.getLogger("astrodb_utils").setLevel(logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(format="%(levelname)s - %(message)s")

SAVE_DB = True  # user confirmed "Yes, save" on 2026-11-23 after a clean dry run
SETTINGS_FILE = "database.toml"

IGNORE_ADS = not check_ads_token()
if IGNORE_ADS:
    raise SystemExit("No ADS token found — set ADS_TOKEN before running (DOIs need ADS to fill metadata).")

# Resolved and verified against NASA ADS on 2026-11-22 (first author + year + title match the stream).
# Shortname = first 4 letters of first author's last name + 2-digit year. Comment = name used in the FITS file.
PUBLICATIONS = [
    {"reference": "Awad24", "doi": "10.1051/0004-6361/202347848"},  # Awad2024 — Jhelum
    {"reference": "Bona20", "doi": "10.3847/2041-8213/ab800c"},     # Bonaca2020 — GD-1
    {"reference": "Chan22", "doi": "10.3847/1538-4357/ac9b4b"},     # Chandra2022 — Bootes
    {"reference": "Ferg22", "doi": "10.3847/1538-3881/ac3492"},     # Ferguson2022 — Jet
    {"reference": "Gril19", "doi": "10.3847/1538-4357/ab441d"},     # Grillmair2019 — M5
    {"reference": "Gril22", "doi": "10.3847/1538-4357/ac5bd7"},     # Grillmair2022 — NGC 7089
    {"reference": "Huan19", "doi": "10.3847/1538-4357/ab158a"},     # Huang2019 — GD-1
    {"reference": "Ibat24", "doi": "10.3847/1538-4357/ad382d"},     # Ibata2024 — all-sky streams
    {"reference": "Kopo23", "doi": "10.1093/mnras/stad551"},        # Koposov2023 — S5
    {"reference": "Li__21", "doi": "10.3847/1538-4357/abeb18"},     # Li2021 — ATLAS-Aliqa Uma
    {"reference": "Ship19", "doi": "10.3847/1538-4357/ab44bf"},     # Shipp2019 — DES streams
    {"reference": "Ship20", "doi": "10.3847/1538-3881/abbd3a"},     # Shipp2020 — Palomar 13
    {"reference": "Vasi21", "doi": "10.1093/mnras/staa3673"},       # Vasiliev2021 — Sagittarius
    {"reference": "Yang22", "doi": "10.1051/0004-6361/202243976"},  # Yang2022 — NGC 5824
    {"reference": "Yang23", "doi": "10.3847/1538-4357/acdee2"},     # Yang2023 — M3
]
KEEP_TEMPLATE_PUBS = {"Cohe03", "Cutr03", "Wrig10", "Gaia23"}

db = build_db_from_json(settings_file=SETTINGS_FILE)

# --- Remove template demo rows nothing in v4 uses ---
template_pubs = [r[0] for r in db.query(db.Publications.c.reference).all()]
remove_pubs = sorted(set(template_pubs) - KEEP_TEMPLATE_PUBS)
with db.engine.begin() as conn:
    conn.execute(delete(db.AssociationList).where(db.AssociationList.c.association == "TW Hydra Association"))
    conn.execute(delete(db.Publications).where(db.Publications.c.reference.in_(remove_pubs)))
logger.info(f"Removed {len(remove_pubs)} template publications: {', '.join(remove_pubs)}")
logger.info("Removed template AssociationList row: TW Hydra Association")


def find_existing(db, doi):
    """Reference of the row with this DOI, or None. Never search by reference (fuzzy match)."""
    found, result = find_publication(db, doi=doi)
    if found:
        return result
    if result:
        return f"{result} existing rows"
    return None


def reference_taken(db, reference):
    return db.query(db.Publications).filter(db.Publications.c.reference == reference).count() > 0


added = already_present = failed = 0
for pub in PUBLICATIONS:
    ref, doi = pub["reference"], pub["doi"]
    existing = find_existing(db, doi)
    if existing:
        already_present += 1
        logger.info(f"Already present, skipping: {ref} ({existing})")
        continue
    if reference_taken(db, ref):
        failed += 1
        logger.warning(f"Shortname {ref} already used by a different paper — needs DOI suffix")
        continue
    try:
        ingest_publication(db, doi=doi, reference=ref, ignore_ads=IGNORE_ADS)
        added += 1
        logger.info(f"Ingested: {ref}")
    except Exception as e:
        failed += 1
        logger.warning(f"Failed to ingest {ref}: {e}")

rows = db.query(db.Publications).all()
logger.info(f"Done: {added} added, {already_present} already present, {failed} failed "
            f"out of {len(PUBLICATIONS)}. Publications now has {len(rows)} rows.")

if SAVE_DB:
    db.save_database("data/")
    logger.info("Database saved to data/.")
else:
    logger.info("Dry run complete — NOT saved.")
