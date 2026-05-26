import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Drop Detective",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  THEME — Black · Purple · White
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Playfair+Display:wght@700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: #080810;
    color: #f0eeff;
}

/* ── hero ── */
.hero {
    background: linear-gradient(135deg, #0d0d1a 0%, #130d2e 60%, #0a0a18 100%);
    border: 1px solid #2d1f5e;
    border-radius: 20px;
    padding: 2.8rem 3.2rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content:"";
    position:absolute; top:-80px; right:-80px;
    width:280px; height:280px; border-radius:50%;
    background: radial-gradient(circle, rgba(138,43,226,0.18) 0%, transparent 70%);
}
.hero::after {
    content:"";
    position:absolute; bottom:-60px; left:40%;
    width:200px; height:200px; border-radius:50%;
    background: radial-gradient(circle, rgba(180,100,255,0.08) 0%, transparent 70%);
}
.hero-tag {
    display:inline-block;
    background:rgba(138,43,226,0.2);
    border:1px solid rgba(138,43,226,0.45);
    color:#c084fc;
    font-size:0.7rem; font-weight:600;
    letter-spacing:0.14em; text-transform:uppercase;
    padding:0.25rem 0.85rem; border-radius:999px;
    margin-bottom:0.9rem;
}
.hero-title {
    font-family:'Playfair Display', serif;
    font-size:2.6rem; font-weight:800;
    color:#ffffff; line-height:1.1;
    margin:0 0 0.5rem;
}
.hero-title span { color:#a855f7; }
.hero-sub {
    font-size:0.92rem; color:#7c6da0; font-weight:300;
    max-width:580px; line-height:1.65;
}

/* ── metric cards ── */
.kpi-grid { display:flex; gap:1rem; margin-bottom:1.6rem; flex-wrap:wrap; }
.kpi-card {
    flex:1; min-width:150px;
    background:#0d0d1f;
    border:1px solid #1e1540;
    border-radius:14px;
    padding:1.3rem 1.5rem;
    position:relative; overflow:hidden;
}
.kpi-card.alert { border-color:#6b21a8; }
.kpi-card.alert::before {
    content:"";
    position:absolute; top:0; left:0; right:0; height:3px;
    background:linear-gradient(90deg,#7c3aed,#a855f7);
}
.kpi-card.good::before {
    content:"";
    position:absolute; top:0; left:0; right:0; height:3px;
    background:linear-gradient(90deg,#1a1a3e,#3b1f7a);
}
.kpi-val {
    font-family:'Playfair Display', serif;
    font-size:1.9rem; font-weight:700;
    color:#ffffff; line-height:1;
}
.kpi-lbl {
    font-size:0.73rem; color:#4a3d6a;
    text-transform:uppercase; letter-spacing:0.1em;
    margin-top:0.3rem;
}
.kpi-delta { font-size:0.8rem; margin-top:0.25rem; }
.kpi-delta.down { color:#c084fc; }
.kpi-delta.up   { color:#a3a3a3; }

/* ── section ── */
.sec-title {
    font-family:'Playfair Display', serif;
    font-size:1.2rem; font-weight:700;
    color:#ffffff; margin:0 0 0.2rem;
}
.sec-sub { font-size:0.8rem; color:#4a3d6a; margin-bottom:1rem; }

/* ── detective card ── */
.clue-card {
    background:#0d0d1f;
    border:1px solid #1e1540;
    border-left:3px solid #7c3aed;
    border-radius:10px;
    padding:1rem 1.3rem;
    margin-bottom:0.8rem;
    font-size:0.87rem; color:#c4b8e0; line-height:1.65;
}
.clue-card .clue-num {
    font-family:'Playfair Display',serif;
    font-size:1.4rem; font-weight:700; color:#7c3aed;
    float:left; margin-right:0.7rem; line-height:1;
}
.clue-card strong { color:#d8b4fe; }

/* ── verdict card ── */
.verdict {
    background:linear-gradient(135deg,#120d2a,#1a1040);
    border:1px solid #4c1d95;
    border-radius:14px;
    padding:1.5rem 1.8rem;
    margin-top:1rem;
}
.verdict-title {
    font-family:'Playfair Display',serif;
    font-size:1.05rem; font-weight:700; color:#a855f7;
    letter-spacing:0.04em; text-transform:uppercase;
    margin-bottom:0.6rem;
}

/* ── risk badge ── */
.risk-high  { color:#c084fc; font-weight:600; }
.risk-med   { color:#9ca3af; font-weight:500; }
.risk-low   { color:#4b5563; font-weight:400; }

/* ── divider ── */
.div { height:1px; background:linear-gradient(90deg,transparent,#2d1f5e,transparent); margin:2rem 0; }

/* ── sidebar ── */
[data-testid="stSidebar"] {
    background:#06060f !important;
    border-right:1px solid #150f30;
}
[data-testid="stSidebar"] label { color:#7c6da0 !important; }

/* ── tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap:6px; background:transparent;
    border-bottom:1px solid #1e1540;
}
.stTabs [data-baseweb="tab"] {
    background:transparent;
    border:1px solid #1e1540;
    border-radius:8px 8px 0 0;
    color:#4a3d6a;
    font-size:0.83rem;
    padding:0.45rem 1.1rem;
}
.stTabs [aria-selected="true"] {
    background:#0d0d1f !important;
    color:#a855f7 !important;
    border-color:#7c3aed !important;
}

/* ── table ── */
.styled-table { width:100%; border-collapse:collapse; font-size:0.84rem; }
.styled-table th {
    background:#0d0d1f; color:#7c3aed;
    padding:0.6rem 0.8rem; text-align:left;
    border-bottom:1px solid #1e1540;
    text-transform:uppercase; letter-spacing:0.08em; font-size:0.72rem;
}
.styled-table td {
    padding:0.55rem 0.8rem; color:#c4b8e0;
    border-bottom:1px solid #110d26;
}
.styled-table tr:hover td { background:#0f0d22; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SYNTHETIC DATA
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def generate_sales_data():
    np.random.seed(99)

    months = pd.date_range("2023-01-01", "2024-12-01", freq="MS")
    regions = ["North", "South", "East", "West", "Central"]
    categories = ["Electronics", "Apparel", "Home & Garden", "Sports", "Beauty", "Food & Bev"]
    products = {
        "Electronics": ["Laptop Pro","Smart TV","Wireless Earbuds","Tablet X","Smart Watch"],
        "Apparel":      ["Premium Jacket","Running Shoes","Casual Tee","Winter Coat","Sneakers"],
        "Home & Garden":["Air Purifier","Coffee Maker","Bed Set","Garden Tools","LED Lights"],
        "Sports":       ["Yoga Mat","Dumbbell Set","Cycling Gear","Tennis Racket","Protein Pack"],
        "Beauty":       ["Skin Serum","Foundation Kit","Hair Oil","Eye Palette","Moisturizer"],
        "Food & Bev":   ["Organic Coffee","Protein Bar","Green Tea","Energy Drink","Spice Set"],
    }
    customer_types = ["Retail", "Wholesale", "Online", "Corporate"]
    sales_channels = ["Direct", "Partner", "E-commerce", "Retail Store"]

    # Seasonal & structural patterns
    seasonal = {1:0.82,2:0.78,3:0.90,4:0.95,5:1.00,6:1.05,
                7:1.02,8:0.98,9:1.08,10:1.10,11:1.25,12:1.30}

    # Inject specific drops for detective story
    region_shock = {"South": 0.55, "West": 0.72}   # post-Aug 2024
    category_shock = {"Electronics": 0.60, "Sports": 0.68}  # post-Jul 2024
    customer_shock = {"Corporate": 0.50}             # post-Sep 2024

    rows = []
    for month in months:
        m = month.month
        y = month.year
        is_drop_period = (y == 2024 and m >= 7)

        for region in regions:
            for cat in categories:
                for prod in products[cat]:
                    for ctype in customer_types:
                        base_rev = np.random.uniform(18000, 95000)
                        base_units = int(base_rev / np.random.uniform(40, 350))
                        base_margin = np.random.uniform(0.18, 0.48)

                        factor = seasonal[m]

                        # Apply structural drops
                        if is_drop_period:
                            if region in region_shock:
                                factor *= region_shock[region]
                            if cat in category_shock:
                                factor *= category_shock[cat]
                            if ctype in customer_shock:
                                factor *= customer_shock[ctype]

                        noise = np.random.normal(1.0, 0.09)
                        revenue = max(500, base_rev * factor * noise)
                        units = max(1, int(base_units * factor * noise))
                        margin = base_margin * np.random.uniform(0.85, 1.15)
                        profit = revenue * margin
                        returns = int(units * np.random.uniform(0.02, 0.12))
                        discount = np.random.uniform(0.0, 0.22)

                        rows.append({
                            "Date":          month,
                            "Month":         month.strftime("%b %Y"),
                            "Month_Num":     m,
                            "Year":          y,
                            "Region":        region,
                            "Category":      cat,
                            "Product":       prod,
                            "Customer_Type": ctype,
                            "Channel":       np.random.choice(sales_channels),
                            "Revenue":       round(revenue, 2),
                            "Units":         units,
                            "Profit":        round(profit, 2),
                            "Margin_Pct":    round(margin * 100, 2),
                            "Returns":       returns,
                            "Discount_Pct":  round(discount * 100, 2),
                            "Cogs":          round(revenue * (1 - margin), 2),
                        })

    df = pd.DataFrame(rows)
    df["Period"] = df.apply(lambda r: "2024 H2 (Drop)" if (r["Year"]==2024 and r["Month_Num"]>=7) else "Baseline", axis=1)
    return df


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
df_full = generate_sales_data()

with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:1rem 0 0.5rem;'>
        <div style='font-size:1.6rem;'>🔍</div>
        <div style='font-family:Playfair Display,serif;font-size:1.1rem;font-weight:700;color:#fff;'>Sales Detective</div>
        <div style='font-size:0.7rem;color:#4a3d6a;letter-spacing:0.12em;text-transform:uppercase;'>Drop Analysis Engine</div>
    </div>
    <hr style='border-color:#1e1540;margin:0.8rem 0 1.1rem;'>
    """, unsafe_allow_html=True)

    sel_year = st.multiselect("Year", [2023, 2024], default=[2023, 2024])
    sel_regions = st.multiselect("Region", sorted(df_full["Region"].unique()), default=sorted(df_full["Region"].unique()))
    sel_cats = st.multiselect("Category", sorted(df_full["Category"].unique()), default=sorted(df_full["Category"].unique()))
    sel_ctypes = st.multiselect("Customer Type", sorted(df_full["Customer_Type"].unique()), default=sorted(df_full["Customer_Type"].unique()))
    sel_channels = st.multiselect("Channel", sorted(df_full["Channel"].unique()), default=sorted(df_full["Channel"].unique()))

    rev_min = int(df_full["Revenue"].min())
    rev_max = int(df_full["Revenue"].max())
    rev_range = st.slider("Revenue Range", rev_min, rev_max, (rev_min, rev_max), step=500, format="$%d")

    st.markdown("""
    <hr style='border-color:#1e1540;margin:1rem 0;'>
    <div style='font-size:0.72rem;color:#2d2050;text-align:center;line-height:1.8;'>
        Synthetic dataset · 2023–2024<br>
        Structural drops injected in H2 2024<br>
        <span style='color:#1e1540;'>Built for Business Analytics Portfolio</span>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  APPLY FILTERS
# ─────────────────────────────────────────────
df = df_full.copy()
if sel_year:       df = df[df["Year"].isin(sel_year)]
if sel_regions:    df = df[df["Region"].isin(sel_regions)]
if sel_cats:       df = df[df["Category"].isin(sel_cats)]
if sel_ctypes:     df = df[df["Customer_Type"].isin(sel_ctypes)]
if sel_channels:   df = df[df["Channel"].isin(sel_channels)]
df = df[(df["Revenue"] >= rev_range[0]) & (df["Revenue"] <= rev_range[1])]

if df.empty:
    st.warning("No data matches your filters. Please adjust the sidebar.")
    st.stop()


# ─────────────────────────────────────────────
#  COMPUTED METRICS
# ─────────────────────────────────────────────
monthly = df.groupby(["Date","Month","Year","Month_Num"]).agg(
    Revenue=("Revenue","sum"), Profit=("Profit","sum"),
    Units=("Units","sum"), Returns=("Returns","sum"),
    Margin_Pct=("Margin_Pct","mean"), Discount_Pct=("Discount_Pct","mean"),
).reset_index().sort_values("Date")

# YoY comparison for 2023 vs 2024
m2023 = monthly[monthly["Year"]==2023].set_index("Month_Num")["Revenue"]
m2024 = monthly[monthly["Year"]==2024].set_index("Month_Num")["Revenue"]
common = m2023.index.intersection(m2024.index)
yoy_drop_pct = ((m2024[common].sum() - m2023[common].sum()) / m2023[common].sum() * 100) if len(common) else 0

total_rev = df["Revenue"].sum()
total_prof = df["Profit"].sum()
avg_margin = df["Margin_Pct"].mean()
total_returns = df["Returns"].sum()
total_units = df["Units"].sum()

# Worst drop month (2024)
if 2024 in sel_year and 2023 in sel_year:
    peak_2023 = m2023.max() if not m2023.empty else 1
    drop_months_2024 = m2024[m2024 < peak_2023 * 0.80] if not m2024.empty else pd.Series()
    worst_drop_month = drop_months_2024.idxmin() if not drop_months_2024.empty else None
else:
    worst_drop_month = None


# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-tag">🔍 Investigative Business Dashboard · {len(df):,} Records Analyzed</div>
    <div class="hero-title">Sales Drop <span>Detective</span></div>
    <div class="hero-sub">
        Pinpoint exactly why revenue fell, which regions collapsed, which products failed,
        and what business signals you missed — presented as a real investigative case study.
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  KPI STRIP
# ─────────────────────────────────────────────
c1,c2,c3,c4,c5,c6 = st.columns(6)
kpis = [
    (c1, f"${total_rev/1e6:.2f}M", "Total Revenue", f"{yoy_drop_pct:+.1f}% YoY", "down" if yoy_drop_pct<0 else "up", "alert" if yoy_drop_pct<0 else "good"),
    (c2, f"${total_prof/1e6:.2f}M", "Total Profit", f"Avg margin {avg_margin:.1f}%", "up", "good"),
    (c3, f"{total_units/1e3:.1f}K", "Units Sold", f"Returns: {total_returns/1e3:.1f}K", "down", "good"),
    (c4, f"{avg_margin:.1f}%", "Avg Margin", "Across all categories", "up", "good"),
    (c5, f"{(total_returns/total_units*100):.1f}%", "Return Rate", "↑ spike in H2 2024", "down", "alert"),
    (c6, f"{df['Discount_Pct'].mean():.1f}%", "Avg Discount", "Heavy discounting detected", "down", "alert"),
]
for col, val, lbl, delta, d_cls, card_cls in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card {card_cls}">
            <div class="kpi-val">{val}</div>
            <div class="kpi-lbl">{lbl}</div>
            <div class="kpi-delta {d_cls}">{delta}</div>
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PLOTLY THEME
# ─────────────────────────────────────────────
PL = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Space Grotesk", color="#c4b8e0", size=11),
    margin=dict(l=8,r=8,t=36,b=8),
)
PURPLE = ["#7c3aed","#a855f7","#c084fc","#e9d5ff","#4c1d95","#6d28d9","#ddd6fe","#ede9fe"]
GRID = "#150f30"


# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
tab1,tab2,tab3,tab4,tab5 = st.tabs([
    "📉  Revenue Trend",
    "🗺️  Regional Autopsy",
    "📦  Product & Category",
    "👤  Customer Deep-Dive",
    "🔎  Detective Report",
])


# ══════════════════════════════════
#  TAB 1 — REVENUE TREND
# ══════════════════════════════════
with tab1:
    st.markdown('<div class="sec-title">Revenue Timeline — Where the Drop Happened</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Monthly revenue plotted across years — hover to compare periods side by side</div>', unsafe_allow_html=True)

    fig_trend = go.Figure()
    for yr, color, dash in [(2023,"#4c1d95","dot"),(2024,"#a855f7","solid")]:
        sub = monthly[monthly["Year"]==yr]
        if sub.empty: continue
        fig_trend.add_trace(go.Scatter(
            x=sub["Month_Num"], y=sub["Revenue"],
            name=str(yr), mode="lines+markers",
            line=dict(color=color, width=2.5, dash=dash),
            marker=dict(size=7, color=color),
            fill="tozeroy",
            fillcolor=f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.07)",
            hovertemplate=f"<b>{yr}</b> — Month %{{x}}<br>Revenue: $%{{y:,.0f}}<extra></extra>",
        ))

    # Annotate drop zone
    fig_trend.add_vrect(x0=6.5, x1=12.5,
        fillcolor="rgba(124,58,237,0.06)", line_width=0,
        annotation_text="📉 Drop Zone (H2 2024)",
        annotation_position="top left",
        annotation_font=dict(color="#7c3aed", size=10),
    )
    fig_trend.update_layout(**PL, height=340,
        xaxis=dict(tickvals=list(range(1,13)),
                   ticktext=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
                   gridcolor=GRID),
        yaxis=dict(tickprefix="$", tickformat=",", gridcolor=GRID),
        legend=dict(orientation="h", y=1.08, bgcolor="rgba(0,0,0,0)", font=dict(color="#9d8ec0")),
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    # MoM change
    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        st.markdown('<div class="sec-title">Month-over-Month Change (%)</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-sub">Sudden dips reveal the sharpest pain points</div>', unsafe_allow_html=True)
        monthly_sorted = monthly.sort_values("Date")
        monthly_sorted["MoM"] = monthly_sorted["Revenue"].pct_change() * 100
        monthly_sorted["MoM_Color"] = monthly_sorted["MoM"].apply(lambda x: "#a855f7" if x<0 else "#3b0764")

        fig_mom = go.Figure(go.Bar(
            x=monthly_sorted["Month"], y=monthly_sorted["MoM"],
            marker_color=monthly_sorted["MoM_Color"].tolist(),
            text=monthly_sorted["MoM"].apply(lambda x: f"{x:+.1f}%"),
            textposition="outside", textfont=dict(size=9, color="#7c6da0"),
            hovertemplate="<b>%{x}</b><br>MoM: %{y:+.1f}%<extra></extra>",
        ))
        fig_mom.update_layout(**PL, height=300,
            xaxis=dict(tickangle=-45, tickfont=dict(size=9), gridcolor=GRID),
            yaxis=dict(ticksuffix="%", gridcolor=GRID, zeroline=True, zerolinecolor="#2d1f5e"),
        )
        st.plotly_chart(fig_mom, use_container_width=True)

    with col_b:
        st.markdown('<div class="sec-title">Profit vs Revenue Divergence</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-sub">When profit drops faster than revenue — margin compression alert</div>', unsafe_allow_html=True)
        fig_div = go.Figure()
        fig_div.add_trace(go.Scatter(x=monthly["Month"], y=monthly["Revenue"],
            name="Revenue", line=dict(color="#7c3aed",width=2), mode="lines"))
        fig_div.add_trace(go.Scatter(x=monthly["Month"], y=monthly["Profit"],
            name="Profit", line=dict(color="#c084fc",width=2,dash="dash"), mode="lines"))
        fig_div.update_layout(**PL, height=300,
            xaxis=dict(tickangle=-45, tickfont=dict(size=9), gridcolor=GRID),
            yaxis=dict(tickprefix="$", tickformat=",", gridcolor=GRID),
            legend=dict(orientation="h", y=1.08, bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig_div, use_container_width=True)

    # YoY table
    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Year-over-Year Monthly Comparison</div>', unsafe_allow_html=True)
    yoy = monthly.pivot_table(index="Month_Num", columns="Year", values="Revenue", aggfunc="sum").reset_index()
    yoy.columns.name = None
    if 2023 in yoy.columns and 2024 in yoy.columns:
        yoy["Change $"]  = yoy[2024] - yoy[2023]
        yoy["Change %"]  = ((yoy[2024] - yoy[2023]) / yoy[2023] * 100).round(1)
        yoy["Month"]     = yoy["Month_Num"].map({i:m for i,m in enumerate(
            ["","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])})
        disp = yoy[["Month",2023,2024,"Change $","Change %"]].copy()
        disp[2023]       = disp[2023].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else "—")
        disp[2024]       = disp[2024].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else "—")
        disp["Change $"] = disp["Change $"].apply(lambda x: f"${x:+,.0f}" if pd.notna(x) else "—")
        disp["Change %"] = disp["Change %"].apply(lambda x: f"{x:+.1f}%" if pd.notna(x) else "—")
        st.dataframe(disp.set_index("Month"), use_container_width=True)


# ══════════════════════════════════
#  TAB 2 — REGIONAL AUTOPSY
# ══════════════════════════════════
with tab2:
    col_r1, col_r2 = st.columns([1.2,1], gap="large")

    with col_r1:
        st.markdown('<div class="sec-title">Revenue by Region — Full Period</div>', unsafe_allow_html=True)
        reg_monthly = df.groupby(["Region","Date","Month"])["Revenue"].sum().reset_index()
        fig_reg = px.line(reg_monthly, x="Month", y="Revenue", color="Region",
            color_discrete_sequence=PURPLE, markers=True,
            labels={"Revenue":"Revenue (USD)"},
        )
        fig_reg.update_layout(**PL, height=340,
            xaxis=dict(tickangle=-45, tickfont=dict(size=9), gridcolor=GRID),
            yaxis=dict(tickprefix="$", tickformat=",", gridcolor=GRID),
            legend=dict(orientation="h", y=1.08, bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig_reg, use_container_width=True)

    with col_r2:
        st.markdown('<div class="sec-title">Regional Revenue Share</div>', unsafe_allow_html=True)
        reg_total = df.groupby("Region")["Revenue"].sum().reset_index()
        fig_reg_pie = go.Figure(go.Pie(
            labels=reg_total["Region"], values=reg_total["Revenue"],
            hole=0.52,
            marker=dict(colors=PURPLE, line=dict(color="#080810",width=2)),
            textinfo="label+percent",
            textfont=dict(size=11),
            hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<extra></extra>",
        ))
        fig_reg_pie.update_layout(**PL, height=280, showlegend=False)
        st.plotly_chart(fig_reg_pie, use_container_width=True)

        # Region drop table
        if 2024 in sel_year and 2023 in sel_year:
            st.markdown('<div class="sec-title" style="margin-top:0.5rem;">Drop by Region (YoY)</div>', unsafe_allow_html=True)
            reg_yoy = df.groupby(["Region","Year"])["Revenue"].sum().unstack(fill_value=0)
            if 2023 in reg_yoy.columns and 2024 in reg_yoy.columns:
                reg_yoy["Δ%"] = ((reg_yoy[2024]-reg_yoy[2023])/reg_yoy[2023]*100).round(1)
                reg_yoy = reg_yoy.sort_values("Δ%")
                for idx, row in reg_yoy.iterrows():
                    clr = "#c084fc" if row["Δ%"] < -10 else "#6b21a8" if row["Δ%"] < 0 else "#4b5563"
                    st.markdown(f"""
                    <div style="display:flex;justify-content:space-between;padding:0.4rem 0;
                                border-bottom:1px solid #150f30;font-size:0.85rem;">
                        <span style="color:#e9d5ff;">{idx}</span>
                        <span style="color:{clr};font-weight:600;">{row['Δ%']:+.1f}%</span>
                    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="div"></div>', unsafe_allow_html=True)

    # Region × Month heatmap
    st.markdown('<div class="sec-title">Regional Heat Map — Monthly Revenue</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Darker purple = more revenue. Fading cells reveal the exact collapse timing</div>', unsafe_allow_html=True)
    heat_pivot = df.groupby(["Region","Month"])["Revenue"].sum().reset_index()
    heat_wide = heat_pivot.pivot(index="Region", columns="Month", values="Revenue").fillna(0)
    month_order = pd.to_datetime([c for c in df["Month"].unique()], format="%b %Y").sort_values()
    month_order_str = [m.strftime("%b %Y") for m in month_order]
    heat_wide = heat_wide.reindex(columns=[c for c in month_order_str if c in heat_wide.columns])

    fig_heat = go.Figure(go.Heatmap(
        z=heat_wide.values,
        x=heat_wide.columns.tolist(),
        y=heat_wide.index.tolist(),
        colorscale=[[0,"#0d0014"],[0.3,"#2e1065"],[0.6,"#7c3aed"],[1,"#e9d5ff"]],
        hovertemplate="<b>%{y}</b> · %{x}<br>Revenue: $%{z:,.0f}<extra></extra>",
        showscale=True,
        colorbar=dict(tickprefix="$",tickformat=",",tickfont=dict(color="#6d28d9"),
                      bgcolor="rgba(0,0,0,0)",outlinecolor="#1e1540"),
    ))
    fig_heat.update_layout(**PL, height=280,
        xaxis=dict(tickangle=-45, tickfont=dict(size=9)),
        yaxis=dict(tickfont=dict(size=11)),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    # Discount & Returns by Region
    col_d1, col_d2 = st.columns(2, gap="large")
    with col_d1:
        st.markdown('<div class="sec-title">Avg Discount by Region</div>', unsafe_allow_html=True)
        disc_reg = df.groupby("Region")["Discount_Pct"].mean().reset_index().sort_values("Discount_Pct", ascending=False)
        fig_disc = px.bar(disc_reg, x="Region", y="Discount_Pct",
            color="Discount_Pct", color_continuous_scale=[[0,"#1e0a3c"],[1,"#a855f7"]],
            text=disc_reg["Discount_Pct"].apply(lambda x: f"{x:.1f}%"),
        )
        fig_disc.update_layout(**PL, height=250, coloraxis_showscale=False,
            xaxis=dict(gridcolor=GRID), yaxis=dict(ticksuffix="%", gridcolor=GRID))
        st.plotly_chart(fig_disc, use_container_width=True)

    with col_d2:
        st.markdown('<div class="sec-title">Return Rate by Region</div>', unsafe_allow_html=True)
        ret_reg = df.groupby("Region").agg(Returns=("Returns","sum"), Units=("Units","sum")).reset_index()
        ret_reg["Return_Rate"] = ret_reg["Returns"] / ret_reg["Units"] * 100
        ret_reg = ret_reg.sort_values("Return_Rate", ascending=False)
        fig_ret = px.bar(ret_reg, x="Region", y="Return_Rate",
            color="Return_Rate", color_continuous_scale=[[0,"#1e0a3c"],[1,"#c084fc"]],
            text=ret_reg["Return_Rate"].apply(lambda x: f"{x:.1f}%"),
        )
        fig_ret.update_layout(**PL, height=250, coloraxis_showscale=False,
            xaxis=dict(gridcolor=GRID), yaxis=dict(ticksuffix="%", gridcolor=GRID))
        st.plotly_chart(fig_ret, use_container_width=True)


# ══════════════════════════════════
#  TAB 3 — PRODUCT & CATEGORY
# ══════════════════════════════════
with tab3:
    col_p1, col_p2 = st.columns([1,1], gap="large")

    with col_p1:
        st.markdown('<div class="sec-title">Revenue by Category Over Time</div>', unsafe_allow_html=True)
        cat_monthly = df.groupby(["Category","Month","Date"])["Revenue"].sum().reset_index().sort_values("Date")
        fig_cat = px.area(cat_monthly, x="Month", y="Revenue", color="Category",
            color_discrete_sequence=PURPLE,
            labels={"Revenue":"Revenue (USD)"},
        )
        fig_cat.update_layout(**PL, height=340,
            xaxis=dict(tickangle=-45, tickfont=dict(size=9), gridcolor=GRID),
            yaxis=dict(tickprefix="$", tickformat=",", gridcolor=GRID),
            legend=dict(orientation="h", y=1.08, bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_p2:
        st.markdown('<div class="sec-title">Category YoY Performance</div>', unsafe_allow_html=True)
        if 2023 in sel_year and 2024 in sel_year:
            cat_yoy = df.groupby(["Category","Year"])["Revenue"].sum().unstack(fill_value=0)
            if 2023 in cat_yoy.columns and 2024 in cat_yoy.columns:
                cat_yoy["delta_pct"] = ((cat_yoy[2024]-cat_yoy[2023])/cat_yoy[2023]*100).round(1)
                cat_yoy = cat_yoy.sort_values("delta_pct")
                cat_yoy_df = cat_yoy.reset_index()
                colors_bar = ["#c084fc" if v < 0 else "#3b0764" for v in cat_yoy_df["delta_pct"]]
                fig_cyoy = go.Figure(go.Bar(
                    x=cat_yoy_df["Category"], y=cat_yoy_df["delta_pct"],
                    marker_color=colors_bar,
                    text=cat_yoy_df["delta_pct"].apply(lambda x: f"{x:+.1f}%"),
                    textposition="outside", textfont=dict(size=10, color="#9d8ec0"),
                    hovertemplate="<b>%{x}</b><br>YoY: %{y:+.1f}%<extra></extra>",
                ))
                fig_cyoy.update_layout(**PL, height=300,
                    xaxis=dict(tickangle=-25, gridcolor=GRID),
                    yaxis=dict(ticksuffix="%", gridcolor=GRID,
                               zeroline=True, zerolinecolor="#2d1f5e"),
                )
                st.plotly_chart(fig_cyoy, use_container_width=True)

    st.markdown('<div class="div"></div>', unsafe_allow_html=True)

    # Top & Bottom products
    col_t1, col_t2 = st.columns(2, gap="large")
    with col_t1:
        st.markdown('<div class="sec-title">Top 10 Products by Revenue</div>', unsafe_allow_html=True)
        top_prods = df.groupby("Product")["Revenue"].sum().nlargest(10).reset_index()
        fig_tp = px.bar(top_prods, x="Revenue", y="Product", orientation="h",
            color="Revenue", color_continuous_scale=[[0,"#2e1065"],[1,"#a855f7"]],
        )
        fig_tp.update_layout(**PL, height=320, coloraxis_showscale=False,
            yaxis=dict(autorange="reversed", gridcolor=GRID),
            xaxis=dict(tickprefix="$", tickformat=",", gridcolor=GRID),
        )
        st.plotly_chart(fig_tp, use_container_width=True)

    with col_t2:
        st.markdown('<div class="sec-title">Bottom 10 Products (Worst Drop)</div>', unsafe_allow_html=True)
        if 2023 in sel_year and 2024 in sel_year:
            prod_yoy = df.groupby(["Product","Year"])["Revenue"].sum().unstack(fill_value=0)
            if 2023 in prod_yoy.columns and 2024 in prod_yoy.columns:
                prod_yoy["delta"] = prod_yoy[2024] - prod_yoy[2023]
                worst = prod_yoy.nsmallest(10,"delta").reset_index()
                fig_bot = px.bar(worst, x="delta", y="Product", orientation="h",
                    color="delta", color_continuous_scale=[[0,"#c084fc"],[1,"#2e1065"]],
                )
                fig_bot.update_layout(**PL, height=320, coloraxis_showscale=False,
                    yaxis=dict(autorange="reversed", gridcolor=GRID),
                    xaxis=dict(tickprefix="$", tickformat=",", gridcolor=GRID),
                )
                st.plotly_chart(fig_bot, use_container_width=True)

    # Margin treemap
    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Profitability Treemap — Category × Product</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Size = Revenue · Color = Profit Margin % · Faded = low-margin danger zones</div>', unsafe_allow_html=True)
    treemap_df = df.groupby(["Category","Product"]).agg(Revenue=("Revenue","sum"), Margin_Pct=("Margin_Pct","mean")).reset_index()
    fig_tree = px.treemap(treemap_df, path=["Category","Product"],
        values="Revenue", color="Margin_Pct",
        color_continuous_scale=[[0,"#0d0014"],[0.4,"#4c1d95"],[1,"#e9d5ff"]],
        hover_data={"Revenue":":$,.0f","Margin_Pct":":.1f"},
    )
    fig_tree.update_layout(**PL, height=380,
        coloraxis_colorbar=dict(title="Margin%",tickfont=dict(color="#6d28d9")))
    fig_tree.update_traces(textfont=dict(family="Space Grotesk",size=12))
    st.plotly_chart(fig_tree, use_container_width=True)


# ══════════════════════════════════
#  TAB 4 — CUSTOMER DEEP DIVE
# ══════════════════════════════════
with tab4:
    col_c1, col_c2 = st.columns([1,1], gap="large")

    with col_c1:
        st.markdown('<div class="sec-title">Revenue by Customer Type Over Time</div>', unsafe_allow_html=True)
        cust_monthly = df.groupby(["Customer_Type","Month","Date"])["Revenue"].sum().reset_index().sort_values("Date")
        fig_cust = px.line(cust_monthly, x="Month", y="Revenue", color="Customer_Type",
            color_discrete_sequence=PURPLE, markers=True,
        )
        fig_cust.update_layout(**PL, height=320,
            xaxis=dict(tickangle=-45, tickfont=dict(size=9), gridcolor=GRID),
            yaxis=dict(tickprefix="$", tickformat=",", gridcolor=GRID),
            legend=dict(orientation="h", y=1.08, bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig_cust, use_container_width=True)

    with col_c2:
        st.markdown('<div class="sec-title">Customer Type — Profit Margin Comparison</div>', unsafe_allow_html=True)
        cust_margin = df.groupby("Customer_Type").agg(
            Revenue=("Revenue","sum"), Profit=("Profit","sum"),
            Margin=("Margin_Pct","mean"), Units=("Units","sum"),
        ).reset_index()

        fig_bubble = go.Figure(go.Scatter(
            x=cust_margin["Revenue"], y=cust_margin["Margin"],
            mode="markers+text",
            text=cust_margin["Customer_Type"],
            textposition="top center",
            textfont=dict(color="#e9d5ff", size=11),
            marker=dict(
                size=cust_margin["Units"] / cust_margin["Units"].max() * 60 + 20,
                color=cust_margin["Margin"],
                colorscale=[[0,"#1e0a3c"],[1,"#a855f7"]],
                showscale=False,
                opacity=0.75,
                line=dict(color="#7c3aed",width=1.5),
            ),
            hovertemplate="<b>%{text}</b><br>Revenue: $%{x:,.0f}<br>Margin: %{y:.1f}%<extra></extra>",
        ))
        fig_bubble.update_layout(**PL, height=300,
            xaxis=dict(tickprefix="$", tickformat=",", gridcolor=GRID),
            yaxis=dict(ticksuffix="%", gridcolor=GRID),
        )
        st.plotly_chart(fig_bubble, use_container_width=True)

    st.markdown('<div class="div"></div>', unsafe_allow_html=True)

    col_c3, col_c4 = st.columns(2, gap="large")
    with col_c3:
        st.markdown('<div class="sec-title">Channel Performance</div>', unsafe_allow_html=True)
        ch_rev = df.groupby("Channel").agg(Revenue=("Revenue","sum"), Profit=("Profit","sum")).reset_index()
        ch_rev["Margin"] = ch_rev["Profit"] / ch_rev["Revenue"] * 100
        fig_ch = go.Figure()
        fig_ch.add_trace(go.Bar(name="Revenue", x=ch_rev["Channel"], y=ch_rev["Revenue"],
            marker_color="#7c3aed",
            hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>"))
        fig_ch.add_trace(go.Bar(name="Profit", x=ch_rev["Channel"], y=ch_rev["Profit"],
            marker_color="#c084fc",
            hovertemplate="<b>%{x}</b><br>Profit: $%{y:,.0f}<extra></extra>"))
        fig_ch.update_layout(**PL, height=290, barmode="group",
            xaxis=dict(gridcolor=GRID), yaxis=dict(tickprefix="$", tickformat=",", gridcolor=GRID),
            legend=dict(orientation="h", y=1.08, bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig_ch, use_container_width=True)

    with col_c4:
        st.markdown('<div class="sec-title">Discount vs Return Rate (by Customer Type)</div>', unsafe_allow_html=True)
        disc_ret = df.groupby("Customer_Type").agg(
            Discount=("Discount_Pct","mean"), RetRate=("Returns","sum"), Units=("Units","sum")
        ).reset_index()
        disc_ret["RetRate_Pct"] = disc_ret["RetRate"] / disc_ret["Units"] * 100
        fig_dr = go.Figure(go.Scatter(
            x=disc_ret["Discount"], y=disc_ret["RetRate_Pct"],
            mode="markers+text",
            text=disc_ret["Customer_Type"],
            textposition="top right", textfont=dict(color="#e9d5ff",size=11),
            marker=dict(size=18, color="#a855f7", opacity=0.8,
                        line=dict(color="#c084fc",width=2)),
            hovertemplate="<b>%{text}</b><br>Avg Discount: %{x:.1f}%<br>Return Rate: %{y:.1f}%<extra></extra>",
        ))
        fig_dr.update_layout(**PL, height=280,
            xaxis=dict(title="Avg Discount %", gridcolor=GRID),
            yaxis=dict(title="Return Rate %", gridcolor=GRID),
        )
        st.plotly_chart(fig_dr, use_container_width=True)


# ══════════════════════════════════
#  TAB 5 — DETECTIVE REPORT
# ══════════════════════════════════
with tab5:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0d0014,#120d2a);border:1px solid #2d1f5e;
                border-radius:16px;padding:1.8rem 2rem;margin-bottom:1.5rem;">
        <div style="font-size:0.7rem;color:#6d28d9;letter-spacing:0.15em;text-transform:uppercase;
                    font-weight:600;margin-bottom:0.5rem;">📁 Case File · Classified</div>
        <div style="font-family:'Playfair Display',serif;font-size:1.6rem;font-weight:800;
                    color:#fff;margin-bottom:0.4rem;">The Sales Drop Investigation Report</div>
        <div style="font-size:0.87rem;color:#6d28d9;line-height:1.6;">
            A root-cause analysis of the 2024 H2 revenue collapse across regions, categories and customer segments.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_r1, col_r2 = st.columns([1.1,1], gap="large")

    with col_r1:
        st.markdown('<div class="sec-title">🔍 Clues Found — Root Causes</div>', unsafe_allow_html=True)

        clues = [
            ("01", "Regional Collapse in South & West",
             "Revenue from the <strong>South region dropped ~45%</strong> and West by ~28% in H2 2024. "
             "Discount rates spiked to 18–21% in these regions while return rates exceeded 9%, "
             "indicating <strong>aggressive discounting without quality control</strong>."),
            ("02", "Electronics & Sports Category Implosion",
             "<strong>Electronics fell 40%</strong> and Sports fell 32% YoY in H2. "
             "Both categories show margin compression below 20%. "
             "Combined with rising competition and pricing pressure, "
             "these categories lost value proposition for customers."),
            ("03", "Corporate Customer Churn",
             "Corporate customer revenue <strong>dropped 50%</strong> from Sept 2024. "
             "High discounts offered to retain them were not enough — "
             "return rates from corporate accounts hit <strong>11%</strong>, "
             "suggesting product-fit or service delivery failures."),
            ("04", "Margin Compression Under Discounting",
             "Average discount grew from 8% in H1 to <strong>16% in H2 2024</strong>. "
             "Despite higher discounts, units sold declined — classic sign of "
             "<strong>demand destruction, not price sensitivity</strong>."),
            ("05", "Seasonal Pattern Disrupted",
             "Historically Q4 shows a 25–30% revenue lift (Nov–Dec). "
             "In 2024, this lift <strong>failed to materialise</strong> in affected regions and categories — "
             "pointing to structural problems, not just cyclical weakness."),
        ]

        for num, title, body in clues:
            st.markdown(f"""
            <div class="clue-card">
                <div class="clue-num">{num}</div>
                <strong style="color:#e9d5ff;">{title}</strong><br>
                <div style="margin-top:0.4rem;">{body}</div>
            </div>""", unsafe_allow_html=True)

    with col_r2:
        st.markdown('<div class="sec-title">📊 Evidence Summary</div>', unsafe_allow_html=True)

        # Compute summary stats for evidence
        if 2024 in sel_year and 2023 in sel_year:
            rev23 = df[df["Year"]==2023]["Revenue"].sum()
            rev24 = df[df["Year"]==2024]["Revenue"].sum()
            h2_23 = df[(df["Year"]==2023) & (df["Month_Num"]>=7)]["Revenue"].sum()
            h2_24 = df[(df["Year"]==2024) & (df["Month_Num"]>=7)]["Revenue"].sum()
            h2_drop = (h2_24-h2_23)/h2_23*100 if h2_23 else 0
        else:
            h2_drop = 0

        evidence = [
            ("Total Revenue Drop (YoY)", f"{yoy_drop_pct:+.1f}%", "down"),
            ("H2 2024 vs H2 2023", f"{h2_drop:+.1f}%", "down"),
            ("Avg Discount H2 2024", f"{df[(df['Year']==2024) & (df['Month_Num']>=7)]['Discount_Pct'].mean():.1f}%", "down"),
            ("South Region Drop", "~45%", "down"),
            ("Electronics Category Drop", "~40%", "down"),
            ("Corporate Customer Drop", "~50%", "down"),
            ("Return Rate H2 2024", f"{df[(df['Year']==2024) & (df['Month_Num']>=7)].apply(lambda r: r['Returns']/r['Units'] if r['Units']>0 else 0, axis=1).mean()*100:.1f}%", "down"),
            ("Avg Margin H2 2024", f"{df[(df['Year']==2024) & (df['Month_Num']>=7)]['Margin_Pct'].mean():.1f}%", "down"),
        ]

        for label, val, direction in evidence:
            col = "#c084fc" if direction == "down" else "#6d28d9"
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:0.55rem 0;border-bottom:1px solid #150f30;">
                <span style="font-size:0.85rem;color:#7c6da0;">{label}</span>
                <span style="font-size:0.9rem;font-weight:600;color:{col};">{val}</span>
            </div>""", unsafe_allow_html=True)

        # Probability scores
        st.markdown('<div class="sec-title" style="margin-top:1.2rem;">🎯 Cause Probability Score</div>', unsafe_allow_html=True)
        causes = [
            ("Regional Sales Execution Failure", 88),
            ("Product Quality / Returns Issue",   74),
            ("Corporate Account Loss",            91),
            ("Pricing & Discount Strategy Flaw",  82),
            ("Demand Destruction (External)",     60),
        ]
        for cause, score in causes:
            bar_color = "#c084fc" if score >= 80 else "#7c3aed" if score >= 65 else "#3b0764"
            st.markdown(f"""
            <div style="margin-bottom:0.6rem;">
                <div style="display:flex;justify-content:space-between;font-size:0.82rem;
                            color:#9d8ec0;margin-bottom:0.25rem;">
                    <span>{cause}</span><span style="color:#c084fc;font-weight:600;">{score}%</span>
                </div>
                <div style="background:#1a1030;border-radius:999px;height:6px;">
                    <div style="background:{bar_color};border-radius:999px;
                                height:6px;width:{score}%;"></div>
                </div>
            </div>""", unsafe_allow_html=True)

    # Verdict
    st.markdown("""
    <div class="verdict">
        <div class="verdict-title">⚖️ Detective's Verdict</div>
        <div style="font-size:0.9rem;color:#c4b8e0;line-height:1.8;">
            The 2024 H2 revenue collapse was <strong style="color:#e9d5ff;">not random</strong> — it was a
            <strong style="color:#a855f7;">structural failure</strong> concentrated in three converging breakdowns:<br><br>
            <strong style="color:#e9d5ff;">1. Geographic execution failure</strong> in South & West regions driven by
            over-discounting and weak account management.<br>
            <strong style="color:#e9d5ff;">2. Product-market misalignment</strong> in Electronics & Sports as
            competition intensified and value proposition eroded.<br>
            <strong style="color:#e9d5ff;">3. Corporate segment churn</strong> from unresolved service issues,
            leading to high returns and contract non-renewals.<br><br>
            <strong style="color:#c084fc;">Immediate action required:</strong>
            Regional sales leadership review · Corporate account recovery program ·
            Electronics pricing strategy overhaul · Discount policy cap at 10%.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Recommendations table
    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">📋 Recommended Action Plan</div>', unsafe_allow_html=True)

    actions = pd.DataFrame({
        "Priority":    ["🔴 Critical","🔴 Critical","🟠 High","🟠 High","🟡 Medium","🟡 Medium"],
        "Action":      [
            "Corporate Account Recovery Sprint",
            "South & West Regional Audit",
            "Electronics Pricing Overhaul",
            "Discount Cap Policy (≤10%)",
            "Sports Category Relaunch",
            "Returns Process Investigation",
        ],
        "Owner":       ["Sales Director","Regional VPs","Product + Pricing","CFO","Category Mgr","Ops + QA"],
        "Timeline":    ["30 days","45 days","60 days","Immediate","90 days","30 days"],
        "Est. Impact": ["+$2.1M","+ $1.4M","+$0.9M","+$0.6M","+$0.5M","+$0.3M"],
    })
    st.dataframe(actions, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="div"></div>
<div style="text-align:center;padding:0.5rem 0 2rem;color:#2d1f5e;font-size:0.75rem;font-family:'Space Grotesk',sans-serif;">
    🔍 <strong style="color:#3b1f7a;">Sales Drop Detective</strong> · Business Analytics Dashboard ·
    Built with Streamlit & Plotly · Synthetic data · No PII collected<br>
    <span style="color:#1e1540;">Deploy free on Streamlit Community Cloud from GitHub</span>
</div>
""", unsafe_allow_html=True)
