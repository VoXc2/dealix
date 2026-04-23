"""
Dealix Admin Dashboard — Streamlit app.
لوحة تحكم Dealix.

Run:  streamlit run dashboard/app.py --server.port 8501
"""

from __future__ import annotations

import os

import streamlit as st

st.set_page_config(
    page_title="Dealix Admin",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# RTL support
st.markdown(
    """
    <style>
      body { direction: rtl; text-align: right; }
      .stButton>button { float: right; }
      [data-testid="stSidebar"] { direction: rtl; }
      .stMarkdown, .stText { text-align: right; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title("🎯 Dealix Admin")
st.sidebar.markdown("**v3.0.0**")
st.sidebar.markdown(f"API: `{os.getenv('DEALIX_API_URL', 'http://127.0.0.1:8001')}`")

st.title("لوحة تحكم Dealix")
st.markdown(
    """
    مرحباً بك في لوحة تحكم Dealix.  اختر من القائمة الجانبية:

    - **Overview** — KPIs، حالة النظام، إنذارات
    - **Leads** — عرض وتحديث العملاء المحتملين
    - **Approvals** — موافقات Policy Engine
    - **Evidence** — سجل القرارات والدليل
    - **Costs** — تحليل إنفاق LLM
    - **Audit** — سجل التكاملات والأحداث
    """
)

col1, col2, col3 = st.columns(3)
col1.metric("عملاء هذا الشهر", "—", help="يتحدّث من /api/v1/admin/stats")
col2.metric("إنفاق LLM اليوم", "— $", help="/api/v1/admin/costs")
col3.metric("معدل الضخ Cache", "— %", help="/api/v1/admin/cache/stats")

st.info("استخدم القائمة على اليسار للتنقل بين الصفحات.")
