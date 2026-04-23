"""Approvals page — Policy Engine pending actions."""
from __future__ import annotations

import os

import httpx
import streamlit as st

st.title("الموافقات")

API = os.getenv("DEALIX_API_URL", "http://127.0.0.1:8001")
H = {"X-API-Key": os.getenv("DEALIX_ADMIN_API_KEY", "")} if os.getenv("DEALIX_ADMIN_API_KEY") else {}

try:
    r = httpx.get(f"{API}/api/v1/cro/approvals", headers=H, timeout=8)
    data = r.json() if r.status_code == 200 else []
except Exception as e:
    data = []
    st.warning(f"تعذر الجلب: {e}")

if not data:
    st.info("لا توجد موافقات معلّقة.")
else:
    for item in data:
        with st.expander(f"#{item.get('id', '?')} — {item.get('action', '?')}"):
            st.json(item)
            c1, c2 = st.columns(2)
            if c1.button("قبول", key=f"y_{item.get('id')}"):
                httpx.post(f"{API}/api/v1/cro/approvals/{item['id']}/approve", headers=H)
                st.success("تم القبول")
            if c2.button("رفض", key=f"n_{item.get('id')}"):
                httpx.post(f"{API}/api/v1/cro/approvals/{item['id']}/reject", headers=H)
                st.warning("تم الرفض")
