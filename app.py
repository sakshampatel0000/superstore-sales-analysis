import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="Superstore Sales Analysis", layout="wide")

# Custom CSS for Professional Styling & Centered Headings
st.markdown("""
    <style>
    /* Centered Header Title */
    .main-title {
        text-align: center;
        font-size: 38px;
        font-weight: 800;
        color: #1E88E5;
        padding-bottom: 10px;
    }
    .sub-title {
        text-align: center;
        font-size: 24px;
        font-weight: 600;
        color: #0D47A1;
        margin-top: 20px;
        margin-bottom: 15px;
        border-bottom: 2px solid #E0E0E0;
        padding-bottom: 5px;
    }
    /* Custom Info Box for Objective */
    .objective-box {
        background-color: #F0F4F8;
        border-left: 6px solid #1E88E5;
        padding: 15px;
        border-radius: 8px;
        color: #333333;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)
# Sidebar File Uploader Component
st.sidebar.markdown("---")
st.sidebar.subheader("📁 Upload Your Own Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

# Dynamic Data Loading Logic (With Auto-Missing Column Fill)

   # Dynamic Data Loading Logic (With NaN / Null Filling)
@st.cache_data
def load_data(file):
    if file is not None:
        try:
            df = pd.read_csv(file)
            
            # Save original present columns to session state
            st.session_state['uploaded_cols'] = list(df.columns)
            
            required_cols = {
                'Sales': np.nan,
                'Profit': np.nan,
                'Category': 'Null',
                'Sub-Category': 'Null',
                'Region': 'Null',
                'Segment': 'Null',
                'Ship Mode': 'Null',
                'State': 'Null',
                'Quantity': np.nan,
                'Discount': np.nan
            }
            
            missing_found = []
            for col, default_val in required_cols.items():
                if col not in df.columns:
                    df[col] = default_val
                    missing_found.append(col)
            
            if missing_found:
                st.sidebar.warning(f"⚠️ Missing columns: {', '.join(missing_found)} (Set to Null)")
            else:
                st.sidebar.success("✅ Complete Dataset Loaded!")
                
            return df
        except Exception as e:
            st.sidebar.error("⚠️ Error reading file! Falling back to default.")
            return pd.read_csv("SampleSuperstore.csv")
    else:
        st.session_state['uploaded_cols'] = ['Sales', 'Profit', 'Category', 'Sub-Category', 'Region', 'Segment', 'Ship Mode', 'State', 'Quantity', 'Discount']
        return pd.read_csv("SampleSuperstore.csv")             
# Load Dataset
Data = load_data(uploaded_file)

        
# Load Dataset
Data = load_data(uploaded_file)


# 2. Sidebar Navigation Switcher
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
st.sidebar.title("📌 Navigation Menu")

page = st.sidebar.radio(
    "Go to:",
    [
        "1️⃣ Data Overview & EDA (Notebook)",
        "2️⃣ Regional & Category Analysis",
        "3️⃣ Segment & Shipping Analysis",
        "4️⃣ Sales vs Profit and distribution Analysis",
        "5️⃣ Business Dashboard & Final Insights",
        "🤖 AI Business Assistant / Chatbot"
    ]
)

# =========================================================
# PAGE 1: DATA OVERVIEW & EDA (EXACT JUPYTER NOTEBOOK)
# =========================================================
if page == "1️⃣ Data Overview & EDA (Notebook)":
    
    # Title (Centered)
    st.markdown("<h1 class='main-title'>🛒 Superstore Sales Analysis using Python & Pandas</h1>", unsafe_allow_html=True)

    # Objective Section (Professional Card)
    st.markdown("<h3 class='sub-title'>🎯 Objective</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div class="objective-box">
        <b>The objective of this project is to analyze superstore sales.</b><br><br>
        <b>In this project we will:</b>
        <ul>
            <li>Load CSV Dataset</li>
            <li>Explore the Dataset</li>
            <li>Analyze Sales & Profit</li>
            <li>Analyze Categories & States</li>
            <li>Find Useful Business Insights</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Metrics Overview (Colorful Cards for Cells 12 to 17)
    st.markdown("<h3 class='sub-title'>📌 Key Sales & Profit Metrics</h3>", unsafe_allow_html=True)
    
    # --- Safe Calculation Logic (Handling Missing/Null Columns) ---
sales_val = "Null" if Data['Sales'].isna().all() else f"${Data['Sales'].sum():,.2f}"
profit_val = "Null" if Data['Profit'].isna().all() else f"${Data['Profit'].sum():,.2f}"
avg_sales_val = "Null" if Data['Sales'].isna().all() else f"${Data['Sales'].mean():,.2f}"
avg_profit_val = "Null" if Data['Profit'].isna().all() else f"${Data['Profit'].mean():,.2f}"

highest_sale_val = "Null" if Data['Sales'].isna().all() else f"${Data['Sales'].max():,.2f}"
lowest_sale_val = "Null" if Data['Sales'].isna().all() else f"${Data['Sales'].min():,.2f}"

# --- Metric Display Cards ---
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
m_col1.metric("💰 Total Sales", sales_val)
m_col2.metric("📈 Total Profit", profit_val)
m_col3.metric("📊 Average Sales", avg_sales_val)
m_col4.metric("📉 Average Profit", avg_profit_val)

m_col5, m_col6, m_col7, m_col8 = st.columns(4)
m_col5.metric("🏷️ Highest Sale", highest_sale_val)
m_col6.metric("🔻 Lowest Sale", lowest_sale_val)
m_col7.metric("📐 Total Rows (Shape)", f"{Data.shape[0]}")
m_col8.metric("🔄 Duplicate Rows", f"{Data.duplicated().sum()}")

st.markdown("---")

    # Load Dataset Display (Cell [2] & [3])
    st.markdown("<h3 class='sub-title'>📁 Full Dataset Load</h3>", unsafe_allow_html=True)
    st.dataframe(Data, use_container_width=True)

    st.markdown("---")

    # First & Last 5 Rows Side-by-Side (Tabs for clean look)
    st.markdown("<h3 class='sub-title'>🔍 Dataset Exploration (Head & Tail)</h3>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📌 First 5 Rows (head)", "📌 Last 5 Rows (tail)", "🏷️ Column Names"])
    
    with tab1:
        st.write("##### First five rows of the Dataset:")
        st.dataframe(Data.head(), use_container_width=True)

    with tab2:
        st.write("##### Last five rows of the Dataset:")
        st.dataframe(Data.tail(), use_container_width=True)

    with tab3:
        st.write("##### Column Names:")
        st.json(list(Data.columns))

    st.markdown("---")

    # Info, Describe & Missing Values Section
    st.markdown("<h3 class='sub-title'>📊 Statistical Summary & Data Information</h3>", unsafe_allow_html=True)
    
    col_info1, col_info2 = st.columns([1, 1])

    with col_info1:
        st.write("##### 📋 Statistical Summary (`describe`)")
        st.dataframe(Data.describe(), use_container_width=True)

    with col_info2:
        st.write("##### 🧹 Missing Values Count (`isnull`)")
        missing_data = Data.isnull().sum().reset_index()
        missing_data.columns = ["Column Name", "Missing Count"]
        st.dataframe(missing_data, use_container_width=True)

    st.markdown("---")

    # Top 10 Highest Sales (Cell [18])
    st.markdown("<h3 class='sub-title'>🏆 Top 10 Highest Sales</h3>", unsafe_allow_html=True)
    st.dataframe(Data.nlargest(10, "Sales"), use_container_width=True)

    st.markdown("---")

    # Top 10 Highest Profit (Cell [19])
    st.markdown("<h3 class='sub-title'>💰 Top 10 Highest Profit</h3>", unsafe_allow_html=True)
    st.dataframe(Data.nlargest(10, "Profit"), use_container_width=True)

    st.markdown("---")

    # Top 10 Loss Making Orders (Cell [20])
    st.markdown("<h3 class='sub-title'>🔻 top 10 loss making orders</h3>", unsafe_allow_html=True)
    st.dataframe(Data.nsmallest(10, "Profit"), use_container_width=True)

    st.markdown("---")

    # Category Analysis (Cell [21] & [22])
    st.markdown("<h3 class='sub-title'>📦 Category Wise Aggregations</h3>", unsafe_allow_html=True)
    col_cat1, col_cat2 = st.columns(2)

    with col_cat1:
        st.write("##### sales by category")
        st.dataframe(Data.groupby("Category")["Sales"].sum().reset_index(), use_container_width=True)

    with col_cat2:
        st.write("##### profit by category")
        st.dataframe(Data.groupby("Category")["Profit"].sum().reset_index(), use_container_width=True)

    st.markdown("---")

    # Sub-Category Analysis (Cell [23] & [24])
    st.markdown("<h3 class='sub-title'>🏷️ Sub-Category Wise Aggregations</h3>", unsafe_allow_html=True)
    col_sub1, col_sub2 = st.columns(2)

    with col_sub1:
        st.write("##### sales by sub-category")
        st.dataframe(Data.groupby("Sub-Category")["Sales"].sum().reset_index(), use_container_width=True)

    with col_sub2:
        st.write("##### profit by sub-category")
        st.dataframe(Data.groupby("Sub-Category")["Profit"].sum().reset_index(), use_container_width=True)

    st.markdown("---")

    # State Analysis (Cell [25] & [26])
    st.markdown("<h3 class='sub-title'>🗺️ State Wise Aggregations</h3>", unsafe_allow_html=True)
    col_st1, col_st2 = st.columns(2)

    with col_st1:
        st.write("##### sales by state")
        st.dataframe(Data.groupby("State")["Sales"].sum().reset_index(), use_container_width=True)

    with col_st2:
        st.write("##### profit by state")
        st.dataframe(Data.groupby("State")["Profit"].sum().reset_index(), use_container_width=True)

    st.markdown("---")

    # Segment & Ship Mode Analysis (Cell [27] & [28])
    st.markdown("<h3 class='sub-title'>👥 Segment & Shipping Aggregations</h3>", unsafe_allow_html=True)
    col_seg, col_ship = st.columns(2)

    with col_seg:
        st.write("##### sales by segment")
        st.dataframe(Data.groupby("Segment")["Sales"].sum().reset_index(), use_container_width=True)

    with col_ship:
        st.write("##### sales by ship mode")
        st.dataframe(Data.groupby("Ship Mode")["Sales"].sum().reset_index(), use_container_width=True)

# =========================================================
# PAGE 2 & PAGE 3 PLACEHOLDERS
# =========================================================
# =========================================================
# PAGE 2: REGIONAL & CATEGORY ANALYSIS
# =========================================================
elif page == "2️⃣ Regional & Category Analysis":
    import plotly.express as px

    st.markdown("<h1 class='main-title'>📊 Regional & Category Visual Analysis</h1>", unsafe_allow_html=True)

    # Sales by Category Analysis (Cell [29] - Colorful & Interactive)
    st.markdown("<h3 class='sub-title'>sales by category analysis</h3>", unsafe_allow_html=True)
    
    category_sales = Data.groupby("Category")["Sales"].sum().reset_index()

    # Dynamic Vibrant Bar Chart
    fig = px.bar(
        category_sales, 
        x="Category", 
        y="Sales", 
        color="Category",
        text_auto=".2s",
        color_discrete_sequence=px.colors.qualitative.Bold,
        title="Sales by Category"
    )
    fig.update_layout(
        xaxis_title="Category",
        yaxis_title="Sales",
        showlegend=False,
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

    # Insights (Cell [30])
    st.markdown("""
    <div class="objective-box">
        <h4>💡 Insights</h4>
        <ul>
            <li><b>Technology</b> generated the highest sales.</li>
            <li><b>Furniture</b> generated comparatively lower sales.</li>
            <li><b>Office Supplies</b> performed moderately.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # Profit by Category Analysis (Cell [31] - Colorful & Interactive)
    st.markdown("<h3 class='sub-title'>Profit by Category Analysis</h3>", unsafe_allow_html=True)
    
    profit_category = Data.groupby("Category")["Profit"].sum().reset_index()

    # Vibrant Plotly Bar Chart with Hover Values
    fig_profit = px.bar(
        profit_category, 
        x="Category", 
        y="Profit", 
        color="Category",
        text_auto=".2s",
        color_discrete_sequence=px.colors.qualitative.Vivid,
        title="profit by category"
    )
    fig_profit.update_layout(
        xaxis_title="category",
        yaxis_title="profit",
        showlegend=False,
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig_profit, use_container_width=True)

    # Insights (Cell [32])
    st.markdown("""
    <div class="objective-box">
        <h4>💡 Insights</h4>
        <ul>
            <li><b>Technology</b> generated the highest profit.</li>
            <li><b>Office Supplies</b> generated a moderate profit.</li>
            <li><b>Furniture</b> generated the lowest profit.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # Sales by Sub_Category Analysis (Cell [33] - Colorful & Interactive)
    st.markdown("<h3 class='sub-title'>Sales by Sub_Category Analysis</h3>", unsafe_allow_html=True)
    
    sub_category_sales = Data.groupby("Sub-Category")["Sales"].sum().reset_index()

    # Vibrant Plotly Bar Chart with Hover Values & Rotated Labels
    fig_sub_sales = px.bar(
        sub_category_sales, 
        x="Sub-Category", 
        y="Sales", 
        color="Sub-Category",
        text_auto=".2s",
        color_discrete_sequence=px.colors.qualitative.Prism,
        title="Sales by Sub_Category"
    )
    fig_sub_sales.update_layout(
        xaxis_title="Sub_category",
        yaxis_title="Sales",
        showlegend=False,
        template="plotly_white",
        height=500
    )
    fig_sub_sales.update_xaxes(tickangle=-45)

    st.plotly_chart(fig_sub_sales, use_container_width=True)

    # Insights (Cell [34])
    st.markdown("""
    <div class="objective-box">
        <h4>💡 insights</h4>
        <ul>
            <li><b>Top-performing chairs</b> generated the highest sales and contribute a major portion of the business revenue.</li>
            <li><b>Phones and Chairs</b> are among the best selling sub-categories.</li>
            <li>Some sub-categories show very low sales, indicating lower customer demand or limited product performance.</li>
            <li>There is a large variation in sales across different sub-categories, which means customer demand is not evenly distributed.</li>
            <li>The company should focus on high-selling sub-categories while analyzing why low-selling ones are underperforming.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # Profit by Sub-Category Analysis (Cell [35] - Colorful & Interactive)
    st.markdown("<h3 class='sub-title'>Profit by Sub-Category Analysis</h3>", unsafe_allow_html=True)
    
    W = Data.groupby("Sub-Category")["Profit"].sum().reset_index()

    # Dynamic Colorful Plotly Bar Chart with Hover Tooltip
    fig_sub_profit = px.bar(
        W, 
        x="Sub-Category", 
        y="Profit", 
        color="Profit",
        text_auto=".2s",
        color_continuous_scale=px.colors.diverging.Tealrose,
        title="Profit by Sub_Category"
    )
    fig_sub_profit.update_layout(
        xaxis_title="Sub_Category",
        yaxis_title="Profit",
        showlegend=False,
        template="plotly_white",
        height=500
    )
    fig_sub_profit.update_xaxes(tickangle=-90)

    st.plotly_chart(fig_sub_profit, use_container_width=True)

    # Insights (Cell [36])
    st.markdown("""
    <div class="objective-box">
        <h4>💡 Insights</h4>
        <ul>
            <li>Some sub-categories generate significantly higher profits than others.</li>
            <li>Certain sub-categories contribute very little profit despite being sold.</li>
            <li>A few sub-categories even show negative profit, one of them is <b>Tables</b>, indicating financial losses.</li>
            <li>The company should focus on expanding high-profit sub-categories while improving or reviewing the loss-making ones.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Sales by Region Analysis (Cell [37] - Colorful & Interactive)
    st.markdown("<h3 class='sub-title'>Sales by region analysis</h3>", unsafe_allow_html=True)
    
    region_sales = Data.groupby("Region")["Sales"].sum().reset_index()

    # Dynamic Vibrant Plotly Bar Chart with Hover Tooltip
    fig_region_sales = px.bar(
        region_sales, 
        x="Region", 
        y="Sales", 
        color="Region",
        text_auto=".2s",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title="Sales by Region"
    )
    fig_region_sales.update_layout(
        xaxis_title="Region",
        yaxis_title="Sales",
        showlegend=False,
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig_region_sales, use_container_width=True)

    # Insights (Cell [38])
    st.markdown("""
    <div class="objective-box">
        <h4>💡 Insights</h4>
        <ul>
            <li>The <b>West region</b> generated the highest sales.</li>
            <li>The <b>East region</b> also contributed significantly.</li>
            <li>The <b>South region</b> generated comparatively lower sales.</li>
            <li>Sales performance varies across different regions.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Profit by Region Analysis (Cell [39] - Colorful & Interactive)
    st.markdown("<h3 class='sub-title'>profit by region analysis</h3>", unsafe_allow_html=True)
    
    region_profit = Data.groupby("Region")["Profit"].sum().reset_index()

    # Dynamic Vibrant Plotly Bar Chart with Hover Tooltip
    fig_region_profit = px.bar(
        region_profit, 
        x="Region", 
        y="Profit", 
        color="Region",
        text_auto=".2s",
        color_discrete_sequence=px.colors.qualitative.Dark2,
        title="Profit by Region"
    )
    fig_region_profit.update_layout(
        xaxis_title="Region",
        yaxis_title="Profit",
        showlegend=False,
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig_region_profit, use_container_width=True)

    # Insights (Cell [40])
    st.markdown("""
    <div class="objective-box">
        <h4>💡 Insights</h4>
        <ul>
            <li>Some regions generate higher profit than others.</li>
            <li>A region with high sales does not always generate the highest profit.</li>
            <li>Profitability differs across regions.</li>
            <li>Business strategies can be improved for low-profit regions.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# PAGE 3: SEGMENT & SHIPPING ANALYSIS
# =========================================================
elif page == "3️⃣ Segment & Shipping Analysis":
    import plotly.express as px

    # Page Title
    st.markdown("<h1 class='main-title'>📈 Segment & Shipping Visual Analysis</h1>", unsafe_allow_html=True)

    # Sales by segment analysis (Cell [41] - Colorful & Interactive)
    st.markdown("<h3 class='sub-title'>Sales by segment analysis</h3>", unsafe_allow_html=True)
    
    segment_sales = Data.groupby("Segment")["Sales"].sum().reset_index()

    # Dynamic Vibrant Plotly Bar Chart with Hover Values
    fig_seg_sales = px.bar(
        segment_sales, 
        x="Segment", 
        y="Sales", 
        color="Segment",
        text_auto=".2s",
        color_discrete_sequence=px.colors.qualitative.Pastel1,
        title="Sales by Segment"
    )
    fig_seg_sales.update_layout(
        xaxis_title="Segment",
        yaxis_title="Sales",
        showlegend=False,
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig_seg_sales, use_container_width=True)

    # Insights (Cell [42])
    st.markdown("""
    <div class="objective-box">
        <h4>💡 Insights</h4>
        <ul>
            <li>The <b>Consumer segment</b> generated the highest sales.</li>
            <li>The <b>Corporate segment</b> contributed moderately.</li>
            <li>The <b>Home Office segment</b> generated comparatively lower sales.</li>
            <li>Sales vary across different customer segments.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Profit by segment analysis (Cell [43] - Colorful & Interactive)
    st.markdown("<h3 class='sub-title'>profit by segment analysis</h3>", unsafe_allow_html=True)
    
    segment_profit = Data.groupby("Segment")["Profit"].sum().reset_index()

    # Dynamic Vibrant Plotly Bar Chart with Hover Tooltip
    fig_seg_profit = px.bar(
        segment_profit, 
        x="Segment", 
        y="Profit", 
        color="Segment",
        text_auto=".2s",
        color_discrete_sequence=px.colors.qualitative.Set2,
        title="Profit by Segment"
    )
    fig_seg_profit.update_layout(
        xaxis_title="Segment",
        yaxis_title="Profit",
        showlegend=False,
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig_seg_profit, use_container_width=True)

    # Insights (Cell [44])
    st.markdown("""
    <div class="objective-box">
        <h4>💡 Insights</h4>
        <ul>
            <li>The <b>Consumer segment</b> generated the highest profit.</li>
            <li>The <b>Corporate segment</b> generated moderate profit.</li>
            <li>The <b>Home Office segment</b> generated the lowest profit.</li>
            <li>Profitability differs across customer segments.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Sales by ship mode analysis (Cell [45] - Colorful & Interactive)
    st.markdown("<h3 class='sub-title'>sales by ship mode analysis</h3>", unsafe_allow_html=True)
    
    shipmode_sales = Data.groupby("Ship Mode")["Sales"].sum().reset_index()

    # Dynamic Vibrant Plotly Bar Chart with Hover Tooltip
    fig_ship_sales = px.bar(
        shipmode_sales, 
        x="Ship Mode", 
        y="Sales", 
        color="Ship Mode",
        text_auto=".2s",
        color_discrete_sequence=px.colors.qualitative.Plotly,
        title="Sales by Ship Mode"
    )
    fig_ship_sales.update_layout(
        xaxis_title="Ship Mode",
        yaxis_title="Sales",
        showlegend=False,
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig_ship_sales, use_container_width=True)

    # Insights (Cell [46])
    st.markdown("""
    <div class="objective-box">
        <h4>💡 Insights</h4>
        <ul>
            <li><b>Standard Class</b> generated the highest sales.</li>
            <li><b>Second Class and First Class</b> contributed moderate sales.</li>
            <li><b>Same Day</b> generated the lowest sales.</li>
            <li>Most customers preferred Standard Class for shipping.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Profit by ship mode analysis (Cell [47] - Colorful & Interactive)
    st.markdown("<h3 class='sub-title'>profit by ship mode analysis</h3>", unsafe_allow_html=True)
    
    shipmode_profit = Data.groupby("Ship Mode")["Profit"].sum().reset_index()

    # Dynamic Vibrant Plotly Bar Chart with Hover Tooltip
    fig_ship_profit = px.bar(
        shipmode_profit, 
        x="Ship Mode", 
        y="Profit", 
        color="Ship Mode",
        text_auto=".2s",
        color_discrete_sequence=px.colors.qualitative.Antique,
        title="Profit by Ship Mode"
    )
    fig_ship_profit.update_layout(
        xaxis_title="Ship Mode",
        yaxis_title="Profit",
        showlegend=False,
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig_ship_profit, use_container_width=True)

    # Insights (Cell [48])
    st.markdown("""
    <div class="objective-box">
        <h4>💡 Insights</h4>
        <ul>
            <li><b>Standard Class</b> generated the highest profit.</li>
            <li>Other shipping modes generated comparatively lower profit.</li>
            <li>Profit varies across different shipping methods.</li>
            <li>Choosing the right shipping mode can impact overall profitability.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# PAGE 4: ADVANCED DISTRIBUTIONS & CORRELATIONS
# =========================================================
# =========================================================
# PAGE 4: SALES VS PROFIT ANALYSIS
# =========================================================
elif page == "4️⃣ Sales vs Profit and distribution Analysis":
    import plotly.express as px

    # Page Title
    st.markdown("<h1 class='main-title'>📈 Sales vs Profit Analysis</h1>", unsafe_allow_html=True)

    # Sales vs profit analysis (Cell [49] - Colorful & Interactive Scatter Plot)
    st.markdown("<h3 class='sub-title'>Sales vs profit analysis</h3>", unsafe_allow_html=True)

    fig_scatter = px.scatter(
        Data,
        x="Sales",
        y="Profit",
        color="Category",
        hover_data=["Sub-Category", "Segment"],
        title="Sales vs Profit",
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    fig_scatter.update_layout(
        xaxis_title="Sales",
        yaxis_title="Profit",
        template="plotly_white",
        height=500
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    # Insights (Cell [50])
    st.markdown("""
    <div class="objective-box">
        <h4>💡 Insights</h4>
        <ul>
            <li>Most orders generated positive profit.</li>
            <li>Some high sales orders still resulted in losses.</li>
            <li>Higher sales do not always guarantee higher profit.</li>
            <li>A few orders generated extremely high sales.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # Sales Distribution (Cell [51] - Interactive Histogram)
    st.markdown("<h3 class='sub-title'>Sales distribution</h3>", unsafe_allow_html=True)

    fig_sales_dist = px.histogram(
        Data,
        x="Sales",
        nbins=30,
        title="Sales Distribution",
        color_discrete_sequence=["#3366CC"]
    )

    fig_sales_dist.update_layout(
        xaxis_title="Sales",
        yaxis_title="Frequency",
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig_sales_dist, use_container_width=True)

    # Insights (Cell [52])
    st.markdown("""
    <div class="objective-box">
        <h4>💡 Insights</h4>
        <ul>
            <li>Most orders have relatively low sales.</li>
            <li>Only a few orders generated very high sales.</li>
            <li>Sales distribution is right-skewed.</li>
            <li>High-value sales orders are comparatively rare.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Profit Distribution (Cell [53] - Interactive Histogram)
    st.markdown("<h3 class='sub-title'>Profit distribution</h3>", unsafe_allow_html=True)

    fig_profit_dist = px.histogram(
        Data,
        x="Profit",
        nbins=30,
        title="Profit Distribution",
        color_discrete_sequence=["#2CA02C"]
    )

    fig_profit_dist.update_layout(
        xaxis_title="Profit",
        yaxis_title="Frequency",
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig_profit_dist, use_container_width=True)

    # Insights (Cell [54])
    st.markdown("""
    <div class="objective-box">
        <h4>💡 Insights</h4>
        <ul>
            <li>Most orders generated small profits.</li>
            <li>Some orders resulted in losses.</li>
            <li>A few orders generated very high profit.</li>
            <li>Profit distribution is uneven across orders.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # Correlation Heatmap (Cell [55] - Interactive Plotly Heatmap)
    st.markdown("<h3 class='sub-title'>Correlation heatmap</h3>", unsafe_allow_html=True)

    # Calculating correlation matrix
    corr_matrix = Data[["Sales", "Profit", "Quantity", "Discount"]].corr().round(4)

    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu_r",
        title="Correlation Heatmap"
    )

    fig_corr.update_layout(
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig_corr, use_container_width=True)

    # Insights (Cell [56])
    st.markdown("""
    <div class="objective-box">
        <h4>💡 Insights</h4>
        <ul>
            <li>Sales and Profit show a positive correlation.</li>
            <li>Discount has a negative correlation with Profit.</li>
            <li>Quantity has a weak correlation with Sales and Profit.</li>
            <li>Higher discounts generally reduce profitability.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # Sales Outlier Detection (Cell [57] - Interactive Boxplot)
    st.markdown("<h3 class='sub-title'>Sales Outlier Detection</h3>", unsafe_allow_html=True)

    fig_sales_box = px.box(
        Data,
        y="Sales",
        title="Sales Boxplot",
        color_discrete_sequence=["#FF7F0E"]
    )

    fig_sales_box.update_layout(
        yaxis_title="Sales",
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig_sales_box, use_container_width=True)

    # Insights (Cell [58])
    st.markdown("""
    <div class="objective-box">
        <h4>💡 Insights</h4>
        <ul>
            <li>Most sales values lie within a limited range.</li>
            <li>Several high-value sales appear as outliers.</li>
            <li>The distribution is positively skewed.</li>
            <li>Outliers contribute significantly to total sales.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # Discount vs Profit Analysis (Cell [59] - Interactive Scatter Plot)
    st.markdown("<h3 class='sub-title'>Discount vs Profit Analysis</h3>", unsafe_allow_html=True)

    fig_disc_prof = px.scatter(
        Data,
        x="Discount",
        y="Profit",
        color="Category",
        hover_data=["Sub-Category", "Sales"],
        title="Discount vs Profit",
        color_discrete_sequence=px.colors.qualitative.Vivid
    )

    fig_disc_prof.update_layout(
        xaxis_title="Discount",
        yaxis_title="Profit",
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig_disc_prof, use_container_width=True)

    # Insights (Cell [60])
    st.markdown("""
    <div class="objective-box">
        <h4>💡 Insights</h4>
        <ul>
            <li>Higher discounts generally reduce profit.</li>
            <li>Some heavily discounted orders result in losses.</li>
            <li>Low-discount orders are generally more profitable.</li>
            <li>Discount strategy has a significant impact on business performance.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# PAGE 5: BUSINESS DASHBOARD & FINAL INSIGHTS
# ==========================================
elif page == "5️⃣ Business Dashboard & Final Insights":
    st.markdown("<h2 class='main-title'>📊 Business Dashboard & Final Insights</h2>", unsafe_allow_html=True)
    st.markdown("This dashboard provides a quick overall overview of business performance using multiple core visualizations.")

    st.markdown("---")

    # 2x2 Layout for Dashboard Visualizations
    col1, col2 = st.columns(2)

    # Chart 1: Sales by Category
    with col1:
        category_sales = Data.groupby("Category")["Sales"].sum().reset_index()
        fig_cat_sales = px.bar(
            category_sales,
            x="Category",
            y="Sales",
            title="1. Sales by Category",
            color="Category",
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        fig_cat_sales.update_layout(template="plotly_white", height=380, showlegend=False)
        st.plotly_chart(fig_cat_sales, use_container_width=True)

    # Chart 2: Profit by Category
    with col2:
        category_profit = Data.groupby("Category")["Profit"].sum().reset_index()
        fig_cat_profit = px.bar(
            category_profit,
            x="Category",
            y="Profit",
            title="2. Profit by Category",
            color="Category",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_cat_profit.update_layout(template="plotly_white", height=380, showlegend=False)
        st.plotly_chart(fig_cat_profit, use_container_width=True)

    col3, col4 = st.columns(2)

    # Chart 3: Sales Distribution
    with col3:
        fig_sales_dist = px.histogram(
            Data,
            x="Sales",
            nbins=30,
            title="3. Sales Distribution",
            color_discrete_sequence=["#2CA02C"]
        )
        fig_sales_dist.update_layout(
            xaxis_title="Sales",
            yaxis_title="Frequency",
            template="plotly_white",
            height=380
        )
        st.plotly_chart(fig_sales_dist, use_container_width=True)

    # Chart 4: Sales vs Profit
    with col4:
        fig_sales_vs_profit = px.scatter(
            Data,
            x="Sales",
            y="Profit",
            title="4. Sales vs Profit",
            color_discrete_sequence=["#E377C2"],
            hover_data=["Category", "Sub-Category"]
        )
        fig_sales_vs_profit.update_layout(
            xaxis_title="Sales",
            yaxis_title="Profit",
            template="plotly_white",
            height=380
        )
        st.plotly_chart(fig_sales_vs_profit, use_container_width=True)

    st.markdown("---")

    # Insights Section (Cell [62])
    st.markdown("""
    <div class="objective-box">
        <h4>💡 Key Business Insights</h4>
        <ul>
            <li><strong>Technology</strong> contributes the highest sales across product categories.</li>
            <li>Profitability varies significantly across categories (Furniture yields very low profit margins).</li>
            <li>Most sales values are concentrated at lower transaction ranges.</li>
            <li>Higher sales do not always generate higher profit due to heavy discounts.</li>
            <li>A few high-value orders act as major outliers driving top-line revenue.</li>
            <li>The dashboard provides a quick, high-level overview of overall business performance.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Final Business Insights Section (Cell [63])
    st.markdown("""
    <div class="objective-box">
        <h4>🎯 Final Business Insights</h4>
        <ul>
            <li><strong>Technology</strong> generated the highest sales.</li>
            <li><strong>Office Supplies</strong> contributed the highest number of orders.</li>
            <li><strong>Standard Class shipping</strong> is the most commonly used shipping mode.</li>
            <li>Sales distribution is <strong>positively skewed</strong>.</li>
            <li>High sales do not always generate high profit.</li>
            <li>Higher discounts often reduce profitability.</li>
            <li>A few high-value orders contribute significantly to total revenue.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    # =========================================================
# PAGE 6: AI BUSINESS ASSISTANT / CHATBOT
# =========================================================
elif page == "🤖 AI Business Assistant / Chatbot":
    st.markdown("<h1 class='main-title'>🤖 Superstore Smart AI Assistant</h1>", unsafe_allow_html=True)
    st.markdown("Aap superstore data ke bare me koi bhi question pooch sakte hain (e.g., *'total profit'*, *'highest sales region'*, *'best sub category'*).")

    # Helper Function to Answer User Queries Smartly
    def answer_query(query, df):
        q = query.lower().strip()

        # 1. Total Profit
        if "total profit" in q or "overall profit" in q or "kitna profit" in q:
            val = df['Profit'].sum()
            return f"💰 **Total Profit:** **${val:,.2f}**"

        # 2. Total Sales
        elif "total sales" in q or "overall sales" in q or "kitni sales" in q:
            val = df['Sales'].sum()
            return f"💵 **Total Sales:** **${val:,.2f}**"

        # 3. Highest Sales Region / Top Region
        elif "highest sales region" in q or "top sales region" in q or "best region" in q or "region" in q and "sales" in q:
            reg = df.groupby("Region")["Sales"].sum().idxmax()
            val = df.groupby("Region")["Sales"].sum().max()
            return f"🌍 **Highest Sales Region:** **{reg}** (Total Sales: **${val:,.2f}**)"

        # 4. Highest Profit Region
        elif "highest profit region" in q or "top profit region" in q or "region" in q and "profit" in q:
            reg = df.groupby("Region")["Profit"].sum().idxmax()
            val = df.groupby("Region")["Profit"].sum().max()
            return f"🏆 **Highest Profit Region:** **{reg}** (Total Profit: **${val:,.2f}**)"

        # 5. Highest Sales Category / Best Category
        elif "top category" in q or "best category" in q or "highest sales category" in q or "category" in q and "sales" in q:
            cat = df.groupby("Category")["Sales"].sum().idxmax()
            val = df.groupby("Category")["Sales"].sum().max()
            return f"📦 **Highest Sales Category:** **{cat}** (Total Sales: **${val:,.2f}**)"

        # 6. Highest Profit Category
        elif "highest profit category" in q or "most profitable category" in q or "category" in q and "profit" in q:
            cat = df.groupby("Category")["Profit"].sum().idxmax()
            val = df.groupby("Category")["Profit"].sum().max()
            return f"💎 **Most Profitable Category:** **{cat}** (Total Profit: **${val:,.2f}**)"

        # 7. Best Sub-Category / Top Sub Category
        elif "top sub category" in q or "best sub category" in q or "sub category" in q and "sales" in q:
            sub = df.groupby("Sub-Category")["Sales"].sum().idxmax()
            val = df.groupby("Sub-Category")["Sales"].sum().max()
            return f"🏷️ **Top Sub-Category (Sales):** **{sub}** (Total Sales: **${val:,.2f}**)"

        # 8. Worst Sub-Category / Loss Making Sub-Category
        elif "loss sub category" in q or "worst sub category" in q or "lowest profit sub category" in q:
            sub = df.groupby("Sub-Category")["Profit"].sum().idxmin()
            val = df.groupby("Sub-Category")["Profit"].sum().min()
            return f"🔻 **Lowest Profit / Loss Sub-Category:** **{sub}** (Total Profit: **${val:,.2f}**)"

        # 9. Top State
        elif "top state" in q or "highest sales state" in q or "best state" in q:
            st_name = df.groupby("State")["Sales"].sum().idxmax()
            val = df.groupby("State")["Sales"].sum().max()
            return f"🏛️ **Top State by Sales:** **{st_name}** (Total Sales: **${val:,.2f}**)"

        # 10. Summary / Everything (Sab Kuch)
        elif "summary" in q or "sab kuch" in q or "overview" in q or "all info" in q:
            top_reg_sales = df.groupby("Region")["Sales"].sum().idxmax()
            top_cat_sales = df.groupby("Category")["Sales"].sum().idxmax()
            top_sub_profit = df.groupby("Sub-Category")["Profit"].sum().idxmax()
            
            summary_msg = f"""
            ### 📊 Quick Superstore Summary:
            * 💰 **Total Sales:** ${df['Sales'].sum():,.2f}
            * 📈 **Total Profit:** ${df['Profit'].sum():,.2f}
            * 🌍 **Top Sales Region:** {top_reg_sales}
            * 📦 **Top Sales Category:** {top_cat_sales}
            * 💎 **Most Profitable Sub-Category:** {top_sub_profit}
            """
            return summary_msg

        # Default fallback
        else:
            return "🤖 Aap in keywords se pooch sakte hain: **'total profit'**, **'total sales'**, **'top region'**, **'top category'**, **'top state'**, ya **'sab kuch'**."

    # Chat UI in Streamlit
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! Mai aapka Superstore Data Assistant hoon. Aap kya poochna chahte hain?"}
        ]

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input Field
    if prompt := st.chat_input("Poochiye (e.g., total profit, top region, top category, sab kuch)..."):
        # Add User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process Answer
        bot_response = answer_query(prompt, Data)

        # Add Assistant Response
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response)
