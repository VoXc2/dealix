"""Evidence page — decision trail + reasoning."""
from __future__ import annotations

import os

import httpx
import pandas as pd
import streamlit as st

st.title("سجل القرارات والدليل")

API = os.getenv("DEALIX_API_URL", "http://127.0.0.1:8001")
H = {"X-API-Key": os.getenv("DEALIX_ADMIN_API_KEY", "")} if os.getenv("DEALIX_ADMIN_API_KEY") else {}

limit = st.slider("عدد الأحداث", 10, 200, 50)
try:
    r = httpx.get(f"{API}/api/v1/cro/evidence?limit={limit}", headers=H, timeout=8)
    entries = r.json() if r.status_code == 200 else []
except Exception:
    entries = []

if entries:
    df = pd.DataFrame(entries)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("لا يوجد سجل بعد.")
