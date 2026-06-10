# Dealix — Database Context (On-Demand Skill)

## ORM & Access Pattern
- SQLAlchemy 2.0 async
- All models in `core/models/`
- Session factory: `core/database.py::get_db`
- Migrations: Alembic in `alembic/versions/`

## Key Tables
- `clients` — client accounts (id, name, ar_name, sector, tier)
- `deals` — pipeline deals (id, client_id, stage, value_sar, owner_id)
- `contacts` — contacts per client (id, client_id, name, role, whatsapp)
- `activities` — CRM activity log (id, deal_id, type, notes, created_at)
- `data_quality_scores` — DQ scoring per client

## Common Patterns
```python
# Correct async pattern
async def get_client(db: AsyncSession, client_id: int):
    result = await db.execute(select(Client).where(Client.id == client_id))
    return result.scalar_one_or_none()
```

## Migration Commands
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1
```
