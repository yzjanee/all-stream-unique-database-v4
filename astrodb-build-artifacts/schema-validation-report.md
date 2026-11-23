## Schema Mapping Validation Report
Source: all_streams_unique.fits → schema.yaml (template schema; v4 schema not generated yet)
Date: 2026-11-22

27 mapped columns checked (13 ignored columns skipped). Script: `astrodb-build-artifacts/validate_mapping.py`.

### Nullable Violations  (7 issues)
| Data Column | Maps To | Null Count | Total Rows | % Null |
|---|---|---|---|---|
| dist | ModeledParameters.value | 24,765 | 80,162 | 30.9% |
| Vr | RadialVelocities.rv_kms | 73,214 | 80,162 | 91.3% |
| FeH | ModeledParameters.value | 78,195 | 80,162 | 97.5% |
| aFe | ModeledParameters.value | 80,113 | 80,162 | 99.9% |
| parallax | Parallaxes.parallax_mas | 5 | 80,162 | 0.0% |
| pmra | ProperMotions.pm_ra | 5 | 80,162 | 0.0% |
| pmdec | ProperMotions.pm_dec | 5 | 80,162 | 0.0% |

All seven are measurements that some stars simply don't have. **Suggested fix: skip the row in that table when the value is empty** (no row is written, so the non-nullable field is never empty). The star still gets its Sources row. This is what v3 did and matches `directions.md`.

### Type Mismatches  (1 issue)
| Data Column | Data Type | Maps To | Expected Type | Compatible? |
|---|---|---|---|---|
| source_id | int64 | Sources.source | string | ❌ No |

Expected: the mapping already says to store it as the string `"Gaia DR3 <source_id>"`. **Suggested fix: build that string in the ingest script.**

### Edge cases
- **Field not in schema.yaml:** `pmra_pmdec_corr` → `ProperMotions.pmra_pmdec_corr`. Expected — it is a proposed new field that `astrodb-build-05-schema-generate` will add (5 nulls, so make it nullable).
- No columns missing from the data. No all-null columns. No masked values or empty strings.

### Clean Mappings  (18 columns OK)
dist_err → ModeledParameters.error · Vr_err → RadialVelocities.rv_error · FeH_err → ModeledParameters.error · aFe_err → ModeledParameters.error · p_mem → Associations.membership_probability · ra → Sources.ra_deg · dec → Sources.dec_deg · parallax_error → Parallaxes.parallax_error · pmra_error → ProperMotions.pm_ra_error · pmdec_error → ProperMotions.pm_dec_error · phot_g_mean_mag → Photometry.magnitude · bp_rp → ModeledParameters.value · name → Associations.association · reference → Publications.reference · d_orb → ModeledParameters.value · X → ModeledParameters.value · Y → ModeledParameters.value · Z → ModeledParameters.value

(float32 → double counted as compatible.)

### Summary
- 7 nullable violations found (all fixed by skipping empty measurements)
- 1 type mismatch found (source_id → "Gaia DR3 <id>" string, already planned)
- 1 proposed field not yet in schema (pmra_pmdec_corr)
- 18 columns passed validation cleanly

**Next steps:**
- For nullable violations: skip rows with empty values in the ingest scripts.
- For the type mismatch: cast `source_id` to the `"Gaia DR3 <id>"` string in the ingest script.
- schema-generate: add nullable `ProperMotions.pmra_pmdec_corr`.
