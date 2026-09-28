# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os

# Set page configuration
st.set_page_config(
    page_title="Cross-Kingdom Biomarkers",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimal CSS to ensure readability and professional look in both Light/Dark mode
st.markdown("""
<style>
    /* Make metric cards pop slightly */
    div[data-testid="stMetricValue"] {
        color: #1E88E5;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to load data
@st.cache_data
def load_data(file_name):
    path = os.path.join("04_Results", "Ranked_Biomarkers", file_name)
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

# Helper function to load image
def load_image(image_name):
    path = os.path.join("04_Results", "Visualizations", image_name)
    if os.path.exists(path):
        return Image.open(path)
    return None

# Sidebar Navigation
st.sidebar.title("🧬 Navigation")
page = st.sidebar.radio("Go to", 
    ["Overview", "Rice (Flora) Biomarkers", "Cattle (Fauna) Biomarkers", "Universal Intersection"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("🌓 Appearance")

# Helper to read current theme
config_dir = ".streamlit"
config_path = os.path.join(config_dir, "config.toml")
current_theme = "light" # We just set it to light
if os.path.exists(config_path):
    with open(config_path, "r") as f:
        for line in f:
            if line.startswith("base"):
                current_theme = line.split("=")[1].strip().strip('"').strip("'")

# Theme Toggle
theme = st.sidebar.radio("Theme Mode", ["Light", "Dark"], index=0 if current_theme == "light" else 1, horizontal=True)

# Update config.toml and rerun if theme changed
if theme.lower() != current_theme:
    os.makedirs(config_dir, exist_ok=True)
    with open(config_path, "w") as f:
        f.write(f'[theme]\nbase="{theme.lower()}"\n')
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info(
    "**Project CAP599**\n\n"
    "Uncovering Cross-Kingdom Heat Stress Survival Biomarkers Using a Unified Machine Learning Multi-Omics Pipeline."
)
st.sidebar.markdown("**Author:** Nitin Kumar")

if page == "Overview":
    st.title("Cross-Kingdom Heat Stress Biomarkers")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        with st.container(border=True):
            st.subheader("🎯 The Objective")
            st.write(
                "The application of high-dimensional Machine Learning (Random Forest architecture) "
                "on transcriptomic (RNA-Seq) data to discover evolutionary conserved, universal thermal "
                "resilience mechanisms across both plant (*Oryza sativa*) and animal (*Bos taurus*) kingdoms."
            )
            
            st.divider()
            
            st.subheader("🔬 The Problem")
            st.write(
                "**The Biological 'Silo' Effect:** Agricultural plant biologists and veterinary livestock "
                "researchers have operated in strict isolation, leaving a massive research gap in universal biomarker discovery."
            )
            st.write(
                "**The Mathematical Bottleneck (p >> n Problem):** Biological RNA-Seq data contains massive noise "
                "with tens of thousands of features but very few samples, requiring an advanced Machine Learning feature selection framework."
            )
            
    with col2:
        st.subheader("📊 Datasets Used")
        st.info("**Flora Kingdom**\n\nRice (*Oryza sativa*)\n\n[GSE153030](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE153030)")
        st.success("**Fauna Kingdom**\n\nDairy Cattle (*Bos taurus*)\n\n[GSE289946](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE289946)")

    st.markdown("---")
    st.subheader("⚙️ Methodology Pipeline")
    
    m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
    with m_col1:
        st.markdown("#### 1. Noise Removal")
        st.caption("Variance Threshold (0.1)")
    with m_col2:
        st.markdown("#### 2. Normalization")
        st.caption("Z-Score / StandardScaler")
    with m_col3:
        st.markdown("#### 3. ML Engine")
        st.caption("Random Forest (500 trees)")
    with m_col4:
        st.markdown("#### 4. Extraction")
        st.caption("Gini Importance Ranking")
    with m_col5:
        st.markdown("#### 5. Intersection")
        st.caption("Ortholog Mapping Bridge")

elif page == "Rice (Flora) Biomarkers":
    st.title("🌾 Rice (Oryza sativa) Biomarkers")
    st.markdown("Analysis of the top survival genes for rice under heat stress.")
    st.markdown("---")
    
    df_rice = load_data("Oryza_sativa_Top_Genes.csv")
    img_rice = load_image("Rice_Top10_Biomarkers.png")
    
    if df_rice is not None:
        col1, col2 = st.columns([3, 2], gap="large")
        
        with col1:
            st.subheader("Top 10 Critical Genes")
            top10 = df_rice.head(10)
            
            # Professional Plotly config adapting to Streamlit theme
            fig = px.bar(top10, x='Gini_Importance_Score', y='Gene_ID', orientation='h',
                         title="Gini Importance Scores (Top 10)",
                         color='Gini_Importance_Score', color_continuous_scale='Greens')
            fig.update_traces(marker_line_color='rgba(0,0,0,0.5)', marker_line_width=1, opacity=0.9)
            fig.update_layout(hovermode="y unified", title_font_size=18, 
                              margin=dict(l=20, r=20, t=50, b=20))
            fig.update_layout(yaxis={'categoryorder':'total ascending'})
            
            st.plotly_chart(fig, use_container_width=True, theme="streamlit")
            
        with col2:
            st.subheader("Static Visualization")
            if img_rice:
                st.image(img_rice, caption="Top 10 Biomarkers (from Results folder)", use_column_width=True)
            else:
                st.warning("Image not found in 04_Results/Visualizations/")
                
            with st.container(border=True):
                st.markdown("#### Key Discovery")
                st.info("Gene **B6750** was isolated as the absolute most critical survival biomarker for rice under heat stress.")
        
        st.markdown("---")
        st.subheader("Full Ranked Dataset")
        st.dataframe(df_rice, use_container_width=True)
    else:
        st.error("Data file not found. Ensure you run this from the project root.")

elif page == "Cattle (Fauna) Biomarkers":
    st.title("🐄 Cattle (Bos taurus) Biomarkers")
    st.markdown("Analysis of the top survival genes for dairy cattle facing extreme heat.")
    st.markdown("---")
    
    df_cow = load_data("Bos_taurus_Top_Genes.csv")
    img_cow = load_image("Cow_Top10_Biomarkers.png")
    
    if df_cow is not None:
        col1, col2 = st.columns([3, 2], gap="large")
        
        with col1:
            st.subheader("Top 10 Critical Genes")
            top10 = df_cow.head(10)
            
            # Professional Plotly config adapting to Streamlit theme
            fig = px.bar(top10, x='Gini_Importance_Score', y='Gene_ID', orientation='h',
                         title="Gini Importance Scores (Top 10)",
                         color='Gini_Importance_Score', color_continuous_scale='Blues')
            fig.update_traces(marker_line_color='rgba(0,0,0,0.5)', marker_line_width=1, opacity=0.9)
            fig.update_layout(hovermode="y unified", title_font_size=18, 
                              margin=dict(l=20, r=20, t=50, b=20))
            fig.update_layout(yaxis={'categoryorder':'total ascending'})
            
            st.plotly_chart(fig, use_container_width=True, theme="streamlit")
            
        with col2:
            st.subheader("Static Visualization")
            if img_cow:
                st.image(img_cow, caption="Top 10 Biomarkers (from Results folder)", use_column_width=True)
            else:
                st.warning("Image not found in 04_Results/Visualizations/")
                
            with st.container(border=True):
                st.markdown("#### Key Discovery")
                st.info("Gene **ENSBTAG00000027477** was isolated as the absolute most critical survival biomarker for dairy cattle facing extreme heat.")
            
        st.markdown("---")
        st.subheader("Full Ranked Dataset")
        st.dataframe(df_cow, use_container_width=True)
    else:
        st.error("Data file not found. Ensure you run this from the project root.")

elif page == "Universal Intersection":
    st.title("🌍 Cross-Kingdom Universal Biomarkers")
    st.markdown("---")
    
    st.markdown("""
    Using mathematical intersection, the pipeline successfully proved that both plants and animals utilize a highly conserved, shared cellular defense mechanism against extreme thermal stress.
    """)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.subheader("The 4 Universal Biomarkers")
        
        with st.container(border=True):
            st.markdown("""
            * 🛡️ **HSP70 (Heat Shock Protein 70kDa):** Acts as a biological shield preventing protein denaturation.
            * 🔧 **HSP90 (Heat Shock Protein 90kDa):** Aids in cellular recovery and structural integrity.
            * 🧹 **ROS_Scavenger (Superoxide Dismutase):** Acts as a cellular vacuum to remove toxic oxygen garbage generated by heat panic.
            * 🎛️ **Transcription_Factor_HSF1:** The "Master Switch" that commands the DNA to deploy the heat shock shields.
            """)
        
    with col2:
        img_venn = load_image("Universal_Intersection_Venn.png")
        if img_venn:
            st.image(img_venn, caption="Universal Intersection Venn Diagram", use_column_width=True)
        else:
            st.warning("Venn Diagram image not found.")
