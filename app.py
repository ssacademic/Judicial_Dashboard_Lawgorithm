# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  JUSTICE BY THE NUMBERS — Karnataka High Court                          ║
# ║  A Lawgorithm Initiative  |  app.py  |  v3                              ║
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
  Cases still pending as of January 2021 are not included.
  Outcome details are recorded for only <strong>26% of cases</strong>.
  Court-level variation is visible in the data — what drives it is not
  determinable from this dataset alone.
</div>
""", unsafe_allow_html=True)

# KPI calculations
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
    half resolved faster, half slower. The long right tail shows a smaller group
    that took 4–6 years.
    </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chart E2 — Speed tiers
    st.markdown("#### How do the numbers break into plain categories?")
    
    tier_order = [
        "Fast (under 1 year)", "Medium (1–2 years)",
        "Slow (2–3 years)",    "Very Slow (3+ years)"
    ]
    tier_vals = (
        dff['speed_tier'].value_counts()
        .reindex(tier_order).fillna(0).astype(int).reset_index()
    )
    tier_vals.columns = ['tier', 'count']
    tier_vals['pct'] = (100 * tier_vals['count'] / len(dff)).round(1)
    
    # Computed variables — used in insight text
    p_fast_e   = tier_vals.loc[tier_vals['tier']=="Fast (under 1 year)",   'pct'].values[0]
    p_medium_e = tier_vals.loc[tier_vals['tier']=="Medium (1–2 years)",    'pct'].values[0]
    p_slow_e   = tier_vals.loc[tier_vals['tier']=="Slow (2–3 years)",      'pct'].values[0]
    p_vslow_e  = tier_vals.loc[tier_vals['tier']=="Very Slow (3+ years)",  'pct'].values[0]
    p_within2  = round(p_fast_e + p_medium_e, 1)
    
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
    📌 {p_fast_e}% resolved within 1 year, {p_medium_e}% in 1–2 years —
    {p_within2}% of resolved cases finished within 2 years.
    {p_slow_e}% took 2–3 years and {p_vslow_e}% took more than 3 years.
    These figures cover resolved cases only — pending cases are not counted.
    </div>""", unsafe_allow_html=True)


    pass

with tab2:
    # ╔══════════════════════════════════════════════════════════════════════════╗
    # ║  BLOCK F — Tab 2: Trends Over Time  (v5)                                ║
    # ╚══════════════════════════════════════════════════════════════════════════╝
    
    st.markdown('<p class="stab-title">How has resolution time changed across filing years?</p>',
                unsafe_allow_html=True)
    
    st.markdown("""<div class="caveat">
    📋 <strong>What this data covers:</strong>
    All figures are based on resolved cases only — cases still pending in January 2021
    are not in this dataset. Cohort sizes and observation windows vary by year and are
    shown on each chart.
    </div>""", unsafe_allow_html=True)
    
    # ── Computed observation windows — not hardcoded ──────────────────────────────
    obs_cutoff  = pd.Timestamp('2021-01-09')
    obs_windows = {
        int(yr): (obs_cutoff - pd.Timestamp(f'{int(yr)}-01-01')).days
        for yr in sorted(dff['filing_year'].unique())
    }
    
    tier_order = [
        "Fast (under 1 year)", "Medium (1–2 years)",
        "Slow (2–3 years)",    "Very Slow (3+ years)"
    ]
    
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
    
    # Precompute values for insight texts
    yr_min = int(cf['filing_year'].min())
    yr_max = int(cf['filing_year'].max())
    fast_min = cohort_tiers.loc[
        (cohort_tiers['filing_year']==yr_min) &
        (cohort_tiers['speed_tier']=="Fast (under 1 year)"), 'pct'].values[0]
    fast_max = cohort_tiers.loc[
        (cohort_tiers['filing_year']==yr_max) &
        (cohort_tiers['speed_tier']=="Fast (under 1 year)"), 'pct'].values[0]
    
    def _get_pct(year, tier):
        row = cohort_tiers.loc[
            (cohort_tiers['filing_year']==year) &
            (cohort_tiers['speed_tier']==tier), 'pct']
        return round(float(row.values[0]), 1) if not row.empty else 0.0
    
    fast_min  = _get_pct(yr_min, "Fast (under 1 year)")
    fast_max  = _get_pct(yr_max, "Fast (under 1 year)")
    vslow_min = _get_pct(yr_min, "Very Slow (3+ years)")
    vslow_max = _get_pct(yr_max, "Very Slow (3+ years)")
    
    med_min   = int(cf.loc[cf['filing_year']==yr_min, 'median_days'].values[0])
    med_max   = int(cf.loc[cf['filing_year']==yr_max, 'median_days'].values[0])
    iqr_min   = int(cf.loc[cf['filing_year']==yr_min, 'p75_days'].values[0] -
                    cf.loc[cf['filing_year']==yr_min, 'p25_days'].values[0])
    iqr_max   = int(cf.loc[cf['filing_year']==yr_max, 'p75_days'].values[0] -
                    cf.loc[cf['filing_year']==yr_max, 'p25_days'].values[0])
    
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
    
    st.markdown(f"""<div class="insight">
    📌 The Fast (under 1 year) share rises from {fast_min}% in {yr_min} to {fast_max}% in {yr_max}.
    The Very Slow (3+ years) share falls from {vslow_min}% in {yr_min} to {vslow_max}% in {yr_max}.
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
    
    st.markdown(f"""<div class="insight">
    📌 Median falls from {med_min} days ({yr_min}) to {med_max} days ({yr_max}).
    The IQR also narrows: {iqr_min} days in {yr_min} down to {iqr_max} days in {yr_max} —
    resolved cases in later cohorts are more consistently timed, not just faster on median.
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
    
    st.markdown(f"""<div class="insight">
    📌 {yr_min} cases resolved spread across all available years with no single year dominant.
    {yr_max} cases resolved heavily in the final two years before the January 2021 snapshot.
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
    # ║  BLOCK G — Tab 3: Court-Level Variation  (v3)                           ║
    # ╚══════════════════════════════════════════════════════════════════════════╝
    
    st.markdown('<p class="stab-title">Variation across court halls</p>',
                unsafe_allow_html=True)
    st.markdown(
        '<p class="stab-sub">'
        'All 20,646 cases were heard at the Karnataka High Court\'s Principal Bench, Bengaluru, '
        'distributed across court halls. One hall — Court 200 — handled 40% of all cases in this '
        'dataset. Resolution times vary widely across halls. MFA covers many different kinds of '
        'cases (motor vehicle, land, family, labour and more), and subject-matter data is '
        'unavailable for 98.4% of records, so the reasons behind variation across halls '
        'are not visible here.'
        '</p>',
        unsafe_allow_html=True)
    
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
    cs_all = cs.copy()   # keep all halls for load chart
    cs = cs[cs['n_cases'] >= 50].sort_values('median_days').reset_index(drop=True)
    cs['court_label'] = 'Court ' + cs['court_hall'].astype(int).astype(str)
    
    vmin  = int(cs['median_days'].min())
    vmax  = int(cs['median_days'].max())
    ratio = round(vmax / vmin, 1)
    total_cases = len(dff)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ── Chart G0: Case load concentration ─────────────────────────────────────────
    st.markdown("#### How are cases distributed across court halls?")
    
    load = cs_all.sort_values('n_cases', ascending=False).copy()
    load['court_label'] = 'Court ' + load['court_hall'].astype(int).astype(str)
    load['pct'] = (100 * load['n_cases'] / total_cases).round(1)
    load['cumulative_pct'] = load['pct'].cumsum().round(1)
    
    # Show top 20 + "others"
    top_n = 20
    top   = load.head(top_n).copy()
    rest  = load.iloc[top_n:]
    if not rest.empty:
        others = pd.DataFrame([{
            'court_label': f'Other {len(rest)} halls',
            'n_cases':     int(rest['n_cases'].sum()),
            'pct':         round(rest['pct'].sum(), 1),
            'cumulative_pct': 100.0
        }])
        load_display = pd.concat([top, others], ignore_index=True)
    else:
        load_display = top
    
    fig_load = go.Figure()
    fig_load.add_trace(go.Bar(
        x=load_display['court_label'],
        y=load_display['n_cases'],
        marker_color=[NAVY if 'Other' not in str(l) else '#ccc'
                      for l in load_display['court_label']],
        text=load_display['pct'].apply(lambda x: f"{x}%"),
        textposition='outside',
        textfont_size=10,
        hovertemplate='%{x}<br>%{y:,} cases (%{text})<extra></extra>'
    ))
    fig_load.update_layout(**chart_layout(
        height=420,
        title=f"Case Volume by Court Hall — Top {top_n} halls + rest<br>"
              f"<sup>Court 200 alone handles "
              f"{load[load['court_label']=='Court 200']['pct'].values[0] if 'Court 200' in load['court_label'].values else '~40'}% "
              f"of all resolved cases in this dataset</sup>",
        xaxis_title="Court Hall",
        yaxis_title="Resolved Cases",
        xaxis_tickangle=-45,
        yaxis_range=[0, load_display['n_cases'].max() * 1.18],
        margin=dict(l=20, r=20, t=80, b=80)
    ))
    fig_load.update_xaxes(showgrid=False)
    fig_load.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_load, width='stretch')
    
    court200_n    = int(dff[dff['court_number'] == 200].shape[0])
    court200_pct  = round(100 * court200_n / len(dff), 1)
    small_n       = int((dff.groupby('court_number').size() < 50).sum())
    small_case_pct= round(100 * dff.groupby('court_number').size()[
                        dff.groupby('court_number').size() < 50].sum() / len(dff), 1)
    total_halls   = dff['court_number'].nunique()
    
    st.markdown(f"""<div class="insight">
    📌 Court 200 handled {court200_n:,} cases — {court200_pct}% of all resolved cases
    in this dataset. {small_n} of {total_halls} halls had fewer than 50 resolved cases
    and together account for {small_case_pct}% of cases.
    </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ── Chart G1: Sorted bar — median resolution per hall (50+ cases) ─────────────
    st.markdown(f"#### Median resolution time across {len(cs)} halls (50+ cases each)")
    
    fig_bar = px.bar(
        cs, x='court_label', y='median_days',
        color='median_days',
        color_continuous_scale=[TEAL, AMBER, CORAL, '#c0392b'],
        text=cs['median_days'].apply(lambda x: f"{int(x)}d"),
        labels={'court_label': '', 'median_days': 'Median Days'}
    )
    fig_bar.update_traces(textposition='outside', textfont_size=9)
    fig_bar.update_layout(**chart_layout(
        height=500, coloraxis_showscale=False,
        xaxis_title="",
        yaxis_title="Median Days to Resolution",
        xaxis_tickangle=-45,
        yaxis_range=[0, cs['median_days'].max() * 1.2],
        margin=dict(l=20, r=20, t=50, b=90)
    ))
    fig_bar.update_xaxes(showgrid=False)
    fig_bar.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_bar, width='stretch')
    
    st.markdown(f"""<div class="insight">
    📌 Across {len(cs)} halls with 50+ resolved cases, median resolution ranges from
    <strong>{vmin} days</strong> to <strong>{vmax} days</strong> — a {ratio}× spread.
    </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ── Chart G2: Caseload vs resolution time ─────────────────────────────────────
    st.markdown("#### Does handling more cases relate to faster or slower resolution?")
    
    corr = round(float(np.corrcoef(cs['n_cases'], cs['median_days'])[0, 1]), 2)
    
    fig_sc = px.scatter(
        cs, x='n_cases', y='median_days',
        size='n_cases', size_max=45,
        color='median_days',
        color_continuous_scale=[TEAL, AMBER, CORAL, '#c0392b'],
        hover_name='court_label',
        hover_data={'n_cases': ':.0f', 'median_days': ':.0f'},
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
        title=f"Caseload vs. Median Resolution Time  (r = {corr})",
        xaxis_title='Cases Handled',
        yaxis_title='Median Days to Resolution',
        legend=dict(x=0.01, y=0.98),
        margin=dict(l=20, r=20, t=60, b=25)
    ))
    fig_sc.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
    fig_sc.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_sc, width='stretch')
    
    st.markdown(f"""<div class="insight">
    📌 Pearson r = {corr}. Each bubble is one court hall; size reflects case volume.
    The dotted line is a linear trend. Halls cluster with wide spread around it —
    volume alone does not explain resolution time.
    </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ── Chart G3: Box plot — spread by filing year ────────────────────────────────
    st.markdown("#### Spread of resolution times within each filing year")
    
    fig_box = px.box(
        dff, x='filing_year', y='disposal_days',
        color='filing_year',
        color_discrete_sequence=[TEAL, BLUE, AMBER, CORAL, '#c0392b'],
        labels={'disposal_days': 'Days to Resolution', 'filing_year': 'Filing Year'},
        title="Resolution Time Spread by Filing Year<br>"
              "<sup>Box = middle 50% · Line = median · Whiskers = 1.5× IQR</sup>",
        points=False
    )
    fig_box.update_layout(**chart_layout(
        height=420,
        xaxis_title="Filing Year",
        yaxis_title="Days to Resolution",
        margin=dict(l=20, r=20, t=70, b=25)
    ))
    fig_box.update_xaxes(showgrid=False, type='category')
    fig_box.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_box, width='stretch')
    
    st.markdown("""<div class="insight">
    📌 The box height (IQR) narrows across years — resolved cases in later cohorts
    are more tightly clustered around the median. 2015 cases had the widest spread:
    some finished quickly, others took the full 6-year window before this snapshot.
    </div>""", unsafe_allow_html=True)

    pass

with tab4:
    # ╔══════════════════════════════════════════════════════════════════════════╗
    # ║  BLOCK H — Tab 4: Outcomes & Patterns  (v2)                             ║
    # ╚══════════════════════════════════════════════════════════════════════════╝
    
    st.markdown('<p class="stab-title">What happened when cases were resolved?</p>',
                unsafe_allow_html=True)
    st.markdown(
        '<p class="stab-sub">Outcome records and filing volume patterns.</p>',
        unsafe_allow_html=True)
    
    outcome_total   = dff['outcome_bucket'].notna().sum()
    outcome_missing = (dff['outcome_bucket'] == 'Data Not Available').sum()
    outcome_known_n = outcome_total - outcome_missing
    outcome_pct     = round(100 * outcome_known_n / len(dff), 1)
    
    st.markdown(f"""<div class="warn">
    ⚠️ Outcome data is recorded for <strong>{outcome_known_n:,} of {len(dff):,} cases
    ({outcome_pct}%)</strong>. The remaining {100-outcome_pct:.1f}% have no outcome
    in the source data. Charts below cover the {outcome_known_n:,} cases with a
    recorded outcome only.
    </div>""", unsafe_allow_html=True)
    
    # ── Chart H1 — Outcome bar (known outcomes only) ──────────────────────────────
    outcome_known = dff[dff['outcome_bucket'] != 'Data Not Available'].copy()
    
    # Keep Dismissed for Non-Prosecution separate — it is procedurally distinct
    # from a contested dismissal on merits
    oc = outcome_known['outcome_bucket'].value_counts().reset_index()
    oc.columns = ['outcome', 'count']
    oc['pct'] = (100 * oc['count'] / len(outcome_known)).round(1)
    
    # Pull key numbers dynamically for insight text
    def _n(label):
        row = oc[oc['outcome'] == label]
        return int(row['count'].values[0]) if not row.empty else 0
    
    n_partly    = _n('Partly Allowed')
    n_dismissed = _n('Dismissed')               # on merits
    n_dnp       = _n('Dismissed for Non-Prosecution')
    n_allowed   = _n('Allowed')
    n_remanded  = _n('Allowed and Remanded')
    n_disposed  = _n('Disposed')                # manner not recorded
    n_rejected  = _n('Rejected')
    
    fig_oc = px.bar(
        oc.sort_values('count'),
        x='count', y='outcome', orientation='h',
        color='outcome',
        color_discrete_sequence=[TEAL, BLUE, AMBER, CORAL, '#8e44ad', NAVY, '#95a5a6'],
        text=oc.sort_values('count')['pct'].apply(lambda x: f"{x}%"),
        labels={'count': 'Number of Cases', 'outcome': ''},
        title=(
            f"Case Outcomes — {outcome_known_n:,} cases with recorded outcomes<br>"
            f"<sup>Remaining {len(dff)-outcome_known_n:,} cases: no outcome in source data</sup>"
        )
    )
    fig_oc.update_traces(textposition='outside', textfont_size=12)
    fig_oc.update_layout(**chart_layout(
        height=460,
        xaxis_title="Number of Cases", yaxis_title="",
        xaxis_range=[0, oc['count'].max() * 1.35],
        margin=dict(l=20, r=70, t=80, b=25)
    ))
    fig_oc.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
    fig_oc.update_yaxes(showgrid=False)
    st.plotly_chart(fig_oc, width='stretch')
    
    st.markdown(f"""<div class="insight">
    📌 Among the {outcome_known_n:,} cases with a recorded outcome:
    <strong>"Disposed — Manner Not Recorded" ({n_disposed:,})</strong> is the largest category —
    the case was closed but the how was not entered in NJDG.
    Of substantive outcomes: Partly Allowed ({n_partly:,}) and Dismissed ({n_dismissed:,})
    are the two largest. "Dismissed for Non-Prosecution" ({n_dnp:,}) is a distinct category —
    the case was dropped because the petitioner did not pursue it, not because it was
    decided against them on merits. "Allowed and Remanded" ({n_remanded:,}) means the HC
    found grounds for reconsideration and returned the case to the lower court.
    </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ── Chart H2 — Contested vs uncontested outcomes ─────────────────────────────
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
    
    # ── Chart H3 — Monthly filing heatmap ────────────────────────────────────────
    st.markdown("#### When are cases filed? (all cases)")
    monthly = dff.groupby(['filing_year', 'filing_month']).size().reset_index(name='count')
    pivot   = monthly.pivot(
        index='filing_year', columns='filing_month', values='count'
    ).fillna(0)
    mnames = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
              7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
    pivot.columns = [mnames.get(c, str(c)) for c in pivot.columns]
    
    # Dynamic high/low months for insight
    monthly_totals = dff.groupby('filing_month').size()
    month_high = mnames[int(monthly_totals.idxmax())]
    month_low  = mnames[int(monthly_totals.idxmin())]
    
    fig_heat = px.imshow(
        pivot, aspect='auto',
        color_continuous_scale=['#eef2ff', NAVY],
        labels=dict(x="Month", y="Filing Year", color="Cases Filed"),
        title=(
            "Monthly Filing Volume by Year<br>"
            "<sup>Darker = more filings</sup>"
        )
    )
    fig_heat.update_layout(**chart_layout(
        height=380,
        margin=dict(l=70, r=20, t=80, b=25)
    ))
    st.plotly_chart(fig_heat, width='stretch')
    
    st.markdown(f"""<div class="insight">
    📌 {month_high} is consistently the highest-volume filing month across years.
    {month_low} is the lowest. Filing volumes vary across months — the pattern
    is visible in the chart above.
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
  Court-level variation is visible in the data. What drives it is not
determinable from this dataset alone.<br><br>

  🔗 <a href="https://njdg.ecourts.gov.in" target="_blank">NJDG Live Portal</a> &nbsp;·&nbsp;
  🔗 <a href="https://ecourts.gov.in" target="_blank">eCourts — Track your case</a> &nbsp;·&nbsp;
  🔗 <a href="https://dakshindia.org" target="_blank">DAKSH India</a> &nbsp;·&nbsp;
  🔗 <a href="https://vidhilegalpolicy.in" target="_blank">Vidhi Centre for Legal Policy</a><br><br>

  <em>Built by Lawgorithm &nbsp;|&nbsp; Data: NJDG / ISDM &nbsp;|&nbsp; For queries: contact Lawgorithm</em>
  </p>
</div>
""", unsafe_allow_html=True)
