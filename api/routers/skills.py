"""
Skills catalog router — public read; tenant-scoped install/run land in
later commits (T6d agent builder).

Endpoints:
    GET /api/v1/skills          — list every skill in skills/MANIFEST.yaml
    GET /api/v1/skills/{id}     — single skill metadata
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Path

from core.logging import get_logger
from dealix.agents.skills import by_id, load

router = APIRouter(prefix="/api/v1/skills", tags=["skills"])
log = get_logger(__name__)


@router.get("")
async def list_skills() -> dict[str, Any]:
    skills = load()
    return {
        "count": len(skills),
        "skills": [
            {
                "id": s.id,
                "path": s.path,
                "description": s.description,
                "inputs": s.inputs,
                "output_shape": s.output_shape,
            }
            for s in skills
        ],
    }


@router.get("/{skill_id}")
async def get_skill(skill_id: str = Path(..., max_length=64)) -> dict[str, Any]:
    s = by_id(skill_id)
    if s is None:
        raise HTTPException(404, "skill_not_found")
    return {
        "id": s.id,
        "path": s.path,
        "description": s.description,
        "inputs": s.inputs,
        "output_shape": s.output_shape,
        "permissions": s.permissions,
    }
