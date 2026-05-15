#!/usr/bin/env python3
"""RAG retrieval-quality eval — deterministic, no API keys required.

Ingests evals/rag_corpus.jsonl, runs every query in evals/rag_cases.jsonl
through the real knowledge_v10 retrieval path, and asserts retrieval
thresholds. Exits non-zero on regression — usable as a CI quality gate.

Embeddings here are a deterministic bag-of-words hash (no network), so the
gate is reproducible without an OpenAI key.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import sys
import tempfile
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from auto_client_acquisition.knowledge_v10.ingestion import ingest_text  # noqa: E402
from auto_client_acquisition.knowledge_v10.rag_eval import (  # noqa: E402
    RagCase,
    evaluate_retrieval,
)
from auto_client_acquisition.knowledge_v10.store import JsonlKnowledgeStore  # noqa: E402

_DIM = 96
_MIN_HIT_RATE = 0.8
_MIN_MRR = 0.5
_STRIP = ".,;:!?()[]\"'—–"


def _embed_one(text: str) -> list[float]:
    """Deterministic bag-of-words hash embedding — reproducible, offline."""
    vec = [0.0] * _DIM
    for raw in text.lower().split():
        tok = raw.strip(_STRIP)
        if len(tok) < 2:
            continue
        digest = hashlib.md5(tok.encode("utf-8"), usedforsecurity=False).hexdigest()
        bucket = int(digest, 16) % _DIM
        vec[bucket] += 1.0
    return vec if any(vec) else [1.0] * _DIM


async def _embed_batch(texts: list[str]) -> list[list[float]]:
    return [_embed_one(t) for t in texts]


async def _embed_query(text: str) -> list[float]:
    return _embed_one(text)


def _load_jsonl(name: str) -> list[dict]:
    rows: list[dict] = []
    with (_REPO / "evals" / name).open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


async def main_async() -> int:
    corpus = _load_jsonl("rag_corpus.jsonl")
    cases_raw = _load_jsonl("rag_cases.jsonl")

    with tempfile.TemporaryDirectory() as tmp:
        store = JsonlKnowledgeStore(path=Path(tmp) / "k.jsonl")
        for doc in corpus:
            await ingest_text(
                document_id=doc["document_id"],
                text=doc["text"],
                customer_handle=doc.get("customer_handle", "eval"),
                store=store,
                embed_fn=_embed_batch,
            )
        cases = [
            RagCase(
                query=c["query"],
                relevant_document_ids=c["relevant_document_ids"],
                customer_handle=c.get("customer_handle", "eval"),
            )
            for c in cases_raw
        ]
        report = await evaluate_retrieval(
            cases, store=store, embed_fn=_embed_query, top_k=3
        )

    print("RAG_EVAL", json.dumps(report, ensure_ascii=False))
    if report["hit_rate"] < _MIN_HIT_RATE or report["mean_mrr"] < _MIN_MRR:
        print(f"RAG_EVAL_FAIL need hit_rate>={_MIN_HIT_RATE} mean_mrr>={_MIN_MRR}")
        return 1
    print("RAG_EVAL_OK")
    return 0


def main() -> int:
    return asyncio.run(main_async())


if __name__ == "__main__":
    raise SystemExit(main())
