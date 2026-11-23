# AstroDB Build Workflow Log

Decisions made during the build phase — what was chosen and why.
Each skill adds one entry. Do not edit existing entries; add new ones at the end.

## astrodb-build-01-setup — 2026-11-22

**Input:** https://github.com/yzjanee/all-stream-unique-database-v4 (created from astrodb-template-db)

### Decisions
- **Database name:** `all_streams_unique_v4` — *because the user agreed to follow the v3 name (`all_streams_unique_v3`) with the version bumped.*
- **Directions document:** copied v3's `astrodb-build-artifacts/directions.md` (July 6, 2026 meeting decisions) — *because the user asked to reuse the v3 answers while re-running every skill from the start.*
- **README/CLAUDE.md description:** reused the v3 README description — *because the user asked to reuse v3 answers; the directions document has no description section.*
- **README badges:** pointed the build and license badges at the v4 repo — *because the template's badges point at the template repo.*
- **LICENSE:** left as BSD 3-Clause with the template authors unchanged — *because that is what v3 did; the directions document does not name a copyright holder, so no name was added.*
- **Source data:** `all_streams_unique.fits` only (unique stars, as in v3) — *because the user chose not to add `all_stream.fits` yet.*

### Open questions
- Whether to add the user's name to the LICENSE copyright line.

## astrodb-build-02-parse-table — 2026-11-22

**Input:** `~/Documents/GitHub/all-stream-unique-database-v2/all_streams_unique.fits` (80,162 rows × 40 columns)

### Decisions
- **Reader:** astropy `Table.read` on the FITS BINTABLE (extension 1) — *because astropy reads FITS natively; no fallback was needed.*
- **Descriptions:** all 40 inferred — *because the file has no `TCOMMn` keywords and no embedded VOTable metadata.* Gaia columns use standard Gaia DR3 meanings; `dist`, `d_orb`, `X/Y/Z` follow v3's description (heliocentric distance, Galactocentric orbital distance, Galactocentric coordinates).
- **Units:** `FeH`/`FeH_err` read as dex (file says `[-]`, not a valid FITS unit); `aFe`/`aFe_err` assumed dex; `p_mem`, `parallax_over_error`, `*_corr` dimensionless — *because the file gives no unit for them.*
- **Gap-filling:** did not ask column by column — *because 40 columns lacked descriptions (the skill asks only when fewer than 10); the user reviews the inferred values in the HTML instead.*
- **Fill values:** flagged `Vr_err = 0` (1,174 rows) as likely "no uncertainty reported"; no `999`-style sentinels found.

### Open questions
- User to confirm the inferred descriptions for `dist`, `d_orb`, `X/Y/Z`, `p_mem`, and `reference`.

## astrodb-build-03-schema-match — 2026-11-22

**Input:** `astrodb-build-artifacts/all_streams_unique-parsed-data-table.md`

### Decisions
- **26 columns** mapped High from name/units and `directions.md` (Sources, Names, Parallaxes, ProperMotions, RadialVelocities, Photometry, Associations, ModeledParameters).
- **`pmra_pmdec_corr`:** proposed new field on ProperMotions — *because directions.md and v3 both put it there.*
- **Ignored (user choice):** `ra_error`, `dec_error` (no Sources field; Sources stays minimal), `pm` and `parallax_over_error` (derivable), and 9 cross-table `*_corr` columns — *because the user accepted these suggestions; directions.md's "`*_corr` → ProperMotions" was read as covering only pmra_pmdec_corr.*
- **No unit conversions:** file units already match the schema.

## astrodb-build-04-schema-validate — 2026-11-22

**Input:** `all_streams_unique.fits` against `schema.yaml` (still the template schema) using `all_streams_unique-schema-match.md`

### Decisions
- **Validated against the template schema** — *because schema.yaml is generated in the next skill (build-05); only the proposed `pmra_pmdec_corr` is missing from it.*
- **7 nullable violations** (`dist`, `Vr`, `FeH`, `aFe`, `parallax`, `pmra`, `pmdec`): suggested skipping rows with empty values rather than making fields nullable — *because these are measurements some stars don't have, and v3 / directions.md did the same.*
- **source_id int → string:** expected; ingest builds `"Gaia DR3 <id>"`.

### Open questions
- build-05 must add `ProperMotions.pmra_pmdec_corr` as nullable (5 empty values).

## astrodb-build-05-schema-generate — 2026-11-22

**Input:** `all_streams_unique-schema-match.md`, `schema-validation-report.md`, template `schema.yaml`

### Decisions
- **Schema name:** `all_streams_unique_v4` — *typed by the user.*
- **Built from the template schema** (`make_schema.py`), keeping the 15 tables the mapping uses (7 lookup + Sources, Names, Photometry, Parallaxes, RadialVelocities, Associations, ProperMotions, ModeledParameters) — *so field definitions, UCDs and FKs stay identical to the template.* Removed: Versions, CompanionList, SourceTypeList, Positions, CompanionRelationships, CompanionParameters, SourceTypes, RotationalParameters, Morphology, Spectra (same set as v3).
- **New field `ProperMotions.pmra_pmdec_corr`** (double, nullable, UCD `stat.correlation`) — *proposed in schema-match; nullable because 5 rows are empty.*
- **ModeledParameters primary key** changed from (source, model, parameter, reference) to (source, parameter, reference) — *because `model` is nullable and unused here; a nullable column in a primary key lets duplicates through in SQLite. v3 made the same change.* The `model` column itself is kept.
- **Nullable flags unchanged** — *because the user chose to skip empty measurements instead of relaxing fields.*
- **Primary keys** all taken from the template; none inferred.
- `felis validate` passed on the first run.

## astrodb-build-06-create-db — 2026-11-22

**Input:** `astrodb-build-artifacts/all_streams_unique_v4-schema.yaml`

### Decisions
- **Project root:** the v4 repo — *confirmed as the project folder during setup.*
- **schema.yaml:** copied the v4 schema over the repo's template `schema.yaml` — *because database.toml and the tests read `schema.yaml` at the root.*
- **database.toml:** kept the existing file; removed `Versions`, `SourceTypeList`, `CompanionList` from `lookup_tables` — *because those tables are no longer in the schema and `build_db_from_json` would try to load them.*
- **data/reference:** removed `CompanionList.json` and `SourceTypeList.json` — *same reason.* Kept the other 7, including the template's 21 demo publications (decide at ingest-01).
- **Old template tests:** removed `test_contents_morphology.py` and `test_contents_positions.py` — *their tables were removed.*
- **Python environment:** ran scripts with `uv run --with astrodbkit --with astrodb-utils --with lsst-felis --with pytest` — *because the repo has no pyproject.toml, so plain `uv run` had no astrodbkit.*
- **Test fix:** generated `test_orm_use` failed with `FOREIGN KEY constraint failed` (it adds a Source whose reference isn't in Publications). Edited it to add the publication first, then delete it. 10/10 tests pass.

## astrodb-build-07-erd — 2026-11-22

**Input:** `schema.yaml` (repo root)

### Decisions
- **Backend:** built-in Mermaid, text only — *user chose it; no image renderer (d2, mmdc, dot) was on PATH, and nothing was installed.*
- **Split:** overview + lookup / main / data views — *15 tables is too many for one readable diagram; user confirmed the template's Lookup/Main/Data grouping.*
- **Detail:** `full` for the split views in artifacts and `docs/schema/erd-*.md`; `keys` for `docs/figures/schema_erd.md` — *the skill's defaults; keys keeps the README-linked diagram small.*
- **README:** added a `## Schema` section linking to `docs/figures/schema_erd.md` — *the README had no Schema section.*
- **Parse check:** not run — *mmdc isn't installed, and the npx fallback downloads mermaid-cli, which needs the user's OK.*
- **Size:** largest diagram 3,163 characters, far under the 45,000 budget.
