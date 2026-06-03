# Dealix — Testing Context (On-Demand Skill)

## Framework
pytest + pytest-asyncio · httpx AsyncClient · factory-boy

## Structure
```
tests/
├── conftest.py         # fixtures: db, client, auth_headers
├── test_clients.py
├── test_deals.py
├── test_auth.py
└── integration/        # slow tests, marked @pytest.mark.integration
```

## Running Tests
```bash
pytest tests/ -x -q                    # fast, stop on first fail
pytest tests/ -x -q -k "test_client"  # filter by name
pytest tests/ --co -q                 # list all tests without running
pytest tests/integration/ -m integration  # integration only
```

## Test Pattern
```python
@pytest.mark.asyncio
async def test_create_client(client: AsyncClient, auth_headers: dict):
    response = await client.post("/api/v1/clients/", json={
        "name": "Test Co",
        "name_ar": "شركة الاختبار",
        "sector": "tech"
    }, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["data"]["name"] == "Test Co"
```

## Fixtures (conftest.py)
- `db` — async test database session
- `client` — httpx AsyncClient
- `auth_headers` — `{"Authorization": "Bearer <test_token>"}`
- `test_client` — seeded Client object
