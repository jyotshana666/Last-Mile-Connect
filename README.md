# 🎯 Last Mile Connect: 

## Project Overview
A data-driven solution to identify and bridge the Aadhaar coverage gap for the last 10-15% of unreached citizens in India. This project analyzes enrolment and update patterns to pinpoint priority districts for targeted interventions.

## Problem Statement
Despite India's massive Aadhaar enrolment success, approximately 15 crore eligible citizens remain uncovered, primarily in remote, tribal, and marginalized communities. Identifying these "last mile" populations efficiently is crucial for achieving universal coverage.

## Solution Approach
We develop an AI-powered targeting system that:
1. **Identifies** low-coverage hotspots using clustering algorithms
2. **Prioritizes** intervention areas based on multiple parameters
3. **Optimizes** resource allocation for mobile enrolment camps
4. **Predicts** future enrolment patterns and requirements

## Key Features
- 🔍 **Gap Analysis**: Identify districts with <85% Aadhaar coverage
- 🗺️ **Heat Mapping**: Visual priority maps of intervention areas
- 📊 **Predictive Models**: Forecast enrolment needs and resource requirements
- 🚀 **Interactive Dashboard**: Real-time monitoring and decision support
- 💡 **Actionable Insights**: Specific recommendations for UIDAI officials

## Tech Stack
- **Data Processing**: Python, Pandas, NumPy
- **Analysis**: Scikit-learn, Statsmodels
- **Visualization**: Plotly, Matplotlib, Folium
- **Web Framework**: Streamlit
- **Deployment**: Streamlit Cloud, GitHub

## Project Structure
```
Last-mile-connect/
├── data/ # Raw and processed datasets
├── notebooks/ # Jupyter notebooks for analysis
├── src/ # Python source modules
├── app/ # Streamlit web application
├── reports/ # Documentation and presentations
└── tests/ # Unit tests
```

### Data Sources
- UIDAI Aadhaar Enrolment Data (2025)
- UIDAI Aadhaar Biometric Update Data (2025)
- UIDAI Aadhaar Demographic Update Data (2025)

## Phase 1: Data Exploration
- Ingested and cleaned UIDAI enrolment, biometric, and demographic datasets
- Standardized geography and time dimensions; removed duplicates
- Generated district-month and pincode-level aggregates
- Engineered core enrolment and update metrics
- Produced validated processed datasets and baseline visualizations

## Phase 2: Coverage Gap Analysis & Prioritization
- Integrated enrolment data with district-level population estimates
- Computed coverage rates, coverage gaps, and unreached population
- Classified districts into intervention priority levels
- Generated ranked priority districts and state-level gap insights

## Phase 3: Clustering & Hotspot Identification
- Performed pincode- and district-level clustering using geospatial and gap metrics
- Identified last-mile hotspots and optimal mobile camp locations
- Generated camp priority rankings, coverage estimates, and cost projections

## Phase 4: Visualization & Executive Insights
- Created executive dashboards summarizing coverage gaps and priorities
- Visualized state, district, age-group, and camp deployment patterns
- Produced budget and resource allocation insights for decision-makers
