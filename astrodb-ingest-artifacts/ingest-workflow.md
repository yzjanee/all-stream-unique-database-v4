## Measurement tables, custom script (2026-11-23)
- No skill covers these, so I adapted v3's script: `astrodb-ingest-artifacts/ingest_all_streams_unique_measurements.py` (SAVE_DB = False).
- Dry run: Parallaxes 80,130; ProperMotions 80,130; RadialVelocities 6,942; Associations 80,162; ModeledParameters 458,088 (bp_rp/d_orb/X/Y/Z 80,135 each, dist 55,397, FeH 1,967, aFe 49); plus 92 AssociationList and 8 ParameterList rows. User confirmed; saved.

## ingest-03-photometry (2026-11-23)
- Script: `astrodb-ingest-artifacts/ingest_all_streams_unique_photometry.py` (SAVE_DB = False).
- Band phot_g_mean_mag -> GAIA/GAIA3.G (filter, Gaia telescope, and Gaia3 instrument already present); regime optical from 5822 Å.
- ingest_photometry forces a SIMBAD lookup per row (SIMBAD returned 404), so a validated bulk insert was used instead.
- Fixed the Gaia telescope description (it was the GALEX text). Epoch empty; reference = the stream paper; second paper in comments.
- Dry run: 80,135 ingested, 27 duplicate star rows skipped, 0 other skips. User confirmed; saved.

## ingest-02-sources (2026-11-23)
- Script: `astrodb-ingest-artifacts/ingest_all_streams_unique_sources.py` (SAVE_DB = False).
- User approved: skip SIMBAD check; `Gaia DR3 <id>` names + raw id in Names; epoch 2016.0; second paper -> `other_references`; first row wins for 27 duplicate stars.
- Dry run: 80,135 ingested, 27 duplicates skipped, 0 failed. User confirmed; saved 80,135 files to data/source/.

# AstroDB Ingest Workflow Log

Decisions made during ingestion — what was chosen and why. Newest entry first.

## astrodb-ingest-01-publications — 2026-11-23

**Input:** `reference` column of `all_streams_unique.fits` (15 unique papers after splitting comma-separated pairs)

### Decisions
- **Paper lookup:** reused v3's 15 DOIs and re-verified each with NASA ADS (first author, year, title fit the stream) — *the user asked to reuse v3 answers; the user confirmed the resolved table.*
- **Shortnames:** first 4 letters + 2-digit year; `Awad2024` → `Awad24`; `Li__21` padded. No collisions.
- **ADS:** token present, `IGNORE_ADS = False`; ADS filled bibcode and description for all 15.
- **Template demo publications:** removed 17 unused ones and the "TW Hydra Association" demo row; kept Cohe03, Cutr03, Wrig10, Gaia23 — *template Telescopes/Instruments rows reference them; the user chose this.*
- **Saved** only after the user said "Yes, save". Result: 15 added, 0 already present, 0 failed; Publications = 19 rows. AssociationList is now empty, so its JSON file was dropped by the save (refilled at ingest-02).
- **RegimeList fix:** the save erased the `nir`/`fir` descriptions (the loader ignores keys missing from a file's first row). Restored them from git and gave every row a `description` key. Logged in gotchas.md.
- 10/10 tests pass after the save.

### Open questions
- `Cutr03` (2MASS catalog) has no DOI — it's a template paper, left as-is.
