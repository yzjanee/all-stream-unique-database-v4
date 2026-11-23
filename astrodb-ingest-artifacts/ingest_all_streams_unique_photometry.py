"""Ingest Gaia DR3 G magnitudes from all_streams_unique.fits into Photometry (astrodb-ingest-03-photometry)."""
import logging, collections
from astropy.table import Table
from sqlalchemy import update
from astrodb_utils import AstroDBError
from astrodb_utils.loaders import build_db_from_json
from astrodb_utils.photometry import ingest_photometry, ingest_photometry_filter
from astrodb_utils.utils import get_db_regime

SAVE_DB = True  # user confirmed 2026-11-23 (epoch empty, stream-paper reference)
SETTINGS_FILE = "database.toml"
DATA = "../all-stream-unique-database-v2/all_streams_unique.fits"
# (magnitude_column, svo_id, error_column, telescope)
BANDS = [("phot_g_mean_mag", "GAIA/GAIA3.G", None, "Gaia")]
BAND_SETUP = {"GAIA/GAIA3.G": ("GAIA", "GAIA3", "G")}
EPOCH = None  # Gaia DR3 G is a mean over 2014.6-2017.4; no single epoch
REF = {"Awad2024": "Awad24", "Bonaca2020": "Bona20", "Chandra2022": "Chan22",
       "Ferguson2022": "Ferg22", "Grillmair2019": "Gril19", "Grillmair2022": "Gril22",
       "Huang2019": "Huan19", "Ibata2024": "Ibat24", "Koposov2023": "Kopo23",
       "Li2021": "Li__21", "Shipp2019": "Ship19", "Shipp2020": "Ship20",
       "Vasiliev2021": "Vasi21", "Yang2022": "Yang22", "Yang2023": "Yang23"}

logging.getLogger("astrodb_utils").setLevel(logging.WARNING)
db = build_db_from_json(settings_file=SETTINGS_FILE)

# Fix template typo: Gaia was described as GALEX
with db.engine.begin() as conn:
    conn.execute(update(db.Telescopes).where(db.Telescopes.c.telescope == "Gaia")
                 .values(description="Gaia, ESA astrometry mission, Satellite/Spacecraft", reference="Gaia23"))

# Filter setup FIRST
for svo_id, (tel, inst, filt) in BAND_SETUP.items():
    if not len(db.query(db.PhotometryFilters).filter(db.PhotometryFilters.c.band == svo_id).table()):
        ingest_photometry_filter(db, telescope=tel, instrument=inst, filter_name=filt)
        print(f"Created filter {svo_id}")
    else:
        print(f"Filter {svo_id} already present")

def regime_from_wavelength(w):
    return "ultraviolet" if w < 3000 else "optical" if w < 10000 else "nir" if w < 30000 else "mir"
REGIME = {}
for _, svo_id, _, _ in BANDS:
    eff = db.query(db.PhotometryFilters).filter(db.PhotometryFilters.c.band == svo_id).table()["effective_wavelength_angstroms"][0]
    REGIME[svo_id] = get_db_regime(db, regime_from_wavelength(eff), raise_error=True)
print("Regimes:", REGIME)

# ingest_photometry() resolves every name through SIMBAD (no use_simbad switch), which is
# 80k web calls and fails when SIMBAD is down. So, per the skill's "custom insert modeled on
# ingest_photometry" pattern, validate source/band/reference against the DB and bulk insert.
t = Table.read(DATA)
known_sources = set(db.query(db.Sources.c.source).table()["source"])
known_refs = set(db.query(db.Publications.c.reference).table()["reference"])
known_bands = set(db.query(db.PhotometryFilters.c.band).table()["band"])
existing = {(r["source"], r["band"], r["reference"]) for r in db.query(db.Photometry).table()}
seen, ok, skips, rows = set(), 0, collections.defaultdict(list), []
for row in t:
    sid = str(row["source_id"])
    if sid in seen:
        skips["duplicate star row (first kept)"].append(sid); continue
    seen.add(sid)
    refs = [REF[r.strip()] for r in str(row["reference"]).split(",")]
    name = f"Gaia DR3 {sid}"
    for col, svo_id, ecol, tel in BANDS:
        mag = row[col]
        if (hasattr(mag, "mask") and mag.mask) or mag != mag:
            skips["no magnitude"].append(sid); continue
        key = (name, svo_id, refs[0])
        if name not in known_sources: skips["source missing"].append(name); continue
        if refs[0] not in known_refs: skips["reference missing"].append(refs[0]); continue
        if svo_id not in known_bands: skips["band missing"].append(svo_id); continue
        if key in existing: skips["duplicate"].append(name); continue
        existing.add(key)
        rows.append({"source": name, "band": svo_id, "magnitude": float(mag),
                     "magnitude_error": None, "telescope": tel, "regime": str(REGIME[svo_id]),
                     "epoch": EPOCH, "reference": refs[0],
                     "comments": (f"Also in: {', '.join(refs[1:])}" if len(refs) > 1 else None)})
with db.engine.begin() as conn:
    conn.execute(db.Photometry.insert(), rows)
ok = len(rows)
print(f"ingested={ok} rows={len(t)}")
for k, v in skips.items():
    print(f"skipped[{k}]={len(v)} e.g. {v[0]}")
if SAVE_DB:
    db.save_database("data/"); print("Saved to data/")
else:
    print("Dry run complete — NOT saved. Set SAVE_DB = True to write the database to JSON files.")
