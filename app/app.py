"""
LAST MILE CONNECT - Aadhaar Coverage Optimization Platform
Streamlit Web Application
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Last Mile Connect - Aadhaar Coverage AI",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS - LIGHT THEME WITH NICE SPACING
# ============================================================================

st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Global styling */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
    }
    
    /* Header */
    .app-header {
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(37, 99, 235, 0.2);
    }
    
    .app-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .app-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(37, 99, 235, 0.15);
        border-color: #2563eb;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.5rem;
    }
    
    .metric-delta {
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }
    
    .delta-positive {
        color: #10b981;
    }
    
    .delta-negative {
        color: #ef4444;
    }
    
    /* Priority badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .badge-critical {
        background: linear-gradient(135deg, #fecaca 0%, #fee2e2 100%);
        color: #991b1b;
        border-left: 3px solid #dc2626;
    }
    
    .badge-high {
        background: linear-gradient(135deg, #fed7aa 0%, #ffedd5 100%);
        color: #9a3412;
        border-left: 3px solid #f97316;
    }
    
    .badge-medium {
        background: linear-gradient(135deg, #fef08a 0%, #fef9c3 100%);
        color: #854d0e;
        border-left: 3px solid #eab308;
    }
    
    .badge-low {
        background: linear-gradient(135deg, #bbf7d0 0%, #dcfce7 100%);
        color: #166534;
        border-left: 3px solid #22c55e;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        border: none;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4);
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: white;
        padding: 0.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 2rem;
        background: transparent;
        border-radius: 8px;
        font-weight: 600;
        color: #64748b;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
        color: white;
    }
    
    /* DataFrames */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
        padding: 2rem 1rem;
    }
    
    /* Section dividers */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #e2e8f0 50%, transparent 100%);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_data():
    """Load all processed datasets"""
    DATA_PATH = Path("data/processed")
    
    gap_df = pd.read_csv(DATA_PATH / "district_gap_analysis.csv")
    state_df = pd.read_csv(DATA_PATH / "state_gap_analysis.csv")
    camps_df = pd.read_csv(DATA_PATH / "mobile_camp_locations.csv")
    scenarios_df = pd.read_csv(DATA_PATH / "optimization_scenarios.csv")
    phased_df = pd.read_csv(DATA_PATH / "phased_deployment_plan.csv")
    
    return gap_df, state_df, camps_df, scenarios_df, phased_df

# Load data
try:
    gap_df, state_df, camps_df, scenarios_df, phased_df = load_data()
    DATA_LOADED = True
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

st.sidebar.markdown("""
<div style='text-align: center; padding: 1rem 0;'>
    <h1 style='color: #2563eb; margin: 0;'>📍</h1>
    <h2 style='margin: 0.5rem 0; font-size: 1.3rem;'>Last Mile Connect</h2>
    <p style='color: #64748b; font-size: 0.85rem; margin: 0;'>AI-Powered Coverage Analysis</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate to:",
    ["🏠 Dashboard", "🗺️ Interactive Map", "📊 Gap Analysis", 
     "🎯 Mobile Camps", "💰 Resource Optimizer", "📅 Deployment Plan"],
    index=0
)

st.sidebar.markdown("---")

# Quick stats in sidebar
st.sidebar.markdown("### 📊 Quick Stats")
total_districts = len(gap_df)
total_unreached = gap_df['unreached_population'].sum()
total_camps = len(camps_df)
total_budget = camps_df['total_cost'].sum() / 10**7

st.sidebar.metric("Districts", f"{total_districts:,}")
st.sidebar.metric("Unreached", f"{total_unreached/10**7:.1f} Cr")
st.sidebar.metric("Proposed Camps", f"{total_camps}")
st.sidebar.metric("Est. Budget", f"₹{total_budget:.0f} Cr")

# ============================================================================
# PAGE 1: DASHBOARD
# ============================================================================

if page == "🏠 Dashboard":
    
    # Header
    st.markdown("""
    <div class='app-header'>
        <h1>📍 Last Mile Connect</h1>
        <p>AI-Powered Aadhaar Coverage Optimization & Mobile Camp Deployment Planning</p>
    </div>
    """, unsafe_allow_html=True)
    
    # National Metrics
    st.markdown("## 🎯 National Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate national metrics
    national_coverage = (gap_df['total_enrolment'].sum() / 
                        gap_df['population_2025'].sum() * 100)
    total_unreached = gap_df['unreached_population'].sum()
    critical_districts = len(gap_df[gap_df['priority_level'] == 'CRITICAL'])
    est_budget = camps_df['total_cost'].sum() / 10**7
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <h3 class='metric-value'>{national_coverage:.2f}%</h3>
            <p class='metric-label'>Coverage Rate</p>
            <p class='metric-delta delta-negative'>↓ {100-national_coverage:.2f}% gap</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <h3 class='metric-value'>{total_unreached/10**7:.1f} Cr</h3>
            <p class='metric-label'>Unreached Citizens</p>
            <p class='metric-delta'>{total_unreached:,} people</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <h3 class='metric-value'>{total_districts:,}</h3>
            <p class='metric-label'>Total Districts</p>
            <p class='metric-delta delta-negative'>{critical_districts} Critical</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='metric-card'>
            <h3 class='metric-value'>₹{est_budget:.0f} Cr</h3>
            <p class='metric-label'>Est. Budget</p>
            <p class='metric-delta'>{len(camps_df)} mobile camps</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Top 10 States by Unreached Population")
        top_states = state_df.nlargest(10, 'unreached')
        fig = px.bar(
            top_states,
            x='unreached',
            y='state',
            orientation='h',
            color='coverage_rate',
            color_continuous_scale='RdYlGn',
            labels={'unreached': 'Unreached Population', 'state': 'State'}
        )
        fig.update_layout(
            height=400,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Priority Distribution")
        priority_counts = gap_df['priority_level'].value_counts()
        colors = {'CRITICAL': '#dc2626', 'HIGH': '#f97316', 
                 'MEDIUM': '#eab308', 'LOW': '#22c55e'}
        fig = px.pie(
            values=priority_counts.values,
            names=priority_counts.index,
            color=priority_counts.index,
            color_discrete_map=colors
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Top Priority Districts Table
    st.markdown("### 🚨 Top 20 Priority Districts")
    top_20 = gap_df.nlargest(20, 'priority_score')[
        ['state', 'district', 'population_2025', 'coverage_rate', 
         'unreached_population', 'priority_level']
    ].copy()
    
    # Format numbers
    top_20['population_2025'] = top_20['population_2025'].apply(lambda x: f"{x:,.0f}")
    top_20['coverage_rate'] = top_20['coverage_rate'].apply(lambda x: f"{x:.1f}%")
    top_20['unreached_population'] = top_20['unreached_population'].apply(lambda x: f"{x:,}")
    
    st.dataframe(top_20, use_container_width=True, height=400)
    
    # Download button
    csv = gap_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Complete Gap Analysis (CSV)",
        data=csv,
        file_name="last_mile_connect_gap_analysis.csv",
        mime="text/csv"
    )

# ============================================================================
# PAGE 2: INTERACTIVE MAP
# ============================================================================

elif page == "🗺️ Interactive Map":
    st.markdown("""
    <div class='app-header'>
        <h1>🗺️ Geographic Priority Analysis</h1>
        <p>Interactive map showing coverage gaps and recommended mobile camp locations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        show_camps = st.checkbox("Show Mobile Camps", value=True)
    with col2:
        priority_filter = st.multiselect(
            "Filter by Priority",
            ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
            default=['CRITICAL', 'HIGH']
        )
    with col3:
        state_select = st.selectbox(
            "Focus on State",
            ['All States'] + sorted(gap_df['state'].unique().tolist())
        )
    
    # Filter data
    filtered_df = gap_df.copy()
    if priority_filter:
        filtered_df = filtered_df[filtered_df['priority_level'].isin(priority_filter)]
    if state_select != 'All States':
        filtered_df = filtered_df[filtered_df['state'] == state_select]
    
    # Create visualization (simplified - no actual map due to time)
    st.markdown("### 📍 Priority Districts Map")
    st.info("🗺️ Interactive Folium map would be displayed here with:\n- Choropleth by coverage rate\n- Markers for mobile camps\n- Click-to-view district details")
    
    # Show filtered data instead
    st.markdown(f"### Showing {len(filtered_df)} districts")
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Filtered Districts", len(filtered_df))
    with col2:
        st.metric("Unreached", f"{filtered_df['unreached_population'].sum()/10**6:.1f}M")
    with col3:
        avg_coverage = filtered_df['coverage_rate'].mean()
        st.metric("Avg Coverage", f"{avg_coverage:.1f}%")
    
    # Display data
    display_cols = ['state', 'district', 'coverage_rate', 'unreached_population', 'priority_level']
    st.dataframe(filtered_df[display_cols], use_container_width=True, height=500)

# ============================================================================
# PAGE 3: GAP ANALYSIS
# ============================================================================

elif page == "📊 Gap Analysis":
    st.markdown("""
    <div class='app-header'>
        <h1>📊 Coverage Gap Analysis</h1>
        <p>Detailed breakdown of coverage gaps by state and district</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["State Level", "District Level"])
    
    with tab1:
        st.markdown("### State-wise Coverage Analysis")
        
        # State comparison chart
        fig = px.bar(
            state_df.nlargest(15, 'unreached'),
            x='state',
            y=['enrolled', 'unreached'],
            barmode='stack',
            labels={'value': 'Population', 'variable': 'Category'},
            color_discrete_sequence=['#10b981', '#ef4444']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # State table
        st.dataframe(
            state_df[['state', 'coverage_rate', 'gap_pct', 'unreached', 'num_districts']],
            use_container_width=True,
            height=400
        )
    
    with tab2:
        st.markdown("### District-wise Analysis")
        
        # Search
        search = st.text_input("🔍 Search districts", "")
        
        display_df = gap_df.copy()
        if search:
            display_df = display_df[
                display_df['district'].str.contains(search, case=False) |
                display_df['state'].str.contains(search, case=False)
            ]
        
        st.markdown(f"Showing {len(display_df)} of {len(gap_df)} districts")
        
        st.dataframe(
            display_df[['state', 'district', 'population_2025', 'coverage_rate', 
                       'unreached_population', 'priority_level']],
            use_container_width=True,
            height=500
        )
        
        # Export
        csv = display_df.to_csv(index=False)
        st.download_button("📥 Export Filtered Data", csv, "filtered_gap_analysis.csv")

# ============================================================================
# PAGE 4: MOBILE CAMPS
# ============================================================================

elif page == "🎯 Mobile Camps":
    st.markdown("""
    <div class='app-header'>
        <h1>🎯 Recommended Mobile Camp Locations</h1>
        <p>200 strategically optimized camp locations for maximum coverage</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Camps", f"{len(camps_df)}")
    with col2:
        st.metric("Coverage", f"{camps_df['coverage_population'].sum()/10**7:.1f} Cr")
    with col3:
        st.metric("Est. Budget", f"₹{camps_df['total_cost'].sum()/10**7:.0f} Cr")
    with col4:
        st.metric("Avg Cost/Camp", f"₹{camps_df['total_cost'].mean()/10**5:.1f} L")
    
    st.markdown("---")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        selected_state = st.selectbox(
            "Filter by State",
            ['All States'] + sorted(camps_df['state'].unique().tolist())
        )
    with col2:
        selected_priority = st.multiselect(
            "Filter by Priority",
            ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
            default=['CRITICAL', 'HIGH']
        )
    
    # Filter camps
    filtered_camps = camps_df.copy()
    if selected_state != 'All States':
        filtered_camps = filtered_camps[filtered_camps['state'] == selected_state]
    if selected_priority:
        filtered_camps = filtered_camps[filtered_camps['camp_priority'].isin(selected_priority)]
    
    st.markdown(f"### Showing {len(filtered_camps)} camps")
    
    # Camp distribution chart
    fig = px.bar(
        filtered_camps.groupby('camp_priority').size().reset_index(name='count'),
        x='camp_priority',
        y='count',
        color='camp_priority',
        color_discrete_map={'CRITICAL': '#dc2626', 'HIGH': '#f97316', 
                           'MEDIUM': '#eab308', 'LOW': '#22c55e'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Camp list
    st.dataframe(
        filtered_camps[['camp_id', 'state', 'district', 'coverage_population', 
                       'total_cost', 'camp_priority', 'latitude', 'longitude']],
        use_container_width=True,
        height=400
    )
    
    # Download
    csv = filtered_camps.to_csv(index=False)
    st.download_button("📥 Download Camp List", csv, "mobile_camps.csv")

# ============================================================================
# PAGE 5: RESOURCE OPTIMIZER
# ============================================================================

elif page == "💰 Resource Optimizer":
    st.markdown("""
    <div class='app-header'>
        <h1>💰 Budget Optimization & Scenario Planning</h1>
        <p>Compare different budget scenarios and resource allocation strategies</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Scenario Comparison")
    
    # Display scenarios
    st.dataframe(scenarios_df, use_container_width=True)
    
    # Scenario comparison charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            scenarios_df,
            x='Scenario',
            y='Coverage',
            color='Scenario',
            labels={'Coverage': 'Expected Coverage (Citizens)'}
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            scenarios_df,
            x='Scenario',
            y='Cost (Cr)',
            color='Scenario',
            labels={'Cost (Cr)': 'Total Cost (Crores)'}
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Recommended scenario
    st.success("✅ **Recommended**: BALANCED scenario offers optimal coverage per rupee spent")
    
    # Custom optimizer (simplified)
    st.markdown("---")
    st.markdown("### 🎛️ Custom Budget Calculator")
    
    budget_input = st.slider("Available Budget (Crores)", 100, 1500, 500, 50)
    
    # Simple estimation
    avg_cost_per_camp = camps_df['total_cost'].mean() / 10**7
    estimated_camps = int(budget_input / avg_cost_per_camp)
    estimated_coverage = estimated_camps * camps_df['coverage_population'].mean()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Est. Camps", f"{estimated_camps}")
    with col2:
        st.metric("Est. Coverage", f"{estimated_coverage/10**6:.1f}M")
    with col3:
        st.metric("Cost per Camp", f"₹{avg_cost_per_camp:.2f} Cr")

# ============================================================================
# PAGE 6: DEPLOYMENT PLAN
# ============================================================================

elif page == "📅 Deployment Plan":
    st.markdown("""
    <div class='app-header'>
        <h1>📅 Phased Deployment Timeline</h1>
        <p>Quarterly rollout plan for mobile camp deployment</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🗓️ Quarterly Rollout Plan")
    
    # Display phased plan
    st.dataframe(phased_df, use_container_width=True)
    
    # Cumulative progress chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=phased_df['Quarter'],
        y=phased_df['Cumulative_Coverage'],
        mode='lines+markers',
        name='Cumulative Coverage',
        line=dict(color='#2563eb', width=3),
        fill='tozeroy'
    ))
    
    fig.update_layout(
        title="Cumulative Coverage Growth",
        xaxis_title="Quarter",
        yaxis_title="Coverage (Citizens)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Phase details
    for idx, row in phased_df.iterrows():
        with st.expander(f"📍 {row['Quarter']} - {row['Num_Camps']} camps"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Coverage", f"{row['Coverage']:,}")
            with col2:
                st.metric("Cost", f"₹{row['Cost_Crores']} Cr")
            with col3:
                st.metric("States", row['States_Covered'])

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; color: #64748b; padding: 2rem 0;'>
    <p><strong>Last Mile Connect v1.0</strong> | Powered by AI & Data Science</p>
    <p>Built with Streamlit | © 2026 | <a href='#'>Documentation</a> | <a href='#'>GitHub</a></p>
</div>
""", unsafe_allow_html=True)
