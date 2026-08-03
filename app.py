import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# PAGE SETTINGS
# -------------------------------------------------
st.set_page_config(
    page_title="Retail Store Business Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)
st.markdown("""
<style>

/* Background */
.stApp{
background:#0E1117;
}

[data-testid="stSidebar"]{
background:#1F2430;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

.chart-card{
    background-color:#1f2430;
    padding:18px;
    border-radius:15px;
    margin-bottom:20px;
    box-shadow:0px 3px 8px rgba(0,0,0,0.25);
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
df = pd.read_excel("RetailStore_New.xlsx")
df["Date"] = pd.to_datetime(df["Date"])

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.image(
    "https://img.icons8.com/color/96/combo-chart.png",
    width=90
)

st.sidebar.title("Dashboard Filters")
st.sidebar.markdown("""
---
### 📌 Filter Options
Use the filters below to analyze the retail data.
""")

product = st.sidebar.multiselect(
    "Select Product",
    df["Product"].unique(),
    default=df["Product"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

month = st.sidebar.multiselect(
    "Select Month",
    df["Date"].dt.month_name().unique(),
    default=df["Date"].dt.month_name().unique()
)

df = df[
    (df["Product"].isin(product)) &
    (df["Category"].isin(category)) &
    (df["Date"].dt.month_name().isin(month))
]
st.sidebar.markdown("---")

with open("RetailStore_New.xlsx", "rb") as file:
    st.sidebar.download_button(
        label="📥 Download Excel Report",
        data=file,
        file_name="RetailStore_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# -------------------------------------------------
# HEADER
# -------------------------------------------------
from datetime import datetime

today = datetime.now().strftime("%d %b %Y")

st.markdown(f"""
<div style="text-align:center;">

<h1 style="color:#1E88E5; font-size:46px; margin-bottom:5px; font-weight:bold;">
📊 Retail Store Business Intelligence Dashboard
</h1>

<p style="color:#A0AEC0; font-size:19px; margin-top:0;">
Real-Time Sales • Revenue • Inventory • Customer Analytics
</p>

<p style="color:#999999;">
📅 Last Updated: {today}
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("---")

# -------------------------------------------------
# KPI VALUES
# -------------------------------------------------
total_revenue = int(df["Revenue"].sum())
total_sales = int(df["Quantity"].sum())
avg_rating = round(df["Customer Rating"].mean(),2)
total_products = df["Product"].nunique()
total_profit = int((df["Revenue"] - df["Cost"]).sum())

# -------------------------------------------------
# KPI CARDS
# -------------------------------------------------
st.markdown("""
<style>

.kpi-card{
    border-radius:18px;
    padding:32px;
    min-height:125px;
    color:white;
    text-align:center;
    font-family:Arial;
    box-shadow:0px 4px 10px rgba(0,0,0,0.25);
}

.revenue{
background:linear-gradient(135deg,#16A34A,#22C55E);
}

.sales{
background:linear-gradient(135deg,#2563EB,#3B82F6);
}

.rating{
background:linear-gradient(135deg,#F59E0B,#FBBF24);
color:black;
}

.product{
background:linear-gradient(135deg,#7C3AED,#A855F7);
}

.kpi-title{
    font-size:20px;
    font-weight:700;
    color:white;
    margin-bottom:10px;
}

.kpi-value{
    font-size:38px;
    font-weight:800;
    color:white;
    margin-top:12px;
}

</style>
""", unsafe_allow_html=True)

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card revenue">
        <div class="kpi-title">💰 Total Revenue</div>
        <div class="kpi-value">₹ {total_revenue:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card sales">
        <div class="kpi-title">🛒 Total Sales</div>
        <div class="kpi-value">{total_sales}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card rating">
        <div class="kpi-title">⭐ Customer Rating</div>
        <div class="kpi-value">{avg_rating} / 5</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card product">
        <div class="kpi-title">💰 Total Profit</div>
        <div class="kpi-value">₹ {total_profit:,}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------
# TOP INSIGHTS
# -----------------------------

top_product = df.groupby("Product")["Quantity"].sum().idxmax()
top_product_qty = df.groupby("Product")["Quantity"].sum().max()

best_category = df.groupby("Category")["Revenue"].sum().idxmax()
best_category_revenue = df.groupby("Category")["Revenue"].sum().max()
col1, col2 = st.columns(2)

with col2:
    st.info(f"""
### 📂 Best Category

**{best_category}**

💰 Revenue: **₹ {best_category_revenue:,}**
""")

st.markdown("---")

# -------------------------------------------------
# PIE CHART - BEST SELLING PRODUCTS
# -------------------------------------------------

pie = px.pie(
    df,
    names="Product",
    values="Quantity",
    hole=0.45,
    color_discrete_sequence=px.colors.qualitative.Set3,
    title="🥧 Best Selling Products"
)
pie.update_layout(
    title={
        "text": "🥧 Best Selling Products",
        "font": {"size": 22},
        "x": 0
    }
)
pie.update_layout(
    height=420,

    margin=dict(
        l=20,
        r=20,
        t=50,
        b=20
    ),

    legend=dict(
        x=0.78,          # Move legend closer to the pie
        y=0.5,           # Vertically center it
        xanchor="left",
        yanchor="middle",

        font=dict(
            size=14       # Bigger legend text
        ),

        itemsizing="constant"
    )
)
pie.update_traces(
    textinfo="percent",
    textfont_size=14
)


# -------------------------------------------------
# MONTHLY SALES TREND
# -------------------------------------------------

monthly = df.groupby(df["Date"].dt.month_name())["Revenue"].sum().reset_index()

months = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

monthly["Date"] = pd.Categorical(
    monthly["Date"],
    categories=months,
    ordered=True
)

monthly = monthly.sort_values("Date")

line = px.line(
    monthly,
    x="Date",
    y="Revenue",
    markers=True,
    title="📈 Monthly Sales Trend"
)
line.update_layout(
    title={
        "text": "📈 Monthly Sales Trend",
        "font": {"size": 22},
        "x": 0
    }
)
line.update_traces(line=dict(width=4))

# -------------------------------------------------
# SHOW BOTH CHARTS
# -------------------------------------------------

left, right = st.columns(2)

with left:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(line, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
# -------------------------------------------------
# REVENUE VS COST
# -------------------------------------------------

compare = df.groupby("Product")[["Revenue","Cost"]].sum().reset_index()

bar = px.bar(
    compare,
    x="Product",
    y=["Revenue","Cost"],
    barmode="group",
    title="📊 Revenue vs Cost",
    color_discrete_sequence=["#4CAF50","#F44336"]
)
bar.update_layout(
    title={
        "text": "📊 Revenue vs Cost",
        "font": {"size": 22},
        "x": 0
    }
)
st.markdown('<div class="chart-card">', unsafe_allow_html=True)

st.plotly_chart(bar, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# -------------------------------------------------
# INVENTORY
# -------------------------------------------------



inventory = (
    df.groupby(["Product", "Category"], as_index=False)["Stock"]
      .max()
)

inventory["Inventory Status"] = inventory["Stock"].apply(
    lambda x: "🟢 In Stock" if x >= 50 else "🔴 Low Stock"
)

inventory = inventory.sort_values("Stock", ascending=False)

inventory_style = (
    inventory.style
    .hide(axis="index")
    .set_properties(**{
        "text-align": "center",
        "font-size": "14px"
    })
    .set_table_styles([
        {"selector": "th",
         "props": [("text-align", "center"),
                   ("font-size", "15px"),
                   ("font-weight", "bold")]},
        {"selector": "td",
         "props": [("padding", "6px 10px")]}
    ])
)


# -------------------------------------------------
# CUSTOMER FEEDBACK
# -------------------------------------------------



feedback = df[["Product","Customer Rating","Feedback"]]

feedback_style = (
    feedback.style
    .hide(axis="index")
    .set_properties(**{
        "text-align": "center",
        "font-size": "14px"
    })
    .set_table_styles([
        {"selector": "th",
         "props": [("text-align", "center"),
                   ("font-size", "15px"),
                   ("font-weight", "bold")]},
        {"selector": "td",
         "props": [("padding", "6px 10px")]}
    ])
)
left, right = st.columns(2)

with left:
    st.subheader("📦 Inventory Status")
    st.dataframe(
        inventory_style,
        use_container_width=True,
        height=350
    )

with right:
    st.subheader("⭐ Customer Feedback")
    st.dataframe(
        feedback_style,
        use_container_width=True,
        height=350
    )

st.markdown("---")

st.markdown("""
<div style='text-align:center;
padding:20px;
color:#6B7280;
font-size:22px;'>

Developed by <b>Reshma Shaik</b> ❤️

Python • Streamlit • Pandas • Plotly

</div>
""", unsafe_allow_html=True)
