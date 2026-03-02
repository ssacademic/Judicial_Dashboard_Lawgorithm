# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  JUSTICE DELAYED — Citizen-First Dashboard                              ║
# ║  Karnataka High Court | First Appeals | 2015–2019                      ║
# ║  A Lawgorithm Initiative   |   app.py   |   v3.0                       ║
# ║  Phase 1: Layout fixes — light hero, single column, breathing room     ║
# ╚══════════════════════════════════════════════════════════════════════════╝

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Justice Delayed | Karnataka HC",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Palette ───────────────────────────────────────────────────────────────────
NAVY  = "#1C2B4A"
AMBER = "#E8920A"
TEAL  = "#1A9E8F"
CORAL = "#D95B3E"
BLUE  = "#3A6EA5"
MUTED = "#6B7A93"
WHITE = "#FFFFFF"

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  CSS — Light, editorial, centered, breathing                            ║
# ╚══════════════════════════════════════════════════════════════════════════╝
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;0,700;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Base reset ───────────────────────────────────────────────────────── */
html, body, [class*="css"]          { font-family: 'DM Sans', sans-serif !important; }
.main                               { background: #F8F8F6 !important; }
.block-container                    { padding: 0 !important; max-width: 100% !important; }
#MainMenu, footer, header           { visibility: hidden; }
section[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"] { display: none !important; }

/* ── Central column — all content lives here ──────────────────────────── */
/* We constrain via HTML wrappers, not Streamlit columns */

/* ── Top accent bar ───────────────────────────────────────────────────── */
.top-bar {
    background: #E8920A;
    height: 4px;
    width: 100%;
}

/* ── Hero ─────────────────────────────────────────────────────────────── */
.hero {
    background: #FFFFFF;
    padding: 3.5rem 0 2.5rem;
    border-bottom: 1px solid #EBEBEB;
}
.hero-inner {
    max-width: 720px;
    margin: 0 auto;
    padding: 0 2rem;
}
.hero-kicker {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #E8920A;
    font-weight: 600;
    margin: 0 0 1rem;
}
.hero-title {
    font-family: 'Lora', Georgia, serif;
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 700;
    color: #1C2B4A;
    line-height: 1.15;
    margin: 0 0 1rem;
}
.hero-sub {
    font-size: 1.05rem;
    color: #4A5568;
    line-height: 1.75;
    margin: 0;
    font-weight: 300;
    max-width: 600px;
}
.hero-note {
    font-size: 0.8rem;
    color: #9AA3AE;
    margin-top: 1.5rem;
    border-top: 1px solid #F0F0F0;
    padding-top: 1rem;
    line-height: 1.6;
}

/* ── Three big facts ──────────────────────────────────────────────────── */
.facts-row {
    background: #FFFFFF;
    border-bottom: 1px solid #EBEBEB;
    padding: 0;
}
.facts-inner {
    max-width: 720px;
    margin: 0 auto;
    padding: 0 2rem 2rem;
    display: flex;
    gap: 0;
}
.fact-item {
    flex: 1;
    padding: 1.5rem 1.2rem 1.2rem;
    border-right: 1px solid #F0F0F0;
}
.fact-item:first-child { padding-left: 0; }
.fact-item:last-child  { border-right: none; padding-right: 0; }
.fact-n {
    font-family: 'Lora', serif;
    font-size: 2rem;
    font-weight: 700;
    color: #E8920A;
    line-height: 1;
    margin: 0 0 0.4rem;
}
.fact-l {
    font-size: 0.88rem;
    color: #1C2B4A;
    font-weight: 500;
    margin: 0 0 0.2rem;
}
.fact-s {
    font-size: 0.75rem;
    color: #9AA3AE;
    margin: 0;
    line-height: 1.4;
}

/* ── Content sections ─────────────────────────────────────────────────── */
.section-wrap {
    background: #F8F8F6;
    padding: 3rem 0;
}
.section-wrap.white { background: #FFFFFF; }
.section-inner {
    max-width: 720px;
    margin: 0 auto;
    padding: 0 2rem;
}
.sec-kicker {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.13em;
    color: #E8920A;
    font-weight: 600;
    margin: 0 0 0.5rem;
}
.sec-h {
    font-family: 'Lora', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #1C2B4A;
    margin: 0 0 0.4rem;
    line-height: 1.25;
}
.sec-sub {
    font-size: 0.93rem;
    color: #6B7A93;
    margin: 0 0 1.8rem;
    line-height: 1.65;
}

/* ── Stat display block ───────────────────────────────────────────────── */
.stat-block {
    background: white;
    border: 1px solid #EBEBEB;
    border-radius: 12px;
    padding: 1.4rem 1.3rem;
    margin-bottom: 1rem;
}
.stat-label-sm {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #9AA3AE;
    font-weight: 600;
    margin: 0 0 0.5rem;
}
.stat-big {
    font-family: 'Lora', serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #1C2B4A;
    line-height: 1;
    margin: 0 0 0.25rem;
}
.stat-big.red   { color: #D95B3E; }
.stat-big.green { color: #1A9E8F; }
.stat-note {
    font-size: 0.8rem;
    color: #6B7A93;
    margin: 0;
    line-height: 1.5;
}
.stat-callout {
    font-size: 0.78rem;
    background: #FFF0EE;
    color: #6B1E00;
    border-radius: 8px;
    padding: 0.55rem 0.8rem;
    margin-top: 0.8rem;
    line-height: 1.5;
}

/* ── Info boxes ───────────────────────────────────────────────────────── */
.box-info  { background: #EEF6FB; border-left: 3px solid #3A6EA5;
             border-radius: 0 8px 8px 0; padding: 0.85rem 1rem;
             font-size: 0.86rem; color: #1C2B4A; line-height: 1.7;
             margin: 1.2rem 0; }
.box-warn  { background: #FFF8ED; border-left: 3px solid #E8920A;
             border-radius: 0 8px 8px 0; padding: 0.85rem 1rem;
             font-size: 0.86rem; color: #5A3E00; line-height: 1.7;
             margin: 1.2rem 0; }
.box-alert { background: #FFF0EE; border-left: 3px solid #D95B3E;
             border-radius: 0 8px 8px 0; padding: 0.85rem 1rem;
             font-size: 0.86rem; color: #6B1E00; line-height: 1.7;
             margin: 1.2rem 0; }

/* ── Outcome guide ────────────────────────────────────────────────────── */
.outcome-guide {
    background: white;
    border: 1px solid #EBEBEB;
    border-radius: 12px;
    padding: 1.4rem;
    margin-top: 1.5rem;
}
.og-title { font-size: 0.68rem; text-transform: uppercase; letter-spacing:.1em;
            color: #9AA3AE; font-weight: 600; margin: 0 0 .9rem; }
.og-row   { display: flex; align-items: flex-start; gap: .6rem;
            font-size: .84rem; padding: .35rem 0; border-bottom: 1px solid #F5F5F5;
            color: #333; line-height: 1.5; }
.og-row:last-child { border-bottom: none; }
.og-icon  { flex-shrink: 0; width: 1.3rem; }

/* ── Speed summary pills ──────────────────────────────────────────────── */
.speed-pills {
    display: flex; gap: .75rem; flex-wrap: wrap; margin-top: 1.2rem;
}
.speed-pill {
    background: white; border: 1px solid #EBEBEB; border-radius: 100px;
    padding: .4rem 1rem; font-size: .83rem; color: #1C2B4A;
    display: flex; align-items: center; gap: .45rem;
}
.sp-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }

/* ── Scorecard ────────────────────────────────────────────────────────── */
.sc-row {
    display: flex; align-items: flex-start; justify-content: space-between;
    padding: .65rem 0; border-bottom: 1px solid #F5F5F5;
    font-size: .84rem; gap: 1.5rem;
}
.sc-field  { color: #333; flex: 1; }
.sc-note   { font-size: .75rem; color: #999; margin-top: .1rem; }
.badge     { border-radius: 100px; padding: .2rem .75rem; font-size: .72rem;
             font-weight: 600; white-space: nowrap; flex-shrink: 0; }
.b-ok      { background: #E8F7F4; color: #0A6B5B; }
.b-warn    { background: #FFF3DC; color: #7A4F00; }
.b-bad     { background: #FFF0EE; color: #7A2000; }

/* ── Action cards ─────────────────────────────────────────────────────── */
.act-grid {
    display: grid; grid-template-columns: repeat(2, 1fr);
    gap: 1rem; margin-top: .5rem;
}
.act-card {
    background: white; border: 1px solid #EBEBEB; border-radius: 12px;
    padding: 1.3rem 1.2rem;
    transition: box-shadow .18s, border-color .18s;
}
.act-card:hover { border-color: #E8920A; box-shadow: 0 4px 16px rgba(0,0,0,.08); }
.act-ico   { font-size: 1.4rem; margin-bottom: .6rem; }
.act-t     { font-weight: 600; font-size: .93rem; color: #1C2B4A; margin: 0 0 .35rem; }
.act-b     { font-size: .82rem; color: #6B7A93; line-height: 1.6; margin: 0; }
.act-lnk   { font-size: .82rem; font-weight: 600; color: #E8920A;
             text-decoration: none; margin-top: .7rem; display: inline-block; }

/* ── Expander tweaks ──────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: white !important;
    border: 1px solid #EBEBEB !important;
    border-radius: 10px !important;
    overflow: hidden;
    margin-bottom: .6rem;
}
[data-testid="stExpander"] > details > summary {
    font-size: .9rem; font-weight: 600; color: #1C2B4A;
    padding: .9rem 1.1rem !important;
    background: white;
}
[data-testid="stExpander"] > details[open] > summary {
    border-bottom: 1px solid #F0F0F0;
}

/* ── Divider ──────────────────────────────────────────────────────────── */
.div-line { border: none; border-top: 1px solid #EBEBEB; margin: 0; }

/* ── Footer ───────────────────────────────────────────────────────────── */
.footer {
    background: #1C2B4A; padding: 2.5rem 0; margin-top: 1rem;
}
.footer-inner {
    max-width: 720px; margin: 0 auto; padding: 0 2rem;
    display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;
    font-size: .81rem; color: #607A93; line-height: 1.9;
}
.footer-inner h4 { color: #C5D8E8; font-size: .88rem; margin: 0 0 .6rem; }
.footer-inner a  { color: #E8920A; text-decoration: none; }

/* ── Mobile ───────────────────────────────────────────────────────────── */
@media (max-width: 680px) {
    .facts-inner          { flex-direction: column; }
    .fact-item            { border-right: none; border-bottom: 1px solid #F0F0F0;
                            padding: 1rem 0 !important; }
    .act-grid             { grid-template-columns: 1fr; }
    .footer-inner         { grid-template-columns: 1fr; }
    .hero-title           { font-size: 1.8rem; }
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
    st.error("**Data file not found.** Place `ISDMHack_Cases_students.csv` inside a `data/` folder next to `app.py`.")
    st.stop()

# ── Key stats ─────────────────────────────────────────────────────────────
N           = len(df)
p25         = int(df["DISPOSALTIME_ADJ"].quantile(0.25))
p50         = int(df["DISPOSALTIME_ADJ"].median())
p75         = int(df["DISPOSALTIME_ADJ"].quantile(0.75))
p90         = int(df["DISPOSALTIME_ADJ"].quantile(0.90))
pct_u1yr    = round(100*(df["DISPOSALTIME_ADJ"] <=  365).mean(), 1)
pct_u2yr    = round(100*(df["DISPOSALTIME_ADJ"] <=  730).mean(), 1)
pct_over3   = round(100*(df["DISPOSALTIME_ADJ"] > 1095).mean(), 1)
outcome_pct = round(100*df["NATURE_OF_DISPOSAL_OUTCOME"].notna().mean(), 1)

cs = (df.groupby("COURT_NUMBER")["DISPOSALTIME_ADJ"]
        .agg(n="count", med="median")
        .reset_index()
        .query("n >= 10")
        .sort_values("med")
        .reset_index(drop=True))
fastest_med = int(cs["med"].min())
slowest_med = int(cs["med"].max())
ratio       = round(slowest_med / fastest_med)
c200_n      = int(df[df["COURT_NUMBER"] == 200].shape[0])
c200_pct    = round(100 * c200_n / N, 1)
c200_med    = int(df[df["COURT_NUMBER"] == 200]["DISPOSALTIME_ADJ"].median())

MONTH = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
         7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}

# ── Chart defaults ────────────────────────────────────────────────────────
def cl(h=360, title="", tl=24, tr=24, tt=44, tb=24, **kw):
    d = dict(plot_bgcolor=WHITE, paper_bgcolor=WHITE,
             font_family="DM Sans", font_color=NAVY,
             height=h, title_text=title,
             title_font_size=13, title_font_family="Lora",
             margin=dict(l=tl, r=tr, t=tt, b=tb),
             showlegend=False)
    d.update(kw)
    return d


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  PAGE                                                                   ║
# ╚══════════════════════════════════════════════════════════════════════════╝

# ── Thin amber accent line ─────────────────────────────────────────────────
st.markdown('<div class="top-bar"></div>', unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-inner">
    <p class="hero-kicker">Karnataka High Court · First Appeals · 2015–2019 · A Lawgorithm Initiative</p>
    <h1 class="hero-title">Justice Delayed<br>— by the Numbers</h1>
    <p class="hero-sub">
      How long do people wait for their case to be resolved
      at the Karnataka High Court? Who decides how long you wait?
      And what can you do about it?
    </p>
    <p class="hero-note">
      Based on <strong>{N:,} closed cases</strong> filed between 2015–2019 at the Karnataka HC
      Principal Bench, Bengaluru. Data snapshot: January 2021.
      Only <em>closed cases</em> are included — see "About this data" below
      for what that means.
    </p>
  </div>
  <div class="facts-inner">
    <div class="fact-item">
      <p class="fact-n">~1.6 yrs</p>
      <p class="fact-l">Median time to resolution</p>
      <p class="fact-s">Half of all cases took longer than this</p>
    </div>
    <div class="fact-item">
      <p class="fact-n">{pct_over3}%</p>
      <p class="fact-l">Waited over 3 years</p>
      <p class="fact-s">That's {int(N*pct_over3/100):,} people waiting 3+ years</p>
    </div>
    <div class="fact-item">
      <p class="fact-n">{ratio}×</p>
      <p class="fact-l">Variation court to court</p>
      <p class="fact-s">Same case type — very different wait</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  S1 — HOW LONG?                                                         ║
# ╚══════════════════════════════════════════════════════════════════════════╝

st.markdown('<div class="div-line"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="section-wrap white">
  <div class="section-inner">
    <p class="sec-kicker">The waiting time</p>
    <h2 class="sec-h">How long does a case actually take?</h2>
    <p class="sec-sub">We looked at when each case was filed and when it was resolved. Here's the full spread — each bar is a group of cases that took that many days.</p>
  </div>
</div>
""", unsafe_allow_html=True)

# Full-width histogram — no side-by-side
fig_h = go.Figure()
fig_h.add_trace(go.Histogram(
    x=df["DISPOSALTIME_ADJ"], nbinsx=55,
    marker_color=BLUE, marker_opacity=0.7,
    hovertemplate="~%{x:.0f} days: %{y:,} cases<extra></extra>",
))
for val, lbl, col, pos in [
    (p25, f"1 in 4 cases<br>closes by {p25}d", TEAL,  "top right"),
    (p50, f"Half close<br>by {p50}d",           AMBER, "top right"),
    (p90, f"9 in 10 close<br>by {p90}d",        CORAL, "top left"),
]:
    fig_h.add_vline(x=val, line_dash="dot", line_color=col, line_width=2,
                    annotation_text=lbl, annotation_position=pos,
                    annotation_font_size=10, annotation_font_color=col,
                    annotation_bgcolor="rgba(255,255,255,0.92)")

fig_h.update_layout(**cl(
    h=360,
    title="Cases by time taken — each bar is a group of cases",
    xaxis_title="Days from filing to resolution",
    yaxis_title="Number of cases",
))
fig_h.update_xaxes(showgrid=False,
    tickvals=[0, 365, 730, 1095, 1460, 1825, 2197],
    ticktext=["0", "1 yr", "2 yrs", "3 yrs", "4 yrs", "5 yrs", "6 yrs"])
fig_h.update_yaxes(showgrid=True, gridcolor="#F0F0F0")

# Render chart centered inside a max-width container
col_pad1, col_chart1, col_pad2 = st.columns([1, 8, 1])
with col_chart1:
    st.plotly_chart(fig_h, use_container_width=True)

# Speed summary — pills below chart, not a competing column
spd = df["speed"].value_counts().reindex(
    ["Under 1 year", "1–2 years", "2–3 years", "Over 3 years"]).fillna(0)
spd_colors = [TEAL, BLUE, AMBER, CORAL]

st.markdown(f"""
<div class="section-wrap white" style="padding-top:0;padding-bottom:2.5rem">
<div class="section-inner">
<div class="speed-pills">
  <div class="speed-pill"><div class="sp-dot" style="background:{TEAL}"></div>
    <strong>{pct_u1yr}%</strong>&nbsp;under 1 year</div>
  <div class="speed-pill"><div class="sp-dot" style="background:{BLUE}"></div>
    <strong>{round(spd['1–2 years']/N*100,1)}%</strong>&nbsp;1–2 years</div>
  <div class="speed-pill"><div class="sp-dot" style="background:{AMBER}"></div>
    <strong>{round(spd['2–3 years']/N*100,1)}%</strong>&nbsp;2–3 years</div>
  <div class="speed-pill"><div class="sp-dot" style="background:{CORAL}"></div>
    <strong>{pct_over3}%</strong>&nbsp;over 3 years</div>
</div>
<div class="box-info" style="margin-top:1rem">
  📌 <strong>Read this as:</strong> 1 in 4 cases closed within {p25} days (~{p25//30} months).
  Half the cases took more than {p50} days (~{p50//30} months).
  1 in 10 waited beyond {p90} days — nearly {round(p90/365,1)} years.
</div>
</div>
</div>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  S2 — THE COURT LOTTERY                                                 ║
# ╚══════════════════════════════════════════════════════════════════════════╝

st.markdown('<div class="div-line"></div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="section-wrap">
<div class="section-inner">
  <p class="sec-kicker">The court lottery</p>
  <h2 class="sec-h">Which court handles your case shapes how long you wait</h2>
  <p class="sec-sub">The same type of case, in the same High Court, can take vastly different
  amounts of time — depending on the court hall it's assigned to. You don't get to choose.</p>

  <div style="display:flex;gap:1rem;margin-bottom:1.5rem;flex-wrap:wrap">
    <div class="stat-block" style="flex:1;min-width:160px">
      <div class="stat-label-sm">Fastest court</div>
      <div class="stat-big green">{fastest_med} days</div>
      <p class="stat-note">Median wait — fastest court (with 10+ cases)</p>
    </div>
    <div class="stat-block" style="flex:1;min-width:160px">
      <div class="stat-label-sm">Slowest court</div>
      <div class="stat-big red">{slowest_med} days</div>
      <p class="stat-note">Median wait — slowest court</p>
      <div class="stat-callout">That's a <strong>{ratio}×</strong> difference — same case type</div>
    </div>
    <div class="stat-block" style="flex:1;min-width:160px">
      <div class="stat-label-sm">Court 200</div>
      <div class="stat-big" style="color:{AMBER}">{c200_pct}%</div>
      <p class="stat-note">of all cases go to this one court hall
      ({c200_n:,} of {N:,} cases, median {c200_med}d)</p>
    </div>
  </div>
</div>
</div>
""", unsafe_allow_html=True)

# Dot chart — full width, stacked below stats
top8 = cs.head(8).copy()
bot8 = cs.tail(8).copy()

fig_dot = go.Figure()

# Fastest courts
fig_dot.add_trace(go.Scatter(
    x=top8["med"], y=top8["COURT_NUMBER"].astype(str) + " (" + top8["n"].astype(str) + " cases)",
    mode="markers",
    marker=dict(size=11, color=TEAL, line=dict(width=1.5, color=WHITE)),
    name="Fastest courts",
    hovertemplate="Court %{y}<br>Median: %{x:.0f} days<extra></extra>",
))
# Slowest courts
fig_dot.add_trace(go.Scatter(
    x=bot8["med"], y=bot8["COURT_NUMBER"].astype(str) + " (" + bot8["n"].astype(str) + " cases)",
    mode="markers",
    marker=dict(size=11, color=CORAL, line=dict(width=1.5, color=WHITE)),
    name="Slowest courts",
    hovertemplate="Court %{y}<br>Median: %{x:.0f} days<extra></extra>",
))
fig_dot.add_vline(x=p50, line_dash="dot", line_color="#CCCCCC", line_width=1.5,
                  annotation_text=f"Overall median ({p50}d)",
                  annotation_font_size=9, annotation_font_color=MUTED,
                  annotation_position="top right")

fig_dot.update_layout(**cl(
    h=400,
    title="Median wait time — 8 fastest (green) and 8 slowest (red) courts with 10+ cases",
    xaxis_title="Median days to resolution",
    yaxis_title="",
    showlegend=True,
    legend=dict(orientation="h", y=1.08, x=1, xanchor="right", font_size=10),
    tl=20, tr=24, tt=50, tb=20,
))
fig_dot.update_xaxes(showgrid=True, gridcolor="#F0F0F0",
    tickvals=[0, 365, 730, 1095, 1460, 1825],
    ticktext=["0", "1 yr", "2 yrs", "3 yrs", "4 yrs", "5 yrs"])
fig_dot.update_yaxes(showgrid=False, tickfont_size=10)

col_pad3, col_chart2, col_pad4 = st.columns([1, 8, 1])
with col_chart2:
    st.plotly_chart(fig_dot, use_container_width=True)

st.markdown("""
<div class="section-wrap" style="padding-top:0;padding-bottom:2.5rem">
<div class="section-inner">
<div class="box-warn">
  ⚠️ <strong>A transparency gap:</strong> Court numbers like "Court 200" are internal NJDG identifiers.
  They don't map to publicly visible court hall names. Citizens cannot look up or request a specific court.
  The variation is real and large — but the system doesn't give litigants a way to act on it.
  This is worth knowing about.
</div>
</div>
</div>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  S3 — OUTCOMES                                                          ║
# ╚══════════════════════════════════════════════════════════════════════════╝

st.markdown('<div class="div-line"></div>', unsafe_allow_html=True)

out_known = df[df["outcome_label"].notna()].copy()
N_out     = len(out_known)

st.markdown(f"""
<div class="section-wrap white">
<div class="section-inner">
  <p class="sec-kicker">Outcomes</p>
  <h2 class="sec-h">When a case was resolved — what happened?</h2>
  <p class="sec-sub">Outcome data exists for only <strong>{outcome_pct}%</strong> of cases.
  For the rest, the case was closed but <em>how</em> it was closed was never entered into the system.
  The chart below covers the {N_out:,} cases where we have data.</p>
  <div class="box-alert">
    ⚠️ <strong>{100-outcome_pct:.0f}% of cases have no recorded outcome</strong> in NJDG.
    This is a systemic data quality problem — the case was closed, but the outcome was never entered.
  </div>
</div>
</div>
""", unsafe_allow_html=True)

_oc_raw = out_known["outcome_label"].value_counts().reset_index()
# Robust across pandas versions: columns are either ['index','outcome_label'] or ['outcome_label','count']
if "index" in _oc_raw.columns:
    oc = _oc_raw.rename(columns={"index":"label","outcome_label":"n"})
else:
    oc = _oc_raw.rename(columns={"outcome_label":"label","count":"n"})
oc = oc.sort_values("n", ascending=True).reset_index(drop=True)
oc["pct"] = (100 * oc["n"] / N_out).round(1)

fig_oc = go.Figure(go.Bar(
    x=oc["n"], y=oc["label"], orientation="h",
    marker_color=BLUE, marker_opacity=0.7,
    text=oc["pct"].apply(lambda x: f"{x}%"),
    textposition="outside", textfont_size=10,
    hovertemplate="%{y}<br>%{x:,} cases (%{text})<extra></extra>",
))
fig_oc.update_layout(**cl(
    h=320,
    title=f"How cases were resolved — {N_out:,} cases with recorded outcomes",
    xaxis_title="Number of cases", yaxis_title="",
    tl=20, tr=55, tt=44, tb=20,
    xaxis_range=[0, oc["n"].max() * 1.3],
))
fig_oc.update_xaxes(showgrid=True, gridcolor="#F0F0F0")
fig_oc.update_yaxes(showgrid=False, tickfont_size=10)

col_pad5, col_chart3, col_pad6 = st.columns([1, 8, 1])
with col_chart3:
    st.plotly_chart(fig_oc, use_container_width=True)

# Outcome guide — below the chart, not competing
st.markdown("""
<div class="section-wrap white" style="padding-top:0;padding-bottom:2.5rem">
<div class="section-inner">
<div class="outcome-guide">
  <div class="og-title">Plain English guide to outcomes</div>
  <div class="og-row"><span class="og-icon">✅</span><div><strong>Fully allowed</strong> — the court ruled in your favour</div></div>
  <div class="og-row"><span class="og-icon">↔️</span><div><strong>Partly allowed</strong> — partial win, some relief granted</div></div>
  <div class="og-row"><span class="og-icon">❌</span><div><strong>Dismissed</strong> — ruled against you on the merits</div></div>
  <div class="og-row"><span class="og-icon">🔄</span><div><strong>Sent back to lower court</strong> — HC found grounds to reconsider; case goes back</div></div>
  <div class="og-row"><span class="og-icon">🚶</span><div><strong>Dropped (not pursued)</strong> — petitioner didn't appear or follow up</div></div>
  <div class="og-row"><span class="og-icon">📁</span><div><strong>Closed — details not recorded</strong> — case closed but NJDG has no entry for how</div></div>
</div>
</div>
</div>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  DEEP DIVES                                                             ║
# ╚══════════════════════════════════════════════════════════════════════════╝

st.markdown('<div class="div-line"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="section-wrap">
<div class="section-inner">
  <p class="sec-kicker">Want to dig deeper?</p>
  <h2 class="sec-h">More detail — for the curious</h2>
  <p class="sec-sub">These sections go further. They're for those who want to understand the data in more depth.</p>
</div>
</div>
""", unsafe_allow_html=True)

# Expanders inside a centered container
col_pad7, col_exp, col_pad8 = st.columns([1, 8, 1])
with col_exp:

    # ── Deep dive 1 ──────────────────────────────────────────────────────
    with st.expander("🔍  Why can't we say the system is 'getting faster'?  (Data blind spot explained)"):
        st.markdown("""
This data shows only cases that were **already closed by January 2021**. Thousands of cases filed
in 2018 and 2019 were still ongoing at that point — and they're completely absent from this dataset.

Think of it this way: if you measured "how long marathon runners take," but only counted runners who
had already crossed the finish line — you'd miss everyone still on the course. The slower runners
(longer cases) from recent years are still out there. We just can't see them.

This is why the chart below appears to show cases "getting faster" over the years — it doesn't.
It just shows that *only the fast cases from 2018–2019 had time to close by Jan 2021.*
We cannot claim the system improved.
""")
        # Survivorship chart
        cohort_d = []
        for yr in [2015, 2016, 2017, 2018, 2019]:
            n   = df[df["filing_year"] == yr].shape[0]
            med = int(df[df["filing_year"] == yr]["DISPOSALTIME_ADJ"].median())
            cohort_d.append({"year": str(yr), "n": n, "med": med})
        cd = pd.DataFrame(cohort_d)

        fig_sv = make_subplots(specs=[[{"secondary_y": True}]])
        fig_sv.add_trace(go.Bar(
            x=cd["year"], y=cd["n"], name="Cases in dataset",
            marker_color=[NAVY, "#3A6EA5", "#4A9EA0", AMBER, CORAL],
            marker_opacity=.8,
            hovertemplate="%{x}: %{y:,} cases<extra></extra>"),
            secondary_y=False)
        fig_sv.add_trace(go.Scatter(
            x=cd["year"], y=cd["med"], mode="lines+markers+text",
            line=dict(color=AMBER, width=2, dash="dot"),
            marker=dict(size=8, color=AMBER),
            text=cd["med"].apply(lambda d: f"{d}d"),
            textposition="top center", textfont_size=9,
            name="Apparent median (misleading ⚠️)",
            hovertemplate="%{x}: %{y}d<extra></extra>"),
            secondary_y=True)
        fig_sv.update_layout(**cl(h=300,
            title="Why apparent 'improvement' is a data artefact",
            showlegend=True,
            legend=dict(orientation="h", y=1.05, x=1, xanchor="right", font_size=9)))
        fig_sv.update_xaxes(title_text="Filing year", showgrid=False)
        fig_sv.update_yaxes(title_text="Cases visible →", secondary_y=False,
                             showgrid=True, gridcolor="#F0F0F0")
        fig_sv.update_yaxes(title_text="Apparent median (days) →", secondary_y=True, showgrid=False)
        st.plotly_chart(fig_sv, use_container_width=True)

        st.markdown("""
<div class="box-warn">
The bars shrink as the years get more recent — not because fewer cases were filed, but because
<strong>only the fast-resolving cases from 2018–2019 had time to close by Jan 2021</strong>.
The dotted line showing faster resolution is a mirage. We cannot draw conclusions about
system-wide improvement from this data.
</div>
""", unsafe_allow_html=True)

    # ── Deep dive 2 ──────────────────────────────────────────────────────
    with st.expander("📅  When are cases filed? (Monthly patterns)"):
        monthly = df.groupby(["filing_year","filing_month"]).size().reset_index(name="n")
        pivot   = monthly.pivot(index="filing_year", columns="filing_month", values="n").fillna(0)
        pivot.columns = [MONTH.get(c, str(c)) for c in pivot.columns]

        fig_hm = px.imshow(pivot, aspect="auto",
            color_continuous_scale=["#EEF5FF", NAVY],
            labels=dict(x="Month", y="Year", color="Cases"),
            title="Filing volume by month — darker = more filings",
            text_auto=True)
        fig_hm.update_layout(**cl(h=240, tl=50, tr=20, tt=44, tb=20))
        fig_hm.update_traces(textfont_size=9)
        st.plotly_chart(fig_hm, use_container_width=True)

        mt = df.groupby("filing_month").size()
        st.markdown(f"""
<div class="box-info">
📌 <strong>{MONTH[int(mt.idxmax())]}</strong> has the most filings — likely post-winter recess.
<strong>{MONTH[int(mt.idxmin())]}</strong> is the quietest. May and December dips align with
court vacation periods.
</div>
""", unsafe_allow_html=True)

    # ── Deep dive 3 ──────────────────────────────────────────────────────
    with st.expander("🏛  Full court performance — all courts with 10+ cases"):
        fig_cm = px.histogram(cs, x="med", nbins=30,
            color_discrete_sequence=[BLUE],
            labels={"med": "Median days to resolution"},
            title=f"How courts are distributed — {len(cs)} courts with 10+ cases")
        fig_cm.add_vline(x=p50, line_dash="dot", line_color=AMBER, line_width=2,
                         annotation_text=f"Overall median: {p50}d",
                         annotation_font_size=9, annotation_font_color=AMBER,
                         annotation_position="top right")
        fig_cm.update_layout(**cl(h=280, xaxis_title="Median days",
            yaxis_title="Number of courts", tl=20, tr=20, tt=44, tb=20))
        fig_cm.update_xaxes(showgrid=False,
            tickvals=[0,365,730,1095,1460], ticktext=["0","1yr","2yrs","3yrs","4yrs"])
        fig_cm.update_yaxes(showgrid=True, gridcolor="#F0F0F0")
        st.plotly_chart(fig_cm, use_container_width=True)

        st.markdown(f"""
<div class="box-info">
📌 Most courts cluster in the 1–2 year range. But there's a long tail of slow courts, and a small
cluster of very fast ones (likely handling specific procedural matters). The spread —
from {fastest_med} days to {slowest_med} days — shows how much court assignment matters.
</div>
""", unsafe_allow_html=True)

    # ── Deep dive 4 — Scorecard ───────────────────────────────────────────
    with st.expander("📊  About this data — what's reliable, what's missing"):
        st.markdown("""
This dashboard is built from an NJDG dataset of Karnataka HC First Appeals (MFA),
accessed via the ISDM Hackathon. Here's an honest field-by-field assessment.
""")
        scorecard = [
            ("Dates (filed & resolved)",    "✅ Complete",      "b-ok",   "100% filled — core metric is reliable"),
            ("How long each case took",     "✅ Complete",      "b-ok",   "Calculated from dates — reliable"),
            ("Which court handled it",      "✅ Complete",      "b-ok",   "175 courts; internal IDs, not public names"),
            ("Case type",                   "✅ All MFA",       "b-ok",   "All First Appeals — narrow but consistent"),
            ("What the outcome was",        f"⚠️ {outcome_pct}% filled", "b-warn", "74% of cases: outcome never entered into NJDG"),
            ("Judge names",                 "❌ Unusable",      "b-bad",  "All say 'Honorable Judge' — no real names"),
            ("Subject matter (Acts)",       "❌ 1.6% filled",  "b-bad",  "What the case was about: mostly unknown"),
            ("Pending cases",               "❌ Not included", "b-bad",  "Only closed cases — survivorship bias"),
            ("Party details",               "❌ Not in data",  "b-bad",  "Names of petitioners/respondents not exported"),
        ]
        half = len(scorecard) // 2 + 1
        c1, c2 = st.columns(2)
        for i, (f, s, cls, note) in enumerate(scorecard):
            col = c1 if i < half else c2
            col.markdown(f"""
<div class="sc-row">
  <div>
    <div class="sc-field"><strong>{f}</strong></div>
    <div class="sc-note">{note}</div>
  </div>
  <span class="badge {cls}">{s}</span>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="box-alert" style="margin-top:1.2rem">
<strong>What we can honestly say:</strong> Court-level variation is real and large.
Speed distributions are valid. Filing patterns are valid. Year-over-year "improvement" claims are
<strong>NOT valid</strong> (survivorship bias). Individual judge performance cannot be assessed.
Subject matter breakdown is not possible.
</div>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  S4 — WHAT CAN YOU DO?                                                  ║
# ╚══════════════════════════════════════════════════════════════════════════╝

st.markdown('<div class="div-line"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="section-wrap white">
<div class="section-inner">
  <p class="sec-kicker">Take action</p>
  <h2 class="sec-h">What can you do as a citizen?</h2>
  <p class="sec-sub">This data is not just for researchers. Here's how it connects to real things you can do.</p>
  <div class="act-grid">
    <div class="act-card">
      <div class="act-ico">🔍</div>
      <p class="act-t">Track your case</p>
      <p class="act-b">Every High Court case has a CNR number. Use eCourts to check your status, next date, and court allocation in real time.</p>
      <a class="act-lnk" href="https://ecourts.gov.in" target="_blank">Go to eCourts →</a>
    </div>
    <div class="act-card">
      <div class="act-ico">📊</div>
      <p class="act-t">See live court data</p>
      <p class="act-b">NJDG publishes real-time pendency statistics across all Indian courts — including how courts are performing right now.</p>
      <a class="act-lnk" href="https://njdg.ecourts.gov.in" target="_blank">Visit NJDG →</a>
    </div>
    <div class="act-card">
      <div class="act-ico">📝</div>
      <p class="act-t">File an RTI</p>
      <p class="act-b">Under the Right to Information Act, you can request court performance data and case-handling information from the HC Registry.</p>
      <a class="act-lnk" href="https://rtionline.gov.in" target="_blank">RTI Portal →</a>
    </div>
    <div class="act-card">
      <div class="act-ico">📖</div>
      <p class="act-t">Read the research</p>
      <p class="act-b">DAKSH India and Vidhi Centre publish independent research on judicial delays and what can be done about them.</p>
      <a class="act-lnk" href="https://dakshindia.org" target="_blank">DAKSH India →</a>
    </div>
  </div>
</div>
</div>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  FOOTER                                                                 ║
# ╚══════════════════════════════════════════════════════════════════════════╝

st.markdown(f"""
<div class="footer">
  <div class="footer-inner">
    <div>
      <h4>About this dashboard</h4>
      Built by <strong style="color:#C5D8E8">Lawgorithm</strong> to make judicial data legible
      to every citizen — not just lawyers and researchers.<br><br>
      <strong style="color:#C5D8E8">Data:</strong> NJDG · Karnataka HC Principal Bench · ISDM Hackathon<br>
      <strong style="color:#C5D8E8">Coverage:</strong> MFA (First Appeals), 2015–2019, disposed by Jan 2021<br>
      <strong style="color:#C5D8E8">Total:</strong> {N:,} closed cases · Version 3.0
    </div>
    <div>
      <h4>Key limitations</h4>
      ① Only closed cases — pending cases not included (survivorship bias)<br>
      ② 74% of cases have no recorded outcome in NJDG<br>
      ③ Judge names anonymised — individual analysis not possible<br>
      ④ Subject matter unknown for 98.4% of cases<br>
      ⑤ Year-on-year trend claims not valid<br><br>
      <a href="https://njdg.ecourts.gov.in">NJDG Portal</a> ·
      <a href="https://ecourts.gov.in">eCourts</a> ·
      <a href="https://dakshindia.org">DAKSH India</a> ·
      <a href="https://vidhilegalpolicy.in">Vidhi Legal</a> ·
      <a href="https://rtionline.gov.in">RTI Portal</a>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
