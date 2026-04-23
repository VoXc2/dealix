"""Audit page — connector audit log."""
from __future__ import annotations

import os

import httpx
import pandas as pd
import streamlit as st

st.title("سجل التكاملات")

API = os.getenv("DEALIX_API_URL", "http://127.0.0.1:8001")
H = {"X-API-Key": os.getenv("DEALIX_ADMIN_API_KEY", "")} if os.getenv("DEALIX_ADMIN_API_KEY") else {}

try:
    r = httpx.get(f"{API}/api/v1/admin/audit?limit=200", headers=H, timeout=8)
    data = r.json() if r.status_code == 200 else []
except Exception as e:
    data = []
    st.warning(f"تعذر الجلب: {e}")

if data:
    df = pd.DataFrame(data)
    cols_ok = [c for c in ["ts", "connector", "operation", "ok", "attempts", "duration_ms", "error"] if c in df.columns]
    st.dataframe(df[cols_ok] if cols_ok else df, use_container_width=True, hide_index=True)
else:
    st.info("لا يوجد سجل بعد.")
