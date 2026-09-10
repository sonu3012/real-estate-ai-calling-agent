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
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* Header */

.dashboard-header {
    background: linear-gradient(135deg, #172554, #1e3a8a);
    padding: 30px;
    border-radius: 18px;
    margin-bottom: 25px;
}

.dashboard-title {
    color: white;
    font-size: 38px;
    font-weight: 800;
}

.dashboard-subtitle {
    color: #dbeafe;
    font-size: 16px;
    margin-top: 8px;
}


/* Metric cards */

.metric-box {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 15px rgba(0,0,0,0.06);
}

.metric-label {
    color: #6b7280;
    font-size: 14px;
    font-weight: 600;
}

.metric-number {
    color: #111827;
    font-size: 32px;
    font-weight: 800;
    margin-top: 8px;
}

.metric-small {
    color: #9ca3af;
    font-size: 12px;
    margin-top: 5px;
}


/* Lead card */

.lead-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    margin-bottom: 15px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.05);
}

.lead-name {
    font-size: 20px;
    font-weight: 700;
    color: #111827;
}

.lead-phone {
    color: #4b5563;
    margin-top: 5px;
}

.lead-tag {
    background: #eef2ff;
    color: #3730a3;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}


/* Sidebar */

section[data-testid="stSidebar"] {
    background-color: #111827;
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
# HEADER
# =========================================================

st.markdown("""
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


st.subheader("📊 Dashboard Overview")

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

    st.subheader("👥 Customer Leads")

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
                    f"### 👤 {name}"
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

    st.subheader("📈 Lead Analytics")

    if leads.empty:

        st.info("No data available.")

    else:

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### 📍 Leads by Location")

            location_data = (
                leads["location"]
                .replace("", "Not Provided")
                .value_counts()
            )

            st.bar_chart(location_data)


        with col2:

            st.markdown("### 🏢 Leads by Property Type")

            property_data = (
                leads["property_type"]
                .replace("", "Not Provided")
                .value_counts()
            )

            st.bar_chart(property_data)


        col3, col4 = st.columns(2)

        with col3:

            st.markdown("### 🎯 Customer Purpose")

            purpose_data = (
                leads["purpose"]
                .replace("", "Not Provided")
                .value_counts()
            )

            st.bar_chart(purpose_data)


        with col4:

            st.markdown("### ⏱️ Purchase Timeline")

            timeline_data = (
                leads["timeline"]
                .replace("", "Not Provided")
                .value_counts()
            )

            st.bar_chart(timeline_data)


# =========================================================
# TAB 3 — DETAILS
# =========================================================

with tab3:

    st.subheader("🔍 Complete Lead Details")

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

            st.markdown("### 👤 Customer Information")

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

            st.markdown("### 🏠 Property Requirement")

            st.info(
                f"""
**Location:** {selected['location'] or 'Not provided'}

**Property Type:** {selected['property_type'] or 'Not provided'}

**Configuration:** {selected['configuration'] or 'Not provided'}

**Budget:** {selected['budget'] or 'Not provided'}
"""
            )


        st.markdown("### 📋 Complete Record")

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

