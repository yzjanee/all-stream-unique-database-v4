# AstroDB build-workflow checklists

## astrodb-build-01-setup

- [x] **Directions** — read v3's directions.md (user-supplied as "use v3 answers") before asking; told the user it supplies the July 6 decisions but not the license holder.
- [x] Repo cloned to `~/Documents/GitHub/all-stream-unique-database-v4`; ✓ data, ✓ database.toml, ✓ schema.yaml.
- [x] `docs/figures/schema_erd.png` confirmed gone ("ERD removed"); `docs/schema/` has 0 files; told the user build-07-erd regenerates the diagram.
- [x] `data/source/` has 0 files; `data/reference/` intact (9 files).
- [x] `db_name = "all_streams_unique_v4"` in database.toml.
- [x] README title `all_streams_unique_v4` + v3 description; astrodb-utils line and ERD image link removed; credit line intact.
- [x] CLAUDE.md description updated, `## Git and GitHub` removed, `astrodb-template.sqlite` → `all_streams_unique_v4.sqlite`; upstream template links left alone.
- [x] LICENSE left as v3 had it (BSD 3-Clause, template authors); no name added that the user didn't give. Offered to add the user's name.
- [x] `astrodb-build-artifacts/` exists with `directions.md` copied from v3 (real, user-authored).
- [x] Told the user the repo folder is the project directory and named the next step (build-02-parse-table).
- [x] Repo name `all-stream-unique-database-v4` vs db_name `all_streams_unique_v4` differ only in style (hyphens vs underscores, "database"); raised it in the completion message.
- [x] Setup entry appended to `astrodb-build-artifacts/build-workflow.md`.
- [x] Two skill problems logged in `gotchas.md`.

## astrodb-build-02-parse-table

- [x] Descriptions taken via `TCOMMn` + VOTMETA check per format-specific-metadata.md — both absent, so all inferred (not from Step 2 output).
- [x] `.txt`/`.dat` MRT check — not applicable (input is `.fits`).
- [x] Sentinel scan done on every numeric column (min/max/mode); `Vr_err = 0` ×1,174 noted; no 999-style values.
- [x] Missing descriptions/units inferred; 40 lacked file descriptions (≥10), so noted in output instead of asking one by one.
- [x] dtypes shown as `float64`, `float32`, `int64`, `str`.
- [x] `all_streams_unique-parsed-data-table.md`/`.html` written flat in `astrodb-build-artifacts/`, each starting with the metadata block; no existing file overwritten.
- [x] Read with astropy under Python 3.13 (uv); sidecar records reader=astropy, format=fits, n_rows=80162, plus output paths.
- [x] Linked both files and asked the user to review; user confirmed "Looks good, continue" with no corrections or skipped columns.
- [x] Entry appended to `build-workflow.md`.
- [x] No skill problems worth logging this step.

## astrodb-build-03-schema-match

- [x] Input was the confirmed parse-table output (parse-table ran first).
- [x] Read references/schema.md and column-patterns.md; applied name/units/description layers; directions.md honored.
- [x] Photometry band resolved to SVO ID `Gaia/Gaia3.G`.
- [x] No spectral-type columns.
- [x] All 40 columns have a row (26 High, 1 Proposed, 13 Ignored); none dropped.
- [x] 13 uncertain columns raised in one combined question; user accepted suggestions.
- [x] `all_streams_unique-schema-match.md`/`.html` written flat in astrodb-build-artifacts/ with Lookup Table Checklist and Proposed Schema Additions.
- [x] Summary and both paths given in chat.
- [x] Asked the user to review the full mapping; user confirmed "Looks good, continue" with no corrections.
- [x] Entry appended to build-workflow.md.
- [x] No skill problems worth logging this step.

## astrodb-build-04-schema-validate

- [x] Had the mapping (schema-match .md), data file (from sidecar), and schema.yaml (repo root, template).
- [x] Parsed schema.yaml for datatype, nullable, length.
- [x] `validate_mapping.py` loaded data via sidecar reader (astropy/fits), counted NaN, masked, and empty-string nulls, read dtypes.
- [x] Checked nullable violations (7) and type mismatches (1) with broad compatibility.
- [x] Edge cases handled: `pmra_pmdec_corr` flagged as not in schema; no missing or all-null columns.
- [x] Report written to `astrodb-build-artifacts/schema-validation-report.md`; path given.
- [x] Asked the user to review; user confirmed "Yes, use fixes" (skip empty measurements, build Gaia DR3 strings).
- [x] Entry appended to build-workflow.md.
- [x] Skill problem logged in gotchas.md (validate runs before schema.yaml exists).

## astrodb-build-05-schema-generate

- [x] Schema name typed by the user: `all_streams_unique_v4`; `name:` and `@id: "#all_streams_unique_v4"` match.
- [x] Unmatched/problematic columns: already resolved in schema-match (13 ignored) and schema-validate (skip empty rows, cast source_id) — no new questions.
- [x] 15 tables, each with a template primary key; ModeledParameters PK changed (logged).
- [x] Felis syntax kept from the template; all FKs point at tables in the file (script asserts this).
- [x] Written to `astrodb-build-artifacts/all_streams_unique_v4-schema.yaml`; path given, YAML not pasted.
- [x] `felis validate` → "Successfully validated".
- [x] Reported path, counts (15 tables, 90 columns), ignored columns, assumptions.
- [x] Entry appended to build-workflow.md.
- [x] No skill problems worth logging this step.

## astrodb-build-06-create-db

- [x] Schema located (artifacts → copied to root); `felis validate schema.yaml` → "Successfully validated".
- [x] Database name from schema `name:` = `all_streams_unique_v4` (not a placeholder).
- [x] `data/reference/` and `data/source/` exist under the v4 repo; schema.yaml at root; existing database.toml kept (lookup list edited, not overwritten).
- [x] `create_db.py` → "Success! Created all_streams_unique_v4.sqlite (196.0 KB)"; `ls -lh` shows 196K.
- [x] `generate_tests.py` made 9 files; `pytest tests/ -v` → 10 passed (after the test_orm_use FK fix).
- [x] Final report given.
- [x] Asked the user to inspect the .sqlite and offered the ERD; user chose "Yes, make the ERD" (database inspection still theirs to do).
- [x] Entry appended to build-workflow.md.
- [x] Three skill problems logged in gotchas.md.

## astrodb-build-07-erd

- [x] Schema: `schema.yaml` in the repo root (location 2); `name: all_streams_unique_v4`.
- [x] `detect_erd_backends.py` run, saved to `erd-backends.md`: built-in Mermaid available; no d2/mmdc/dot; npx present.
- [x] Backend chosen with the user: built-in Mermaid, text only. Nothing installed; graphviz not suggested.
- [x] 15 tables > 10: overview + lookup/main/data proposed; user confirmed "Yes, go ahead".
- [x] 4 files written flat in astrodb-build-artifacts/ (`all_streams_unique_v4-erd-{overview,lookup,main,data}.md`); largest 3,163 chars vs 45,000 budget.
- [x] Files start with an `erDiagram` block; 23 relationships in the diagram = 23 ForeignKey constraints in schema.yaml. Parse check NOT run (no mmdc; npx download needs the user's OK) — told the user.
- [x] `docs/figures/schema_erd.md` written (ERD markers, keys detail) + `docs/schema/erd-*.md`; README `## Schema` section links to it (none existed before).
- [x] Report given with backend, paths, counts, changed files, regenerate and `--check` commands.
- [x] Entry appended to build-workflow.md.
- [x] No new skill problems this step.
