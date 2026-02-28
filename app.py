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
    # ║  BLOCK F — Tab 2: Trends Over Time                                      ║
    # ╚══════════════════════════════════════════════════════════════════════════╝
    
    st.markdown('<p class="stab-title">Are cases getting resolved faster over time?</p>',
                unsafe_allow_html=True)
    st.markdown(
        '<p class="stab-sub">Each bar represents one filing-year cohort. '
        'We measure what share was resolved within a fixed time window — '
        'the only fair comparison across years.</p>',
        unsafe_allow_html=True)
    
    st.markdown("""<div class="warn">
    ⚠️ <strong>Survivorship caveat — important before reading these charts:</strong>
    Cases filed in 2019 had only ~2 years to be resolved before this data was collected (Jan 2021).
    Slow 2019 cases were still pending and are absent from this dataset, making the 2019
    cohort look faster partly by selection. Earlier cohorts (2015, 2016) had 5–6 years to
    accumulate resolved cases and are more complete. Treat the trend direction as plausible;
    treat the 2019 magnitude as a <strong>lower-bound estimate only</strong>.
    </div>""", unsafe_allow_html=True)
    
    # Chart F1 — % within 1 year per cohort
    fig_1yr = go.Figure()
    fig_1yr.add_trace(go.Bar(
        x=cf['filing_year'].astype(str), y=cf['pct_within_1yr'],
        marker_color=TEAL,
        text=cf['pct_within_1yr'].apply(lambda x: f"{x}%"),
        textposition='outside',
        hovertemplate='Filed %{x}<br>%{y}% resolved within 1 year<br><i>(of cases in this dataset)</i><extra></extra>'
    ))
    fig_1yr.update_layout(**chart_layout(
        height=400,
        title="% of Each Year's Cases Resolved Within 1 Year",
        xaxis_title="Year Case Was Filed",
        yaxis_title="% Resolved Within 1 Year",
        yaxis_range=[0, min(cf['pct_within_1yr'].max() * 1.3, 100)],
        margin=dict(l=20, r=20, t=60, b=25)
    ))
    fig_1yr.update_xaxes(showgrid=False)
    fig_1yr.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_1yr, width='stretch')
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chart F2 — Median days with p25–p75 band
    fig_med = go.Figure()
    # Shaded band: p25–p75
    fig_med.add_trace(go.Scatter(
        x=list(cf['filing_year'].astype(str)) + list(cf['filing_year'].astype(str))[::-1],
        y=list(cf['p75_days']) + list(cf['p25_days'])[::-1],
        fill='toself', fillcolor='rgba(244,163,0,0.13)',
        line=dict(color='rgba(0,0,0,0)'),
        hoverinfo='skip', showlegend=True, name='Middle 50% of cases'
    ))
    # Median line
    fig_med.add_trace(go.Scatter(
        x=cf['filing_year'].astype(str), y=cf['median_days'],
        mode='lines+markers+text',
        line=dict(color=NAVY, width=3),
        marker=dict(size=10, color=AMBER, line=dict(color=NAVY, width=2)),
        text=cf['median_days'].apply(lambda x: f"{x}d"),
        textposition='top center', textfont_size=12,
        hovertemplate='Filed %{x}<br>Median: %{y} days<br><i>(resolved cases only)</i><extra></extra>',
        showlegend=True, name='Median days'
    ))
    fig_med.update_layout(**chart_layout(
        height=430, showlegend=True,
        title="Median Days to Resolution by Filing Year — with Middle 50% Range",
        xaxis_title="Year Case Was Filed",
        yaxis_title="Days to Resolution",
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(l=20, r=20, t=70, b=25)
    ))
    fig_med.update_xaxes(showgrid=False)
    fig_med.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_med, width='stretch')
    
    st.markdown("""<div class="insight">
    📌 <strong>The shaded band</strong> shows the middle 50% of cases (25th–75th percentile).
    A wider band means more spread — more inconsistency in how long cases within that year
    took. Earlier cohorts have wider bands partly because they include more resolved cases
    across the full range of speeds. The trend in median is downward, but interpret
    2018–2019 with caution given the survivorship issue above.
    </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chart F3 — Disposal by calendar year
    st.markdown("#### In which years were the most cases actually concluded?")
    disp_yr = dff.groupby('disposal_year').size().reset_index(name='count')
    fig_disp = px.bar(
        disp_yr, x='disposal_year', y='count',
        color_discrete_sequence=[BLUE],
        text='count',
        labels={'disposal_year': 'Year of Judgment', 'count': 'Cases Resolved'},
        title="Cases Resolved Per Calendar Year (year of final judgment)"
    )
    fig_disp.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig_disp.update_layout(**chart_layout(
        height=380,
        xaxis_title="Year of Final Judgment",
        yaxis_title="Cases Resolved",
        yaxis_range=[0, disp_yr['count'].max() * 1.2],
        xaxis=dict(tickmode='linear', dtick=1),
        margin=dict(l=20, r=20, t=60, b=25)
    ))
    fig_disp.update_xaxes(showgrid=False)
    fig_disp.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_disp, width='stretch')
    st.caption("Note: The 2021 bar is very low — the data snapshot ends in the first week of January 2021.")

    pass

with tab3:
    # ╔══════════════════════════════════════════════════════════════════════════╗
    # ║  BLOCK G — Tab 3: Court-Level Variation                                 ║
    # ╚══════════════════════════════════════════════════════════════════════════╝
    
    st.markdown('<p class="stab-title">One court complex, very different experiences</p>',
                unsafe_allow_html=True)
    st.markdown(
        '<p class="stab-sub">All cases were heard at the Principal Bench, Bengaluru — '
        'same building, same case type (MFA First Appeals), different court hall numbers. '
        'The variation across halls is therefore a within-system comparison.</p>',
        unsafe_allow_html=True)
    
    st.markdown("""<div class="warn">
    ⚠️ <strong>Not a ranking or performance scorecard.</strong>
    Court halls receive different mixes of cases in terms of complexity and parties involved.
    Judges are transferred; bench composition changes. What we observe is that the
    <em>range</em> of resolution times within the same court complex is large —
    a system-level observation, not an accusation against any hall or individual.
    </div>""", unsafe_allow_html=True)
    
    # Build court stats — halls with 50+ cases
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
    📌 <strong>The headline:</strong>
    Among {len(cs)} court halls with 50+ resolved cases, the fastest had a median of
    <strong>{vmin} days</strong> and the slowest <strong>{vmax} days</strong> —
    a <strong>{ratio}× difference</strong> for the same case type, same court complex.
    </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chart G1 — Sorted bar all qualifying halls
    fig_bar = px.bar(
        cs, x='court_label', y='median_days',
        color='median_days',
        color_continuous_scale=[TEAL, AMBER, CORAL, '#c0392b'],
        text=cs['median_days'].apply(lambda x: f"{int(x)}d"),
        labels={'court_label': 'Court Hall', 'median_days': 'Median Days'},
        title=(
            "Median Resolution Time by Court Hall<br>"
            "<sup>Halls with 50+ cases · Sorted fastest → slowest · "
            "All cases: MFA First Appeals, Principal Bench Bengaluru</sup>"
        )
    )
    fig_bar.update_traces(textposition='outside', textfont_size=10)
    fig_bar.update_layout(**chart_layout(
        height=500, coloraxis_showscale=False,
        xaxis_title="Court Hall Number",
        yaxis_title="Median Days to Resolution",
        xaxis_tickangle=-45,
        yaxis_range=[0, cs['median_days'].max() * 1.2],
        margin=dict(l=20, r=20, t=90, b=80)
    ))
    fig_bar.update_xaxes(showgrid=False)
    fig_bar.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_bar, width='stretch')
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chart G2 — Scatter: caseload vs resolution
    st.markdown("#### Is a heavier caseload linked to slower resolution?")
    corr = round(float(np.corrcoef(cs['n_cases'], cs['median_days'])[0,1]), 2)
    
    fig_sc = px.scatter(
        cs, x='n_cases', y='median_days',
        size='n_cases', size_max=45,
        color='median_days',
        color_continuous_scale=[TEAL, AMBER, CORAL, '#c0392b'],
        hover_name='court_label',
        hover_data={'court_hall': True, 'n_cases': ':.0f', 'median_days': ':.0f'},
        labels={'n_cases': 'Cases Handled', 'median_days': 'Median Days'},
        title=(
            "Caseload vs. Median Resolution Time<br>"
            "<sup>Each bubble = one court hall · Bubble size ∝ case volume</sup>"
        )
    )
    x_line = np.linspace(cs['n_cases'].min(), cs['n_cases'].max(), 100)
    z = np.polyfit(cs['n_cases'], cs['median_days'], 1)
    fig_sc.add_trace(go.Scatter(
        x=x_line, y=np.polyval(z, x_line),
        mode='lines', name='Trend',
        line=dict(color=NAVY, width=1.5, dash='dot'),
        showlegend=True
    ))
    fig_sc.update_layout(**chart_layout(
        height=460, coloraxis_showscale=False, showlegend=True,
        xaxis_title='Cases Handled', yaxis_title='Median Days to Resolution',
        legend=dict(x=0.01, y=0.98),
        margin=dict(l=20, r=20, t=80, b=25)
    ))
    fig_sc.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
    fig_sc.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_sc, width='stretch')
    
    if abs(corr) <= 0.15:
        corr_text = "near zero — caseload alone does not explain resolution speed in this dataset"
    elif 0.15 < corr <= 0.4:
        corr_text = "weak positive — halls with more cases tend to take slightly longer, but the relationship is not strong"
    elif corr > 0.4:
        corr_text = "moderate positive — higher caseload is associated with longer resolution times"
    else:
        corr_text = "negative — larger halls resolved cases faster on median, possibly reflecting specialised benches"
    
    st.markdown(f"""<div class="insight">
    📌 <strong>Correlation: {corr}</strong> ({corr_text}).
    The dotted line is a simple linear trend. Points far above it are halls that
    are slower than their caseload would suggest; points below are faster.
    </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chart G3 — Box plot spread by filing year
    st.markdown("#### How consistent were outcomes within each filing year?")
    fig_box = px.box(
        dff, x='filing_year', y='disposal_days',
        color='filing_year',
        color_discrete_sequence=[TEAL, BLUE, AMBER, CORAL, '#c0392b'],
        labels={'disposal_days': 'Days to Resolution', 'filing_year': 'Filing Year'},
        title=(
            "Spread of Resolution Times by Filing Year<br>"
            "<sup>Box = middle 50% · Line = median · Whiskers extend to 1.5× IQR</sup>"
        ),
        points=False
    )
    fig_box.update_layout(**chart_layout(
        height=430,
        xaxis_title="Filing Year", yaxis_title="Days to Resolution",
        margin=dict(l=20, r=20, t=80, b=25)
    ))
    fig_box.update_xaxes(showgrid=False, type='category')
    fig_box.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_box, width='stretch')

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
