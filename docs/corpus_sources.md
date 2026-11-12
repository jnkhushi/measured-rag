# Corpus Sources and Licensing (M1 Starter)

Every ingested source must document: **original source URL, title, publication/version date, and licence/usage terms**.

This project’s M1 starter corpus includes locally stored Markdown excerpts/summaries created for baseline pipeline development. They are **not substitutes** for the full official documents. Verify current terms at each source URL before reuse or redistribution.

## Sources

| ID | Title | Source URL | Publication/Version Date | Version | Licence / Usage Terms | Local File |
|---|---|---|---|---|---|---|
| nist-csf-2.0-overview | The NIST Cybersecurity Framework (CSF) 2.0 | https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf | 2024-02-26 | 2.0 | U.S. Government work; NIST publications are generally available for public use. Verify current terms at the source URL. | `data/raw/nist_csf_2_overview.md` |
| cisa-incident-response-playbook | Cybersecurity Incident & Vulnerability Response Playbooks | https://www.cisa.gov/sites/default/files/publications/Federal_Government_Cybersecurity_Incident_and_Vulnerability_Response_Playbooks_508C.pdf | 2021-11 | 1.0 | U.S. Government public information published by CISA; generally available for public use. Verify current terms at the source URL. | `data/raw/cisa_incident_response.md` |

Machine-readable manifest: `data/raw/source_manifest.yaml`.

## Attribution and redistribution note

**Verified facts (recorded in project artifacts):**
- The two local starter files (`data/raw/nist_csf_2_overview.md`, `data/raw/cisa_incident_response.md`) are **project-authored starter excerpts/summaries** created for baseline pipeline development, as documented in `data/raw/source_manifest.yaml` notes and this document. They are **not** copies of, or substitutes for, the full official documents.
- Provenance metadata (source URL, title, publication/version date, recorded licence/usage terms, local path) is maintained in `data/raw/source_manifest.yaml` and summarized above.
- **NIST:** the recorded terms state “U.S. Government work; NIST publications are generally available for public use. Verify current terms at the source URL.” (as recorded in manifest/docs).
- **CISA:** the recorded terms state “U.S. Government public information published by CISA; generally available for public use. Verify current terms at the source URL.” (as recorded in manifest/docs).

**Unresolved / not legally cleared in this project:**
- **Redistribution of the CISA-derived local summary/excerpt (`data/raw/cisa_incident_response.md`) in a public repository has not been legally cleared or independently verified** by this project. Treat public redistribution as requiring confirmation of current official terms/conditions and any required attribution or notices.
- **Redistribution of the NIST-derived local summary/excerpt (`data/raw/nist_csf_2_overview.md`) has not been independently verified** here beyond the recorded provenance/terms; confirm current NIST/USG terms for derivative summaries before public redistribution if in doubt.

**Guidance:** Do not assume that the project’s software license (MIT, for original project code) covers NIST materials, CISA materials, third-party datasets, external model weights, or third-party dependencies. Retain source attribution and provenance fields, verify current terms at the official source URLs, and do not present these starter files as official publications. If redistribution terms cannot be confirmed, consider replacing distributed corpus files with user-supplied/local copies and documented fetch instructions (subject to separate approval).
