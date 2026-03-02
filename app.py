# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  JUSTICE DELAYED — Citizen-First Dashboard                              ║
# ║  Karnataka High Court | First Appeals | 2015–2019                      ║
# ║  A Lawgorithm Initiative   |   app.py   |   v2.0                       ║
# ╚══════════════════════════════════════════════════════════════════════════╝

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

# ── Page config — no sidebar chrome ──────────────────────────────────────────
st.set_page_config(
    page_title="Justice Delayed | Karnataka HC",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Palette ───────────────────────────────────────────────────────────────────
NAVY   = "#1C2B4A"
AMBER  = "#E8920A"
TEAL   = "#1A9E8F"
CORAL  = "#D95B3E"
MUTED  = "#6B7A93"
LIGHT  = "#F7F8FA"
WHITE  = "#FFFFFF"
WARM   = "#FAFAF8"

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  CSS — Feels like a public-interest website, not a dashboard            ║
# ╚══════════════════════════════════════════════════════════════════════════╝
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Reset Streamlit defaults ─────────────────────────────────────────── */
html, body, [class*="css"]    { font-family: 'DM Sans', sans-serif !important; }
.main                         { background: #FAFAF8; }
.block-container              { padding: 0 !important; max-width: 100% !important; }
#MainMenu, footer, header     { visibility: hidden; }
section[data-testid="stSidebar"] { display: none !important; }
[data-testid="stSidebarCollapsedControl"] { display: none !important; }

/* Plotly chart containers */
.js-plotly-plot .plotly, div.stPlotlyChart { border-radius: 12px; }

/* ── Layout wrapper ───────────────────────────────────────────────────── */
.page-wrap   { max-width: 960px; margin: 0 auto; padding: 0 1.5rem 4rem; }
.wide-wrap   { max-width: 1100px; margin: 0 auto; padding: 0 1.5rem; }

/* ── Hero ─────────────────────────────────────────────────────────────── */
.hero-band {
    background: linear-gradient(160deg, #1C2B4A 0%, #243655 55%, #1A3E5C 100%);
    padding: 3.5rem 0 3rem;
    margin-bottom: 0;
}
.hero-inner   { max-width: 960px; margin: 0 auto; padding: 0 1.5rem; }
.hero-kicker  { font-family: 'DM Sans', sans-serif; font-size: 0.72rem;
                text-transform: uppercase; letter-spacing: 0.14em;
                color: #7A9CC0; margin-bottom: 0.8rem; }
.hero-title   { font-family: 'Lora', Georgia, serif; font-size: clamp(1.9rem,4vw,2.8rem);
                font-weight: 700; color: #FFFFFF; line-height: 1.2; margin: 0 0 0.7rem; }
.hero-sub     { font-size: 1.05rem; color: #B8CEDF; line-height: 1.65;
                max-width: 640px; margin: 0; font-weight: 300; }
.hero-meta    { font-size: 0.75rem; color: #5A7A99; margin-top: 1.5rem;
                border-top: 1px solid rgba(255,255,255,0.08); padding-top: 1rem; }

/* ── Three big facts strip ────────────────────────────────────────────── */
.facts-band   { background: #1C2B4A; padding-bottom: 2.5rem; }
.facts-grid   { max-width: 960px; margin: 0 auto; padding: 0 1.5rem;
                display: grid; grid-template-columns: repeat(3,1fr); gap: 1px;
                background: rgba(255,255,255,0.08); border-radius: 12px;
                overflow: hidden; }
.fact-card    { background: rgba(255,255,255,0.04); padding: 1.5rem 1.4rem; }
.fact-card:hover { background: rgba(255,255,255,0.07); transition: background 0.2s; }
.fact-n       { font-family: 'Lora', serif; font-size: 2.4rem; font-weight: 700;
                color: #E8920A; line-height: 1; margin: 0; }
.fact-l       { font-size: 0.9rem; color: #C5D8E8; margin: 0.45rem 0 0; font-weight: 400; }
.fact-s       { font-size: 0.74rem; color: #5A7A99; margin: 0.25rem 0 0; }

/* ── Section ──────────────────────────────────────────────────────────── */
.section      { max-width: 960px; margin: 0 auto; padding: 2.8rem 1.5rem; }
.section + .section { padding-top: 0; }
.sec-rule     { border: none; border-top: 1px solid #E8ECF2; margin: 0 1.5rem; }

/* ── Section heading ──────────────────────────────────────────────────── */
.sec-label    { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.12em;
                color: #E8920A; font-weight: 600; margin: 0 0 0.5rem; }
.sec-title    { font-family: 'Lora', serif; font-size: 1.45rem; font-weight: 700;
                color: #1C2B4A; margin: 0 0 0.35rem; line-height: 1.3; }
.sec-desc     { font-size: 0.93rem; color: #6B7A93; margin: 0; line-height: 1.6; max-width: 600px; }

/* ── Insight box ──────────────────────────────────────────────────────── */
.insight      { background: #EEF5FB; border-left: 3px solid #1A9E8F;
                border-radius: 0 8px 8px 0; padding: 0.8rem 1rem;
                font-size: 0.875rem; color: #1C2B4A; line-height: 1.65; margin: 1rem 0; }
.caveat-sm    { background: #FFF8ED; border-left: 3px solid #E8920A;
                border-radius: 0 8px 8px 0; padding: 0.75rem 1rem;
                font-size: 0.83rem; color: #5A3E00; line-height: 1.6; margin: 0.8rem 0; }
.warn-sm      { background: #FFF2EF; border-left: 3px solid #D95B3E;
                border-radius: 0 8px 8px 0; padding: 0.75rem 1rem;
                font-size: 0.83rem; color: #6B1E00; line-height: 1.6; margin: 0.8rem 0; }

/* ── Big number callout ───────────────────────────────────────────────── */
.big-stat     { text-align: center; padding: 1.4rem; }
.big-stat-n   { font-family: 'Lora', serif; font-size: 3.2rem; font-weight: 700;
                color: #1C2B4A; line-height: 1; }
.big-stat-l   { font-size: 0.85rem; color: #6B7A93; margin-top: 0.3rem; }

/* ── Data cards (scorecard) ───────────────────────────────────────────── */
.field-row    { display: flex; align-items: flex-start; justify-content: space-between;
                padding: 0.6rem 0; border-bottom: 1px solid #F0F2F5;
                font-size: 0.85rem; gap: 1rem; }
.field-label  { color: #444; flex: 1; }
.field-note   { color: #999; font-size: 0.78rem; margin-top: 0.1rem; }
.badge        { border-radius: 100px; padding: 0.18rem 0.7rem; font-size: 0.73rem;
                font-weight: 600; white-space: nowrap; flex-shrink: 0; }
.b-ok         { background: #E6F7F4; color: #0A6B5B; }
.b-warn       { background: #FFF3DC; color: #7A4F00; }
.b-bad        { background: #FFF0EE; color: #7A2000; }

/* ── Action cards ─────────────────────────────────────────────────────── */
.act-card     { background: white; border: 1px solid #E8ECF2; border-radius: 12px;
                padding: 1.3rem 1.2rem; height: 100%; transition: box-shadow 0.2s;
                box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
.act-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.1); }
.act-icon     { font-size: 1.5rem; margin-bottom: 0.6rem; }
.act-title    { font-weight: 600; font-size: 0.95rem; color: #1C2B4A; margin: 0 0 0.4rem; }
.act-body     { font-size: 0.83rem; color: #6B7A93; line-height: 1.6; margin: 0; }
.act-link     { font-size: 0.82rem; font-weight: 600; color: #E8920A;
                text-decoration: none; margin-top: 0.8rem; display: inline-block; }

/* ── Chart container ──────────────────────────────────────────────────── */
.chart-wrap   { background: white; border-radius: 12px; border: 1px solid #EAECF0;
                padding: 1rem; margin: 1rem 0; }

/* ── Footer ───────────────────────────────────────────────────────────── */
.footer-band  { background: #1C2B4A; padding: 2.5rem 0; margin-top: 2rem; }
.footer-inner { max-width: 960px; margin: 0 auto; padding: 0 1.5rem;
                font-size: 0.81rem; color: #607A93; line-height: 1.9; }
.footer-inner h4 { color: #C5D8E8; font-size: 0.9rem; margin: 0 0 0.8rem; }
.footer-inner a  { color: #E8920A; text-decoration: none; }
.footer-grid  { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }

/* ── Expander styling ─────────────────────────────────────────────────── */
[data-testid="stExpander"] { border: 1px solid #E8ECF2 !important;
    border-radius: 12px !important; overflow: hidden; background: white; }
[data-testid="stExpander"] > details > summary {
    font-size: 0.93rem; font-weight: 600; color: #1C2B4A;
    padding: 0.9rem 1.1rem !important; }

/* ── Mobile ───────────────────────────────────────────────────────────── */
@media (max-width: 680px) {
    .facts-grid { grid-template-columns: 1fr; }
    .fact-n     { font-size: 2rem; }
    .hero-title { font-size: 1.7rem; }
    .footer-grid { grid-template-columns: 1fr; }
}
</style>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  DATA                                                                   ║
# ╚══════════════════════════════════════════════════════════════════════════╝

@st.cache_data(show_spinner=False)
def load(path):
    df = pd.read_csv(path, parse_dates=["DATE_FILED", "DECISION_DATE"])
    df["filing_year"]  = df["DATE_FILED"].dt.year
    df["filing_month"] = df["DATE_FILED"].dt.month

    bins   = [0, 365, 730, 1095, 99999]
    labels = ["Under 1 year", "1–2 years", "2–3 years", "Over 3 years"]
    df["speed"] = pd.cut(df["DISPOSALTIME_ADJ"], bins=bins, labels=labels, right=True)

    outcome_map = {
        "DISPOSED":                        "Closed — details not recorded",
        "Partly Allowed":                  "Partly allowed",
        "DISMISSED":                       "Dismissed",
        "Dismissed for Non-Prosecution":   "Dropped (not pursued)",
        "ALLOWED":                         "Fully allowed",
        "ALLOWED AND REMANDED":            "Sent back to lower court",
        "REJECTED":                        "Rejected",
        "Abated":                          "Case lapsed",
        "IA/Memo/VK/OP in disposal":       "Procedural",
        "DROPPED":                         "Dropped",
    }
    df["outcome_label"] = df["NATURE_OF_DISPOSAL_OUTCOME"].map(outcome_map)
    return df

DATA_PATH = "data/ISDMHack_Cases_students.csv"
try:
    df = load(DATA_PATH)
except FileNotFoundError:
    st.error("**Data file not found.** Place `ISDMHack_Cases_students.csv` inside a `data/` folder next to `app.py`. See README.md.")
    st.stop()

N   = len(df)
p10 = int(df["DISPOSALTIME_ADJ"].quantile(0.10))
p25 = int(df["DISPOSALTIME_ADJ"].quantile(0.25))
p50 = int(df["DISPOSALTIME_ADJ"].median())
p75 = int(df["DISPOSALTIME_ADJ"].quantile(0.75))
p90 = int(df["DISPOSALTIME_ADJ"].quantile(0.90))

pct_u1yr   = round(100*(df["DISPOSALTIME_ADJ"] <=  365).mean(), 1)
pct_u2yr   = round(100*(df["DISPOSALTIME_ADJ"] <=  730).mean(), 1)
pct_over3  = round(100*(df["DISPOSALTIME_ADJ"] > 1095).mean(), 1)

outcome_pct = round(100 * df["NATURE_OF_DISPOSAL_OUTCOME"].notna().mean(), 1)

# Court stats — only courts with ≥10 cases
cs = df.groupby("COURT_NUMBER")["DISPOSALTIME_ADJ"].agg(n="count", med="median").reset_index()
cs = cs[cs["n"] >= 10].sort_values("med").reset_index(drop=True)
fastest_med = int(cs["med"].min())
slowest_med = int(cs["med"].max())
ratio       = round(slowest_med / fastest_med)
c200_med    = int(cs[cs["COURT_NUMBER"] == 200]["med"].values[0]) if 200 in cs["COURT_NUMBER"].values else p50
c200_n      = int(df[df["COURT_NUMBER"] == 200].shape[0])
c200_pct    = round(100 * c200_n / N, 1)

MONTH_NAMES = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
               7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}


# ── Chart defaults ─────────────────────────────────────────────────────────
def cl(height=380, title="", pad_l=24, pad_r=24, pad_t=44, pad_b=20, **kw):
    d = dict(plot_bgcolor=WHITE, paper_bgcolor=WHITE,
             font_family="DM Sans", font_color=NAVY,
             height=height, title_text=title, title_font_size=13,
             title_font_family="Lora",
             margin=dict(l=pad_l, r=pad_r, t=pad_t, b=pad_b),
             showlegend=False)
    d.update(kw)
    return d


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  HERO                                                                   ║
# ╚══════════════════════════════════════════════════════════════════════════╝

st.markdown(f"""
<div class="hero-band">
  <div class="hero-inner">
    <p class="hero-kicker">Karnataka High Court · First Appeals · 2015–2019 · A Lawgorithm Initiative</p>
    <h1 class="hero-title">Justice Delayed<br>— by the Numbers</h1>
    <p class="hero-sub">
      How long do people wait for their case to be resolved at the
      Karnataka High Court? Who decides how long you wait?
      And what can you do about it?
    </p>
    <p class="hero-meta">
      Based on <strong style="color:#C5D8E8">{N:,} closed cases</strong> filed between 2015–2019
      at the Karnataka HC Principal Bench, Bengaluru.
      Data snapshot: January 2021. Only <em>closed cases</em> are included — see
      "About this data" below for what that means.
    </p>
  </div>
</div>

<div class="facts-band">
  <div class="facts-grid">
    <div class="fact-card">
      <p class="fact-n">~1.6 yrs</p>
      <p class="fact-l">Median time from filing to resolution</p>
      <p class="fact-s">Half of all cases took longer than this</p>
    </div>
    <div class="fact-card">
      <p class="fact-n">{pct_over3}%</p>
      <p class="fact-l">Of cases waited over 3 years</p>
      <p class="fact-s">That's {int(N * pct_over3 / 100):,} people waiting 3+ years</p>
    </div>
    <div class="fact-card">
      <p class="fact-n">{ratio}×</p>
      <p class="fact-l">Difference between fastest and slowest court</p>
      <p class="fact-s">Same case type, same court building — very different wait</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  SECTION 1 — HOW LONG DOES IT TAKE?                                     ║
# ╚══════════════════════════════════════════════════════════════════════════╝

st.markdown('<hr class="sec-rule">', unsafe_allow_html=True)
st.markdown("""
<div class="section">
  <p class="sec-label">The waiting time</p>
  <h2 class="sec-title">How long does a case actually take?</h2>
  <p class="sec-desc">We looked at when each case was filed and when it was resolved. Here's the spread.</p>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns([3, 2], gap="medium")

with c1:
    # Clean histogram — no jargon axes
    fig_h = go.Figure()
    fig_h.add_trace(go.Histogram(
        x=df["DISPOSALTIME_ADJ"],
        nbinsx=55,
        marker_color="#3A6EA5",
        marker_opacity=0.7,
        hovertemplate="~%{x:.0f} days: %{y:,} cases<extra></extra>",
    ))
    # Key percentile lines
    for val, label, col, pos in [
        (p25, f"1 in 4 cases closes<br>by {p25} days", TEAL, "top right"),
        (p50, f"Half close by<br>{p50} days", AMBER, "top right"),
        (p90, f"9 in 10 close<br>by {p90} days", CORAL, "top left"),
    ]:
        fig_h.add_vline(x=val, line_dash="dot", line_color=col, line_width=2,
                        annotation_text=label, annotation_position=pos,
                        annotation_font_size=10, annotation_font_color=col,
                        annotation_bgcolor="rgba(255,255,255,0.9)")

    fig_h.update_layout(**cl(
        height=340, title="Number of cases vs. how long they took (in days)",
        xaxis_title="Days from filing to resolution",
        yaxis_title="Cases",
    ))
    fig_h.update_xaxes(showgrid=False, tickvals=[0, 365, 730, 1095, 1825, 2197],
                       ticktext=["0", "1 yr", "2 yrs", "3 yrs", "5 yrs", "6 yrs"])
    fig_h.update_yaxes(showgrid=True, gridcolor="#F0F2F5")
    st.plotly_chart(fig_h, use_container_width=True)

with c2:
    # Speed breakdown — plain language donut
    spd = df["speed"].value_counts().reindex(["Under 1 year","1–2 years","2–3 years","Over 3 years"]).fillna(0)
    spd_pcts = (100 * spd / N).round(1)

    fig_d = go.Figure(go.Pie(
        labels=spd.index.tolist(), values=spd.values.tolist(),
        hole=0.65,
        marker_colors=[TEAL, "#3A6EA5", AMBER, CORAL],
        textinfo="percent", textfont_size=11,
        hovertemplate="%{label}<br>%{value:,} cases (%{percent})<extra></extra>",
        sort=False,
    ))
    fig_d.update_layout(**cl(height=240, title="How long cases took", pad_l=10, pad_r=10, pad_t=40, pad_b=10))
    st.plotly_chart(fig_d, use_container_width=True)

    st.markdown(f"""
<div class="insight">
<strong>Put simply:</strong><br>
• {pct_u1yr}% of cases closed within a year<br>
• {pct_u2yr}% closed within 2 years<br>
• {pct_over3}% waited over 3 years<br>
• The very slowest cases took nearly 6 years
</div>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  SECTION 2 — THE COURT LOTTERY                                          ║
# ╚══════════════════════════════════════════════════════════════════════════╝

st.markdown('<hr class="sec-rule">', unsafe_allow_html=True)
st.markdown("""
<div class="section">
  <p class="sec-label">The court lottery</p>
  <h2 class="sec-title">Which court handles your case shapes how long you wait</h2>
  <p class="sec-desc">The same type of case, in the same High Court, can take vastly different amounts of time
  — depending on the court hall it's assigned to. You don't get to choose.</p>
</div>
""", unsafe_allow_html=True)

c3, c4 = st.columns([2, 3], gap="medium")

with c3:
    # Big stat
    st.markdown(f"""
<div style="background:white;border:1px solid #E8ECF2;border-radius:12px;padding:1.5rem 1.4rem;margin-bottom:1rem;">
  <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:.1em;color:{MUTED};margin-bottom:.5rem">FASTEST vs SLOWEST</div>
  <div style="font-family:'Lora',serif;font-size:2rem;font-weight:700;color:{NAVY}">{fastest_med} days</div>
  <div style="font-size:0.82rem;color:{MUTED};margin:.2rem 0 1rem">Median wait — fastest court</div>
  <div style="font-family:'Lora',serif;font-size:2rem;font-weight:700;color:{CORAL}">{slowest_med} days</div>
  <div style="font-size:0.82rem;color:{MUTED};margin:.2rem 0 1rem">Median wait — slowest court</div>
  <div style="font-size:0.78rem;background:#FFF2EF;color:#6B1E00;border-radius:8px;padding:.6rem .8rem;line-height:1.5">
    That's a <strong>{ratio}× difference</strong> — for the exact same type of case
  </div>
</div>
<div style="background:white;border:1px solid #E8ECF2;border-radius:12px;padding:1.3rem 1.4rem;">
  <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:.1em;color:{MUTED};margin-bottom:.5rem">COURT 200</div>
  <div style="font-family:'Lora',serif;font-size:1.8rem;font-weight:700;color:{AMBER}">{c200_pct}%</div>
  <div style="font-size:0.82rem;color:{MUTED};margin:.2rem 0 .5rem">of all cases go to this one court hall</div>
  <div style="font-size:0.78rem;color:#5A4200;background:#FFF8ED;border-radius:8px;padding:.6rem .8rem;line-height:1.5">
    {c200_n:,} of {N:,} cases. Median wait: {c200_med} days (~{c200_med//365:.1f} yrs)
  </div>
</div>
""", unsafe_allow_html=True)

with c4:
    # Show fastest 8 and slowest 8 in a clear dot chart
    top8  = cs.head(8).copy()
    bot8  = cs.tail(8).copy()
    both  = pd.concat([top8.assign(group="Fastest 8 courts"),
                       bot8.assign(group="Slowest 8 courts")], ignore_index=True)
    both["color"] = both["group"].map({"Fastest 8 courts": TEAL, "Slowest 8 courts": CORAL})
    both["label"] = both["COURT_NUMBER"].astype(str) + " (" + both["n"].astype(str) + " cases)"

    fig_lr = go.Figure()
    for group, grp_color in [("Fastest 8 courts", TEAL), ("Slowest 8 courts", CORAL)]:
        sub = both[both["group"] == group]
        fig_lr.add_trace(go.Scatter(
            x=sub["med"], y=sub["label"],
            mode="markers+lines",
            marker=dict(size=10, color=grp_color, line=dict(width=1.5, color=WHITE)),
            line=dict(width=0),
            name=group,
            hovertemplate="Court %{y}<br>Median: %{x:.0f} days<extra></extra>",
        ))

    fig_lr.add_vline(x=p50, line_dash="dot", line_color="#CCCCCC", line_width=1,
                     annotation_text=f"Overall median ({p50}d)", annotation_font_size=9,
                     annotation_position="top", annotation_font_color=MUTED)

    fig_lr.update_layout(**cl(
        height=360, title="Median wait time — fastest & slowest courts (courts with 10+ cases)",
        xaxis_title="Median days to resolution",
        yaxis_title="",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font_size=10),
        pad_l=20, pad_r=30, pad_t=50, pad_b=20,
    ))
    fig_lr.update_xaxes(showgrid=True, gridcolor="#F0F2F5",
                        tickvals=[0, 365, 730, 1095, 1460],
                        ticktext=["0","1 yr","2 yrs","3 yrs","4 yrs"])
    fig_lr.update_yaxes(showgrid=False, tickfont_size=10)
    st.plotly_chart(fig_lr, use_container_width=True)

st.markdown("""
<div class="section" style="padding-top:.5rem;padding-bottom:1.5rem">
<div class="caveat-sm">
⚠️ <strong>Important note:</strong> Court numbers (like "Court 200") are internal NJDG identifiers.
They don't correspond to publicly visible court hall names. Citizens cannot directly look up or request a specific court.
The variation shown here is real and significant, but the system doesn't give litigants a way to act on this information.
That's a transparency gap worth knowing about.
</div>
</div>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  SECTION 3 — WHAT HAPPENED TO CASES?                                    ║
# ╚══════════════════════════════════════════════════════════════════════════╝

st.markdown('<hr class="sec-rule">', unsafe_allow_html=True)
st.markdown(f"""
<div class="section">
  <p class="sec-label">Outcomes</p>
  <h2 class="sec-title">When a case closed — what happened?</h2>
  <p class="sec-desc">Outcome data exists for only {outcome_pct}% of cases.
  For the rest, the case was closed but <em>how it was closed</em> was never entered into the system.</p>
</div>
""", unsafe_allow_html=True)

out_known = df[df["outcome_label"].notna()].copy()
N_out = len(out_known)

st.markdown(f"""
<div class="section" style="padding-top:0">
<div class="warn-sm">
⚠️ <strong>Data gap:</strong> Only {N_out:,} of {N:,} cases ({outcome_pct}%) have a recorded outcome.
The remaining {N - N_out:,} cases are marked "closed" in NJDG but with no details.
The chart below shows <em>only the {N_out:,} cases we have data for.</em>
</div>
</div>
""", unsafe_allow_html=True)

oc = out_known["outcome_label"].value_counts().reset_index()
oc.columns = ["label", "n"]
oc["pct"] = (100 * oc["n"] / N_out).round(1)
oc = oc.sort_values("n", ascending=True)

col_oc, col_guide = st.columns([3, 2], gap="medium")

with col_oc:
    fig_oc = go.Figure(go.Bar(
        x=oc["n"], y=oc["label"], orientation="h",
        marker_color="#3A6EA5", marker_opacity=0.75,
        text=oc["pct"].apply(lambda x: f"{x}%"),
        textposition="outside", textfont_size=10,
        hovertemplate="%{y}<br>%{x:,} cases (%{text})<extra></extra>",
    ))
    fig_oc.update_layout(**cl(
        height=340, title=f"How cases were resolved — {N_out:,} cases with recorded outcomes",
        xaxis_title="Number of cases", yaxis_title="",
        pad_l=20, pad_r=60, pad_t=44, pad_b=20,
        xaxis_range=[0, oc["n"].max() * 1.3],
    ))
    fig_oc.update_xaxes(showgrid=True, gridcolor="#F0F2F5")
    fig_oc.update_yaxes(showgrid=False, tickfont_size=10)
    st.plotly_chart(fig_oc, use_container_width=True)

with col_guide:
    st.markdown("""
<div style="background:white;border:1px solid #E8ECF2;border-radius:12px;padding:1.3rem 1.2rem;margin-top:0.5rem">
  <p style="font-size:0.75rem;text-transform:uppercase;letter-spacing:.1em;color:#6B7A93;margin:0 0 .9rem;font-weight:600">Plain English guide</p>

  <div style="font-size:0.84rem;line-height:2;color:#333">
    ✅ <strong>Fully allowed</strong> — court ruled in your favour<br>
    ↔️ <strong>Partly allowed</strong> — partial win<br>
    ❌ <strong>Dismissed</strong> — ruled against you on merits<br>
    🔄 <strong>Sent back</strong> — returned to lower court to reconsider<br>
    🚪 <strong>Dropped (not pursued)</strong> — petitioner didn't appear or follow up<br>
    📁 <strong>Closed — details not recorded</strong> — case closed, but NJDG has no entry for <em>how</em>
  </div>

  <div style="margin-top:1rem;background:#EEF5FB;border-radius:8px;padding:.7rem .9rem;font-size:0.8rem;color:#1C2B4A;line-height:1.6">
    📌 <strong>Biggest category:</strong> "Closed — details not recorded" — meaning the case
    was resolved but no one entered the outcome into the system. This is a systemic data quality problem.
  </div>
</div>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  DEEP DIVE (collapsible)                                                ║
# ╚══════════════════════════════════════════════════════════════════════════╝

st.markdown('<hr class="sec-rule">', unsafe_allow_html=True)
st.markdown("""
<div class="section" style="padding-bottom:1rem">
  <p class="sec-label">Want to dig deeper?</p>
  <h2 class="sec-title">More detail — for the curious</h2>
  <p class="sec-desc">These sections go further. They're for those who want to understand the data in more depth.</p>
</div>
""", unsafe_allow_html=True)

# ── Deep dive 1: Why does this data have blind spots? ─────────────────────
with st.expander("🔍 Why can't we say the system is 'getting faster'?  (Data blind spot explained)"):
    st.markdown("""
<div style="padding:.5rem .2rem">
<p style="font-size:0.93rem;color:#333;line-height:1.75;max-width:700px">
This data shows only cases that were <strong>already closed by January 2021</strong>.
Thousands of cases filed in 2018 and 2019 were still ongoing at that point — and they're missing from this dataset entirely.
</p>
<p style="font-size:0.93rem;color:#333;line-height:1.75;max-width:700px;margin-top:.8rem">
Think of it this way: if you measured "how long marathon runners take," but only counted runners who had
already crossed the finish line — you'd miss everyone still running. The slower runners (longer cases)
from recent years are still out there. We just can't see them.
</p>
<p style="font-size:0.93rem;color:#333;line-height:1.75;max-width:700px;margin-top:.8rem">
This is why the bar chart below appears to show cases "getting faster" over the years — it doesn't.
It just shows that <em>only the fast cases from 2018–2019 had time to close</em>.
We cannot claim the system improved.
</p>
</div>
""", unsafe_allow_html=True)

    cohort_d = []
    BASELINE = 6500
    for yr in [2015, 2016, 2017, 2018, 2019]:
        n   = df[df["filing_year"] == yr].shape[0]
        med = int(df[df["filing_year"] == yr]["DISPOSALTIME_ADJ"].median())
        cohort_d.append({"year": str(yr), "n": n, "med": med,
                         "est_complete": min(100, round(n / BASELINE * 100)),
                         "window": 2021 - yr})
    cd = pd.DataFrame(cohort_d)

    fig_sv = go.Figure()
    fig_sv.add_trace(go.Bar(
        x=cd["year"], y=cd["n"], name="Cases visible",
        marker_color=[NAVY, "#3A6EA5", "#4A9EA0", AMBER, CORAL],
        marker_opacity=0.8,
        hovertemplate="%{x}: %{y:,} cases visible in dataset<extra></extra>",
    ))
    fig_sv2 = go.Figure()
    from plotly.subplots import make_subplots
    fig_sv = make_subplots(specs=[[{"secondary_y": True}]])
    fig_sv.add_trace(go.Bar(x=cd["year"], y=cd["n"], name="Cases in dataset",
                            marker_color=[NAVY,"#3A6EA5","#4A9EA0",AMBER,CORAL], marker_opacity=.8,
                            hovertemplate="%{x}: %{y:,} cases<extra></extra>"), secondary_y=False)
    fig_sv.add_trace(go.Scatter(x=cd["year"], y=cd["med"], mode="lines+markers+text",
                                line=dict(color=AMBER, width=2, dash="dot"),
                                marker=dict(size=8, color=AMBER),
                                text=cd["med"].apply(lambda d: f"{d}d"),
                                textposition="top center", textfont_size=9,
                                name="Apparent median (misleading ⚠️)",
                                hovertemplate="%{x}: %{y}d median<extra></extra>"), secondary_y=True)
    fig_sv.update_layout(**cl(height=300, title="Why apparent 'improvement' is a data artefact",
                              showlegend=True, legend=dict(orientation="h", y=1.05, x=1,
                              xanchor="right", font_size=9)))
    fig_sv.update_xaxes(title_text="Filing year", showgrid=False)
    fig_sv.update_yaxes(title_text="Cases in dataset →", secondary_y=False, showgrid=True, gridcolor="#F0F2F5")
    fig_sv.update_yaxes(title_text="Apparent median (days) →", secondary_y=True, showgrid=False)
    st.plotly_chart(fig_sv, use_container_width=True)

    st.markdown("""
<div class="caveat-sm">
The bars shrink as the years get more recent — not because fewer cases were filed, but because
<strong>only the fast-resolving cases from 2018–2019 had time to close by Jan 2021</strong>.
The dotted line showing faster resolution is a mirage. We cannot draw conclusions about system-wide improvement from this data.
</div>
""", unsafe_allow_html=True)

# ── Deep dive 2: When are cases filed? ────────────────────────────────────
with st.expander("📅 When are cases filed? (Monthly patterns)"):
    monthly = df.groupby(["filing_year","filing_month"]).size().reset_index(name="n")
    pivot   = monthly.pivot(index="filing_year", columns="filing_month", values="n").fillna(0)
    pivot.columns = [MONTH_NAMES.get(c, str(c)) for c in pivot.columns]

    fig_hm = px.imshow(
        pivot, aspect="auto",
        color_continuous_scale=["#EEF5FF", NAVY],
        labels=dict(x="Month", y="Year", color="Cases"),
        title="Filing volume by month — darker = more filings",
        text_auto=True,
    )
    fig_hm.update_layout(**cl(height=260, pad_l=50, pad_r=20, pad_t=44, pad_b=20))
    fig_hm.update_traces(textfont_size=9)
    st.plotly_chart(fig_hm, use_container_width=True)

    mt = df.groupby("filing_month").size()
    h_m = MONTH_NAMES[int(mt.idxmax())]
    l_m = MONTH_NAMES[int(mt.idxmin())]
    st.markdown(f"""
<div class="insight">
📌 <strong>{h_m}</strong> has the most filings across years — likely post-winter recess.
<strong>{l_m}</strong> is quietest. May and December dips align with court vacation periods.
</div>
""", unsafe_allow_html=True)

# ── Deep dive 3: Full court distribution ──────────────────────────────────
with st.expander("🏛 Full court performance — all courts with 10+ cases"):
    # Histogram of court medians
    fig_cm = px.histogram(
        cs, x="med", nbins=30,
        color_discrete_sequence=["#3A6EA5"],
        labels={"med": "Median days to resolution", "count": "Courts"},
        title=f"Distribution of median wait times across {len(cs)} courts"
    )
    fig_cm.add_vline(x=p50, line_dash="dot", line_color=AMBER, line_width=2,
                     annotation_text=f"Overall median: {p50}d",
                     annotation_font_size=9, annotation_font_color=AMBER,
                     annotation_position="top right")
    fig_cm.update_layout(**cl(height=280, xaxis_title="Median days", yaxis_title="Number of courts",
                              pad_t=44, pad_b=20))
    fig_cm.update_xaxes(showgrid=False, tickvals=[0,365,730,1095,1460],
                        ticktext=["0","1yr","2yrs","3yrs","4yrs"])
    fig_cm.update_yaxes(showgrid=True, gridcolor="#F0F2F5")
    st.plotly_chart(fig_cm, use_container_width=True)

    st.markdown(f"""
<div class="insight">
📌 Most courts cluster around the 1–2 year range. But there is a long tail of slow courts — and a small
cluster of extremely fast courts (likely handling specific procedural categories or very few cases).
The spread alone — from {fastest_med} days to {slowest_med} days — shows how much court assignment matters.
</div>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  SECTION 4 — ABOUT THIS DATA                                            ║
# ╚══════════════════════════════════════════════════════════════════════════╝

st.markdown('<hr class="sec-rule">', unsafe_allow_html=True)
with st.expander("📊 About this data — what's reliable, what's missing, and what we can't claim"):
    st.markdown("""
<div style="padding:.5rem .2rem">
<p style="font-size:0.93rem;color:#333;line-height:1.7;max-width:700px">
This dashboard is built from an NJDG (National Judicial Data Grid) dataset of Karnataka High Court
First Appeals (MFA), accessed via the ISDM Hackathon. Here's an honest assessment of what the data can
and cannot tell us.
</p>
</div>
""", unsafe_allow_html=True)

    scorecard = [
        ("Dates (filed & resolved)",  "✅ Complete",       "b-ok",   "100% filled — core metric is reliable"),
        ("How long each case took",   "✅ Complete",       "b-ok",   "Calculated from dates — reliable"),
        ("Which court handled it",    "✅ Complete",       "b-ok",   "175 courts; internal IDs, not public names"),
        ("Case type",                 "✅ All MFA",        "b-ok",   "All First Appeals — narrow but consistent"),
        ("What the outcome was",      "⚠️ 26% filled",    "b-warn", "74% of cases: outcome never entered into NJDG"),
        ("Judge names",               "❌ Unusable",       "b-bad",  "All entries say 'Honorable Judge' — no real names"),
        ("Subject matter (Acts)",     "❌ 1.6% filled",   "b-bad",  "What the case was about: mostly unknown"),
        ("Pending cases",             "❌ Not included",   "b-bad",  "Only closed cases — survivorship bias"),
        ("Party details",             "❌ Not in data",    "b-bad",  "Names of petitioners/respondents not exported"),
    ]

    col_s1, col_s2 = st.columns(2)
    for i, (f, s, cls, note) in enumerate(scorecard):
        col = col_s1 if i < len(scorecard)//2 + 1 else col_s2
        col.markdown(f"""
<div class="field-row">
  <div>
    <div class="field-label"><strong>{f}</strong></div>
    <div class="field-note">{note}</div>
  </div>
  <span class="badge {cls}">{s}</span>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="warn-sm" style="margin-top:1rem">
<strong>What we can honestly say:</strong> Court-level variation is real and large.
Speed distributions are valid. Filing patterns are valid. Year-over-year "improvement" claims are NOT valid
(survivorship bias). Individual judge performance cannot be assessed. Subject matter breakdown is not possible.
</div>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  SECTION 5 — WHAT CAN YOU DO?                                           ║
# ╚══════════════════════════════════════════════════════════════════════════╝

st.markdown('<hr class="sec-rule">', unsafe_allow_html=True)
st.markdown("""
<div class="section">
  <p class="sec-label">Take action</p>
  <h2 class="sec-title">What can you do as a citizen?</h2>
  <p class="sec-desc">This data is not just for researchers. Here's how it connects to real things you can do.</p>
</div>
""", unsafe_allow_html=True)

ac1, ac2, ac3, ac4 = st.columns(4, gap="small")

actions = [
    (ac1, "🔍", "Track your case",
     "Every High Court case has a CNR number. Use eCourts to check your status, next date, and court allocation.",
     "https://ecourts.gov.in", "Go to eCourts →"),
    (ac2, "📊", "See live court data",
     "NJDG publishes real-time pendency statistics across all Indian courts — including live numbers right now.",
     "https://njdg.ecourts.gov.in", "Visit NJDG →"),
    (ac3, "📝", "File an RTI",
     "Under the Right to Information Act, you can request data about court performance and case handling from the HC Registry.",
     "https://rtionline.gov.in", "RTI Portal →"),
    (ac4, "📖", "Read the research",
     "DAKSH India and Vidhi Legal Policy publish independent research on judicial delays and how to fix them.",
     "https://dakshindia.org", "DAKSH India →"),
]

for col, icon, title, body, link, lt in actions:
    col.markdown(f"""
<div class="act-card">
  <div class="act-icon">{icon}</div>
  <p class="act-title">{title}</p>
  <p class="act-body">{body}</p>
  <a class="act-link" href="{link}" target="_blank">{lt}</a>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  FOOTER                                                                 ║
# ╚══════════════════════════════════════════════════════════════════════════╝

st.markdown(f"""
<div class="footer-band">
  <div class="footer-inner">
    <div class="footer-grid">
      <div>
        <h4>About this dashboard</h4>
        Built by <strong style="color:#C5D8E8">Lawgorithm</strong> to make judicial data
        legible to every citizen — not just lawyers and researchers.<br><br>
        <strong style="color:#C5D8E8">Data:</strong> NJDG · Karnataka HC Principal Bench · ISDM Hackathon dataset<br>
        <strong style="color:#C5D8E8">Coverage:</strong> MFA (First Appeals), filed 2015–2019, resolved by Jan 2021<br>
        <strong style="color:#C5D8E8">Cases:</strong> {N:,} closed cases after loading<br>
        <strong style="color:#C5D8E8">Version:</strong> 2.0 · Built with Python & Streamlit
      </div>
      <div>
        <h4>Key limitations</h4>
        ① Only closed cases — pending cases as of Jan 2021 not included<br>
        ② 74% of cases have no recorded outcome in NJDG<br>
        ③ Judge names anonymised — individual analysis not possible<br>
        ④ Subject matter unknown for 98.4% of cases<br>
        ⑤ Year-on-year trend claims not valid without total filing data<br><br>
        <a href="https://njdg.ecourts.gov.in">NJDG Portal</a> ·
        <a href="https://ecourts.gov.in">eCourts</a> ·
        <a href="https://dakshindia.org">DAKSH India</a> ·
        <a href="https://vidhilegalpolicy.in">Vidhi Legal</a> ·
        <a href="https://rtionline.gov.in">RTI Portal</a>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
