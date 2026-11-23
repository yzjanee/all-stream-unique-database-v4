# Column Information: all_streams_unique.fits

**File:** `~/Documents/GitHub/all-stream-unique-database-v2/all_streams_unique.fits`
**Format:** FITS (BINTABLE, extension 1)
**Reader:** astropy
**Rows:** 80162
**Columns:** 40

| Column | Description | Units | Type |
|--------|-------------|-------|------|
| `source_id` | Gaia DR3 source identifier | — | int64 |
| `dist` | Heliocentric distance | kpc | float64 |
| `dist_err` | Uncertainty on dist | kpc | float64 |
| `Vr` | Heliocentric radial velocity | km s-1 | float64 |
| `Vr_err` | Uncertainty on Vr | km s-1 | float64 |
| `FeH` | Iron abundance [Fe/H] | dex* | float64 |
| `FeH_err` | Uncertainty on FeH | dex* | float64 |
| `aFe` | Alpha-element abundance [α/Fe] | dex* | float64 |
| `aFe_err` | Uncertainty on aFe | dex* | float64 |
| `p_mem` | Stream membership probability | — (0–1)* | float64 |
| `ra` | Right ascension (ICRS, Gaia DR3 epoch J2016.0) | deg | float64 |
| `ra_error` | Uncertainty on ra | mas | float32 |
| `dec` | Declination (ICRS, Gaia DR3 epoch J2016.0) | deg | float64 |
| `dec_error` | Uncertainty on dec | mas | float32 |
| `parallax` | Gaia DR3 parallax | mas | float64 |
| `parallax_error` | Uncertainty on parallax | mas | float32 |
| `parallax_over_error` | Parallax divided by its uncertainty | — (dimensionless)* | float32 |
| `pm` | Total proper motion | mas yr-1 | float32 |
| `pmra` | Proper motion in right ascension (pmra·cos dec) | mas yr-1 | float64 |
| `pmra_error` | Uncertainty on pmra | mas yr-1 | float32 |
| `pmdec` | Proper motion in declination | mas yr-1 | float64 |
| `pmdec_error` | Uncertainty on pmdec | mas yr-1 | float32 |
| `ra_dec_corr` | Gaia DR3 correlation coefficient between ra and dec | — (dimensionless)* | float32 |
| `ra_parallax_corr` | Gaia DR3 correlation coefficient between ra and parallax | — (dimensionless)* | float32 |
| `ra_pmra_corr` | Gaia DR3 correlation coefficient between ra and pmra | — (dimensionless)* | float32 |
| `ra_pmdec_corr` | Gaia DR3 correlation coefficient between ra and pmdec | — (dimensionless)* | float32 |
| `dec_parallax_corr` | Gaia DR3 correlation coefficient between dec and parallax | — (dimensionless)* | float32 |
| `dec_pmra_corr` | Gaia DR3 correlation coefficient between dec and pmra | — (dimensionless)* | float32 |
| `dec_pmdec_corr` | Gaia DR3 correlation coefficient between dec and pmdec | — (dimensionless)* | float32 |
| `parallax_pmra_corr` | Gaia DR3 correlation coefficient between parallax and pmra | — (dimensionless)* | float32 |
| `parallax_pmdec_corr` | Gaia DR3 correlation coefficient between parallax and pmdec | — (dimensionless)* | float32 |
| `pmra_pmdec_corr` | Gaia DR3 correlation coefficient between pmra and pmdec | — (dimensionless)* | float32 |
| `phot_g_mean_mag` | Gaia G-band mean magnitude | mag | float32 |
| `bp_rp` | Gaia BP−RP colour | mag | float32 |
| `name` | Stellar stream name | — | str (15-char) |
| `reference` | Paper(s) that identified the star as a stream member; some rows list two, comma-separated | — | str (33-char) |
| `d_orb` | Galactocentric orbital distance | kpc | float64 |
| `X` | Galactocentric X coordinate | kpc | float64 |
| `Y` | Galactocentric Y coordinate | kpc | float64 |
| `Z` | Galactocentric Z coordinate | kpc | float64 |

## Notes

- The FITS file has no column descriptions (no `TCOMMn` keywords, no embedded VOTable metadata). All 40 descriptions are inferred from column names, standard Gaia DR3 naming, and v3's `directions.md`. Check the non-Gaia ones: `dist`, `d_orb`, `X`, `Y`, `Z`, `p_mem`, `reference`.
- Units marked * are inferred. The file gives `FeH`/`FeH_err` the unit `[-]` (not a valid FITS unit); read here as dex. `aFe`, `aFe_err`, `p_mem`, `parallax_over_error` and all `*_corr` columns have no unit in the file.
- 27 stars appear twice (members of two streams): 80,162 rows, 80,135 unique `source_id`s. 92 unique stream names; 46 unique `reference` strings.
- Many empty values (NaN): `Vr`/`Vr_err` 73,214; `FeH`/`FeH_err` 78,195; `aFe`/`aFe_err` 80,113; `p_mem` 79,913; `dist` 24,765; `dist_err` 24,927. 5 stars have NaN parallax, proper motions, and their correlations.
- Possible fill value: `Vr_err = 0` in 1,174 rows that have a valid `Vr` — likely "no uncertainty reported", not a real zero error.
- No `999`/`-999`-style fill values found. The most common `dist` value (26.76 kpc, 414 rows) matches the most common `d_orb` value, so it looks like a stream-wide distance, not a fill value.
- Gaia DR3 positions and proper motions are at epoch J2016.0.
