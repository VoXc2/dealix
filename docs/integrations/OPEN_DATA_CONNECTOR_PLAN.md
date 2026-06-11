# Open Data Connector Plan

## Purpose
Use Saudi public datasets (data.gov.sa) for sector hypotheses, not for individual profiles.

## Sources
- `data.gov.sa` datasets (sector mix, commercial registrations, economic indicators)
- Public CSV/JSON from ministries

## Safety
- Aggregate only
- No re-identification
- Cite source URL in every record

## Implementation (V1 plan)
- `connectors/open_data_connector.py`
- Inputs: dataset URL + filter
- Outputs: segment-level hypothesis record
- Marks `sourceType: "open_data"`
