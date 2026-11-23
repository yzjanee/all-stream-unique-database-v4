# v4 review list

Every question asked, assumption made, and problem hit while building v4. Sent to Jane when v4 is done.

## Questions asked (and answers)
- **build-01-setup:** Reuse v3's directions.md? → Yes, use v3 answers but run every skill from the start.
- **build-01-setup:** Database name `all_streams_unique_v4`? Data file `all_streams_unique.fits` only? → Yes to both.
- **build-02-parse-table:** Are the 40 inferred descriptions/units right? → Confirmed, no changes.
- **build-03-schema-match:** What to do with `ra_error`, `dec_error`, `pm`, `parallax_over_error`, and the 9 non-pmra/pmdec `*_corr` columns? → Ignore all (suggestion accepted).
- **build-03-schema-match:** Does the full mapping look right? → Confirmed, no changes.

- **build-04-schema-validate:** Skip rows with empty measurements (7 columns) and build "Gaia DR3 <id>" strings? → Yes, use fixes.

- **build-05-schema-generate:** Schema name? → `all_streams_unique_v4`.

- **build-07-erd:** Mermaid text with overview + lookup/main/data views? → Yes.

- **ingest-01-publications:** Confirm the 15 papers resolved via ADS? → Yes.
- **ingest-01-publications:** Remove the template's 21 demo papers? → Yes, but keep the 4 that template Telescopes/Instruments rows need (Cohe03, Cutr03, Wrig10, Gaia23); removed 17 + the TW Hydra demo association.
- **ingest-01-publications:** Save after the dry run? → Yes, save (15 added, 19 rows total).

## Assumptions
- **build-01-setup:** README/CLAUDE.md description copied from v3; LICENSE left with template authors (no name given).
- **build-02-parse-table:** All 40 column descriptions inferred (file has none). `FeH` unit `[-]` read as dex; `aFe` assumed dex; `p_mem`, `parallax_over_error`, `*_corr` assumed dimensionless.
- **build-02-parse-table:** `Vr_err = 0` (1,174 rows) treated as "no uncertainty reported".
- **build-03-schema-match:** Directions say "`*_corr` → ProperMotions"; read as only `pmra_pmdec_corr` (the others span tables).
- **build-04-schema-validate:** Validated against the template schema.yaml, since v4's isn't generated until build-05.

- **build-05-schema-generate:** ModeledParameters primary key changed to (source, parameter, reference), dropping the nullable `model` (as v3 did; not in directions.md).
- **build-05-schema-generate:** Removed the same 10 unused template tables as v3.

- **build-06-create-db:** Removed Versions/SourceTypeList/CompanionList from database.toml and their JSON files, and the morphology/positions template tests.
- **build-06-create-db:** Kept the template's 21 demo publications in `data/reference/Publications.json` for now — decide at ingest-01 whether to remove them (v3 cleared them).

- **build-07-erd:** ERD was not parse-checked (would need downloading mermaid-cli with npx).

- **ingest-01-publications:** Used v3's DOIs and re-verified each against ADS (author, year, title). `Awad2024` renamed `Awad24` to follow the naming rule.

## Problems
- **build-01-setup (skill bug):** Step 9 names the next skill by an old name (`astro-parse-data-table`). Logged in `gotchas.md`.
- **build-01-setup (skill bug):** Step 7 says "move on to Step 7". Logged in `gotchas.md`.
- **ADS token:** pasted into chat twice; needs regenerating and setting as `ADS_TOKEN` by Jane before ingest-01.
- **build-04-schema-validate (skill issue):** Runs before schema.yaml is generated, so proposed fields show as missing. Logged in `gotchas.md`.
- **build-06-create-db (skill bug):** Generated `test_orm_use` fails on a foreign key; fixed by hand. Logged in `gotchas.md`.
- **build-06-create-db (skill gap):** Removed tables stay in database.toml and data/reference. Logged in `gotchas.md`.
- **build-06-create-db (skill gap):** `uv run` has no astrodbkit in a template repo. Logged in `gotchas.md`.
- **Template data bug:** `Telescopes.json` describes `Gaia` as "Galaxy Evolution Explorer 50 cm" (that's GALEX). Fix at the photometry step.
- **ingest-01-publications (skill bug):** Example script calls `save_database()` without the required directory. Logged in `gotchas.md`.
- **ingest-01-publications (skill gap):** No guidance on template demo publications, which other lookup rows depend on. Logged in `gotchas.md`.
- **ingest-01-publications (dependency bug):** Saving erased 2 RegimeList descriptions because the loader only reads keys from a file's first row. Restored and fixed. Logged in `gotchas.md`.

## ingest-02-sources (2026-11-23)
- **Assumption (approved):** skipped the SESAME/SIMBAD name check for 80,135 Gaia DR3 IDs (too slow; most stream stars not in SIMBAD). Same as v3. `use_simbad=False`, `search_db=False`.
- **Assumption (approved):** source name = `Gaia DR3 <source_id>`; raw source_id also added to Names; epoch_year fixed at 2016.0.
- **Decision (approved, differs from v3 directions.md):** for the 484 rows with two papers, the second paper goes in `Sources.other_references` instead of `comments`.
- **Note:** 27 stars appear twice in the FITS file; the first row is used.
- **Note:** paper names in the data (e.g. Ibata2024) are converted to shortnames (Ibat24) in the script.

## ingest-03-photometry (2026-11-23)
- **Problem:** `ingest_photometry` makes a SIMBAD call per star and has no switch to turn that off. SIMBAD was down, so I used a custom bulk insert with the same checks (logged in gotchas.md).
- **Assumption:** band `GAIA/GAIA3.G` (SVO), telescope Gaia, regime optical (derived from 5822 Å). No G error column in the FITS file.
- **Assumption (please check):** epoch left empty. Gaia DR3 G is a mean over 2014.6–2017.4, so there is no single epoch. 2016.0 is the alternative.
- **Assumption (please check):** the reference is the star's stream paper (from directions.md), not Gaia DR3 (Gaia23), even though the magnitude comes from Gaia.
- **Fix:** the template's Gaia telescope description said "Galaxy Evolution Explorer 50 cm" (GALEX). Changed it to a Gaia description with reference Gaia23.
- **Note:** a second paper goes in `comments` ("Also in: ..."), because Photometry has no other_references column.

## Measurement tables, custom script (2026-11-23)
- **Problem:** no skill covers Parallaxes, ProperMotions, RadialVelocities, ModeledParameters, or Associations/AssociationList/ParameterList. Adapted v3's custom script (`ingest_all_streams_unique_measurements.py`).
- **Changes from v3:** Photometry, Telescopes, Instruments, and filters removed (already done); `adopted` dropped from ModeledParameters (not in the v4 schema); `Awad2024` → `Awad24`; second paper written as "Also in: X".
- **Carried over from v3 (please check):** the reference for each stream in AssociationList is a hand-picked "first paper" (mostly Ibat24); all association_type = "stellar_stream"; adopted=True everywhere; Vr_err = 0 stored as NULL.
- **Note:** 5 stars have no parallax or proper motion and are skipped. 27 stars belong to two streams, so they have 2 Associations rows each.
- **Note:** v3's `insert_or_skip` silently ignores insert errors for the lookup rows. The Associations and ModeledParameters inserts would fail on the foreign keys if any lookup row were missing, so this is low risk, but it would hide a bad description.
- **build-06-create-db (skill gap):** generated content tests expect 0 rows; after ingest I updated the counts by hand (Sources 80,135; Parallaxes/ProperMotions 80,130; RadialVelocities 6,942; ModeledParameters 458,088). Logged in gotchas.md.
