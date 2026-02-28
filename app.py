# ╔══════════════════════════════════════════════════════════════════════╗
# ║  JUSTICE BY THE NUMBERS — Karnataka High Court                      ║
# ║  A Lawgorithm Initiative | app.py                                   ║
# ╚══════════════════════════════════════════════════════════════════════╝

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

# ── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.main { background-color: #f4f6f9; }
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1200px; }
#MainMenu, footer { visibility: hidden; }

.main-header {
    background: linear-gradient(135deg, #1a2744 0%, #2d4270 100%);
    color: white; border-radius: 14px; padding: 2rem 2.5rem; margin-bottom: 1.5rem;
}
.main-header h1 { font-size: 1.9rem; font-weight: 700; margin: 0; color: white !important; }
.main-header .subtitle { font-size: 1rem; opacity: 0.8; margin-top: 0.4rem; color: white !important; }
.main-header .byline { font-size: 0.75rem; opacity: 0.5; margin-top: 1rem;
    text-transform: uppercase; letter-spacing: 0.1em; color: white !important; }

.kpi-card {
    background: white; border-radius: 12px; padding: 1.4rem 1.2rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06); border-top: 4px solid #f4a300;
}
.kpi-card.teal  { border-top-color: #2a9d8f; }
.kpi-card.coral { border-top-color: #e76f51; }
.kpi-card.blue  { border-top-color: #457b9d; }
.kpi-num   { font-size: 2rem; font-weight: 700; color: #1a2744; margin: 0; line-height: 1.1; }
.kpi-label { font-size: 0.78rem; color: #888; margin-top: 0.3rem;
    text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600; }
.kpi-sub   { font-size: 0.8rem; color: #aaa; margin-top: 0.15rem; }

.caveat {
    background: #fffbea; border: 1.5px solid #f4a300; border-radius: 10px;
    padding: 1rem 1.3rem; font-size: 0.87rem; color: #5a4200; line-height: 1.65;
    margin-bottom: 1.5rem;
}
.insight {
    background: #eaf4fb; border-left: 4px solid #457b9d; border-radius: 0 8px 8px 0;
    padding: 0.9rem 1.2rem; font-size: 0.88rem; color: #1a2744; line-height: 1.6;
    margin: 0.8rem 0 1.2rem 0;
}
.sec-title { font-size: 1.4rem; font-weight: 700; color: #1a2744; margin-bottom: 0.2rem; }
.sec-sub   { font-size: 0.92rem; color: #666; margin-bottom: 1.1rem; }
.divider   { border: none; border-top: 2px solid #e8ebf0; margin: 2rem 0; }
.footer {
    background: #1a2744; color: #9fb0cc; border-radius: 14px;
    padding: 2rem 2.5rem; margin-top: 2rem; font-size: 0.84rem; line-height: 1.9;
}
.footer h4 { color: #fff; margin-bottom: 0.4rem; font-size: 0.95rem; }
.footer a  { color: #f4a300; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('data/processed_cases.csv',
                     parse_dates=['date_filed', 'decision_date'])
    cohort = pd.read_csv('data/cohort_stats.csv')
    return df, cohort

df, cohort_df = load_data()

# ── COLORS ───────────────────────────────────────────────────────────────────
NAVY, AMBER, TEAL, CORAL, BLUE = '#1a2744', '#f4a300', '#2a9d8f', '#e76f51', '#457b9d'
SPEED_COLORS = {
    "Fast (under 1 year)":          TEAL,
    "Medium (1–2 years)":           AMBER,
    "Slow (2–3 years)":             CORAL,
    "Very Slow (3+ years)":         '#c0392b',
}

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Filter Cases")
    years = sorted(df['filing_year'].unique())
    year_range = st.slider(
        "Filing year range",
        min_value=int(min(years)), max_value=int(max(years)),
        value=(int(min(years)), int(max(years))), step=1
    )
    st.markdown("---")
    st.markdown("""
**About this tool**

Built by **Lawgorithm** as a pro bono public interest initiative.

Data: NJDG Karnataka HC via ISDM Hackathon (2015–2021)

🔗 [eCourts — Track your case](https://ecourts.gov.in)
🔗 [NJDG Live Portal](https://njdg.ecourts.gov.in)
""")

# Apply filter
mask = (df['filing_year'] >= year_range[0]) & (df['filing_year'] <= year_range[1])
dff = df[mask].copy()

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="main-header">
  <h1>⚖️ Justice by the Numbers</h1>
  <p class="subtitle">
    An independent look at <strong>{len(dff):,} resolved Motor Accident Appeals</strong>
    from the Karnataka High Court — what they reveal about the journey to justice.
  </p>
  <p class="byline">A Lawgorithm initiative &nbsp;|&nbsp; Data: NJDG via ISDM Hackathon
     &nbsp;|&nbsp; Filing years {year_range[0]}–{year_range[1]}</p>
</div>
""", unsafe_allow_html=True)

# ── CAVEAT BANNER ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="caveat">
  ⚠️ <strong>What this data can and cannot tell you:</strong> This dashboard shows only
  <strong>cases that have already been resolved</strong> — not the thousands still waiting.
  All patterns here describe completed cases. Use these as <em>reference benchmarks</em>,
  not as measures of current court performance or guarantees about any specific case.
  Outcome records are incomplete for ~74% of cases; those charts are marked accordingly.
</div>
""", unsafe_allow_html=True)

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
med_days  = int(dff['disposal_days'].median())
pct_fast  = round(100 * (dff['speed_tier'] == "Fast (under 1 year)").sum() / len(dff), 1)
pct_slow  = round(100 * (dff['disposal_days'] > 730).sum() / len(dff), 1)
p25       = int(dff['disposal_days'].quantile(0.25))

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="kpi-card">
        <p class="kpi-num">{len(dff):,}</p>
        <p class="kpi-label">Resolved Cases Studied</p>
        <p class="kpi-sub">Motor Accident Appeals, Karnataka HC</p>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="kpi-card">
        <p class="kpi-num">{med_days:,} days</p>
        <p class="kpi-label">Median Time to Judgment</p>
        <p class="kpi-sub">~{round(med_days/365.25,1)} years — half took less, half took more</p>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="kpi-card teal">
        <p class="kpi-num">{pct_fast}%</p>
        <p class="kpi-label">Resolved Within 1 Year</p>
        <p class="kpi-sub">Fastest quartile: under {p25} days</p>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="kpi-card coral">
        <p class="kpi-num">{pct_slow}%</p>
        <p class="kpi-label">Took More Than 2 Years</p>
        <p class="kpi-sub">of all studied resolved cases</p>
    </div>""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# SECTION 1 — HOW LONG DOES JUSTICE TAKE?
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="sec-title">⏱️ How Long Does Justice Take?</p>', unsafe_allow_html=True)
st.markdown('<p class="sec-sub">Time from filing to final judgment, for all resolved Motor Accident Appeals in this dataset.</p>', unsafe_allow_html=True)

col_a, col_b = st.columns([3, 2])

with col_a:
    p50 = dff['disposal_days'].quantile(0.50)
    p75 = dff['disposal_days'].quantile(0.75)
    fig_hist = px.histogram(
        dff, x='disposal_days', nbins=60,
        color_discrete_sequence=[NAVY],
        title="Distribution of Days to Resolution",
        labels={'disposal_days': 'Days from Filing to Judgment'}
    )
    for val, lbl, col in [(p25, '25th percentile', TEAL),
                          (p50, 'Median',           AMBER),
                          (p75, '75th percentile',  CORAL)]:
        fig_hist.add_vline(x=val, line_dash="dash", line_color=col, line_width=2,
                           annotation_text=f" {lbl}: {int(val)}d",
                           annotation_font_color=col, annotation_position="top left")
    fig_hist.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        font_family='Inter', font_color=NAVY,
        height=340, showlegend=False, title_font_size=14,
        xaxis_title="Days from Filing to Judgment",
        yaxis_title="Number of Cases",
        margin=dict(l=20, r=20, t=50, b=20)
    )
    fig_hist.update_xaxes(showgrid=False)
    fig_hist.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_hist, use_container_width=True)

with col_b:
    tier_order = ["Fast (under 1 year)","Medium (1–2 years)","Slow (2–3 years)","Very Slow (3+ years)"]
    tier_vals  = dff['speed_tier'].value_counts().reindex(tier_order).dropna()
    fig_pie = go.Figure(go.Pie(
        labels=tier_vals.index, values=tier_vals.values,
        hole=0.52,
        marker_colors=[SPEED_COLORS[t] for t in tier_vals.index],
        textinfo='percent', textfont_size=12,
        hovertemplate='<b>%{label}</b><br>%{value:,} cases (%{percent})<extra></extra>'
    ))
    fig_pie.update_layout(
        title="Cases by Resolution Speed",
        showlegend=True, legend=dict(orientation='v', x=1, y=0.5),
        height=340, plot_bgcolor='white', paper_bgcolor='white',
        font_family='Inter', font_color=NAVY, title_font_size=14,
        margin=dict(l=0, r=10, t=50, b=10),
        annotations=[dict(text=f"{med_days}d<br><b>median</b>", x=0.38, y=0.5,
                          font_size=13, font_color=NAVY, showarrow=False)]
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown(f"""<div class="insight">
📌 <strong>What this means for you:</strong> These cases are motor accident compensation
appeals — typically filed by accident victims or their families. Among the cases that
<em>did</em> get resolved, the median wait was <strong>{med_days} days
(~{round(med_days/365.25,1)} years)</strong>.
1 in 4 resolved cases was concluded within <strong>{p25} days (~{p25//30} months)</strong>.
1 in 4 took longer than <strong>{int(p75)} days (~{int(p75)//30} months)</strong>.
These are benchmarks from <em>completed</em> cases — not predictions.
</div>""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# SECTION 2 — ARE CASES GETTING FASTER?
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="sec-title">📅 Are Cases Getting Resolved Faster Over Time?</p>', unsafe_allow_html=True)
st.markdown("""<p class="sec-sub">
To compare years fairly, we ask: <em>"Of all cases filed in a given year,
what share was resolved within 1 year? Within 2 years?"</em>
This is more honest than comparing raw medians, which are distorted by how long each
filing year had to accumulate resolved cases.
</p>""", unsafe_allow_html=True)

cf = cohort_df[(cohort_df['filing_year'] >= year_range[0]) &
               (cohort_df['filing_year'] <= year_range[1])].copy()

col_c, col_d = st.columns(2)

with col_c:
    fig_c1 = go.Figure()
    fig_c1.add_trace(go.Bar(
        x=cf['filing_year'].astype(str), y=cf['pct_within_1yr'],
        marker_color=TEAL,
        text=cf['pct_within_1yr'].apply(lambda x: f"{x}%"),
        textposition='outside',
        hovertemplate='Filing year: %{x}<br>%{y}% resolved within 1 year<extra></extra>'
    ))
    fig_c1.update_layout(
        title="% of Each Year's Cases Resolved Within 1 Year",
        xaxis_title="Year Case Was Filed", yaxis_title="% Resolved in Under 1 Year",
        plot_bgcolor='white', paper_bgcolor='white', font_family='Inter',
        font_color=NAVY, height=300, showlegend=False, title_font_size=13,
        yaxis_range=[0, min(cf['pct_within_1yr'].max() * 1.3, 100)],
        margin=dict(l=20, r=20, t=50, b=20)
    )
    fig_c1.update_xaxes(showgrid=False)
    fig_c1.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_c1, use_container_width=True)

with col_d:
    fig_c2 = go.Figure()
    fig_c2.add_trace(go.Bar(
        x=cf['filing_year'].astype(str), y=cf['median_days'],
        marker_color=BLUE,
        text=cf['median_days'].apply(lambda x: f"{x}d"),
        textposition='outside',
        hovertemplate='Filing year: %{x}<br>Median: %{y} days<extra></extra>'
    ))
    fig_c2.update_layout(
        title="Median Days to Resolution (by Filing Year)",
        xaxis_title="Year Case Was Filed", yaxis_title="Median Days to Resolution",
        plot_bgcolor='white', paper_bgcolor='white', font_family='Inter',
        font_color=NAVY, height=300, showlegend=False, title_font_size=13,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    fig_c2.update_xaxes(showgrid=False)
    fig_c2.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig_c2, use_container_width=True)

st.markdown("""<div class="insight">
⚠️ <strong>Read with caution:</strong> The 2019 cohort looks fastest (59% resolved in 1 year)
partly because only the fastest 2019 cases had time to be resolved by January 2021.
Slower 2019 cases were still pending when this data was collected.
The <em>direction</em> of the trend (improving) is likely real, but the <em>magnitude</em>
is overstated for recent years. Think of these as <strong>lower-bound resolution rates</strong>.
</div>""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# SECTION 3 — ONE SYSTEM, MANY EXPERIENCES
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="sec-title">🏛️ One System, Many Experiences</p>', unsafe_allow_html=True)
st.markdown("""<p class="sec-sub">
The same type of case — a motor accident appeal — can take vastly different amounts of time
depending on which bench hears it. The charts below show this range. This is not an
accusation against any court — case complexity, bench constitution, and workload all differ.
But the <em>extent</em> of the variation is a system-level signal worth noting.
</p>""", unsafe_allow_html=True)

# Box plot: spread by filing year
fig_box = px.box(
    dff, x='filing_year', y='disposal_days',
    color='filing_year',
    color_discrete_sequence=[TEAL, BLUE, AMBER, CORAL, '#c0392b'],
    labels={'disposal_days': 'Days to Resolution', 'filing_year': 'Filing Year'},
    title="Spread of Resolution Times by Filing Year",
    points=False
)
fig_box.update_layout(
    plot_bgcolor='white', paper_bgcolor='white', font_family='Inter',
    font_color=NAVY, height=300, showlegend=False, title_font_size=13,
    margin=dict(l=20, r=20, t=50, b=20)
)
fig_box.update_xaxes(showgrid=False, type='category')
fig_box.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
st.plotly_chart(fig_box, use_container_width=True)

# Court-level analysis
court_stats = (
    dff.groupby('court_number')['disposal_days']
    .agg(median_days='median', n_cases='count')
    .reset_index()
)
court_stats = court_stats[court_stats['n_cases'] >= 50].sort_values('median_days')

col_e, col_f = st.columns(2)

with col_e:
    n_show = min(8, len(court_stats))
    top_bottom = pd.concat([
        court_stats.head(n_show).assign(group='Faster resolution'),
        court_stats.tail(n_show).assign(group='Slower resolution')
    ]).drop_duplicates(subset='court_number')

    fig_courts = px.bar(
        top_bottom.sort_values('median_days'),
        x='median_days',
        y=top_bottom.sort_values('median_days')['court_number'].astype(str),
        orientation='h',
        color='median_days',
        color_continuous_scale=[TEAL, AMBER, CORAL],
        text='n_cases',
        title="Court Halls: Fastest vs. Slowest Median Resolution<br><sup>(benches with 50+ cases | same case type throughout)</sup>",
        labels={'median_days': 'Median Days', 'court_number': 'Court Hall No.'}
    )
    fig_courts.update_traces(texttemplate='%{text:,} cases', textposition='outside')
    fig_courts.update_layout(
        plot_bgcolor='white', paper_bgcolor='white', font_family='Inter',
        font_color=NAVY, height=420, showlegend=False,
        coloraxis_showscale=False, title_font_size=12,
        margin=dict(l=30, r=70, t=70, b=20)
    )
    fig_courts.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
    fig_courts.update_yaxes(showgrid=False)
    st.plotly_chart(fig_courts, use_container_width=True)

with col_f:
    fig_scatter = px.scatter(
        court_stats, x='n_cases', y='median_days',
        size='n_cases', size_max=40,
        color='median_days',
        color_continuous_scale=[TEAL, AMBER, CORAL],
        title="Caseload vs. Resolution Time<br><sup>Each dot = one court bench | Same case type</sup>",
        labels={'n_cases': 'Cases Handled', 'median_days': 'Median Days'},
        hover_data={'court_number': True, 'n_cases': ':.0f', 'median_days': ':.0f'}
    )
    fig_scatter.update_layout(
        plot_bgcolor='white', paper_bgcolor='white', font_family='Inter',
        font_color=NAVY, height=420, showlegend=False,
        coloraxis_showscale=False, title_font_size=12,
        margin=dict(l=20, r=20, t=70, b=20)
    )
    fig_scatter.update_xaxes(showgrid=True, gridcolor='#f0f0f0', title='Cases Handled')
    fig_scatter.update_yaxes(showgrid=True, gridcolor='#f0f0f0', title='Median Days to Resolution')
    st.plotly_chart(fig_scatter, use_container_width=True)

vmax = int(court_stats['median_days'].max())
vmin = int(court_stats['median_days'].min())
ratio = round(vmax / vmin, 1) if vmin > 0 else '—'
st.markdown(f"""<div class="insight">
📌 <strong>The range:</strong> Among court benches with 50+ cases, the slowest had a median
of <strong>{vmax} days</strong> and the fastest <strong>{vmin} days</strong> — a
<strong>{ratio}× difference</strong>, all for the same type of case, within the same
High Court. This variance is systemic: it may reflect case complexity, bench size, or
workload — not individual blame. But it signals that outcomes are not uniformly delivered.
</div>""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# SECTION 4 — WHAT HAPPENED TO THESE CASES?
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="sec-title">📋 What Happened When Cases Were Resolved?</p>', unsafe_allow_html=True)
st.markdown("""<p class="sec-sub">
Outcome details are recorded for only <strong>26% of cases</strong> in this dataset — the rest
show no outcome in the source data. The charts below cover only the cases where an outcome
was recorded, and <strong>should not be read as representative of all cases.</strong>
</p>""", unsafe_allow_html=True)

col_g, col_h = st.columns(2)

with col_g:
    outcome_counts = (
        dff[dff['outcome_bucket'] != 'Data Not Available']['outcome_bucket']
        .value_counts().reset_index()
    )
    outcome_counts.columns = ['outcome', 'count']
    total_with_outcome = outcome_counts['count'].sum()

    fig_out = px.bar(
        outcome_counts.sort_values('count'),
        x='count', y='outcome', orientation='h',
        title=f"Case Outcomes (based on {total_with_outcome:,} cases with recorded outcomes)",
        labels={'count': 'Number of Cases', 'outcome': ''},
        color='outcome',
        color_discrete_sequence=[TEAL, BLUE, AMBER, CORAL, NAVY, '#8e44ad']
    )
    fig_out.update_layout(
        plot_bgcolor='white', paper_bgcolor='white', font_family='Inter',
        font_color=NAVY, height=300, showlegend=False, title_font_size=12,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    fig_out.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
    fig_out.update_yaxes(showgrid=False)
    st.plotly_chart(fig_out, use_container_width=True)
    st.caption(f"⚠️ Outcome data available for {total_with_outcome:,} of {len(dff):,} cases "
               f"({100*total_with_outcome//len(dff)}%). The remaining {len(dff)-total_with_outcome:,} "
               f"cases have no outcome recorded in the source data.")

with col_h:
    # Filing heatmap
    monthly = dff.groupby(['filing_year','filing_month']).size().reset_index(name='count')
    pivot   = monthly.pivot(index='filing_year', columns='filing_month', values='count').fillna(0)
    mnames  = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
               7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
    pivot.columns = [mnames.get(c, str(c)) for c in pivot.columns]

    fig_heat = px.imshow(
        pivot, aspect='auto',
        color_continuous_scale=['#eef2ff', NAVY],
        title="When Are Cases Filed? (Month × Year)",
        labels=dict(x="Month", y="Filing Year", color="Cases Filed")
    )
    fig_heat.update_layout(
        plot_bgcolor='white', paper_bgcolor='white', font_family='Inter',
        font_color=NAVY, height=300, title_font_size=12,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    st.caption("Filing volumes by month reveal seasonal patterns — useful context for litigants "
               "and court administrators alike.")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  <h4>📖 About This Dashboard</h4>
  <p>
  Built as a <strong>pro bono civic initiative</strong> by
  <a href="#">Lawgorithm</a> to make judicial data legible to every citizen.
  <br><br>
  <strong>Data:</strong> National Judicial Data Grid (NJDG), Karnataka High Court,
  accessed via ISDM Hackathon dataset. Covers <strong>Motor Accident Appeals (MFA)</strong>
  filed 2015–2019 and resolved by January 2021.
  All {len(dff):,} cases in this dataset are from the Principal Bench at Bengaluru.
  <br><br>
  <strong>Survivorship Bias:</strong> This dataset shows only <em>resolved</em> cases.
  Cases still pending — likely numbering in the tens of thousands for Karnataka HC alone —
  are not included. All statistics describe completed cases, not the system's current state.
  <br><br>
  <strong>Court-level variance:</strong> Differences in resolution times across benches
  reflect case mix, bench constitution, workload, and complexity — not individual performance.
  No court is named, ranked, or implicated.
  <br><br>
  <strong>Useful resources:</strong><br>
  🔗 <a href="https://njdg.ecourts.gov.in" target="_blank">NJDG Live Portal</a>
     — National case pendency and disposal data (live)<br>
  🔗 <a href="https://ecourts.gov.in" target="_blank">eCourts Services</a>
     — Track any case status by CNR number<br>
  🔗 <a href="https://dakshindia.org" target="_blank">DAKSH India</a>
     — Independent judicial data research<br>
  🔗 <a href="https://vidhilegalpolicy.in" target="_blank">Vidhi Centre for Legal Policy</a>
     — Justice reform research<br><br>
  <em>Built with ❤️ for transparent justice &nbsp;|&nbsp; Powered by Lawgorithm
  &nbsp;|&nbsp; Data: CC-BY, NJDG / ISDM</em>
  </p>
</div>
""", unsafe_allow_html=True)
