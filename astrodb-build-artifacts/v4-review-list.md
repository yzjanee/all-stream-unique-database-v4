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

## Problems
- **build-01-setup (skill bug):** Step 9 names the next skill by an old name (`astro-parse-data-table`). Logged in `gotchas.md`.
- **build-01-setup (skill bug):** Step 7 says "move on to Step 7". Logged in `gotchas.md`.
- **ADS token:** pasted into chat twice; needs regenerating and setting as `ADS_TOKEN` by Jane before ingest-01.
- **build-04-schema-validate (skill issue):** Runs before schema.yaml is generated, so proposed fields show as missing. Logged in `gotchas.md`.
- **build-06-create-db (skill bug):** Generated `test_orm_use` fails on a foreign key; fixed by hand. Logged in `gotchas.md`.
- **build-06-create-db (skill gap):** Removed tables stay in database.toml and data/reference. Logged in `gotchas.md`.
- **build-06-create-db (skill gap):** `uv run` has no astrodbkit in a template repo. Logged in `gotchas.md`.
