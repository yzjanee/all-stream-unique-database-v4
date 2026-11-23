# AstroDB Schema Match: all_streams_unique.fits

**Date:** 2026-11-22  
**Input:** all_streams_unique-parsed-data-table.md  
**Summary:** {'High': 26, 'Ignored': 13, 'Proposed (new field)': 1}

| Column | Description | Units | DB Table | DB Field | Confidence | Notes |
|---|---|---|---|---|---|---|
| `source_id` | Gaia DR3 source identifier | — | Sources | `source` | High | Stored as "Gaia DR3 <id>"; raw integer also to Names.other_name (directions.md) |
| `dist` | Heliocentric distance | kpc | ModeledParameters | `value` | High | parameter=dist_kpc (directions.md) |
| `dist_err` | Uncertainty on dist | kpc | ModeledParameters | `error` | High | error for dist_kpc |
| `Vr` | Heliocentric radial velocity | km s-1 | RadialVelocities | `rv_kms` | High | name + units |
| `Vr_err` | Uncertainty on Vr | km s-1 | RadialVelocities | `rv_error` | High | Vr_err = 0 stored as NULL |
| `FeH` | Iron abundance [Fe/H] | dex | ModeledParameters | `value` | High | parameter=FeH (directions.md) |
| `FeH_err` | Uncertainty on FeH | dex | ModeledParameters | `error` | High | error for FeH |
| `aFe` | Alpha-element abundance | dex | ModeledParameters | `value` | High | parameter=aFe (directions.md) |
| `aFe_err` | Uncertainty on aFe | dex | ModeledParameters | `error` | High | error for aFe |
| `p_mem` | Stream membership probability | — | Associations | `membership_probability` | High | (directions.md) |
| `ra` | Right ascension (J2016.0) | deg | Sources | `ra_deg` | High | epoch_year = 2016.0 |
| `ra_error` | Uncertainty on ra | mas | — | `—` | Ignored | No position-error field in Sources; user chose ignore |
| `dec` | Declination (J2016.0) | deg | Sources | `dec_deg` | High | epoch_year = 2016.0 |
| `dec_error` | Uncertainty on dec | mas | — | `—` | Ignored | No position-error field in Sources; user chose ignore |
| `parallax` | Gaia DR3 parallax | mas | Parallaxes | `parallax_mas` | High | Keep negative/bad parallaxes; 5 NaN rows skipped |
| `parallax_error` | Uncertainty on parallax | mas | Parallaxes | `parallax_error` | High |  |
| `parallax_over_error` | Parallax / error | — | — | `—` | Ignored | Derivable; user chose ignore |
| `pm` | Total proper motion | mas yr-1 | — | `—` | Ignored | Derivable from pmra, pmdec; user chose ignore |
| `pmra` | Proper motion in RA | mas yr-1 | ProperMotions | `pm_ra` | High |  |
| `pmra_error` | Uncertainty on pmra | mas yr-1 | ProperMotions | `pm_ra_error` | High |  |
| `pmdec` | Proper motion in Dec | mas yr-1 | ProperMotions | `pm_dec` | High |  |
| `pmdec_error` | Uncertainty on pmdec | mas yr-1 | ProperMotions | `pm_dec_error` | High |  |
| `ra_dec_corr` | Gaia DR3 correlation coefficient | — | — | `—` | Ignored | Spans tables; user chose ignore (as v3) |
| `ra_parallax_corr` | Gaia DR3 correlation coefficient | — | — | `—` | Ignored | Spans tables; user chose ignore (as v3) |
| `ra_pmra_corr` | Gaia DR3 correlation coefficient | — | — | `—` | Ignored | Spans tables; user chose ignore (as v3) |
| `ra_pmdec_corr` | Gaia DR3 correlation coefficient | — | — | `—` | Ignored | Spans tables; user chose ignore (as v3) |
| `dec_parallax_corr` | Gaia DR3 correlation coefficient | — | — | `—` | Ignored | Spans tables; user chose ignore (as v3) |
| `dec_pmra_corr` | Gaia DR3 correlation coefficient | — | — | `—` | Ignored | Spans tables; user chose ignore (as v3) |
| `dec_pmdec_corr` | Gaia DR3 correlation coefficient | — | — | `—` | Ignored | Spans tables; user chose ignore (as v3) |
| `parallax_pmra_corr` | Gaia DR3 correlation coefficient | — | — | `—` | Ignored | Spans tables; user chose ignore (as v3) |
| `parallax_pmdec_corr` | Gaia DR3 correlation coefficient | — | — | `—` | Ignored | Spans tables; user chose ignore (as v3) |
| `pmra_pmdec_corr` | pmra–pmdec correlation | — | ProperMotions | `pmra_pmdec_corr` | Proposed (new field) | Needs schema update — see Proposed Schema Additions (directions.md) |
| `phot_g_mean_mag` | Gaia G mean magnitude | mag | Photometry | `magnitude` | High | band = Gaia/Gaia3.G; telescope Gaia; regime optical |
| `bp_rp` | Gaia BP−RP colour | mag | ModeledParameters | `value` | High | parameter=bp_rp (directions.md) |
| `name` | Stellar stream name | — | Associations | `association` | High | 92 streams → AssociationList (directions.md) |
| `reference` | Membership paper(s) | — | Publications | `reference` | High | FK on every row; 2nd of comma-separated pair → comments |
| `d_orb` | Galactocentric orbital distance | kpc | ModeledParameters | `value` | High | parameter=d_orb_kpc (directions.md) |
| `X` | Galactocentric X | kpc | ModeledParameters | `value` | High | parameter=X_kpc (directions.md) |
| `Y` | Galactocentric Y | kpc | ModeledParameters | `value` | High | parameter=Y_kpc (directions.md) |
| `Z` | Galactocentric Z | kpc | ModeledParameters | `value` | High | parameter=Z_kpc (directions.md) |

## Lookup Table Checklist

- **Publications:** 46 reference strings → ~15 papers (map full names like Bonaca2020 to shortnames)
- **Telescopes:** Gaia
- **Instruments:** Gaia AF (imaging); Gaia RVS (spectroscopy, for Vr)
- **PhotometryFilters:** Gaia/Gaia3.G
- **RegimeList:** optical
- **AssociationList:** 92 stream names
- **ParameterList:** bp_rp, d_orb_kpc, X_kpc, Y_kpc, Z_kpc, dist_kpc, FeH, aFe

## Proposed Schema Additions

| Table | Field | Unit | Type | Description |
|---|---|---|---|---|
| ProperMotions | pmra_pmdec_corr | — | float | Correlation between pm_ra and pm_dec |

## Ignored Columns

- `ra_error` — No position-error field in Sources; user chose ignore
- `dec_error` — No position-error field in Sources; user chose ignore
- `parallax_over_error` — Derivable; user chose ignore
- `pm` — Derivable from pmra, pmdec; user chose ignore
- `ra_dec_corr` — Spans tables; user chose ignore (as v3)
- `ra_parallax_corr` — Spans tables; user chose ignore (as v3)
- `ra_pmra_corr` — Spans tables; user chose ignore (as v3)
- `ra_pmdec_corr` — Spans tables; user chose ignore (as v3)
- `dec_parallax_corr` — Spans tables; user chose ignore (as v3)
- `dec_pmra_corr` — Spans tables; user chose ignore (as v3)
- `dec_pmdec_corr` — Spans tables; user chose ignore (as v3)
- `parallax_pmra_corr` — Spans tables; user chose ignore (as v3)
- `parallax_pmdec_corr` — Spans tables; user chose ignore (as v3)

## Ingestion Notes

- `epoch_year = 2016.0` for every Sources row (constant, not a column).
- `adopted = True` on every measurement row (one measurement per star).
- 27 stars are in two streams: one Sources row each, two Associations rows.
- 5 stars have NaN parallax/proper motion: kept in Sources, skipped in Parallaxes/ProperMotions.
- No unit conversions needed: units already match the schema (km s-1 = km/s, mas yr-1 = mas/yr).
