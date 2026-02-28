# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  JUSTICE BY THE NUMBERS — Karnataka High Court                          ║
# ║  A Lawgorithm Initiative  |  app.py  |  v2                              ║
# ╚══════════════════════════════════════════════════════════════════════════╝

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  BLOCK A — Page config, imports, CSS                                    ║
# ╚══════════════════════════════════════════════════════════════════════════╝

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Justice by the Numbers | Karnataka HC",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.main  { background-color: #f4f6f9; }
.block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1200px; }
#MainMenu, footer { visibility: hidden; }

.main-header {
    background: linear-gradient(135deg, #1a2744 0%, #2d4270 100%);
    border-radius: 14px; padding: 2rem 2.5rem; margin-bottom: 1.2rem;
}
.main-header h1  { font-size: 1.85rem; font-weight: 700; margin: 0; color: white !important; }
.main-header .sub { font-size: 0.97rem; opacity: 0.78; margin-top: 0.4rem; color: white !important; }
.main-header .tag { font-size: 0.72rem; opacity: 0.48; margin-top: 0.9rem;
    text-transform: uppercase; letter-spacing: 0.12em; color: white !important; }

.kpi { background: white; border-radius: 12px; padding: 1.3rem 1.1rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06); border-top: 4px solid #f4a300; }
.kpi.t  { border-top-color: #2a9d8f; }
.kpi.c  { border-top-color: #e76f51; }
.kpi.b  { border-top-color: #457b9d; }
.kpi-n  { font-size: 1.9rem; font-weight: 700; color: #1a2744; margin: 0; line-height: 1.1; }
.kpi-l  { font-size: 0.75rem; color: #888; margin-top: 0.25rem;
    text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600; }
.kpi-s  { font-size: 0.78rem; color: #aaa; margin-top: 0.15rem; }

.caveat {
    background: #fffbea; border: 1.5px solid #f4a300; border-radius: 10px;
    padding: 0.9rem 1.2rem; font-size: 0.86rem; color: #5a4200;
    line-height: 1.65; margin-bottom: 1.2rem;
}
.insight {
    background: #eaf4fb; border-left: 4px solid #457b9d;
    border-radius: 0 8px 8px 0; padding: 0.85rem 1.1rem;
    font-size: 0.87rem; color: #1a2744; line-height: 1.6; margin: 0.8rem 0 0.5rem 0;
}
.warn {
    background: #fff3f0; border-left: 4px solid #e76f51;
    border-radius: 0 8px 8px 0; padding: 0.85rem 1.1rem;
    font-size: 0.87rem; color: #7a2000; line-height: 1.6; margin: 0.8rem 0 0.5rem 0;
}
.stab-title { font-size: 1.3rem; font-weight: 700; color: #1a2744;
    margin-bottom: 0.2rem; margin-top: 0.4rem; }
.stab-sub   { font-size: 0.9rem; color: #666; margin-bottom: 1rem; }

.footer {
    background: #1a2744; color: #8fa8c8; border-radius: 14px;
    padding: 2rem 2.5rem; margin-top: 2.5rem; font-size: 0.83rem; line-height: 1.95;
}
.footer h4 { color: #fff; margin-bottom: 0.3rem; font-size: 0.93rem; }
.footer a  { color: #f4a300; text-decoration: none; }
</style>
""", unsafe_allow_html=True)



# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  BLOCK B — Data load, palette, shared helpers                           ║
# ╚══════════════════════════════════════════════════════════════════════════╝

@st.cache_data
def load_data():
    df     = pd.read_csv('data/processed_cases.csv',
                         parse_dates=['date_filed', 'decision_date'])
    cohort = pd.read_csv('data/cohort_stats.csv')
    return df, cohort

df, cohort_df = load_data()

# Palette
NAVY, AMBER, TEAL, CORAL, BLUE = '#1a2744', '#f4a300', '#2a9d8f', '#e76f51', '#457b9d'
SPEED_COLORS = {
    "Fast (under 1 year)":  TEAL,
    "Medium (1–2 years)":   AMBER,
    "Slow (2–3 years)":     CORAL,
    "Very Slow (3+ years)": '#c0392b',
}

# Shared layout — NO margin key here (each chart sets its own)
def chart_layout(height=420, title_font_size=14, **kwargs):
    """Return a layout dict. Pass custom keys to override."""
    base = dict(
        plot_bgcolor='white', paper_bgcolor='white',
        font_family='Inter', font_color=NAVY,
        height=height,
        title_font_size=title_font_size,
        margin=dict(l=20, r=20, t=60, b=25),
        showlegend=False,
    )
    base.update(kwargs)
    return base


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  BLOCK C — Sidebar and filters                                          ║
# ╚══════════════════════════════════════════════════════════════════════════╝

with st.sidebar:
    st.markdown("## ⚙️ Filters")
    years = sorted(df['filing_year'].unique())
    year_range = st.slider(
        "Filing year",
        min_value=int(min(years)), max_value=int(max(years)),
        value=(int(min(years)), int(max(years))), step=1
    )
    st.caption(
        "Filter cases by the year they were filed. "
        "Applies to all charts. Default: all years (2015–2019)."
    )
    st.markdown("---")
    st.markdown("""
**About**

An initiative by **Lawgorithm** to make judicial data
legible to every citizen.

🔗 [eCourts — Track your case](https://ecourts.gov.in)
🔗 [NJDG Live Data](https://njdg.ecourts.gov.in)
🔗 [DAKSH Judicial Research](https://dakshindia.org)
""")

# Filtered dataframes — used by all tabs
mask = (df['filing_year'] >= year_range[0]) & (df['filing_year'] <= year_range[1])
dff  = df[mask].copy()
cf   = cohort_df[
    (cohort_df['filing_year'] >= year_range[0]) &
    (cohort_df['filing_year'] <= year_range[1])
].copy()


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  BLOCK D — Header, caveat banner, KPI cards                             ║
# ╚══════════════════════════════════════════════════════════════════════════╝

st.markdown(f"""
<div class="main-header">
  <h1>⚖️ Justice by the Numbers</h1>
  <p class="sub">
    An independent analysis of <strong>{len(dff):,} resolved First Appeals (MFA)</strong>
    from the Karnataka High Court, Principal Bench, Bengaluru &nbsp;·&nbsp;
    Filing years {year_range[0]}–{year_range[1]} &nbsp;·&nbsp; Data snapshot: January 2021
  </p>
  <p class="tag">A Lawgorithm Initiative &nbsp;|&nbsp; Data: NJDG via ISDM Hackathon
    &nbsp;|&nbsp; All cases: MFA — First Appeals</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="caveat">
  ⚠️ <strong>What this data is — and is not:</strong>
  This dashboard shows only <strong>resolved (disposed) cases</strong>.
  Cases still pending as of January 2021 are not included — so this is not a picture
  of how fast the court resolves cases overall.
  Outcome details are recorded for only <strong>26% of cases</strong>.
  Court-level variation reflects differences in caseload, bench composition, and case
  complexity — not individual performance. All insights should be read as benchmarks
  from completed cases, not as predictions or assessments.
</div>
""", unsafe_allow_html=True)

# KPI calculations — all from filtered data
med   = int(dff['disposal_days'].median())
p25   = int(dff['disposal_days'].quantile(0.25))
p75   = int(dff['disposal_days'].quantile(0.75))
pfast = round(100 * (dff['disposal_days'] <= 365).mean(), 1)
pslow = round(100 * (dff['disposal_days'] > 1095).mean(), 1)

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""<div class="kpi">
        <p class="kpi-n">{len(dff):,}</p>
        <p class="kpi-l">Resolved Cases Studied</p>
        <p class="kpi-s">Karnataka HC · Principal Bench · Bengaluru</p>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class="kpi">
        <p class="kpi-n">{med:,} days</p>
        <p class="kpi-l">Median Time to Judgment</p>
        <p class="kpi-s">≈ {round(med/365.25, 1)} years &nbsp;·&nbsp; half took less, half took more</p>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class="kpi t">
        <p class="kpi-n">{pfast}%</p>
        <p class="kpi-l">Resolved Within 1 Year</p>
        <p class="kpi-s">Fastest quarter: under {p25} days (~{p25//30} months)</p>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class="kpi c">
        <p class="kpi-n">{pslow}%</p>
        <p class="kpi-l">Took Longer Than 3 Years</p>
        <p class="kpi-s">Slowest quarter: over {p75} days (~{p75//30} months)</p>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  BLOCK I — Tab shell (wraps E/F/G/H) + Footer                          ║
# ╚══════════════════════════════════════════════════════════════════════════╝

tab1, tab2, tab3, tab4 = st.tabs([
    "⏱️  How Long Does It Take?",
    "📅  Trends Over Time",
    "🏛️  Court-Level Variation",
    "📋  Outcomes & Patterns",
])

with tab1:
    # ╔══════════════════════════════════════════════════════════════════════════╗
    # ║  BLOCK E — Tab 1: How Long Does It Take?                                ║
    # ╚══════════════════════════════════════════════════════════════════════════╝
    
    # NOTE: This block must be inside   with tab1:   — see BLOCK H for tab setup
    
    st.markdown('<p class="stab-title">How long did resolved appeals take?</p>',
                unsafe_allow_html=True)
    st.markdown(
        '<p class="stab-sub">Time between case filing and final judgment, '
        'for all resolved First Appeals in this dataset.</p>',
        unsafe_allow_html=True)
    
    # Chart E1 — Histogram
    fig_hist = px.histogram(
        dff, x='disposal_days', nbins=60,
        color_discrete_sequence=[NAVY],
        labels={'disposal_days': 'Days from Filing to Judgment', 'count': 'Number of Cases'},
        title="Distribution of Time to Resolution"
    )
    for val, lbl, col in [
        (p25, f"Fastest 25%: {p25}d",        TEAL),
        (med, f"Median: {med}d",              AMBER),
        (p75, f"Slowest 25% starts: {p75}d",  CORAL),
    ]:
        fig_hist.add_vline(
            x=val, line_dash="dash", line_color=col, line_width=2.5,
            annotation_text=f" {lbl}", annotation_font_color=col,
            annotation_position="top left", annotation_font_size=12
        )
    fig_hist.update_layout(**chart_layout(
        height=420,
        xaxis_title="Days from Filing to Judgment",
        yaxis_title="Number of Cases",
        margin=dict(l=20, r=20, t=60, b=25)
    ))
    fig_hist.update_xaxes(showgrid=False)
    fig_hist.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_hist, width='stretch')
    
    st.markdown(f"""<div class="insight">
    📌 <strong>Reading this chart:</strong>
    Each bar groups cases that took roughly the same number of days to resolve.
    The median ({med} days, ~{round(med/365.25,1)} years) is the middle value —
    half resolved faster, half slower. The long right tail shows a smaller but real
    group that took 4–6 years. The peak of the curve is where most cases cluster.
    </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chart E2 — Speed tiers
    st.markdown("#### How do the numbers break into plain categories?")
    tier_order = ["Fast (under 1 year)","Medium (1–2 years)","Slow (2–3 years)","Very Slow (3+ years)"]
    tier_vals  = (
        dff['speed_tier'].value_counts()
        .reindex(tier_order).fillna(0).astype(int).reset_index()
    )
    tier_vals.columns = ['tier', 'count']
    tier_vals['pct'] = (100 * tier_vals['count'] / len(dff)).round(1)
    
    fig_tiers = px.bar(
        tier_vals, x='tier', y='count',
        color='tier',
        color_discrete_map=SPEED_COLORS,
        text=tier_vals['pct'].apply(lambda x: f"{x}%"),
        labels={'tier': '', 'count': 'Number of Cases'},
        title="Resolved Cases by Resolution Speed"
    )
    fig_tiers.update_traces(textposition='outside', textfont_size=13)
    fig_tiers.update_layout(**chart_layout(
        height=400,
        xaxis_title="", yaxis_title="Number of Cases",
        yaxis_range=[0, tier_vals['count'].max() * 1.2],
        margin=dict(l=20, r=20, t=60, b=25)
    ))
    fig_tiers.update_xaxes(showgrid=False)
    fig_tiers.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_tiers, width='stretch')
    
    st.markdown(f"""<div class="insight">
    📌 <strong>What this means:</strong>
    Among resolved cases — {pfast}% were done within a year, and 35.1% took 1–2 years.
    Nearly two-thirds finished within 2 years. The remaining third split between
    2–3 years (17.7%) and over 3 years ({pslow}%).
    This is the population of completed cases only — cases still pending are not counted.
    </div>""", unsafe_allow_html=True)

    pass

with tab2:
    # ╔══════════════════════════════════════════════════════════════════════════╗
    # ║  BLOCK F — Tab 2: Trends Over Time  (v4)                                ║
    # ╚══════════════════════════════════════════════════════════════════════════╝
    
    st.markdown('<p class="stab-title">How has resolution time changed across filing years?</p>',
                unsafe_allow_html=True)
    
    st.markdown("""<div class="caveat">
    📋 <strong>What this data covers:</strong>
    All figures are based on resolved cases only — cases still pending in January 2021
    are not in this dataset. Cohort sizes and observation windows vary by year and are
    shown on each chart.
    </div>""", unsafe_allow_html=True)
    
    # ── Build cohort-level speed breakdown ────────────────────────────────────────
    tier_order = [
        "Fast (under 1 year)", "Medium (1–2 years)",
        "Slow (2–3 years)",    "Very Slow (3+ years)"
    ]
    obs_windows = {2015: 2200, 2016: 1835, 2017: 1469, 2018: 1104, 2019: 739}
    
    cohort_tiers = (
        dff.groupby(['filing_year', 'speed_tier'])
        .size().reset_index(name='count')
    )
    totals = dff.groupby('filing_year').size().reset_index(name='total')
    cohort_tiers = cohort_tiers.merge(totals, on='filing_year')
    cohort_tiers['pct'] = (100 * cohort_tiers['count'] / cohort_tiers['total']).round(1)
    cohort_tiers['speed_tier'] = pd.Categorical(
        cohort_tiers['speed_tier'], categories=tier_order, ordered=True
    )
    cohort_tiers = cohort_tiers.sort_values(['filing_year', 'speed_tier'])
    
    # ── Chart F1: Stacked distribution ────────────────────────────────────────────
    st.markdown("#### How are resolved cases distributed across speed categories?")
    
    fig_stack = px.bar(
        cohort_tiers,
        x='filing_year', y='pct',
        color='speed_tier',
        color_discrete_map=SPEED_COLORS,
        barmode='stack',
        text=cohort_tiers['pct'].apply(lambda x: f"{x}%" if x >= 7 else ""),
        labels={
            'filing_year': 'Filing Year',
            'pct':         '% of Resolved Cases',
            'speed_tier':  'Speed'
        },
        title="Speed Breakdown of Resolved Cases by Filing Year",
        category_orders={'speed_tier': tier_order}
    )
    fig_stack.update_traces(textposition='inside', insidetextanchor='middle', textfont_size=11)
    
    # Observation window + n as annotation above each bar
    for yr, window in obs_windows.items():
        yr_data = totals[totals['filing_year'] == yr]
        if not yr_data.empty:
            n = int(yr_data['total'].values[0])
            fig_stack.add_annotation(
                x=yr, y=104,
                text=f"n={n:,} · {window}d window",
                showarrow=False,
                font=dict(size=9, color='#888'),
                align='center'
            )
    
    fig_stack.update_layout(**chart_layout(
        height=480, showlegend=True,
        xaxis_title="Filing Year",
        yaxis_title="% of Resolved Cases",
        legend_title="Speed",
        legend=dict(orientation='h', yanchor='bottom', y=1.08, xanchor='right', x=1),
        xaxis=dict(tickmode='linear', dtick=1),
        yaxis_range=[0, 116],
        margin=dict(l=20, r=20, t=105, b=25)
    ))
    fig_stack.update_xaxes(showgrid=False)
    fig_stack.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_stack, width='stretch')
    
    st.markdown("""<div class="insight">
    📌 The Fast (under 1 year) share rises from 22.7% in 2015 to 59.4% in 2019.
    The Very Slow (3+ years) share falls from 31.0% in 2015 to near-zero in 2018–2019.
    The Medium (1–2 years) share is the most consistent across years, ranging 29–52%.
    </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ── Chart F2: Median + IQR trend ──────────────────────────────────────────────
    st.markdown("#### How did median resolution time and spread change?")
    
    fig_med = go.Figure()
    fig_med.add_trace(go.Scatter(
        x=list(cf['filing_year'].astype(str)) + list(cf['filing_year'].astype(str))[::-1],
        y=list(cf['p75_days']) + list(cf['p25_days'])[::-1],
        fill='toself', fillcolor='rgba(244,163,0,0.13)',
        line=dict(color='rgba(0,0,0,0)'),
        hoverinfo='skip', showlegend=True,
        name='Middle 50% of cases (p25–p75)'
    ))
    fig_med.add_trace(go.Scatter(
        x=cf['filing_year'].astype(str), y=cf['median_days'],
        mode='lines+markers+text',
        line=dict(color=NAVY, width=3),
        marker=dict(size=10, color=AMBER, line=dict(color=NAVY, width=2)),
        text=cf['median_days'].apply(lambda x: f"{x}d"),
        textposition='top center', textfont_size=12,
        hovertemplate='Filed %{x}<br>Median: %{y} days<extra></extra>',
        showlegend=True, name='Median'
    ))
    for _, row in cf.iterrows():
        fig_med.add_annotation(
            x=str(int(row['filing_year'])),
            y=row['p25_days'] - 65,
            text=f"IQR: {int(row['p75_days'] - row['p25_days'])}d",
            showarrow=False,
            font=dict(size=9, color='#aaa'),
            align='center'
        )
    fig_med.update_layout(**chart_layout(
        height=440, showlegend=True,
        title="Median Days to Resolution + Middle 50% Range<br>"
              "<sup>IQR (interquartile range) shown below each year</sup>",
        xaxis_title="Filing Year",
        yaxis_title="Days to Resolution",
        legend=dict(orientation='h', yanchor='bottom', y=1.03, xanchor='right', x=1),
        margin=dict(l=20, r=20, t=80, b=25)
    ))
    fig_med.update_xaxes(showgrid=False)
    fig_med.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_med, width='stretch')
    
    st.markdown("""<div class="insight">
    📌 Median falls from 703 days (2015) to 319 days (2019).
    The IQR — the gap between the fastest and slowest quartile — also narrows:
    879 days in 2015 down to 346 days in 2019. Later cohorts' resolved cases
    are not just faster on median — they are more consistently timed.
    </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ── Chart F3: Filing vs disposal year heatmap ─────────────────────────────────
    st.markdown("#### In which years were each cohort's cases actually concluded?")
    
    cross = (
        dff.groupby(['filing_year', 'disposal_year'])
        .size().reset_index(name='count')
    )
    totals_map = dff.groupby('filing_year').size().to_dict()
    cross['pct'] = cross.apply(
        lambda r: round(100 * r['count'] / totals_map[r['filing_year']], 1), axis=1
    )
    pivot = cross.pivot(
        index='filing_year', columns='disposal_year', values='pct'
    ).fillna(0)
    
    fig_heat = px.imshow(
        pivot, aspect='auto',
        color_continuous_scale=['#f7f9fc', NAVY],
        text_auto='.1f',
        labels=dict(
            x="Year Judgment Was Delivered",
            y="Year Case Was Filed",
            color="% of Cohort"
        ),
        title="% of Each Filing Year's Cases Resolved in Each Calendar Year<br>"
              "<sup>Each row sums to 100%</sup>"
    )
    fig_heat.update_traces(textfont_size=11)
    fig_heat.update_layout(**chart_layout(
        height=360,
        margin=dict(l=80, r=20, t=75, b=25),
        coloraxis_colorbar=dict(title="% of cohort")
    ))
    st.plotly_chart(fig_heat, width='stretch')
    
    st.markdown("""<div class="insight">
    📌 2015 cases resolved across all six years (2015–2020), with no single year dominant.
    2018 and 2019 cases resolved heavily in 2019–2020 — the same two years where
    disposal volumes across all cohorts peak (see chart below).
    </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ── Chart F4: Disposal volume by calendar year ────────────────────────────────
    st.markdown("#### How many cases were concluded each calendar year?")
    
    disp_yr = dff.groupby('disposal_year').size().reset_index(name='count')
    fig_disp = px.bar(
        disp_yr, x='disposal_year', y='count',
        color_discrete_sequence=[BLUE], text='count',
        labels={'disposal_year': 'Year of Judgment', 'count': 'Cases Resolved'},
        title="Cases Resolved Per Calendar Year"
    )
    fig_disp.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig_disp.update_layout(**chart_layout(
        height=360,
        xaxis_title="Year of Final Judgment",
        yaxis_title="Cases Resolved",
        yaxis_range=[0, disp_yr['count'].max() * 1.2],
        xaxis=dict(tickmode='linear', dtick=1),
        margin=dict(l=20, r=20, t=60, b=25)
    ))
    fig_disp.update_xaxes(showgrid=False)
    fig_disp.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_disp, width='stretch')
    st.caption("2021 captures only the first week of January.")

    pass

with tab3:
    # ╔══════════════════════════════════════════════════════════════════════════╗
    # ║  BLOCK G — Tab 3: Court-Level Variation  (v2)                           ║
    # ╚══════════════════════════════════════════════════════════════════════════╝
    
    st.markdown('<p class="stab-title">Variation across court halls</p>',
                unsafe_allow_html=True)
    st.markdown(
        '<p class="stab-sub">All cases were heard at the Principal Bench, Bengaluru — '
        'same building, different court hall numbers. '
        'MFA is an administrative filing category, not a substantive legal classification. '
        'Cases under MFA can span motor vehicle compensation, land acquisition, family matters, '
        'labour disputes, and more. Subject-matter data is unavailable for 98.4% of cases.</p>',
        unsafe_allow_html=True)
    
    st.markdown("""<div class="warn">
    ⚠️ <strong>What we can and cannot say about court-level variation:</strong>
    MFA is an administrative entry category — not a measure of legal complexity or subject matter.
    Different halls may receive different mixes of underlying case types, but we have no
    subject-matter data for 98.4% of cases to verify or control for this.
    Judges are also transferred between halls over time.
    The variation we observe is real in the data — what drives it is not determinable
    from this dataset alone.
    </div>""", unsafe_allow_html=True)
    
    # ── Build court stats ─────────────────────────────────────────────────────────
    cs = (
        dff.groupby('court_number')['disposal_days']
        .agg(
            median_days='median',
            n_cases='count',
            p25=lambda x: int(x.quantile(0.25)),
            p75=lambda x: int(x.quantile(0.75))
        )
        .reset_index()
    )
    cs.columns = ['court_hall', 'median_days', 'n_cases', 'p25', 'p75']
    cs = cs[cs['n_cases'] >= 50].sort_values('median_days').reset_index(drop=True)
    cs['court_label'] = 'Hall ' + cs['court_hall'].astype(int).astype(str)
    
    vmin  = int(cs['median_days'].min())
    vmax  = int(cs['median_days'].max())
    ratio = round(vmax / vmin, 1)
    
    st.markdown(f"""<div class="insight">
    📌 Among {len(cs)} court halls with 50+ resolved cases, the fastest median was
    <strong>{vmin} days</strong> and the slowest <strong>{vmax} days</strong> —
    a <strong>{ratio}× difference</strong>. What drives this variation — case mix,
    complexity, bench composition, or other factors — is not visible in this dataset.
    </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ── Chart G1: Sorted bar — all qualifying halls ───────────────────────────────
    st.markdown("#### Median resolution time by court hall")
    st.caption(f"Halls with 50+ resolved cases · Sorted fastest → slowest · n={len(cs)} halls")
    
    fig_bar = px.bar(
        cs, x='court_label', y='median_days',
        color='median_days',
        color_continuous_scale=[TEAL, AMBER, CORAL, '#c0392b'],
        text=cs['median_days'].apply(lambda x: f"{int(x)}d"),
        labels={'court_label': 'Court Hall', 'median_days': 'Median Days'}
    )
    fig_bar.update_traces(textposition='outside', textfont_size=10)
    fig_bar.update_layout(**chart_layout(
        height=500, coloraxis_showscale=False,
        xaxis_title="Court Hall Number",
        yaxis_title="Median Days to Resolution",
        xaxis_tickangle=-45,
        yaxis_range=[0, cs['median_days'].max() * 1.2],
        margin=dict(l=20, r=20, t=50, b=80)
    ))
    fig_bar.update_xaxes(showgrid=False)
    fig_bar.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_bar, width='stretch')
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ── Chart G2: Scatter — caseload vs resolution ────────────────────────────────
    st.markdown("#### Is caseload associated with resolution time?")
    
    corr = round(float(np.corrcoef(cs['n_cases'], cs['median_days'])[0, 1]), 2)
    
    fig_sc = px.scatter(
        cs, x='n_cases', y='median_days',
        size='n_cases', size_max=45,
        color='median_days',
        color_continuous_scale=[TEAL, AMBER, CORAL, '#c0392b'],
        hover_name='court_label',
        hover_data={'court_hall': True, 'n_cases': ':.0f', 'median_days': ':.0f'},
        labels={'n_cases': 'Cases Handled', 'median_days': 'Median Days'}
    )
    x_line = np.linspace(cs['n_cases'].min(), cs['n_cases'].max(), 100)
    z = np.polyfit(cs['n_cases'], cs['median_days'], 1)
    fig_sc.add_trace(go.Scatter(
        x=x_line, y=np.polyval(z, x_line),
        mode='lines', name='Linear trend',
        line=dict(color=NAVY, width=1.5, dash='dot'),
        showlegend=True
    ))
    fig_sc.update_layout(**chart_layout(
        height=460, coloraxis_showscale=False, showlegend=True,
        title=f"Caseload vs. Median Resolution Time (Pearson r = {corr})<br>"
              f"<sup>Each bubble = one court hall · Bubble size ∝ case volume</sup>",
        xaxis_title='Cases Handled',
        yaxis_title='Median Days to Resolution',
        legend=dict(x=0.01, y=0.98),
        margin=dict(l=20, r=20, t=80, b=25)
    ))
    fig_sc.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
    fig_sc.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_sc, width='stretch')
    
    st.markdown(f"""<div class="insight">
    📌 Pearson correlation between caseload and median resolution time: <strong>{corr}</strong>.
    A linear trend line is shown for reference. Individual halls vary widely around it —
    caseload volume alone does not explain the spread.
    </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ── Chart G3: Box plot — spread by filing year ────────────────────────────────
    st.markdown("#### How wide is the spread of resolution times within each filing year?")
    
    fig_box = px.box(
        dff, x='filing_year', y='disposal_days',
        color='filing_year',
        color_discrete_sequence=[TEAL, BLUE, AMBER, CORAL, '#c0392b'],
        labels={'disposal_days': 'Days to Resolution', 'filing_year': 'Filing Year'},
        title="Spread of Resolution Times by Filing Year<br>"
              "<sup>Box = middle 50% · Line = median · Whiskers = 1.5× IQR</sup>",
        points=False
    )
    fig_box.update_layout(**chart_layout(
        height=430,
        xaxis_title="Filing Year",
        yaxis_title="Days to Resolution",
        margin=dict(l=20, r=20, t=80, b=25)
    ))
    fig_box.update_xaxes(showgrid=False, type='category')
    fig_box.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_box, width='stretch')
    
    st.markdown("""<div class="insight">
    📌 The box height (IQR) shrinks across years — resolved cases in later cohorts
    are more tightly clustered in time. Whether that reflects court capacity, case mix
    shifts, or other factors is not visible in this data.
    </div>""", unsafe_allow_html=True)

    pass

with tab4:
    # ╔══════════════════════════════════════════════════════════════════════════╗
    # ║  BLOCK H — Tab 4: Outcomes & Patterns                                   ║
    # ╚══════════════════════════════════════════════════════════════════════════╝
    
    st.markdown('<p class="stab-title">What happened when cases were resolved?</p>',
                unsafe_allow_html=True)
    st.markdown(
        '<p class="stab-sub">Outcome records and filing seasonality patterns.</p>',
        unsafe_allow_html=True)
    
    st.markdown("""<div class="warn">
    ⚠️ <strong>Outcome data is recorded for only 26.3% of cases (5,420 of 20,646).</strong>
    Charts below are illustrative only. The 73.7% with no outcome is a data quality gap
    in the NJDG source — not something this dashboard fills or estimates.
    Do not treat percentages here as representative of all appeals.
    </div>""", unsafe_allow_html=True)
    
    # Chart H1 — Outcome bar (known outcomes only)
    outcome_known = dff[dff['outcome_bucket'] != 'Data Not Available'].copy()
    oc = outcome_known['outcome_bucket'].value_counts().reset_index()
    oc.columns = ['outcome', 'count']
    oc['pct'] = (100 * oc['count'] / len(outcome_known)).round(1)
    
    fig_oc = px.bar(
        oc.sort_values('count'),
        x='count', y='outcome', orientation='h',
        color='outcome',
        color_discrete_sequence=[TEAL, BLUE, AMBER, CORAL, '#8e44ad', NAVY],
        text=oc.sort_values('count')['pct'].apply(lambda x: f"{x}%"),
        labels={'count': 'Number of Cases', 'outcome': ''},
        title=(
            f"Case Outcomes — {len(outcome_known):,} cases with recorded outcomes<br>"
            f"<sup>Remaining {len(dff)-len(outcome_known):,} cases: no outcome in source data</sup>"
        )
    )
    fig_oc.update_traces(textposition='outside', textfont_size=12)
    fig_oc.update_layout(**chart_layout(
        height=440,
        xaxis_title="Number of Cases", yaxis_title="",
        xaxis_range=[0, oc['count'].max() * 1.3],
        margin=dict(l=20, r=70, t=80, b=25)
    ))
    fig_oc.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
    fig_oc.update_yaxes(showgrid=False)
    st.plotly_chart(fig_oc, width='stretch')
    
    st.markdown("""<div class="insight">
    📌 <strong>Reading outcomes carefully:</strong>
    "Disposed — Manner Not Recorded" is a data quality issue in the source — the case was
    closed but how it closed was not entered. Of cases with a substantive outcome:
    Partly Allowed (1,258) and Dismissed/Rejected (1,270) are the two largest categories,
    roughly equal. Fully Allowed (113) is a small fraction.
    "Allowed & Sent Back" means the High Court found merit but referred the matter
    back to the lower court for fresh consideration — not a final conclusion.
    </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chart H2 — Contested vs uncontested outcomes
    st.markdown("#### Contested vs. Uncontested — in the data we have")
    cont_oc = (
        dff[(dff['contested_label'] != 'Not Recorded') &
            (dff['outcome_bucket'] != 'Data Not Available')]
        .groupby(['contested_label', 'outcome_bucket'])
        .size().reset_index(name='count')
    )
    if not cont_oc.empty and len(cont_oc) > 1:
        fig_cont = px.bar(
            cont_oc, x='contested_label', y='count',
            color='outcome_bucket', barmode='group',
            labels={'contested_label': '', 'count': 'Cases', 'outcome_bucket': 'Outcome'},
            title=(
                "Outcome by Contested / Uncontested Status<br>"
                "<sup>Only cases where both status AND outcome are recorded</sup>"
            ),
            color_discrete_sequence=[TEAL, BLUE, AMBER, CORAL, '#8e44ad', NAVY]
        )
        fig_cont.update_layout(**chart_layout(
            height=400, showlegend=True,
            xaxis_title="", yaxis_title="Number of Cases",
            legend_title="Outcome",
            margin=dict(l=20, r=20, t=80, b=25)
        ))
        fig_cont.update_xaxes(showgrid=False)
        fig_cont.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
        st.plotly_chart(fig_cont, width='stretch')
    else:
        st.info("Not enough data with both contested status and outcome recorded to show this chart for the selected year range.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chart H3 — Monthly filing heatmap
    st.markdown("#### When are cases filed? (all 20,646 cases)")
    monthly = dff.groupby(['filing_year', 'filing_month']).size().reset_index(name='count')
    pivot   = monthly.pivot(index='filing_year', columns='filing_month', values='count').fillna(0)
    mnames  = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
               7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
    pivot.columns = [mnames.get(c, str(c)) for c in pivot.columns]
    
    fig_heat = px.imshow(
        pivot, aspect='auto',
        color_continuous_scale=['#eef2ff', NAVY],
        labels=dict(x="Month", y="Filing Year", color="Cases Filed"),
        title=(
            "Monthly Filing Volume by Year<br>"
            "<sup>Darker = more filings · Based on all resolved cases in this dataset</sup>"
        )
    )
    fig_heat.update_layout(**chart_layout(
        height=380,
        margin=dict(l=70, r=20, t=80, b=25)
    ))
    st.plotly_chart(fig_heat, width='stretch')
    
    st.markdown("""<div class="insight">
    📌 <strong>Seasonality:</strong>
    Filing volumes vary by month, often reflecting court vacation periods
    (summer, Diwali, Christmas breaks). Peaks on either side of a break can indicate
    filings compressed before or after vacations. These patterns are useful context for
    litigants timing their filings and for administrators planning resources.
    </div>""", unsafe_allow_html=True)

    pass


# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  <h4>📖 About This Dashboard</h4>
  <p>
  An initiative by <strong>Lawgorithm</strong> to make judicial data legible
  to citizens, researchers, and policy stakeholders.<br><br>

  <strong>Data source:</strong> National Judicial Data Grid (NJDG), Karnataka High Court
  (Principal Bench, Bengaluru), accessed via ISDM Hackathon dataset.
  Covers <strong>MFA (First Appeals)</strong> filed 2015–2019, resolved by January 2021.
  Total after cleaning: {len(df):,} cases.<br><br>

  <strong>Case type — MFA:</strong> All cases are classified as MFA (First Appeal) in NJDG.
  Subject-matter details are recorded for only 1.6% of cases. Of those,
  Motor Vehicles Act cases are the plurality — but no claim is made about the remaining 98.4%.<br><br>

  <strong>Key limitation — survivorship:</strong> Only resolved cases are included.
  Pending cases as of January 2021 are absent. All statistics describe
  completed cases, not current court performance or future case timelines.<br><br>

  <strong>Court variation:</strong> Court hall numbers are NJDG identifiers.
  Variation in resolution times reflects case complexity, bench composition,
  and workload — not individual performance.<br><br>

  🔗 <a href="https://njdg.ecourts.gov.in" target="_blank">NJDG Live Portal</a> &nbsp;·&nbsp;
  🔗 <a href="https://ecourts.gov.in" target="_blank">eCourts — Track your case</a> &nbsp;·&nbsp;
  🔗 <a href="https://dakshindia.org" target="_blank">DAKSH India</a> &nbsp;·&nbsp;
  🔗 <a href="https://vidhilegalpolicy.in" target="_blank">Vidhi Centre for Legal Policy</a><br><br>

  <em>Built by Lawgorithm &nbsp;|&nbsp; Data: NJDG / ISDM &nbsp;|&nbsp; For queries: contact Lawgorithm</em>
  </p>
</div>
""", unsafe_allow_html=True)
