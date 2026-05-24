# Security Policy

This repository is designed to run as a public GitHub Pages application using only public source data.

## Secrets

Do not commit API keys, tokens, credentials, local `.env` files, private datasets, brokerage data, or logs containing personal information. Optional API keys must be stored in GitHub Actions Secrets.

Configured secret names:

- `FRED_API_KEY`
- `BEA_API_KEY`
- `EIA_API_KEY`
- `ALPHA_VANTAGE_API_KEY`
- `ACLED_API_KEY`
- `ACLED_EMAIL`
- `GEMINI_API_KEY`

## Public Data

Files under `public/data/` and `logs/latest.json` are public once the repository is public and once GitHub Pages is deployed. Collector error messages should not include secrets or private data.

## Reporting

Open a private security advisory if available, or contact the repository owner directly before filing a public issue for sensitive findings.
