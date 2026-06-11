# Lead Source Operating Rules (Dealix)

1. Every lead has a `sourceType` and a `sourceNote`
2. Every lead carries `reviewStatus`
3. Every connector writes a `reports/sources/source-audit-YYYY-MM-DD.md` file
4. No auto-send from any connector
5. Approved connectors are listed in `business/_data/sources.registry.json`
6. New connectors must be added to the registry before use
7. Demo data is marked `demo=true` in every record
