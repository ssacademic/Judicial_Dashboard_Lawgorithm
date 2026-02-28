# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  JUSTICE BY THE NUMBERS — Karnataka High Court                          ║
# ║  A Lawgorithm Initiative  |  app.py  |  v2                              ║
# ╚══════════════════════════════════════════════════════════════════════════╝

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Justice by the Numbers | Karnataka HC",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.main  { background-color: #f4f6f9; }
.block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1200px; }
#MainMenu, footer { visibility: hidden; }

/* Header */
.main-header {
    background: linear-gradient(135deg, #1a2744 0%, #2d4270 100%);
    border-radius: 14px; padding: 2rem 2.5rem; margin-bottom: 1.2rem;
}
.main-header h1  { font-size: 1.85rem; font-weight: 700; margin: 0; color: white !important; }
.main-header .sub { font-size: 0.97rem; opacity: 0.78; margin-top: 0.4rem; color: white !important; }
.main-header .tag { font-size: 0.72rem; opacity: 0.48; margin-top: 0.9rem;
    text-transform: uppercase; letter-spacing: 0.12em; color: white !important; }

/* KPI cards */
.kpi { background: white; border-radius: 12px; padding: 1.3rem 1.1rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06); border-top: 4px solid #f4a300; }
.kpi.t  { border-top-color: #2a9d8f; }
.kpi.c  { border-top-color: #e76f51; }
.kpi.b  { border-top-color: #457b9d; }
.kpi-n  { font-size: 1.9rem; font-weight: 700; color: #1a2744; margin: 0; line-height: 1.1; }
.kpi-l  { font-size: 0.75rem; color: #888; margin-top: 0.25rem;
    text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600; }
.kpi-s  { font-size: 0.78rem; color: #aaa; margin-top: 0.15rem; }

/* Caveat & insight boxes */
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

/* Section titles inside tabs */
.stab-title { font-size: 1.3rem; font-weight: 700; color: #1a2744;
    margin-bottom: 0.2rem; margin-top: 0.4rem; }
.stab-sub   { font-size: 0.9rem; color: #666; margin-bottom: 1rem; }

/* Footer */
.footer {
    background: #1a2744; color: #8fa8c8; border-radius: 14px;
    padding: 2rem 2.5rem; margin-top: 2.5rem; font-size: 0.83rem; line-height: 1.95;
}
.footer h4 { color: #fff; margin-bottom: 0.3rem; font-size: 0.93rem; }
.footer a  { color: #f4a300; text-decoration: none; }
</style>
""", unsafe_allow_html=True)


# ── DATA LOAD ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df     = pd.read_csv('data/processed_cases.csv',
                         parse_dates=['date_filed', 'decision_date'])
    cohort = pd.read_csv('data/cohort_stats.csv')
    return df, cohort

df, cohort_df = load_data()

# ── PALETTE ───────────────────────────────────────────────────────────────────
NAVY, AMBER, TEAL, CORAL, BLUE = '#1a2744', '#f4a300', '#2a9d8f', '#e76f51', '#457b9d'
SPEED_COLORS = {
    "Fast (under 1 year)":   TEAL,
    "Medium (1–2 years)":    AMBER,
    "Slow (2–3 years)":      CORAL,
    "Very Slow (3+ years)":  '#c0392b',
}
CHART_DEFAULTS = dict(
    plot_bgcolor='white', paper_bgcolor='white',
    font_family='Inter', font_color=NAVY,
    margin=dict(l=20, r=20, t=55, b=25)
)


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
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
        "This affects all charts. Default: all years (2015–2019)."
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

# Apply filter
mask = (df['filing_year'] >= year_range[0]) & (df['filing_year'] <= year_range[1])
dff  = df[mask].copy()
cf   = cohort_df[
    (cohort_df['filing_year'] >= year_range[0]) &
    (cohort_df['filing_year'] <= year_range[1])
].copy()


# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="main-header">
  <h1>⚖️ Justice by the Numbers</h1>
  <p class="sub">
    An independent analysis of <strong>{len(dff):,} resolved appeals</strong>
    from the Karnataka High Court (Principal Bench, Bengaluru) &nbsp;·&nbsp;
    Filing years {year_range[0]}–{year_range[1]} &nbsp;·&nbsp; Data snapshot: Jan 2021
  </p>
  <p class="tag">A Lawgorithm Initiative &nbsp;|&nbsp; Data: NJDG via ISDM Hackathon
    &nbsp;|&nbsp; Case type: MFA (First Appeals)</p>
</div>
""", unsafe_allow_html=True)

# ── CAVEAT — always visible above tabs ───────────────────────────────────────
st.markdown("""
<div class="caveat">
  ⚠️ <strong>What this data is — and isn't:</strong>
  This dashboard covers only <strong>resolved (disposed) cases</strong>.
  Cases still pending at the time of the data snapshot (January 2021) are not included.
  All insights describe cases that <em>reached a conclusion</em> — not the full picture of
  how the system performs today.
  Outcome details are recorded for only <strong>26% of cases</strong>; those charts are
  clearly marked. Court-level variation reflects differences in caseload, bench composition,
  and case complexity — not individual performance.
</div>
""", unsafe_allow_html=True)

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
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
        <p class="kpi-s">≈ {round(med/365.25, 1)} years &nbsp;·&nbsp;
            half took less, half took more</p>
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


# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "⏱️  How Long Does It Take?",
    "📅  Trends Over Time",
    "🏛️  Court-Level Variation",
    "📋  Outcomes & Patterns",
])


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TAB 1 — HOW LONG DOES IT TAKE?                                             ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
with tab1:
    st.markdown('<p class="stab-title">How long did resolved appeals take?</p>',
                unsafe_allow_html=True)
    st.markdown(
        '<p class="stab-sub">Distribution of time between case filing and final judgment, '
        'for all resolved cases in this dataset.</p>',
        unsafe_allow_html=True)

    # ── Chart 1: Histogram ──────────────────────────────────────────────────
    fig_hist = px.histogram(
        dff, x='disposal_days', nbins=60,
        color_discrete_sequence=[NAVY],
        labels={'disposal_days': 'Days from Filing to Judgment', 'count': 'Number of Cases'},
        title="Distribution of Resolution Times (days)"
    )
    for val, lbl, col in [
        (p25, f"Fastest 25%: {p25}d",  TEAL),
        (med, f"Median: {med}d",        AMBER),
        (p75, f"Slowest 25% starts: {p75}d", CORAL),
    ]:
        fig_hist.add_vline(
            x=val, line_dash="dash", line_color=col, line_width=2.5,
            annotation_text=f" {lbl}", annotation_font_color=col,
            annotation_position="top left", annotation_font_size=12
        )
    fig_hist.update_layout(
        **CHART_DEFAULTS, height=420, showlegend=False,
        xaxis_title="Days from Filing to Judgment",
        yaxis_title="Number of Cases", title_font_size=15
    )
    fig_hist.update_xaxes(showgrid=False)
    fig_hist.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown(f"""<div class="insight">
    📌 <strong>Reading this chart:</strong>
    Each bar is a group of cases that took roughly the same number of days to resolve.
    The dashed lines show key thresholds.
    The median ({med} days, ~{round(med/365.25,1)} years) means half of all resolved
    cases finished faster, half slower.
    The long right tail shows a smaller but real group of cases that took 5–6 years.
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chart 2: Speed tiers ────────────────────────────────────────────────
    st.markdown("#### How do the numbers break down into plain categories?")

    tier_order = [
        "Fast (under 1 year)", "Medium (1–2 years)",
        "Slow (2–3 years)", "Very Slow (3+ years)"
    ]
    tier_vals  = (
        dff['speed_tier'].value_counts()
        .reindex(tier_order).fillna(0).astype(int).reset_index()
    )
    tier_vals.columns = ['tier', 'count']
    tier_vals['pct']   = (100 * tier_vals['count'] / len(dff)).round(1)
    tier_vals['color'] = tier_vals['tier'].map(SPEED_COLORS)
    tier_vals['label'] = tier_vals.apply(
        lambda r: f"{r['tier']}<br>{r['count']:,} cases ({r['pct']}%)", axis=1
    )

    fig_tiers = px.bar(
        tier_vals, x='tier', y='count',
        color='tier',
        color_discrete_map=SPEED_COLORS,
        text=tier_vals['pct'].apply(lambda x: f"{x}%"),
        labels={'tier': '', 'count': 'Number of Cases'},
        title="Resolved Cases by Resolution Speed"
    )
    fig_tiers.update_traces(textposition='outside', textfont_size=13)
    fig_tiers.update_layout(
        **CHART_DEFAULTS, height=400, showlegend=False,
        title_font_size=15,
        xaxis_title="", yaxis_title="Number of Cases",
        yaxis_range=[0, tier_vals['count'].max() * 1.18]
    )
    fig_tiers.update_xaxes(showgrid=False)
    fig_tiers.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_tiers, use_container_width=True)

    st.markdown(f"""<div class="insight">
    📌 <strong>What this tells a litigant:</strong>
    Among the cases that did get resolved —
    <strong>{pfast}% were done within a year</strong>,
    and <strong>35.1% took 1–2 years</strong>.
    Together, nearly two-thirds of resolved cases finished within 2 years.
    The remaining third split between 2–3 years (17.7%) and over 3 years ({pslow}%).
    Remember: this is only the population of <em>cases that have been resolved</em>.
    Cases still pending are not reflected.
    </div>""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TAB 2 — TRENDS OVER TIME                                                   ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
with tab2:
    st.markdown('<p class="stab-title">Are cases getting resolved faster over time?</p>',
                unsafe_allow_html=True)
    st.markdown(
        '<p class="stab-sub">Each bar represents one filing-year cohort. '
        'We measure what share of that cohort was resolved within a fixed time window '
        '— the only fair way to compare across years.</p>',
        unsafe_allow_html=True)

    st.markdown("""<div class="warn">
    ⚠️ <strong>Survivorship caveat — read before interpreting:</strong>
    Cases filed in 2019 had only ~2 years to be resolved before this dataset was collected
    (January 2021). Slow 2019 cases were still pending and are <em>not in our dataset</em>,
    so the 2019 cohort looks faster partly by selection, not only by genuine improvement.
    Earlier cohorts (2015, 2016) are more complete because they had 5–6 years to resolve.
    Treat the trend direction as plausible; treat the magnitude — especially for 2019 —
    as a <strong>lower bound estimate</strong>, not a reliable measure.
    </div>""", unsafe_allow_html=True)

    # ── Chart 1: % within 1 year ────────────────────────────────────────────
    fig_1yr = go.Figure()
    fig_1yr.add_trace(go.Bar(
        x=cf['filing_year'].astype(str),
        y=cf['pct_within_1yr'],
        marker_color=TEAL,
        text=cf['pct_within_1yr'].apply(lambda x: f"{x}%"),
        textposition='outside',
        hovertemplate=(
            'Filed in %{x}<br>'
            '%{y}% resolved within 1 year<br>'
            '<i>(of cases in this dataset)</i><extra></extra>'
        )
    ))
    fig_1yr.update_layout(
        **CHART_DEFAULTS, height=400, showlegend=False,
        title="% of Each Filing-Year Cohort Resolved Within 1 Year",
        title_font_size=15,
        xaxis_title="Year Case Was Filed",
        yaxis_title="% Resolved Within 1 Year",
        yaxis_range=[0, min(cf['pct_within_1yr'].max() * 1.3, 100)]
    )
    fig_1yr.update_xaxes(showgrid=False)
    fig_1yr.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_1yr, use_container_width=True)

    # ── Chart 2: median days by cohort ──────────────────────────────────────
    fig_med = go.Figure()
    fig_med.add_trace(go.Scatter(
        x=cf['filing_year'].astype(str),
        y=cf['median_days'],
        mode='lines+markers+text',
        line=dict(color=NAVY, width=3),
        marker=dict(size=10, color=AMBER, line=dict(color=NAVY, width=2)),
        text=cf['median_days'].apply(lambda x: f"{x}d"),
        textposition='top center', textfont_size=12,
        hovertemplate=(
            'Filed in %{x}<br>'
            'Median: %{y} days<br>'
            '<i>(of resolved cases only)</i><extra></extra>'
        )
    ))
    # Shaded band: p25 to p75
    fig_med.add_trace(go.Scatter(
        x=pd.concat([cf['filing_year'].astype(str),
                     cf['filing_year'].astype(str).iloc[::-1]]),
        y=pd.concat([cf['p75_days'], cf['p25_days'].iloc[::-1]]),
        fill='toself',
        fillcolor='rgba(244,163,0,0.12)',
        line=dict(color='rgba(0,0,0,0)'),
        hoverinfo='skip',
        name='Middle 50% range'
    ))
    fig_med.update_layout(
        **CHART_DEFAULTS, height=420, showlegend=False,
        title="Median Days to Resolution by Filing Year<br>"
              "<sup>Shaded band = middle 50% of cases (25th–75th percentile)</sup>",
        title_font_size=15,
        xaxis_title="Year Case Was Filed",
        yaxis_title="Days to Resolution"
    )
    fig_med.update_xaxes(showgrid=False)
    fig_med.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_med, use_container_width=True)

    st.markdown("""<div class="insight">
    📌 <strong>The pattern:</strong>
    Earlier cohorts (2015, 2016) show longer median resolution times, and their 25th–75th
    percentile band is wider — meaning more spread in outcomes.
    Later cohorts appear faster and tighter, but this is partly because the slowest cases
    from those years had not yet been resolved when this snapshot was taken.
    The shaded band shows the middle 50% of cases for each year — a wider band means
    more inconsistency in how long cases took.
    </div>""", unsafe_allow_html=True)

    # ── Chart 3: Disposal year (when cases actually concluded) ──────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### When were cases actually being resolved? (by calendar year of judgment)")
    disp_yr = dff.groupby('disposal_year').size().reset_index(name='count')
    fig_disp = px.bar(
        disp_yr, x='disposal_year', y='count',
        color_discrete_sequence=[BLUE],
        text='count',
        labels={'disposal_year': 'Year of Judgment', 'count': 'Cases Resolved'},
        title="Cases Resolved Per Calendar Year"
    )
    fig_disp.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig_disp.update_layout(
        **CHART_DEFAULTS, height=380, showlegend=False, title_font_size=15,
        xaxis_title="Year of Final Judgment", yaxis_title="Cases Resolved",
        yaxis_range=[0, disp_yr['count'].max() * 1.18],
        xaxis=dict(tickmode='linear', dtick=1)
    )
    fig_disp.update_xaxes(showgrid=False)
    fig_disp.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_disp, use_container_width=True)

    st.caption(
        "Note: The 2021 bar is low because the data snapshot ends January 2021 — "
        "only a week of 2021 data is captured."
    )


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TAB 3 — COURT-LEVEL VARIATION                                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
with tab3:
    st.markdown('<p class="stab-title">One court complex, very different experiences</p>',
                unsafe_allow_html=True)
    st.markdown(
        '<p class="stab-sub">All 20,646 cases were heard at the Principal Bench, Bengaluru '
        '— same building, same case type (MFA First Appeals), different court hall numbers. '
        'The variation in resolution times across halls is therefore a meaningful '
        'within-system comparison.</p>',
        unsafe_allow_html=True)

    st.markdown("""<div class="warn">
    ⚠️ <strong>This is not a ranking or a performance scorecard.</strong>
    Court halls receive different mixes of cases — some more complex, some with more
    parties involved. Judges are transferred between halls. Benches change composition.
    What we can say is that the <em>range</em> of outcomes within the same court complex
    is large — and that is a system-level observation, not an accusation.
    </div>""", unsafe_allow_html=True)

    # Court stats: halls with 50+ cases
    cs = (
        dff.groupby('court_number')['disposal_days']
        .agg(median_days='median', n_cases='count',
             p25='quantile', p75=lambda x: x.quantile(0.75))
        .reset_index()
    )
    cs.columns = ['court_hall', 'median_days', 'n_cases', 'p25', 'p75']
    cs = cs[cs['n_cases'] >= 50].sort_values('median_days').reset_index(drop=True)
    cs['court_label'] = 'Hall ' + cs['court_hall'].astype(int).astype(str)

    vmin  = int(cs['median_days'].min())
    vmax  = int(cs['median_days'].max())
    ratio = round(vmax / vmin, 1)

    st.markdown(f"""<div class="insight">
    📌 <strong>The headline number:</strong>
    Among {len(cs)} court halls with 50+ resolved cases,
    the fastest had a median of <strong>{vmin} days</strong>
    and the slowest <strong>{vmax} days</strong> —
    a <strong>{ratio}× difference</strong>
    for the same case type within the same court complex.
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chart 1: Sorted bar — all qualifying halls ───────────────────────────
    fig_bar = px.bar(
        cs, x='court_label', y='median_days',
        color='median_days',
        color_continuous_scale=[TEAL, AMBER, CORAL, '#c0392b'],
        text=cs['median_days'].apply(lambda x: f"{int(x)}d"),
        labels={'court_label': 'Court Hall', 'median_days': 'Median Days to Resolution'},
        title=f"Median Resolution Time by Court Hall<br>"
              f"<sup>Halls with 50+ cases | Sorted fastest → slowest | "
              f"All cases: MFA First Appeals, Principal Bench Bengaluru</sup>"
    )
    fig_bar.update_traces(textposition='outside', textfont_size=10)
    fig_bar.update_layout(
        **CHART_DEFAULTS,
        height=480, showlegend=False, coloraxis_showscale=False,
        title_font_size=14,
        xaxis_title="Court Hall Number", yaxis_title="Median Days to Resolution",
        xaxis_tickangle=-45,
        yaxis_range=[0, cs['median_days'].max() * 1.18],
        margin=dict(l=20, r=20, t=80, b=60)
    )
    fig_bar.update_xaxes(showgrid=False)
    fig_bar.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chart 2: Scatter — caseload vs resolution time ───────────────────────
    st.markdown("#### Is a heavier caseload associated with slower resolution?")
    fig_sc = px.scatter(
        cs, x='n_cases', y='median_days',
        size='n_cases', size_max=45,
        color='median_days',
        color_continuous_scale=[TEAL, AMBER, CORAL, '#c0392b'],
        hover_data={'court_hall': True, 'n_cases': ':.0f', 'median_days': ':.0f'},
        hover_name='court_label',
        labels={
            'n_cases':     'Cases Handled (count)',
            'median_days': 'Median Days to Resolution'
        },
        title="Caseload vs. Median Resolution Time<br>"
              "<sup>Each bubble = one court hall | Bubble size = case volume</sup>"
    )
    # Add trend line
    z = np.polyfit(cs['n_cases'], cs['median_days'], 1)
    x_line = np.linspace(cs['n_cases'].min(), cs['n_cases'].max(), 100)
    fig_sc.add_trace(go.Scatter(
        x=x_line, y=np.polyval(z, x_line),
        mode='lines',
        line=dict(color=NAVY, width=1.5, dash='dot'),
        name='Trend', showlegend=True
    ))
    fig_sc.update_layout(
        **CHART_DEFAULTS,
        height=460, coloraxis_showscale=False, title_font_size=14,
        xaxis_title='Cases Handled (count)',
        yaxis_title='Median Days to Resolution',
        legend=dict(x=0.01, y=0.98)
    )
    fig_sc.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
    fig_sc.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_sc, use_container_width=True)

    # Quick correlation note
    corr = round(cs['n_cases'].corr(cs['median_days']), 2)
    st.markdown(f"""<div class="insight">
    📌 <strong>Correlation between caseload and resolution time: {corr}</strong>
    {'(weak positive — higher caseload halls tend to take slightly longer, but the relationship is not strong)'
      if 0 < corr <= 0.4
      else '(moderate positive — higher caseload is associated with longer resolution times)'
      if corr > 0.4
      else '(near zero — no clear relationship between caseload and resolution speed in this dataset)'
      if abs(corr) <= 0.1
      else '(negative — higher caseload halls actually resolved cases faster on median, possibly reflecting specialised or efficient benches)'}.
    The dotted trend line is a simple linear fit.
    </div>""", unsafe_allow_html=True)

    # ── Chart 3: Box plot — spread by filing year ────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### How wide is the spread of outcomes within each filing year?")
    fig_box = px.box(
        dff, x='filing_year', y='disposal_days',
        color='filing_year',
        color_discrete_sequence=[TEAL, BLUE, AMBER, CORAL, '#c0392b'],
        labels={'disposal_days': 'Days to Resolution', 'filing_year': 'Filing Year'},
        title="Range of Resolution Times by Filing Year<br>"
              "<sup>Box = middle 50% of cases | Line = median | Whiskers = 5th–95th percentile</sup>",
        points=False
    )
    fig_box.update_layout(
        **CHART_DEFAULTS, height=420, showlegend=False, title_font_size=14,
        xaxis_title="Filing Year", yaxis_title="Days to Resolution"
    )
    fig_box.update_xaxes(showgrid=False, type='category')
    fig_box.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_box, use_container_width=True)


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TAB 4 — OUTCOMES & PATTERNS                                                ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
with tab4:
    st.markdown('<p class="stab-title">What happened when cases were resolved?</p>',
                unsafe_allow_html=True)
    st.markdown(
        '<p class="stab-sub">Two separate analyses: case outcomes (where data exists) '
        'and filing seasonality (available for all cases).</p>',
        unsafe_allow_html=True)

    st.markdown("""<div class="warn">
    ⚠️ <strong>Outcome data is recorded for only 26.3% of cases (5,420 of 20,646).</strong>
    The charts below cover only those cases. They are <strong>illustrative</strong> —
    do not treat percentages here as representative of all appeals.
    The 73.7% with no outcome data is a data quality issue in the source (NJDG), not
    something this dashboard can resolve.
    </div>""", unsafe_allow_html=True)

    # ── Chart 1: Outcome bar ──────────────────────────────────────────────────
    outcome_known = dff[dff['outcome_bucket'] != 'Data Not Available']
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
        title=f"Case Outcomes — based on {len(outcome_known):,} cases with recorded outcomes<br>"
              f"<sup>Remaining {len(dff)-len(outcome_known):,} cases have no outcome in source data</sup>"
    )
    fig_oc.update_traces(textposition='outside', textfont_size=12)
    fig_oc.update_layout(
        **CHART_DEFAULTS, height=420, showlegend=False, title_font_size=14,
        xaxis_title="Number of Cases", yaxis_title="",
        xaxis_range=[0, oc['count'].max() * 1.28],
        margin=dict(l=20, r=60, t=80, b=25)
    )
    fig_oc.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
    fig_oc.update_yaxes(showgrid=False)
    st.plotly_chart(fig_oc, use_container_width=True)

    st.markdown("""<div class="insight">
    📌 <strong>Reading outcomes carefully:</strong>
    "Disposed — Manner Not Recorded" is the single largest category even among
    cases that do have outcome data. This means the case was closed but
    <em>how</em> it was closed was not recorded.
    Of cases with a meaningful outcome: Partly Allowed (1,258), Dismissed/Rejected (1,270),
    and Fully Allowed (113) are the main categories.
    "Allowed & Sent Back to Lower Court" means the High Court found merit but
    referred the matter back for fresh consideration — not a final win for either party.
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chart 2: Outcome by contested vs uncontested ──────────────────────────
    st.markdown("#### Contested vs. Uncontested cases — in the data we have")
    cont_oc = (
        dff[dff['contested_label'] != 'Not Recorded']
        .groupby(['contested_label', 'outcome_bucket'])
        .size().reset_index(name='count')
    )
    cont_oc = cont_oc[cont_oc['outcome_bucket'] != 'Data Not Available']

    if not cont_oc.empty:
        fig_cont = px.bar(
            cont_oc, x='contested_label', y='count',
            color='outcome_bucket',
            barmode='group',
            labels={'contested_label': '', 'count': 'Cases', 'outcome_bucket': 'Outcome'},
            title="Outcome Breakdown: Contested vs. Uncontested<br>"
                  "<sup>Only cases where both contested status AND outcome are recorded</sup>",
            color_discrete_sequence=[TEAL, BLUE, AMBER, CORAL, '#8e44ad', NAVY]
        )
        fig_cont.update_layout(
            **CHART_DEFAULTS, height=400, title_font_size=14,
            xaxis_title="", yaxis_title="Number of Cases",
            legend_title="Outcome"
        )
        fig_cont.update_xaxes(showgrid=False)
        fig_cont.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
        st.plotly_chart(fig_cont, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chart 3: Monthly filing heatmap ──────────────────────────────────────
    st.markdown("#### When are cases filed? (available for all 20,646 cases)")
    monthly = dff.groupby(['filing_year', 'filing_month']).size().reset_index(name='count')
    pivot   = monthly.pivot(
        index='filing_year', columns='filing_month', values='count'
    ).fillna(0)
    mnames  = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
               7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
    pivot.columns = [mnames.get(c, str(c)) for c in pivot.columns]

    fig_heat = px.imshow(
        pivot, aspect='auto',
        color_continuous_scale=['#eef2ff', NAVY],
        labels=dict(x="Month", y="Filing Year", color="Cases Filed"),
        title="Monthly Filing Volume by Year<br>"
              "<sup>Darker = more filings | Based on all 20,646 resolved cases</sup>"
    )
    fig_heat.update_layout(
        **CHART_DEFAULTS, height=380, title_font_size=14,
        margin=dict(l=60, r=20, t=80, b=25)
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("""<div class="insight">
    📌 <strong>Seasonality context:</strong>
    Filing volumes by month can reflect court calendar patterns — courts typically
    have vacation periods (summer, Diwali, Christmas) which can compress filings
    into peak months either side of the break.
    These patterns are useful context for litigants timing their filings, and
    for administrators planning court resources.
    </div>""", unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  <h4>📖 About This Dashboard</h4>
  <p>
  An initiative by <strong>Lawgorithm</strong> to make judicial data legible
  to citizens, researchers, and policy stakeholders.<br><br>

  <strong>Data:</strong> National Judicial Data Grid (NJDG), Karnataka High Court
  (Principal Bench, Bengaluru), accessed via ISDM Hackathon dataset.
  Covers <strong>MFA (First Appeals)</strong> filed 2015–2019 and resolved by
  January 2021. Total: {len(df):,} cases after data cleaning.<br><br>

  <strong>Case type — MFA:</strong> All {len(df):,} cases are classified as
  MFA (Miscellaneous First Appeal / First Appeal) in the NJDG source.
  Subject-matter details (the underlying legal act) are recorded for only 1.6%
  of cases. Of those, Motor Vehicles Act cases are the majority — but we make
  no claim about the remaining 98.4%.<br><br>

  <strong>Survivorship bias:</strong> This dataset covers only resolved cases.
  Appeals still pending as of January 2021 are not included.
  All statistics describe the population of completed cases, not current court performance.<br><br>

  <strong>Court-level variation:</strong> Court hall numbers are internal NJDG
  identifiers. Variation in resolution times across halls reflects differences
  in case complexity, bench composition, and workload — not individual performance.
  No hall is named, ranked, or implicated.<br><br>

  <strong>Useful resources:</strong><br>
  🔗 <a href="https://njdg.ecourts.gov.in" target="_blank">NJDG Live Portal</a>
     — National live pendency and disposal data<br>
  🔗 <a href="https://ecourts.gov.in" target="_blank">eCourts Services</a>
     — Track any case by CNR number<br>
  🔗 <a href="https://dakshindia.org" target="_blank">DAKSH India</a>
     — Independent judicial data research<br>
  🔗 <a href="https://vidhilegalpolicy.in" target="_blank">Vidhi Centre for Legal Policy</a>
     — Justice reform and legal policy research<br><br>

  <em>Built by Lawgorithm &nbsp;|&nbsp; Data: NJDG / ISDM &nbsp;|&nbsp;
  For questions: contact Lawgorithm</em>
  </p>
</div>
""", unsafe_allow_html=True)
