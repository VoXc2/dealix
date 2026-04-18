# Lead Intelligence Engine V2 — Dealix

Gulf-focused B2B lead discovery engine. Searches across 8 sources in Arabic and English,
normalizes and deduplicates results, enriches with WHOIS + email discovery, and scores
each lead against your ICP using Groq LLM.

---

## Architecture

```
                           ┌─────────────────────────────────────────────┐
                           │             API Layer (api.py)               │
                           │  POST /discover  GET /jobs/{id}  WS /stream  │
                           └─────────────────┬───────────────────────────┘
                                             │
                           ┌─────────────────▼───────────────────────────┐
                           │         Planner (planner.py)                 │
                           │   Groq LLM → List[SearchPlan]               │
                           │   (fallback: rule-based plans)               │
                           └─────────────────┬───────────────────────────┘
                                             │ parallel asyncio.gather
                    ┌────────────────────────┼────────────────────────┐
                    │                        │                        │
         ┌──────────▼──────────┐  ┌──────────▼──────────┐  ┌────────▼────────────┐
         │   Search Sources    │  │    Map Sources      │  │   Other Sources    │
         │  google_custom      │  │  google_places      │  │  linkedin_public   │
         │  duckduckgo         │  │  osm_nominatim      │  │  sa_mc_gov         │
         │  brave_search       │  └─────────────────────┘  │  bayt_jobs         │
         └─────────────────────┘                            └────────────────────┘
                    │                        │                        │
                    └────────────────────────┼────────────────────────┘
                                             │ List[RawLead]
                           ┌─────────────────▼───────────────────────────┐
                           │          Normalizer (normalizer.py)          │
                           │  phone → E.164 | email validation | AR names │
                           └─────────────────┬───────────────────────────┘
                                             │ List[NormalizedLead]
                           ┌─────────────────▼───────────────────────────┐
                           │            Dedup (dedup.py)                  │
                           │  Exact (domain/phone) + Fuzzy (rapidfuzz)   │
                           └─────────────────┬───────────────────────────┘
                                             │ List[NormalizedLead] (deduped)
                           ┌─────────────────▼───────────────────────────┐
                           │          Enrichment (enrichment.py)          │
                           │  WHOIS | website check | email patterns      │
                           │  LinkedIn discovery                          │
                           └─────────────────┬───────────────────────────┘
                                             │ List[EnrichedLead]
                           ┌─────────────────▼───────────────────────────┐
                           │            Scoring (scoring.py)              │
                           │  Groq LLM: ICP fit (0-100) + 3 talking pts  │
                           │  (fallback: rule-based scoring)              │
                           └─────────────────┬───────────────────────────┘
                                             │ List[ScoredLead]
                           ┌─────────────────▼───────────────────────────┐
                           │         Response / Export / Stream           │
                           └─────────────────────────────────────────────┘
```

**Data flow summary:**
`DiscoveryQuery` → Planner → `List[SearchPlan]` → Orchestrator (parallel) → `List[RawLead]` → Normalizer → Dedup → Enrichment → Scoring → `List[ScoredLead]`

---

## How to Run Locally

### Prerequisites

```bash
cd backend
pip install phonenumbers rapidfuzz python-whois httpx pydantic
```

### Start the server

```bash
cd /home/user/workspace/dealix-clean/backend
uvicorn dashboard_api:app --port 8001 --reload
```

The V2 intelligence API is available at: `http://localhost:8001/api/v2/intelligence`

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | Recommended | Groq API key for LLM planning + scoring. Falls back to rule-based. |
| `GOOGLE_CSE_KEY` | Optional | Google Custom Search API key |
| `GOOGLE_CSE_CX` | Optional | Google CSE CX (search engine ID) |
| `GOOGLE_PLACES_KEY` | Optional | Google Places API key (best for local businesses) |
| `BRAVE_SEARCH_KEY` | Optional | Brave Search API key |

All sources work without API keys — they return `is_mock=true` data when keys are missing.

---

## API Examples (curl)

### 1. Start a discovery job

```bash
curl -X POST http://localhost:8001/api/v2/intelligence/discover \
  -H "Content-Type: application/json" \
  -d '{
    "icp": {
      "industries": ["restaurants"],
      "geo": {"countries": ["SA"], "cities": ["Riyadh"]},
      "signals": ["hiring"]
    },
    "depth": "quick",
    "limit": 10
  }'
```

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "message": "Discovery job started",
  "poll_url": "/api/v2/intelligence/jobs/550e8400-...",
  "leads_url": "/api/v2/intelligence/jobs/550e8400-.../leads",
  "stream_url": "/api/v2/intelligence/jobs/550e8400-.../stream"
}
```

### 2. Check job status

```bash
curl http://localhost:8001/api/v2/intelligence/jobs/{job_id}
```

**Response:**
```json
{
  "job_id": "550e8400-...",
  "status": "completed",
  "progress": 100.0,
  "leads_found": 15,
  "leads_scored": 10,
  "sources_completed": ["google_places", "duckduckgo", "bayt_jobs"],
  "sources_total": 4
}
```

### 3. Get leads (paginated)

```bash
curl "http://localhost:8001/api/v2/intelligence/jobs/{job_id}/leads?page=1&page_size=10&min_score=50"
```

### 4. Export leads

```bash
# CSV
curl -o leads.csv "http://localhost:8001/api/v2/intelligence/jobs/{job_id}/export?format=csv"

# JSON
curl -o leads.json "http://localhost:8001/api/v2/intelligence/jobs/{job_id}/export?format=json"
```

### 5. WebSocket streaming (wscat)

```bash
wscat -c "ws://localhost:8001/api/v2/intelligence/jobs/{job_id}/stream"
```

### 6. List available sources

```bash
curl http://localhost:8001/api/v2/intelligence/sources
```

---

## How to Add a New Source

1. **Create the adapter** in the appropriate subdirectory:
   - Search engines → `sources/search/`
   - Maps/geocoding → `sources/maps/`
   - Social media → `sources/social/`
   - Government registries → `sources/registries/`
   - Directories → `sources/directories/`

2. **Inherit from BaseSource:**

```python
from app.intelligence.v2.sources.base import BaseSource, rate_limited, with_retry
from app.intelligence.v2.models import DiscoveryQuery, RawLead, SearchPlan

class MyNewSource(BaseSource):
    SOURCE_NAME = "my_source"      # Unique identifier
    REQUIRES_KEY = True            # Does it need an API key?
    RATE_LIMIT_CPS = 1.0           # Calls per second

    @property
    def api_key(self):
        return os.getenv("MY_SOURCE_API_KEY")

    @with_retry(max_attempts=3)
    @rate_limited(calls_per_second=1.0)
    async def _fetch(self, query: str) -> dict:
        # ... call the API ...

    async def discover(self, query: DiscoveryQuery, plan: SearchPlan) -> List[RawLead]:
        if not self.api_key:
            return self._mock_leads(query, plan, count=3)
        
        data = await self._fetch(plan.query_string)
        leads = []
        for item in data.get("results", []):
            provenance = self._make_provenance(plan, url=item["url"])
            lead = RawLead(
                provenance=provenance,
                company_name=item["name"],
                # ... other fields ...
            )
            leads.append(lead)
        return leads
```

3. **Register in `orchestrator.py`:**

```python
from app.intelligence.v2.sources.my_dir.my_source import MyNewSource

SOURCE_REGISTRY["my_source"] = MyNewSource
```

4. **Add to `planner.py` source list:**

```python
ALL_SOURCES = [..., "my_source"]
```

---

## Running Tests

```bash
cd /home/user/workspace/dealix-clean/backend
pytest tests/test_intelligence_v2.py -v
```

Expected: 15+ tests passing.

---

## Data Models

| Model | Description |
|---|---|
| `DiscoveryQuery` | Top-level input: ICP + depth + limit |
| `ICP` | Ideal Customer Profile: industries, geo, signals |
| `SearchPlan` | LLM-generated plan: (source, query, filters) |
| `RawLead` | Unvalidated data from a source |
| `ProvenanceRecord` | Source attribution: name, query, timestamp, URL, is_mock |
| `NormalizedLead` | Validated: E.164 phone, MX-checked email, normalized names |
| `EnrichedLead` | + WHOIS, website, email patterns, LinkedIn |
| `ScoredLead` | + ICP score (0-100), tier, talking points (AR) |
| `DiscoveryJob` | Job tracking: status, progress, leads |

---

## Mock Data

When no API keys are configured, sources return `is_mock: true` leads.
These are clearly flagged in every response. To get real data, set the relevant env vars in `.env`.
