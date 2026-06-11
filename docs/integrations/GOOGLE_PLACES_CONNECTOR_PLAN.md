# Google Places Connector Plan

## Purpose
Verify the public surface of a candidate account (address, hours, rating, reviews count).

## Required env
- `GOOGLE_PLACES_API_KEY`

## Endpoints
- `places.details` — read public business profile
- `places.find_place_from_text` — resolve a name to a place_id

## Safety
- No `places.delete` or any write call
- Cache for 7 days to respect rate limits
- Never store personal reviewer names
- Never bypass Google's ToS

## Implementation (V1 plan)
- `connectors/google_places_connector.py`
- Returns normalized lead record
- Marks `sourceType: "google_places"`
- Requires `sourceNote` (the place_id + URL)
