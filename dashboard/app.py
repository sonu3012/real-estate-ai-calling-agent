import streamlit as st
import sqlite3
import pandas as pd
import os


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Real Estate AI CRM",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# DATABASE
# =========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_NAME = os.path.join(BASE_DIR, "real_estate_leads.db")


def get_all_leads():

    connection = sqlite3.connect(DATABASE_NAME)

    query = """
        SELECT
            id,
            name,
            phone,
            requirement,
            location,
            property_type,
            configuration,
            budget,
            purpose,
            timeline
        FROM leads
        ORDER BY id DESC
    """

    df = pd.read_sql_query(query, connection)

    connection.close()

    return df


# =========================================================
# CUSTOM CSS — "Browser App" theme with gradient type
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main {
    background: radial-gradient(circle at 10% 0%, #eef2ff 0%, #f5f7fb 35%, #f5f7fb 100%);
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* ---------- Fake browser chrome bar ---------- */

.browser-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #e5e7eb;
    border-radius: 14px 14px 0 0;
    padding: 10px 16px;
    margin-bottom: -2px;
}

.browser-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
}

.dot-red { background: #ff5f57; }
.dot-yellow { background: #febc2e; }
.dot-green { background: #28c840; }

.browser-url {
    margin-left: 14px;
    background: white;
    border-radius: 8px;
    padding: 4px 14px;
    font-size: 12px;
    color: #6b7280;
    flex: 1;
    max-width: 420px;
    border: 1px solid #d1d5db;
}

/* ---------- Header ---------- */

.dashboard-header {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 45%, #4338ca 100%);
    padding: 38px 34px;
    border-radius: 0 0 20px 20px;
    margin-bottom: 30px;
    box-shadow: 0 12px 30px rgba(30, 41, 59, 0.25);
}

.dashboard-header::before {
    content: "";
    position: absolute;
    top: -60px;
    right: -60px;
    width: 220px;
    height: 220px;
    background: radial-gradient(circle, rgba(129,140,248,0.35) 0%, transparent 70%);
}

.dashboard-title {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(90deg, #ffffff 0%, #c7d2fe 50%, #93c5fd 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -0.5px;
    position: relative;
    z-index: 1;
}

.dashboard-subtitle {
    color: #dbeafe;
    font-size: 16px;
    margin-top: 8px;
    position: relative;
    z-index: 1;
}

/* ---------- Section headings with gradient ---------- */

.gradient-heading {
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
    font-size: 24px;
    background: linear-gradient(90deg, #4338ca, #7c3aed, #db2777);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 6px 0 14px 0;
}

/* ---------- Metric cards ---------- */

.metric-box {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(6px);
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 6px 18px rgba(30,41,59,0.07);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.metric-box:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(67,56,202,0.15);
}

.metric-label {
    color: #6b7280;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.4px;
}

.metric-number {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(90deg, #1e3a8a, #4338ca, #7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 34px;
    font-weight: 800;
    margin-top: 6px;
}

.metric-small {
    color: #9ca3af;
    font-size: 12px;
    margin-top: 4px;
}

/* ---------- Lead cards ---------- */

.lead-name {
    font-family: 'Poppins', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #111827;
}

.lead-phone {
    color: #4b5563;
    margin-top: 5px;
}

.lead-tag {
    display: inline-block;
    background: linear-gradient(90deg, #6366f1, #a855f7);
    color: white;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}

/* Streamlit's bordered container used for lead cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 16px !important;
    box-shadow: 0 4px 14px rgba(30,41,59,0.06);
    transition: box-shadow 0.15s ease;
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: 0 8px 22px rgba(67,56,202,0.14);
}

/* ---------- Tabs ---------- */

.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
}

.stTabs [data-baseweb="tab"] {
    background: white;
    border-radius: 10px 10px 0 0;
    padding: 10px 18px;
    font-weight: 600;
    color: #4b5563;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #4338ca, #7c3aed) !important;
    color: white !important;
}

/* ---------- Buttons ---------- */

.stButton > button {
    background: linear-gradient(90deg, #4338ca, #7c3aed);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 0.5rem 1rem;
    transition: opacity 0.15s ease, transform 0.1s ease;
}

.stButton > button:hover {
    opacity: 0.9;
    transform: translateY(-1px);
    color: white;
}

/* ---------- Sidebar ---------- */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 100%);
}

section[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}

section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
    background-color: #1f2937 !important;
    color: #f9fafb !important;
    border-radius: 8px !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

try:

    leads = get_all_leads()

except Exception as error:

    st.error(f"Database error: {error}")
    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🏠 Real Estate AI")

    st.caption("Lead Management CRM")

    st.divider()

    st.markdown("### 🔎 Search Leads")

    search_text = st.text_input(
        "Search",
        placeholder="Name, phone or location"
    )

    if not leads.empty:

        locations = ["All"] + sorted(
            leads["location"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_location = st.selectbox(
            "📍 Location",
            locations
        )

        property_types = ["All"] + sorted(
            leads["property_type"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_property = st.selectbox(
            "🏢 Property Type",
            property_types
        )

        purposes = ["All"] + sorted(
            leads["purpose"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_purpose = st.selectbox(
            "🎯 Purpose",
            purposes
        )

    else:

        selected_location = "All"
        selected_property = "All"
        selected_purpose = "All"

    st.divider()

    if st.button(
        "🔄 Refresh Dashboard",
        use_container_width=True
    ):
        st.rerun()


# =========================================================
# FAKE BROWSER CHROME + HEADER
# =========================================================

st.markdown("""
<div class="browser-bar">
    <div class="browser-dot dot-red"></div>
    <div class="browser-dot dot-yellow"></div>
    <div class="browser-dot dot-green"></div>
    <div class="browser-url">🔒 realestate-ai-crm.app/dashboard</div>
</div>

<div class="dashboard-header">
    <div class="dashboard-title">
        🏠 Real Estate AI Agent
    </div>
    <div class="dashboard-subtitle">
        AI-powered customer qualification & lead management dashboard
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# FILTER
# =========================================================

filtered = leads.copy()

if search_text:

    search = search_text.lower()

    filtered = filtered[
        filtered.apply(
            lambda row:
            search in str(row["name"]).lower()
            or search in str(row["phone"]).lower()
            or search in str(row["location"]).lower(),
            axis=1
        )
    ]


if selected_location != "All":

    filtered = filtered[
        filtered["location"].astype(str) == selected_location
    ]


if selected_property != "All":

    filtered = filtered[
        filtered["property_type"].astype(str) == selected_property
    ]


if selected_purpose != "All":

    filtered = filtered[
        filtered["purpose"].astype(str) == selected_purpose
    ]


# =========================================================
# METRICS
# =========================================================

total_leads = len(leads)

locations_count = (
    leads["location"]
    .replace("", pd.NA)
    .dropna()
    .nunique()
)

property_count = (
    leads["property_type"]
    .replace("", pd.NA)
    .dropna()
    .nunique()
)

filtered_count = len(filtered)


st.markdown('<div class="gradient-heading">📊 Dashboard Overview</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)


with c1:

    st.markdown("""
    <div class="metric-box">
        <div class="metric-label">👥 TOTAL LEADS</div>
        <div class="metric-number">%s</div>
        <div class="metric-small">Customers captured</div>
    </div>
    """ % total_leads, unsafe_allow_html=True)


with c2:

    st.markdown("""
    <div class="metric-box">
        <div class="metric-label">🔎 FILTERED LEADS</div>
        <div class="metric-number">%s</div>
        <div class="metric-small">Current results</div>
    </div>
    """ % filtered_count, unsafe_allow_html=True)


with c3:

    st.markdown("""
    <div class="metric-box">
        <div class="metric-label">📍 LOCATIONS</div>
        <div class="metric-number">%s</div>
        <div class="metric-small">Customer locations</div>
    </div>
    """ % locations_count, unsafe_allow_html=True)


with c4:

    st.markdown("""
    <div class="metric-box">
        <div class="metric-label">🏢 PROPERTY TYPES</div>
        <div class="metric-number">%s</div>
        <div class="metric-small">Property categories</div>
    </div>
    """ % property_count, unsafe_allow_html=True)


st.divider()


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3 = st.tabs(
    [
        "👥 Lead Management",
        "📈 Analytics",
        "🔍 Lead Details"
    ]
)


# =========================================================
# TAB 1 — LEADS
# =========================================================

with tab1:

    st.markdown('<div class="gradient-heading">👥 Customer Leads</div>', unsafe_allow_html=True)

    if filtered.empty:

        st.warning("No leads found.")

    else:

        for _, lead in filtered.iterrows():

            name = str(lead["name"]).strip()
            phone = str(lead["phone"]).strip()
            requirement = str(lead["requirement"]).strip()
            location = str(lead["location"]).strip()
            property_type = str(lead["property_type"]).strip()
            configuration = str(lead["configuration"]).strip()
            budget = str(lead["budget"]).strip()
            purpose = str(lead["purpose"]).strip()
            timeline = str(lead["timeline"]).strip()

            if not name:
                name = "Unknown Customer"

            with st.container(border=True):

                st.markdown(
                    f'<div class="lead-name">👤 {name}</div>',
                    unsafe_allow_html=True
                )

                st.caption(
                    f"📞 {phone if phone else 'Phone not provided'}"
                )

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.write("📍 **Location**")
                    st.write(location or "Not provided")

                with col2:
                    st.write("🏢 **Property**")
                    st.write(property_type or "Not provided")

                with col3:
                    st.write("🏠 **Configuration**")
                    st.write(configuration or "Not provided")

                with col4:
                    st.write("💰 **Budget**")
                    st.write(budget or "Not provided")

                st.divider()

                col5, col6, col7 = st.columns(3)

                with col5:
                    st.write("🎯 **Purpose**")
                    st.write(purpose or "Not provided")

                with col6:
                    st.write("⏱️ **Timeline**")
                    st.write(timeline or "Not provided")

                with col7:
                    st.write("💬 **Requirement**")
                    st.write(requirement or "Not provided")


# =========================================================
# TAB 2 — ANALYTICS
# =========================================================

with tab2:

    st.markdown('<div class="gradient-heading">📈 Lead Analytics</div>', unsafe_allow_html=True)

    if leads.empty:

        st.info("No data available.")

    else:

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("#### 📍 Leads by Location")

            location_data = (
                leads["location"]
                .replace("", "Not Provided")
                .value_counts()
            )

            st.bar_chart(location_data, color="#7c3aed")


        with col2:

            st.markdown("#### 🏢 Leads by Property Type")

            property_data = (
                leads["property_type"]
                .replace("", "Not Provided")
                .value_counts()
            )

            st.bar_chart(property_data, color="#4338ca")


        col3, col4 = st.columns(2)

        with col3:

            st.markdown("#### 🎯 Customer Purpose")

            purpose_data = (
                leads["purpose"]
                .replace("", "Not Provided")
                .value_counts()
            )

            st.bar_chart(purpose_data, color="#db2777")


        with col4:

            st.markdown("#### ⏱️ Purchase Timeline")

            timeline_data = (
                leads["timeline"]
                .replace("", "Not Provided")
                .value_counts()
            )

            st.bar_chart(timeline_data, color="#0ea5e9")


# =========================================================
# TAB 3 — DETAILS
# =========================================================

with tab3:

    st.markdown('<div class="gradient-heading">🔍 Complete Lead Details</div>', unsafe_allow_html=True)

    if leads.empty:

        st.info("No leads available.")

    else:

        selected_id = st.selectbox(
            "Select Lead",
            leads["id"].tolist()
        )

        selected = leads[
            leads["id"] == selected_id
        ].iloc[0]


        col1, col2 = st.columns(2)


        with col1:

            st.markdown("#### 👤 Customer Information")

            st.info(
                f"""
**Name:** {selected['name'] or 'Not provided'}

**Phone:** {selected['phone'] or 'Not provided'}

**Requirement:** {selected['requirement'] or 'Not provided'}

**Purpose:** {selected['purpose'] or 'Not provided'}

**Timeline:** {selected['timeline'] or 'Not provided'}
"""
            )


        with col2:

            st.markdown("#### 🏠 Property Requirement")

            st.info(
                f"""
**Location:** {selected['location'] or 'Not provided'}

**Property Type:** {selected['property_type'] or 'Not provided'}

**Configuration:** {selected['configuration'] or 'Not provided'}

**Budget:** {selected['budget'] or 'Not provided'}
"""
            )


        st.markdown("#### 📋 Complete Record")

        st.dataframe(
            selected.to_frame("Value"),
            use_container_width=True
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🏠 Real Estate AI Calling Agent • "
    "Vapi + Google Gemini + Flask + SQLite + Streamlit"
)

