all_streams_unique_v4
---------------------------

[![build](https://github.com/yzjanee/all-stream-unique-database-v4/actions/workflows/run_tests.yml/badge.svg)](https://github.com/yzjanee/all-stream-unique-database-v4/actions/workflows/run_tests.yml)  ![GitHub License](https://img.shields.io/github/license/yzjanee/all-stream-unique-database-v4)

A database of unique Gaia DR3 stellar stream members (80,162 stars across 92 streams from Ibata et al. 2024 and associated works), built with the AstroDB Toolkit.

## Schema

See the [entity relationship diagram](docs/figures/schema_erd.md) — GitHub renders it inline.

Acknowledgements
----------------

- The `PhotometryFilters` data is sourced from the SVO Filter Profile Service "Carlos Rodrigo", funded by MCIN/AEI/10.13039/501100011033/ through grant PID2023-146210NB-I00.

  - Rodrigo, C., Cruz, P., Aguilar, J.F., et al. 2024, [2024A&A...689A..93R](https://ui.adsabs.harvard.edu/abs/2024A%26A...689A..93R/abstract)
  - Rodrigo, C., Solano, E., 2020, *The SVO Filter Profile Service*, [2020sea..confE.182R](https://ui.adsabs.harvard.edu/abs/2020sea..confE.182R/abstract)
  - Rodrigo, C., Solano, E., Bayo, A., 2012, *The SVO Filter Profile Service*, [2012ivoa.rept.1015R](https://ui.adsabs.harvard.edu/abs/2012ivoa.rept.1015R/abstract)

- The telescope and instrument data are based on the Weizmann Interactive Supernova Data Repository (WISeREP), <https://www.wiserep.org>.
Yaron, O. & Gal-Yam, A. 2012, PASP, 124, 668 ([2012PASP..124..668Y](https://ui.adsabs.harvard.edu/abs/2012PASP..124..668Y)).

---
<!-- Do not delete this line. It is used to identify repositories based on this template. -->
This repository is based on the [astrodb-template](https://github.com/astrodbtoolkit/astrodb-template-db) template repository, which is part of the [AstroDB Toolkit](https://github.com/astrodbtoolkit).

## Website

A browsable web interface for this database lives in its own repo: [all-stream-unique-database-v4-website](https://github.com/yzjanee/all-stream-unique-database-v4-website) (built from the [astrodb-web](https://github.com/astrodbtoolkit/astrodb-web) template). It runs locally; it is not hosted online yet.

To run it, clone it into this repo's `website/` folder (git-ignored here), point it at the database, and start the server:

```bash
git clone https://github.com/yzjanee/all-stream-unique-database-v4-website website
cd website
cat > .env <<ENV
ASTRO_WEB_DATABASE_URL="sqlite:///$(cd .. && pwd)/all_streams_unique_v4.sqlite"
ASTRO_WEB_LOOKUP_TABLES="Publications,Telescopes,Instruments,PhotometryFilters,RegimeList,AssociationList,ParameterList"
ASTRO_WEB_PRIMARY_TABLE="Sources"
ASTRO_WEB_SOURCE_COLUMN="source"
ASTRO_WEB_FOREIGN_KEY="source"
ASTRO_WEB_RA_COLUMN="ra_deg"
ASTRO_WEB_DEC_COLUMN="dec_deg"
ENV
uv sync
uv run serve
```

Then open <http://localhost:8000>. The `.sqlite` file must exist first. Build it from the JSON data by running the tests once (`uv run pytest tests/`). Restart the server after the database changes.
