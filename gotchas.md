# AstroDB Gotchas

Problems hit while running the AstroDB skills, and suggested fixes to the skills themselves.
Entries marked **gotcha** are worth reporting at
https://github.com/astrodbtoolkit/astrodb-bot/issues/new.
Each skill appends its own entries; do not edit existing ones.

## Setup names the next skill by an old name — astrodb-build-01-setup, 2026-11-22

**Kind:** gotcha
**Where:** astrodb-build-01-setup Step 9
**What happened:** Step 9 tells the user the next step is the `astro-parse-data-table` skill, which no longer exists. The skill is now `astrodb-build-02-parse-table`.
**Workaround:** Named `astrodb-build-02-parse-table` instead.
**Suggested change:** In `skills/astrodb-build-01-setup/SKILL.md` Step 9, replace both mentions of `astro-parse-data-table` with `astrodb-build-02-parse-table`.

## LICENSE step says "move on to Step 7" from inside Step 7 — astrodb-build-01-setup, 2026-11-22

**Kind:** gotcha
**Where:** astrodb-build-01-setup Step 7 (last line)
**What happened:** The skip instruction at the end of Step 7 says "move on to Step 7 without pressing", which points back at itself.
**Workaround:** Moved on to Step 8.
**Suggested change:** In `skills/astrodb-build-01-setup/SKILL.md` Step 7, change "move on to Step 7" to "move on to Step 8".

## Schema-validate runs before the schema it validates against exists — astrodb-build-04-schema-validate, 2026-11-22

**Kind:** gotcha
**Where:** astrodb-build-04-schema-validate Inputs (item 3) and Checkpoint
**What happened:** The pipeline order is 03 schema-match → 04 schema-validate → 05 schema-generate, but 04 needs `schema.yaml` to check against. At step 04 the repo only has the untouched template `schema.yaml`, so any proposed field from schema-match (here `ProperMotions.pmra_pmdec_corr`) shows up as "field not in schema.yaml", and nullability is checked against template rules rather than the user's schema.
**Workaround:** Validated against the template schema and reported the proposed field as expected-missing.
**Suggested change:** In `skills/astrodb-build-04-schema-validate/SKILL.md`, say explicitly that at this point `schema.yaml` is the template, and treat fields listed under the mapping's "Proposed Schema Additions" as expected rather than errors — or swap the order so validate runs after schema-generate.

## Generated test_orm_use fails on a foreign key — astrodb-build-06-create-db, 2026-11-22

**Kind:** gotcha
**Where:** astrodb-build-06-create-db `scripts/generate_tests.py` (test_database.py template)
**What happened:** The generated `test_orm_use` adds `Sources(source="Test ORM Source", reference="Test ORM Source")` without a matching Publications row, so pytest fails with `sqlite3.IntegrityError: FOREIGN KEY constraint failed`. v3 hit the same failure.
**Workaround:** Edited the generated test to add `Publications(reference="Test ORM Source")` first and delete it at the end.
**Suggested change:** In `generate_tests.py`, have the test_database.py template add and later remove a Publications row before inserting the Source.

## Removed tables stay in database.toml and data/reference — astrodb-build-06-create-db, 2026-11-22

**Kind:** gotcha
**Where:** astrodb-build-06-create-db Step 5 (and astrodb-build-01-setup Step 4)
**What happened:** When the generated schema drops template tables (here Versions, SourceTypeList, CompanionList), the existing `database.toml` still lists them in `lookup_tables`, and `data/reference/` still has their JSON files. Setup says to leave `data/reference/` alone and create-db says not to overwrite `database.toml`, so neither skill cleans them up; `build_db_from_json` would try to load tables that no longer exist.
**Workaround:** Removed the dropped tables from `lookup_tables`, deleted their JSON files, and deleted the old template tests for removed tables (morphology, positions).
**Suggested change:** In create-db Step 5, after copying schema.yaml: edit `lookup_tables` to only tables in the schema, delete `data/reference/<Table>.json` and `tests/test_contents_<table>.py` for tables not in the schema, and tell the user what was removed.

## create-db's `uv run` has no astrodbkit in a template-db repo — astrodb-build-06-create-db, 2026-11-22

**Kind:** gotcha
**Where:** astrodb-build-06-create-db Steps 6 and 8
**What happened:** The skill says `uv run python create_db.py`, but repos made from astrodb-template-db have no `pyproject.toml`, so `uv run` has no astrodbkit: `ERROR: Could not import astrodbkit: No module named 'astrodbkit'`. The suggested fix, `uv add astrodbkit`, also fails without a pyproject.
**Workaround:** `uv run --with astrodbkit --with astrodb-utils --with lsst-felis --with pytest python ...`
**Suggested change:** In Steps 6 and 8, use `uv run --with astrodbkit --with astrodb-utils --with lsst-felis --with pytest ...` when there's no `pyproject.toml` (matches the template's CLAUDE.md install line).
