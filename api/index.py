"""
<<<<<<< HEAD
api/index.py — Flask entry point (Vercel-compatible)
Indian Stock Predictor · Alpha Five Team · Brainware University
=======
api/index.py — Flask entry point for Vercel
Indian Stock Predictor by Alpha Five Team
>>>>>>> 236a2c92b346f989d77d458d7e9deda2ee9cb5d1
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from flask import Flask, jsonify, request, Response
import traceback

from src.data_fetcher import NIFTY50_STOCKS
from src.predictor    import run
<<<<<<< HEAD
from src.charts       import (chart_price, chart_performance,
                               chart_overlay, chart_target,
                               chart_feature_importance)
=======
from src.charts       import chart_price, chart_performance, chart_overlay, chart_next
>>>>>>> 236a2c92b346f989d77d458d7e9deda2ee9cb5d1

app = Flask(__name__)

# ══════════════════════════════════════════════════════════════════════════════
<<<<<<< HEAD
#  FULL PAGE HTML
=======
#  HTML PAGE
>>>>>>> 236a2c92b346f989d77d458d7e9deda2ee9cb5d1
# ══════════════════════════════════════════════════════════════════════════════
HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<<<<<<< HEAD
<title>Indian Stock Predictor · Alpha Five · Brainware University</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Cinzel:wght@700&display=swap" rel="stylesheet"/>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
/* ══════════════════════════════════════════════════════════════════
   CSS VARIABLES
══════════════════════════════════════════════════════════════════ */
:root {
  --bg:          #050d1a;
  --surface:     #08111f;
  --card:        #0c1829;
  --card2:       #0f1e32;
  --border:      #162035;
  --border2:     #1e2f4a;
  --text:        #e8eef6;
  --muted:       #5a7090;
  --muted2:      #3d5570;

  /* Brand palette */
  --saffron:     #ff9500;
  --saffron2:    #ffb733;
  --saffron-glow:rgba(255,149,0,0.18);
  --cyan:        #00c8e8;
  --cyan2:       #38bdf8;
  --cyan-glow:   rgba(0,200,232,0.15);
  --violet:      #a78bfa;
  --violet2:     #c4b5fd;
  --violet-glow: rgba(167,139,250,0.15);
  --green:       #22c55e;
  --red:         #ef4444;
  --gold:        #f59e0b;

  --font:    'DM Sans', sans-serif;
  --mono:    'JetBrains Mono', monospace;
  --display: 'Playfair Display', serif;
  --cinzel:  'Cinzel', serif;
}

/* ══════════════════════════════════════════════════════════════════
   RESET & BASE
══════════════════════════════════════════════════════════════════ */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{
  font-family:var(--font);
  background:var(--bg);
  color:var(--text);
  min-height:100vh;
  overflow-x:hidden;
}

/* ── Animated particle canvas ── */
#canvas-bg{
  position:fixed;inset:0;z-index:0;
  pointer-events:none;opacity:.55;
}

/* ── Subtle grid overlay ── */
body::after{
  content:'';
  position:fixed;inset:0;z-index:0;
  background-image:
    linear-gradient(rgba(0,200,232,.025) 1px,transparent 1px),
    linear-gradient(90deg,rgba(0,200,232,.025) 1px,transparent 1px);
  background-size:56px 56px;
  pointer-events:none;
}

/* ══════════════════════════════════════════════════════════════════
   HEADER
══════════════════════════════════════════════════════════════════ */
header{
  position:relative;z-index:100;
  background:rgba(5,13,26,0.92);
  backdrop-filter:blur(24px);
  border-bottom:1px solid var(--border2);
  padding:0 28px;
  height:82px;
  display:flex;align-items:center;justify-content:space-between;
  gap:16px;
}

/* ── Logo / Title block ── */
.title-block{display:flex;align-items:center;gap:16px}
.flag-icon{
  width:48px;height:48px;border-radius:12px;
  background:linear-gradient(135deg,#ff9500 33%,#fff 33%,#fff 66%,#138808 66%);
  display:flex;align-items:center;justify-content:center;
  font-size:22px;
  box-shadow:0 0 24px rgba(255,149,0,.3),0 0 48px rgba(255,149,0,.12);
  flex-shrink:0;position:relative;overflow:hidden;
}
.flag-icon::after{
  content:'';
  position:absolute;inset:0;
  background:radial-gradient(circle at 50% 50%,rgba(255,255,255,.12),transparent 60%);
}
.title-lines{display:flex;flex-direction:column;gap:1px}

.t-main{
  font-family:var(--cinzel);
  font-size:1.18rem;
  font-weight:700;
  letter-spacing:.06em;
  background:linear-gradient(90deg,#ff9500 0%,#ffcc44 45%,#ff7800 100%);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  background-clip:text;
  text-shadow:none;
  white-space:nowrap;
}
.t-sub1{
  font-family:var(--font);
  font-size:.78rem;
  font-weight:600;
  letter-spacing:.08em;
  color:var(--cyan);
  text-transform:uppercase;
  white-space:nowrap;
}
.t-sub2{
  font-family:var(--font);
  font-size:.7rem;
  font-weight:400;
  letter-spacing:.05em;
  color:var(--violet);
  white-space:nowrap;
}

/* ── Live badge ── */
.live-badge{
  display:flex;align-items:center;gap:7px;
  font-family:var(--mono);font-size:.7rem;
  color:var(--cyan2);
  border:1px solid rgba(0,200,232,.25);
  background:rgba(0,200,232,.06);
  padding:5px 12px;border-radius:20px;
  white-space:nowrap;
}
.pulse-dot{
  width:7px;height:7px;border-radius:50%;
  background:var(--cyan);
  box-shadow:0 0 6px var(--cyan);
  animation:pulse-dot 1.5s ease-in-out infinite;
}
@keyframes pulse-dot{
  0%,100%{opacity:1;transform:scale(1)}
  50%{opacity:.4;transform:scale(.7)}
}

/* ══════════════════════════════════════════════════════════════════
   LAYOUT
══════════════════════════════════════════════════════════════════ */
.layout{
  display:flex;
  min-height:calc(100vh - 82px);
  position:relative;z-index:1;
}

/* ══════════════════════════════════════════════════════════════════
   SIDEBAR
══════════════════════════════════════════════════════════════════ */
aside{
  width:296px;flex-shrink:0;
  background:rgba(8,17,31,0.75);
  border-right:1px solid var(--border2);
  padding:24px 18px 32px;
  overflow-y:auto;
  backdrop-filter:blur(16px);
  display:flex;flex-direction:column;gap:0;
}
aside::-webkit-scrollbar{width:3px}
aside::-webkit-scrollbar-thumb{background:var(--border2);border-radius:4px}

.s-section-label{
  font-size:.65rem;
  text-transform:uppercase;
  letter-spacing:.14em;
  color:var(--muted);
  font-weight:700;
  margin:22px 0 9px;
  display:flex;align-items:center;gap:6px;
}
.s-section-label:first-child{margin-top:0}
.s-section-label::after{
  content:'';flex:1;height:1px;
  background:linear-gradient(to right,var(--border2),transparent);
}

/* Stock search */
.search-wrap{position:relative;margin-bottom:6px}
.search-wrap input{
  width:100%;
  padding:10px 36px 10px 13px;
  background:var(--card);
  border:1px solid var(--border2);
  border-radius:9px;
  color:var(--text);
  font-family:var(--font);font-size:.84rem;
  outline:none;
  transition:border-color .2s,box-shadow .2s;
}
.search-wrap input:focus{
  border-color:var(--cyan);
  box-shadow:0 0 0 3px rgba(0,200,232,.1);
}
.search-wrap input::placeholder{color:var(--muted2)}
.si{position:absolute;right:11px;top:50%;transform:translateY(-50%);color:var(--muted);font-size:15px;pointer-events:none}

/* Stock list */
.stock-list{
  max-height:210px;overflow-y:auto;
  border:1px solid var(--border);border-radius:9px;
  background:var(--card);
}
.stock-list::-webkit-scrollbar{width:3px}
.stock-list::-webkit-scrollbar-thumb{background:var(--border2);border-radius:4px}
.sitem{
  padding:8px 12px;cursor:pointer;
  border-bottom:1px solid rgba(22,32,53,.6);
  transition:background .12s;
  display:flex;align-items:center;justify-content:space-between;
  gap:6px;
}
.sitem:last-child{border-bottom:none}
.sitem:hover{background:rgba(0,200,232,.07)}
.sitem.active{background:rgba(0,200,232,.12);border-left:2px solid var(--cyan)}
.si-name{font-size:.81rem;font-weight:500;color:var(--text)}
.si-sym{font-size:.66rem;font-family:var(--mono);color:var(--muted)}

/* Selected stock pill */
.sel-pill{
  display:none;
  align-items:center;gap:10px;
  background:linear-gradient(135deg,rgba(255,149,0,.08),rgba(0,200,232,.06));
  border:1px solid rgba(255,149,0,.25);
  border-radius:9px;padding:9px 12px;margin-bottom:6px;
}
.sel-pill.show{display:flex}
.sel-dot{width:8px;height:8px;border-radius:50%;background:var(--saffron);flex-shrink:0;box-shadow:0 0 8px var(--saffron)}
.sel-name{font-size:.82rem;font-weight:600;color:var(--saffron2)}
.sel-sym{font-size:.67rem;font-family:var(--mono);color:var(--muted)}

/* Controls */
.ctrl{margin-top:14px}
.ctrl-label{
  font-size:.73rem;color:var(--muted);font-weight:500;
  margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;
}
.ctrl-val{color:var(--cyan);font-family:var(--mono);font-size:.73rem}

input[type=date]{
  width:100%;padding:9px 12px;
  background:var(--card);border:1px solid var(--border2);
  border-radius:9px;color:var(--text);
  font-family:var(--mono);font-size:.84rem;
  outline:none;transition:border-color .2s;
  cursor:pointer;
}
input[type=date]:focus{border-color:var(--cyan);box-shadow:0 0 0 3px rgba(0,200,232,.1)}
input[type=date]::-webkit-calendar-picker-indicator{filter:invert(.4) sepia(1) saturate(3) hue-rotate(172deg);cursor:pointer}

input[type=range]{
  width:100%;-webkit-appearance:none;
  height:4px;background:var(--border2);
  border-radius:2px;outline:none;cursor:pointer;
}
input[type=range]::-webkit-slider-thumb{
  -webkit-appearance:none;width:16px;height:16px;
  border-radius:50%;background:var(--cyan);
  box-shadow:0 0 10px rgba(0,200,232,.5);cursor:pointer;
}

/* Run button */
#run-btn{
  margin-top:22px;width:100%;
  padding:14px;
  background:linear-gradient(135deg,#ff8c00,#ff5e00,#e04000);
  color:white;border:none;border-radius:11px;
  font-family:var(--font);font-size:.95rem;font-weight:700;
  cursor:pointer;letter-spacing:.03em;
  position:relative;overflow:hidden;
  transition:transform .15s,box-shadow .2s,opacity .2s;
  box-shadow:0 4px 24px rgba(255,140,0,.35);
}
#run-btn::before{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(255,255,255,.15),transparent 50%);
}
#run-btn::after{
  content:'';position:absolute;inset:0;
  background:radial-gradient(circle at 50% 120%,rgba(255,255,255,.1),transparent 60%);
}
#run-btn:hover:not(:disabled){transform:translateY(-2px);box-shadow:0 8px 32px rgba(255,140,0,.45)}
#run-btn:active:not(:disabled){transform:translateY(0)}
#run-btn:disabled{opacity:.4;cursor:not-allowed;transform:none}

/* ══════════════════════════════════════════════════════════════════
   MAIN CONTENT
══════════════════════════════════════════════════════════════════ */
main{flex:1;padding:26px 28px;overflow-y:auto;min-width:0}

/* Status bar */
#status{
  display:none;align-items:center;gap:10px;
  padding:11px 16px;border-radius:10px;
  margin-bottom:18px;font-size:.84rem;font-weight:500;
  border:1px solid;
}
#status.show{display:flex}
#status.info{background:rgba(0,200,232,.07);border-color:rgba(0,200,232,.25);color:#7dd3fc}
#status.success{background:rgba(34,197,94,.07);border-color:rgba(34,197,94,.25);color:#86efac}
#status.error{background:rgba(239,68,68,.07);border-color:rgba(239,68,68,.25);color:#fca5a5}
#status.warn{background:rgba(245,158,11,.07);border-color:rgba(245,158,11,.25);color:#fcd34d}

/* ── Welcome screen ── */
#welcome{
  display:flex;flex-direction:column;
  align-items:center;justify-content:center;
  min-height:72vh;text-align:center;
  gap:0;
}
.orb-container{position:relative;margin-bottom:36px}
.orb{
  width:130px;height:130px;border-radius:50%;
  background:radial-gradient(circle at 35% 35%,
    rgba(255,149,0,.3) 0%,
    rgba(0,200,232,.15) 50%,
    rgba(167,139,250,.1) 100%);
  border:1px solid rgba(255,149,0,.3);
  display:flex;align-items:center;justify-content:center;
  font-size:56px;
  box-shadow:
    0 0 60px rgba(255,149,0,.18),
    0 0 120px rgba(0,200,232,.1),
    inset 0 0 40px rgba(255,149,0,.06);
  animation:orb-pulse 4s ease-in-out infinite;
}
@keyframes orb-pulse{
  0%,100%{
    box-shadow:0 0 60px rgba(255,149,0,.18),0 0 120px rgba(0,200,232,.1),inset 0 0 40px rgba(255,149,0,.06);
    transform:scale(1);
  }
  50%{
    box-shadow:0 0 90px rgba(255,149,0,.28),0 0 180px rgba(0,200,232,.18),inset 0 0 60px rgba(255,149,0,.1);
    transform:scale(1.04);
  }
}
.orb-ring{
  position:absolute;inset:-18px;border-radius:50%;
  border:1px solid rgba(0,200,232,.18);
  animation:ring-spin 8s linear infinite;
}
.orb-ring2{
  position:absolute;inset:-32px;border-radius:50%;
  border:1px dashed rgba(255,149,0,.12);
  animation:ring-spin 14s linear infinite reverse;
}
@keyframes ring-spin{to{transform:rotate(360deg)}}

#welcome h2{
  font-family:var(--display);
  font-size:2.1rem;font-weight:900;
  background:linear-gradient(135deg,var(--text),#94a3b8);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  margin-bottom:12px;letter-spacing:-.02em;
}
#welcome p{
  color:var(--muted);font-size:.9rem;line-height:1.75;
  max-width:500px;
}
.model-pills{display:flex;gap:8px;margin-top:22px;flex-wrap:wrap;justify-content:center}
.pill{
  padding:5px 15px;border-radius:20px;
  font-size:.73rem;font-weight:600;border:1px solid;
  letter-spacing:.03em;
}
.pill-a{border-color:rgba(0,200,232,.4);color:var(--cyan);background:rgba(0,200,232,.07)}
.pill-b{border-color:rgba(251,146,60,.4);color:#fb923c;background:rgba(251,146,60,.07)}
.pill-c{border-color:rgba(167,139,250,.4);color:var(--violet);background:rgba(167,139,250,.07)}

/* ── Metric cards ── */
.metric-row{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
  gap:12px;margin-bottom:22px;
}
.mcard{
  background:var(--card);border:1px solid var(--border);
  border-radius:13px;padding:17px 18px;
  position:relative;overflow:hidden;
  transition:border-color .2s,transform .2s,box-shadow .2s;
}
.mcard:hover{
  border-color:var(--border2);
  transform:translateY(-2px);
  box-shadow:0 8px 32px rgba(0,0,0,.25);
}
.mcard::before{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
}
.mcard.saffron::before{background:linear-gradient(90deg,var(--saffron),transparent)}
.mcard.cyan::before{background:linear-gradient(90deg,var(--cyan),transparent)}
.mcard.green::before{background:linear-gradient(90deg,var(--green),transparent)}
.mcard.red::before{background:linear-gradient(90deg,var(--red),transparent)}
.mcard.violet::before{background:linear-gradient(90deg,var(--violet),transparent)}
.mcard.gold::before{background:linear-gradient(90deg,var(--gold),transparent)}
.mcard::after{
  content:'';position:absolute;inset:0;
  background:radial-gradient(circle at 80% 20%,rgba(255,255,255,.025),transparent 60%);
  pointer-events:none;
}

.mc-label{font-size:.63rem;text-transform:uppercase;letter-spacing:.12em;color:var(--muted);font-weight:700}
.mc-val{font-family:var(--mono);font-size:1.45rem;font-weight:600;color:var(--text);margin:5px 0 3px;line-height:1}
.mc-sub{font-size:.72rem;color:var(--muted)}
.mc-up{color:var(--green)}.mc-dn{color:var(--red)}

/* Confidence bar */
.conf-bar-wrap{
  margin-top:10px;height:4px;background:var(--border);border-radius:2px;overflow:hidden;
}
.conf-bar-fill{height:100%;border-radius:2px;transition:width .6s ease}

/* ── Tabs ── */
.tab-bar{
  display:flex;gap:2px;
  border-bottom:1px solid var(--border);
  margin-bottom:20px;
}
.tab-btn{
  padding:10px 18px;border:none;background:transparent;
  color:var(--muted);font-family:var(--font);font-size:.83rem;font-weight:600;
  cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-1px;
  transition:color .2s,border-color .2s;display:flex;align-items:center;gap:7px;
  border-radius:4px 4px 0 0;
  white-space:nowrap;
}
.tab-btn:hover{color:var(--text);background:rgba(255,255,255,.03)}
.tab-btn.active{color:var(--saffron);border-bottom-color:var(--saffron)}
.tab-panel{display:none}.tab-panel.active{display:block}

/* ── Chart card ── */
.chart-card{
  background:var(--card);border:1px solid var(--border);
  border-radius:13px;padding:20px;margin-bottom:16px;
  transition:border-color .2s;
}
.chart-card:hover{border-color:var(--border2)}
.chart-card h3{
  font-size:.72rem;text-transform:uppercase;letter-spacing:.1em;
  color:var(--muted);font-weight:700;margin-bottom:14px;
  display:flex;align-items:center;gap:8px;
}
.chart-card h3 .acc{color:var(--saffron)}

/* ── Prediction highlight card ── */
.pred-hero{
  background:linear-gradient(135deg,rgba(255,149,0,.08),rgba(0,200,232,.05),rgba(167,139,250,.06));
  border:1px solid rgba(255,149,0,.2);
  border-radius:16px;padding:24px 28px;
  margin-bottom:22px;position:relative;overflow:hidden;
}
.pred-hero::before{
  content:'';position:absolute;inset:0;
  background:radial-gradient(circle at 80% 20%,rgba(255,149,0,.06),transparent 50%);
  pointer-events:none;
}
.pred-hero-label{
  font-size:.68rem;text-transform:uppercase;letter-spacing:.14em;
  color:var(--saffron);font-weight:700;margin-bottom:8px;
}
.pred-hero-val{
  font-family:var(--mono);font-size:2.5rem;font-weight:600;
  color:var(--text);line-height:1;margin-bottom:8px;
}
.pred-hero-val.up{color:var(--green)}.pred-hero-val.dn{color:var(--red)}
.pred-hero-meta{font-size:.8rem;color:var(--muted);display:flex;gap:16px;flex-wrap:wrap}
.pred-hero-meta span b{color:var(--text)}
.conf-pill{
  display:inline-flex;align-items:center;gap:5px;
  padding:3px 10px;border-radius:12px;
  font-size:.7rem;font-weight:600;
  background:rgba(167,139,250,.12);border:1px solid rgba(167,139,250,.25);
  color:var(--violet2);
}

/* ── Tables ── */
.tbl-wrap{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:.83rem}
thead th{
  background:rgba(22,32,53,.5);padding:10px 15px;
  text-align:left;font-size:.67rem;text-transform:uppercase;
  letter-spacing:.09em;color:var(--muted);font-weight:700;
  border-bottom:1px solid var(--border);
}
tbody td{
  padding:11px 15px;border-bottom:1px solid rgba(22,32,53,.5);
  color:var(--text);font-family:var(--mono);font-size:.81rem;
}
tbody tr:hover td{background:rgba(0,200,232,.03)}
tbody tr:last-child td{border-bottom:none}
.td-model{font-family:var(--font);font-weight:600;color:var(--text)}
.badge{
  display:inline-block;padding:2px 9px;border-radius:12px;
  font-size:.72rem;font-weight:700;font-family:var(--mono);
}
.badge-up{background:rgba(34,197,94,.12);color:var(--green);border:1px solid rgba(34,197,94,.25)}
.badge-dn{background:rgba(239,68,68,.12);color:var(--red);border:1px solid rgba(239,68,68,.25)}

/* Spinner */
.spinner{
  width:17px;height:17px;border-radius:50%;flex-shrink:0;
  border:2px solid rgba(0,200,232,.2);
  border-top-color:var(--cyan);
  animation:spin .6s linear infinite;
}
@keyframes spin{to{transform:rotate(360deg)}}

/* Reveal */
.reveal{animation:reveal .45s ease both}
@keyframes reveal{
  from{opacity:0;transform:translateY(14px)}
  to{opacity:1;transform:translateY(0)}
}
.reveal-2{animation-delay:.1s}.reveal-3{animation-delay:.2s}.reveal-4{animation-delay:.3s}

/* Scrollbar */
::-webkit-scrollbar{width:4px;height:4px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--border2);border-radius:4px}

/* Horizon warning */
.horizon-warn{
  display:none;
  padding:10px 14px;border-radius:8px;
  background:rgba(245,158,11,.07);border:1px solid rgba(245,158,11,.2);
  color:#fcd34d;font-size:.78rem;margin-top:10px;line-height:1.5;
}
.horizon-warn.show{display:block}

@media(max-width:800px){
  .layout{flex-direction:column}
  aside{width:100%;border-right:none;border-bottom:1px solid var(--border2);max-height:400px}
  main{padding:16px}
  .t-main{font-size:.95rem}
  .t-sub1,.t-sub2{display:none}
=======
<title>Indian Stock Predictor · Alpha Five</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
/* ── CSS Variables ──────────────────────────────────────── */
:root {
  --bg:       #020817;
  --surface:  #0f172a;
  --card:     #111827;
  --border:   #1e293b;
  --border2:  #243044;
  --text:     #e2e8f0;
  --muted:    #64748b;
  --accent:   #38bdf8;
  --accent2:  #818cf8;
  --green:    #22c55e;
  --red:      #ef4444;
  --gold:     #f59e0b;
  --orange:   #fb923c;
  --glow:     rgba(56,189,248,0.18);
  --font:     'Space Grotesk', sans-serif;
  --mono:     'JetBrains Mono', monospace;
  --display:  'Syne', sans-serif;
}

/* ── Reset ──────────────────────────────────────────────── */
*,*::before,*::after { box-sizing:border-box; margin:0; padding:0; }
html { scroll-behavior:smooth; }
body {
  font-family: var(--font);
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  overflow-x: hidden;
}

/* ── Animated background grid ───────────────────────────── */
body::before {
  content:'';
  position:fixed; inset:0; z-index:0;
  background-image:
    linear-gradient(rgba(56,189,248,.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(56,189,248,.03) 1px, transparent 1px);
  background-size: 48px 48px;
  pointer-events:none;
}

/* ── Header ─────────────────────────────────────────────── */
header {
  position: relative; z-index:10;
  border-bottom: 1px solid var(--border);
  background: rgba(2,8,23,0.92);
  backdrop-filter: blur(20px);
  padding: 0 32px;
  display: flex; align-items: center; justify-content: space-between;
  height: 72px;
}
.logo {
  display: flex; align-items: center; gap: 14px;
}
.logo-icon {
  width: 42px; height: 42px;
  background: linear-gradient(135deg, #38bdf8, #818cf8);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px;
  box-shadow: 0 0 20px rgba(56,189,248,0.3);
}
.logo-text h1 {
  font-family: var(--display);
  font-size: 1.2rem;
  font-weight: 800;
  background: linear-gradient(90deg, #38bdf8, #818cf8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.02em;
}
.logo-text p {
  font-size: 0.7rem;
  color: var(--muted);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-top: 1px;
}
.header-badge {
  font-family: var(--mono);
  font-size: 0.7rem;
  color: var(--accent);
  border: 1px solid rgba(56,189,248,0.3);
  padding: 4px 12px;
  border-radius: 20px;
  background: rgba(56,189,248,0.06);
}

/* ── Layout ─────────────────────────────────────────────── */
.layout {
  display: flex;
  min-height: calc(100vh - 72px);
  position: relative; z-index:1;
}

/* ── Sidebar ─────────────────────────────────────────────── */
aside {
  width: 290px;
  flex-shrink: 0;
  background: rgba(15,23,42,0.7);
  border-right: 1px solid var(--border);
  padding: 28px 20px;
  overflow-y: auto;
  backdrop-filter: blur(10px);
}
.sidebar-section { margin-bottom: 8px; }
.sidebar-label {
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--muted);
  font-weight: 600;
  margin-bottom: 10px;
  margin-top: 20px;
  display: flex; align-items: center; gap: 6px;
}
.sidebar-label:first-child { margin-top: 0; }

/* Stock search */
.stock-search-wrap {
  position: relative;
  margin-bottom: 6px;
}
.stock-search-wrap input {
  width: 100%;
  padding: 10px 36px 10px 12px;
  background: var(--card);
  border: 1px solid var(--border2);
  border-radius: 8px;
  color: var(--text);
  font-family: var(--font);
  font-size: 0.85rem;
  outline: none;
  transition: border-color .2s, box-shadow .2s;
}
.stock-search-wrap input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(56,189,248,0.12);
}
.search-icon {
  position:absolute; right:10px; top:50%;
  transform:translateY(-50%);
  color:var(--muted); font-size:14px; pointer-events:none;
}

/* Stock list */
.stock-list {
  max-height: 220px;
  overflow-y: auto;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--card);
}
.stock-list::-webkit-scrollbar { width: 4px; }
.stock-list::-webkit-scrollbar-track { background: transparent; }
.stock-list::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 4px; }
.stock-item {
  padding: 9px 12px;
  cursor: pointer;
  border-bottom: 1px solid rgba(30,41,59,0.5);
  transition: background .15s;
  display: flex; align-items: center; justify-content: space-between;
}
.stock-item:last-child { border-bottom: none; }
.stock-item:hover { background: rgba(56,189,248,0.08); }
.stock-item.selected {
  background: rgba(56,189,248,0.14);
  color: var(--accent);
}
.stock-item-name { font-size: 0.82rem; font-weight: 500; }
.stock-item-sym  { font-size: 0.68rem; font-family: var(--mono); color: var(--muted); }

/* Form controls */
.ctrl-group { margin-top: 16px; }
.ctrl-label {
  font-size: 0.75rem;
  color: var(--muted);
  font-weight: 500;
  margin-bottom: 6px;
  display: flex; justify-content: space-between;
}
.ctrl-label span { color: var(--accent); font-family: var(--mono); }

input[type=date], input[type=number] {
  width: 100%;
  padding: 9px 12px;
  background: var(--card);
  border: 1px solid var(--border2);
  border-radius: 8px;
  color: var(--text);
  font-family: var(--mono);
  font-size: 0.85rem;
  outline: none;
  transition: border-color .2s;
}
input[type=date]:focus, input[type=number]:focus {
  border-color: var(--accent);
}
input[type=date]::-webkit-calendar-picker-indicator { filter: invert(0.5); }

/* Range slider */
input[type=range] {
  width: 100%;
  -webkit-appearance: none;
  height: 4px;
  background: var(--border2);
  border-radius: 2px;
  outline: none;
  cursor: pointer;
}
input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px; height: 16px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 8px var(--glow);
  cursor: pointer;
}

/* Run button */
#run-btn {
  margin-top: 24px;
  width: 100%;
  padding: 13px;
  background: linear-gradient(135deg, #0ea5e9, #6366f1);
  color: white;
  border: none;
  border-radius: 10px;
  font-family: var(--font);
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  letter-spacing: 0.02em;
  position: relative;
  overflow: hidden;
  transition: opacity .2s, transform .15s, box-shadow .2s;
  box-shadow: 0 4px 20px rgba(14,165,233,0.3);
}
#run-btn::before {
  content:'';
  position:absolute; inset:0;
  background: linear-gradient(135deg, rgba(255,255,255,0.12), transparent);
}
#run-btn:hover  { opacity:.92; transform:translateY(-1px); box-shadow: 0 6px 28px rgba(14,165,233,0.4); }
#run-btn:active { transform:translateY(0); }
#run-btn:disabled { opacity:.45; cursor:not-allowed; transform:none; }

/* Selected stock display */
.selected-display {
  background: rgba(56,189,248,0.06);
  border: 1px solid rgba(56,189,248,0.2);
  border-radius: 8px;
  padding: 10px 12px;
  margin-bottom: 6px;
  display: none;
}
.selected-display.show { display: block; }
.selected-display .name { font-size: 0.82rem; font-weight: 600; color: var(--accent); }
.selected-display .sym  { font-size: 0.7rem; font-family: var(--mono); color: var(--muted); margin-top: 2px; }

/* ── Main content ────────────────────────────────────────── */
main {
  flex: 1;
  padding: 28px 32px;
  overflow-y: auto;
}

/* ── Welcome screen ──────────────────────────────────────── */
#welcome {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
  text-align: center;
}
.welcome-orb {
  width: 120px; height: 120px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(56,189,248,0.25), rgba(99,102,241,0.1));
  border: 1px solid rgba(56,189,248,0.3);
  display: flex; align-items: center; justify-content: center;
  font-size: 52px;
  margin-bottom: 28px;
  box-shadow: 0 0 60px rgba(56,189,248,0.15);
  animation: pulse-orb 3s ease-in-out infinite;
}
@keyframes pulse-orb {
  0%,100% { box-shadow: 0 0 60px rgba(56,189,248,0.15); }
  50%      { box-shadow: 0 0 90px rgba(56,189,248,0.28); }
}
#welcome h2 {
  font-family: var(--display);
  font-size: 2rem;
  font-weight: 800;
  background: linear-gradient(90deg, #e2e8f0, #94a3b8);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  margin-bottom: 12px;
}
#welcome p { color: var(--muted); font-size: 0.9rem; line-height: 1.7; max-width: 480px; }
.model-pills { display: flex; gap: 8px; margin-top: 20px; flex-wrap: wrap; justify-content: center; }
.pill {
  padding: 5px 14px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  border: 1px solid;
}
.pill-blue   { border-color: rgba(56,189,248,0.4);  color: #38bdf8;  background: rgba(56,189,248,0.07); }
.pill-purple { border-color: rgba(129,140,248,0.4); color: #818cf8; background: rgba(129,140,248,0.07); }
.pill-orange { border-color: rgba(251,146,60,0.4);  color: #fb923c;  background: rgba(251,146,60,0.07); }

/* ── Status bar ──────────────────────────────────────────── */
#status {
  display: none;
  padding: 12px 18px;
  border-radius: 10px;
  margin-bottom: 20px;
  font-size: 0.85rem;
  font-weight: 500;
  align-items: center;
  gap: 10px;
  border: 1px solid;
}
#status.show { display: flex; }
#status.info    { background: rgba(56,189,248,0.08);  border-color: rgba(56,189,248,0.25);  color: #7dd3fc; }
#status.success { background: rgba(34,197,94,0.08);   border-color: rgba(34,197,94,0.25);   color: #86efac; }
#status.error   { background: rgba(239,68,68,0.08);   border-color: rgba(239,68,68,0.25);   color: #fca5a5; }

/* ── Metric cards ─────────────────────────────────────────── */
.metric-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 14px;
  margin-bottom: 24px;
}
.metric-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 18px 20px;
  position: relative;
  overflow: hidden;
  transition: border-color .2s, transform .2s;
}
.metric-card:hover { border-color: var(--border2); transform: translateY(-2px); }
.metric-card::before {
  content:'';
  position:absolute;
  top:0; left:0; right:0;
  height:2px;
}
.metric-card.blue::before   { background: linear-gradient(90deg, #38bdf8, transparent); }
.metric-card.purple::before { background: linear-gradient(90deg, #818cf8, transparent); }
.metric-card.green::before  { background: linear-gradient(90deg, #22c55e, transparent); }
.metric-card.red::before    { background: linear-gradient(90deg, #ef4444, transparent); }
.metric-card.gold::before   { background: linear-gradient(90deg, #f59e0b, transparent); }

.m-label { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--muted); font-weight: 600; }
.m-value { font-family: var(--mono); font-size: 1.5rem; font-weight: 600; color: var(--text); margin: 6px 0 4px; }
.m-sub   { font-size: 0.75rem; color: var(--muted); }
.m-up    { color: var(--green); }
.m-dn    { color: var(--red); }

/* ── Tabs ────────────────────────────────────────────────── */
.tab-bar {
  display: flex; gap: 4px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 20px;
}
.tab-btn {
  padding: 10px 20px;
  border: none; background: transparent;
  color: var(--muted);
  font-family: var(--font); font-size: 0.85rem; font-weight: 600;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  transition: color .2s, border-color .2s;
  display: flex; align-items: center; gap: 7px;
}
.tab-btn:hover { color: var(--text); }
.tab-btn.active { color: var(--accent); border-bottom-color: var(--accent); }

.tab-panel { display: none; }
.tab-panel.active { display: block; }

/* ── Chart card ──────────────────────────────────────────── */
.chart-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 18px;
}
.chart-card h3 {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--muted);
  font-weight: 700;
  margin-bottom: 14px;
  display: flex; align-items: center; gap: 8px;
}
.chart-card h3 span { color: var(--accent); }

/* ── Tables ──────────────────────────────────────────────── */
.tbl-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-size: 0.84rem; }
thead th {
  background: rgba(30,41,59,0.6);
  padding: 11px 16px;
  text-align: left;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
  font-weight: 700;
  border-bottom: 1px solid var(--border);
}
tbody td {
  padding: 12px 16px;
  border-bottom: 1px solid rgba(30,41,59,0.5);
  color: var(--text);
  font-family: var(--mono);
  font-size: 0.83rem;
}
tbody tr:hover td { background: rgba(56,189,248,0.04); }
tbody tr:last-child td { border-bottom: none; }
.td-model { font-family: var(--font); font-weight: 600; color: var(--text); }

.badge {
  display: inline-block;
  padding: 3px 9px;
  border-radius: 20px;
  font-size: 0.74rem;
  font-weight: 700;
}
.badge-up { background: rgba(34,197,94,0.15); color: var(--green); border: 1px solid rgba(34,197,94,0.3); }
.badge-dn { background: rgba(239,68,68,0.15);  color: var(--red);   border: 1px solid rgba(239,68,68,0.3); }

/* ── Loading spinner ─────────────────────────────────────── */
.spinner {
  width: 18px; height: 18px;
  border: 2px solid rgba(56,189,248,0.2);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin .6s linear infinite;
  flex-shrink: 0;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Reveal animation ────────────────────────────────────── */
.reveal { animation: reveal .4s ease both; }
@keyframes reveal {
  from { opacity:0; transform:translateY(12px); }
  to   { opacity:1; transform:translateY(0); }
}

/* ── Scrollbar ───────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 4px; }

@media (max-width:768px) {
  .layout { flex-direction: column; }
  aside   { width:100%; border-right:none; border-bottom:1px solid var(--border); max-height:420px; }
  main    { padding: 18px; }
>>>>>>> 236a2c92b346f989d77d458d7e9deda2ee9cb5d1
}
</style>
</head>
<body>

<<<<<<< HEAD
<!-- Particle background -->
<canvas id="canvas-bg"></canvas>

<!-- ══ HEADER ═══════════════════════════════════════════════════════════ -->
<header>
  <div class="title-block">
    <div class="flag-icon">🇮🇳</div>
    <div class="title-lines">
      <div class="t-main">Indian Stock Predictor</div>
      <div class="t-sub1">⚡ by Alpha Five Team</div>
      <div class="t-sub2">✦ Brainware University Project</div>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:12px">
    <div class="live-badge">
      <div class="pulse-dot"></div>
      Nifty 50 · Live NSE Data
    </div>
    <div class="live-badge" style="border-color:rgba(167,139,250,.25);background:rgba(167,139,250,.06);color:var(--violet2)">
      3 ML Models
    </div>
  </div>
=======
<!-- ══ HEADER ═══════════════════════════════════════════════════ -->
<header>
  <div class="logo">
    <div class="logo-icon">📈</div>
    <div class="logo-text">
      <h1>Indian Stock Predictor</h1>
      <p>by Alpha Five Team</p>
    </div>
  </div>
  <div class="header-badge">Nifty 50 · 3 ML Models · Live NSE Data</div>
>>>>>>> 236a2c92b346f989d77d458d7e9deda2ee9cb5d1
</header>

<div class="layout">

<<<<<<< HEAD
<!-- ══ SIDEBAR ══════════════════════════════════════════════════════════ -->
<aside>

  <div class="s-section-label">🏢 Select Stock</div>

  <div class="search-wrap">
    <input type="text" id="stock-search" placeholder="Search Nifty 50 stocks…"
           autocomplete="off" oninput="filterStocks()"/>
    <span class="si">⌕</span>
  </div>

  <div class="sel-pill" id="sel-pill">
    <div class="sel-dot"></div>
    <div>
      <div class="sel-name" id="sel-name">—</div>
      <div class="sel-sym"  id="sel-sym">—</div>
    </div>
=======
<!-- ══ SIDEBAR ══════════════════════════════════════════════════ -->
<aside>

  <div class="sidebar-label">🏢 Select Stock</div>

  <div class="stock-search-wrap">
    <input type="text" id="stock-search" placeholder="Search Nifty 50 stocks…" autocomplete="off" oninput="filterStocks()"/>
    <span class="search-icon">⌕</span>
  </div>

  <div class="selected-display" id="sel-display">
    <div class="name" id="sel-name">—</div>
    <div class="sym"  id="sel-sym">—</div>
>>>>>>> 236a2c92b346f989d77d458d7e9deda2ee9cb5d1
  </div>

  <div class="stock-list" id="stock-list"></div>

<<<<<<< HEAD
  <div class="s-section-label" style="margin-top:20px">📅 Prediction Date</div>
  <input type="date" id="pred-date"/>
  <div class="horizon-warn" id="horizon-warn">
    ⚠️ Predicting far ahead increases uncertainty. The model uses recursive forecasting and shows ±1σ confidence bands.
  </div>

  <div class="ctrl">
    <div class="ctrl-label">
      <span>📆 History Days</span>
      <span class="ctrl-val" id="lb-val">730</span>
    </div>
    <input type="range" id="lookback" min="180" max="1095" value="730" step="30"
           oninput="document.getElementById('lb-val').textContent=this.value"/>
  </div>

  <div class="ctrl">
    <div class="ctrl-label">
      <span>🧪 Test Split</span>
      <span class="ctrl-val" id="ts-val">20%</span>
=======
  <div class="ctrl-group">
    <div class="sidebar-label">📅 Prediction Date</div>
    <input type="date" id="pred-date"/>
  </div>

  <div class="ctrl-group">
    <div class="sidebar-label">📆 History Days
      <span style="margin-left:auto;font-family:var(--mono);color:var(--accent)" id="lb-val">365</span>
    </div>
    <input type="range" id="lookback" min="90" max="730" value="365" step="30"
           oninput="document.getElementById('lb-val').textContent=this.value"/>
  </div>

  <div class="ctrl-group">
    <div class="sidebar-label">🧪 Test Split
      <span style="margin-left:auto;font-family:var(--mono);color:var(--accent)" id="ts-val">20%</span>
>>>>>>> 236a2c92b346f989d77d458d7e9deda2ee9cb5d1
    </div>
    <input type="range" id="test-frac" min="0.1" max="0.35" value="0.2" step="0.05"
           oninput="document.getElementById('ts-val').textContent=Math.round(this.value*100)+'%'"/>
  </div>

<<<<<<< HEAD
  <button id="run-btn" onclick="runAnalysis()" disabled>
    🚀 &nbsp; Run Analysis
=======
  <div class="ctrl-group">
    <div class="sidebar-label">⏩ Days Ahead</div>
    <input type="number" id="pred-days" min="1" max="5" value="1"/>
  </div>

  <button id="run-btn" onclick="runAnalysis()" disabled>
    🚀 &nbsp;Run Analysis
>>>>>>> 236a2c92b346f989d77d458d7e9deda2ee9cb5d1
  </button>

</aside>

<<<<<<< HEAD
<!-- ══ MAIN ═════════════════════════════════════════════════════════════ -->
=======
<!-- ══ MAIN ═════════════════════════════════════════════════════ -->
>>>>>>> 236a2c92b346f989d77d458d7e9deda2ee9cb5d1
<main>

  <div id="status"></div>

  <!-- Welcome -->
  <div id="welcome">
<<<<<<< HEAD
    <div class="orb-container">
      <div class="orb-ring2"></div>
      <div class="orb-ring"></div>
      <div class="orb">📊</div>
    </div>
    <h2>Start Your Analysis</h2>
    <p>Choose a Nifty 50 stock, pick a prediction date, and let three
       production-grade ML models forecast the price for you.</p>
    <div class="model-pills">
      <span class="pill pill-a">Ridge Regression</span>
      <span class="pill pill-b">Gradient Boosting</span>
      <span class="pill pill-c">Random Forest</span>
    </div>
  </div>

  <!-- Results -->
  <div id="results" style="display:none">

    <!-- Prediction hero -->
    <div class="pred-hero reveal" id="pred-hero"></div>

    <!-- Metric cards -->
    <div class="metric-row reveal reveal-2" id="metric-row"></div>
=======
    <div class="welcome-orb">📊</div>
    <h2>Start Predicting</h2>
    <p>Choose a Nifty 50 stock from the sidebar, set your parameters, and click <strong style="color:var(--accent)">Run Analysis</strong> to see ML-powered price predictions.</p>
    <div class="model-pills">
      <span class="pill pill-blue">Linear Regression</span>
      <span class="pill pill-orange">Decision Tree</span>
      <span class="pill pill-purple">Random Forest</span>
    </div>
  </div>

  <!-- Results (hidden until analysis runs) -->
  <div id="results" style="display:none">

    <!-- Metric cards -->
    <div class="metric-row reveal" id="metric-row"></div>
>>>>>>> 236a2c92b346f989d77d458d7e9deda2ee9cb5d1

    <!-- Tabs -->
    <div class="tab-bar">
      <button class="tab-btn active" onclick="switchTab('tech',this)">📊 Technical Chart</button>
      <button class="tab-btn"        onclick="switchTab('ml',this)">🤖 Model Results</button>
      <button class="tab-btn"        onclick="switchTab('pred',this)">🔮 Predictions</button>
<<<<<<< HEAD
      <button class="tab-btn"        onclick="switchTab('feat',this)">⚙️ Features</button>
    </div>

    <!-- Technical Chart tab -->
    <div id="tab-tech" class="tab-panel active">
      <div class="chart-card reveal">
        <h3><span class="acc">◈</span> Candlestick · SMA 20/50 · EMA 20 · Bollinger Bands · Volume · RSI</h3>
        <div id="ch-price" style="min-height:860px"></div>
      </div>
    </div>

    <!-- Model Results tab -->
    <div id="tab-ml" class="tab-panel">
      <div class="chart-card reveal">
        <h3><span class="acc">◈</span> Model Performance — RMSE · MAE · R² · CV-RMSE (Walk-Forward)</h3>
        <div id="ch-perf" style="min-height:420px"></div>
      </div>
      <div class="chart-card reveal reveal-2">
        <h3><span class="acc">◈</span> Predictions vs Actual Price (Test Window)</h3>
        <div id="ch-overlay" style="min-height:500px"></div>
      </div>
      <div class="chart-card reveal reveal-3">
        <h3><span class="acc">◈</span> Performance Summary</h3>
=======
    </div>

    <!-- Tab: Technical -->
    <div id="tab-tech" class="tab-panel active">
      <div class="chart-card reveal">
        <h3><span>◈</span> Price · SMA 20/50 · Bollinger Bands · Volume · RSI</h3>
        <div id="ch-price" style="min-height:820px"></div>
      </div>
    </div>

    <!-- Tab: ML Results -->
    <div id="tab-ml" class="tab-panel">
      <div class="chart-card reveal">
        <h3><span>◈</span> Model Performance — RMSE · MAE · R²</h3>
        <div id="ch-perf" style="min-height:380px"></div>
      </div>
      <div class="chart-card reveal" style="animation-delay:.1s">
        <h3><span>◈</span> Predictions vs Actual Price (Test Window)</h3>
        <div id="ch-overlay" style="min-height:480px"></div>
      </div>
      <div class="chart-card reveal" style="animation-delay:.2s">
        <h3><span>◈</span> Performance Summary</h3>
>>>>>>> 236a2c92b346f989d77d458d7e9deda2ee9cb5d1
        <div class="tbl-wrap" id="perf-tbl"></div>
      </div>
    </div>

<<<<<<< HEAD
    <!-- Predictions tab -->
    <div id="tab-pred" class="tab-panel">
      <div class="chart-card reveal">
        <h3><span class="acc">◈</span> Target-Date Prediction by Model (±1σ Confidence)</h3>
        <div id="ch-target" style="min-height:360px"></div>
      </div>
      <div class="chart-card reveal reveal-2">
        <h3><span class="acc">◈</span> Prediction Summary</h3>
=======
    <!-- Tab: Predictions -->
    <div id="tab-pred" class="tab-panel">
      <div class="chart-card reveal">
        <h3><span>◈</span> Next-Day Prediction by Model</h3>
        <div id="ch-next" style="min-height:340px"></div>
      </div>
      <div class="chart-card reveal" style="animation-delay:.1s">
        <h3><span>◈</span> Prediction Summary</h3>
>>>>>>> 236a2c92b346f989d77d458d7e9deda2ee9cb5d1
        <div class="tbl-wrap" id="pred-tbl"></div>
      </div>
    </div>

<<<<<<< HEAD
    <!-- Feature Importance tab -->
    <div id="tab-feat" class="tab-panel">
      <div class="chart-card reveal">
        <h3><span class="acc">◈</span> Feature Importance — Top 10 Drivers per Model</h3>
        <div id="ch-feat" style="min-height:380px"></div>
      </div>
      <div class="chart-card reveal reveal-2">
        <h3><span class="acc">◈</span> All 18 Engineered Features Explained</h3>
        <div class="tbl-wrap" id="feat-tbl"></div>
      </div>
    </div>

  </div><!-- #results -->

</main>
</div><!-- .layout -->

<script>
/* ════════════════════════════════════════════════════════════════
   PARTICLE BACKGROUND
════════════════════════════════════════════════════════════════ */
(function(){
  const c = document.getElementById('canvas-bg');
  const ctx = c.getContext('2d');
  let W, H, pts=[];
  function resize(){W=c.width=innerWidth;H=c.height=innerHeight}
  resize();window.addEventListener('resize',resize);
  for(let i=0;i<60;i++) pts.push({
    x:Math.random()*1920, y:Math.random()*1080,
    vx:(Math.random()-.5)*.25, vy:(Math.random()-.5)*.25,
    r:Math.random()*1.5+.5, a:Math.random()
  });
  function draw(){
    ctx.clearRect(0,0,W,H);
    ctx.fillStyle='rgba(0,200,232,0.5)';
    for(const p of pts){
      p.x+=p.vx;p.y+=p.vy;
      if(p.x<0)p.x=W;if(p.x>W)p.x=0;
      if(p.y<0)p.y=H;if(p.y>H)p.y=0;
      ctx.globalAlpha=p.a*.4;
      ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill();
    }
    ctx.globalAlpha=.06;
    for(let i=0;i<pts.length;i++) for(let j=i+1;j<pts.length;j++){
      const dx=pts[i].x-pts[j].x,dy=pts[i].y-pts[j].y;
      const d=Math.sqrt(dx*dx+dy*dy);
      if(d<160){
        ctx.strokeStyle='rgba(0,200,232,'+(1-d/160)*.3+')';
        ctx.lineWidth=.5;ctx.globalAlpha=(1-d/160)*.08;
        ctx.beginPath();ctx.moveTo(pts[i].x,pts[i].y);ctx.lineTo(pts[j].x,pts[j].y);ctx.stroke();
      }
    }
    ctx.globalAlpha=1;
    requestAnimationFrame(draw);
  }
  draw();
})();

/* ════════════════════════════════════════════════════════════════
   STOCK LIST
════════════════════════════════════════════════════════════════ */
let ALL={}, selSym=null, selName=null;

fetch('/api/stocks').then(r=>r.json()).then(d=>{ALL=d.stocks;renderList(ALL)});

function renderList(stocks){
  const el=document.getElementById('stock-list');
  const entries=Object.entries(stocks);
  if(!entries.length){el.innerHTML='<div style="padding:12px 14px;color:var(--muted);font-size:.8rem">No matches</div>';return}
  el.innerHTML=entries.map(([n,s])=>
    `<div class="sitem${s===selSym?' active':''}" onclick="selectStock('${n.replace(/'/g,"\\'")}','${s}')">
       <span class="si-name">${n}</span>
       <span class="si-sym">${s.replace('.NS','')}</span>
     </div>`
  ).join('');
}

function filterStocks(){
  const q=document.getElementById('stock-search').value.toLowerCase();
  renderList(Object.fromEntries(Object.entries(ALL).filter(([n,s])=>n.toLowerCase().includes(q)||s.toLowerCase().includes(q))));
}

function selectStock(name,sym){
  selSym=sym;selName=name;
  document.getElementById('sel-pill').classList.add('show');
  document.getElementById('sel-name').textContent=name;
  document.getElementById('sel-sym').textContent=sym;
  document.getElementById('run-btn').disabled=false;
  filterStocks();
}

/* ── Default date: next trading day ─────────────────────────── */
const tomorrow=new Date();
tomorrow.setDate(tomorrow.getDate()+1);
// Skip weekends
while(tomorrow.getDay()===0||tomorrow.getDay()===6) tomorrow.setDate(tomorrow.getDate()+1);
document.getElementById('pred-date').value=tomorrow.toISOString().split('T')[0];

document.getElementById('pred-date').addEventListener('change',function(){
  const sel=new Date(this.value), today=new Date();
  const diffMs=sel-today;
  const diffDays=Math.round(diffMs/(1000*60*60*24));
  const warn=document.getElementById('horizon-warn');
  if(diffDays>10) warn.classList.add('show');
  else warn.classList.remove('show');
});

/* ════════════════════════════════════════════════════════════════
   TABS
════════════════════════════════════════════════════════════════ */
function switchTab(name,btn){
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
  document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));
  document.getElementById('tab-'+name).classList.add('active');
  btn.classList.add('active');
}

/* ════════════════════════════════════════════════════════════════
   STATUS
════════════════════════════════════════════════════════════════ */
function setStatus(msg,type,spin=false){
  const el=document.getElementById('status');
  el.innerHTML=(spin?'<div class="spinner"></div>':'')+`<span>${msg}</span>`;
  el.className='show '+type;
}
function hideStatus(){document.getElementById('status').className=''}

const fmt=v=>v!=null?Number(v).toLocaleString('en-IN',{maximumFractionDigits:2}):'—';

/* ════════════════════════════════════════════════════════════════
   MAIN: RUN ANALYSIS
════════════════════════════════════════════════════════════════ */
async function runAnalysis(){
  if(!selSym){setStatus('Please select a stock first.','error');return}
  const btn=document.getElementById('run-btn');
  btn.disabled=true; btn.innerHTML='⏳ &nbsp; Analysing…';
  setStatus(`Fetching ${selName} data and training models — this takes ~15s…`,'info',true);
  document.getElementById('welcome').style.display='none';
  document.getElementById('results').style.display='none';

  const payload={
    ticker:          selSym,
    prediction_date: document.getElementById('pred-date').value,
    lookback_days:   +document.getElementById('lookback').value,
    test_frac:       +document.getElementById('test-frac').value,
  };

  try{
    const res  = await fetch('/api/analyze',{method:'POST',
      headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    const data = await res.json();
    if(!res.ok){setStatus('❌ '+(data.error||'Server error'),'error');return}

    renderPredHero(data);
    renderMetrics(data);
    renderChart('ch-price',   data.chart_price);
    renderChart('ch-perf',    data.chart_perf);
    renderChart('ch-overlay', data.chart_overlay);
    renderChart('ch-target',  data.chart_target);
    renderChart('ch-feat',    data.chart_feat_imp);
    renderPerfTable(data.performance);
    renderPredTable(data.target_pred, data.current_price, data.res_std, data.conf_band);
    renderFeatTable();

    document.getElementById('results').style.display='block';
    const dir=data.ensemble>=data.current_price?'▲ Bullish':'▼ Bearish';
    setStatus(
      `✅ Done! Ensemble: ₹${fmt(data.ensemble)} · Current: ₹${fmt(data.current_price)} · Signal: ${dir}`,
      'success'
    );
  }catch(e){
    setStatus('❌ Network / server error: '+e.message,'error');
  }finally{
    btn.disabled=false;btn.innerHTML='🚀 &nbsp; Run Analysis';
  }
}

function renderChart(id,json){
  const fig=JSON.parse(json);
  Plotly.react(id,fig.data,fig.layout,{responsive:true,displayModeBar:false});
}

/* ── Prediction hero card ────────────────────────────────────── */
function renderPredHero(d){
  const ens=d.ensemble, cur=d.current_price;
  const diff=ens&&cur?ens-cur:null;
  const pct=diff&&cur?diff/cur*100:null;
  const up=diff>=0;
  const days=d.days_ahead||1;
  const label=days===1?'Next Trading Day':days+' Trading Days Ahead';
  document.getElementById('pred-hero').innerHTML=`
    <div class="pred-hero-label">🔮 Ensemble Prediction — ${label} (${d.prediction_date})</div>
    <div class="pred-hero-val ${up?'up':'dn'}">₹${fmt(ens)}</div>
    <div class="pred-hero-meta">
      <span>Current Price: <b>₹${fmt(cur)}</b></span>
      <span>Change: <b class="${up?'mc-up':'mc-dn'}">${diff!=null?(up?'▲+':'▼')+'₹'+fmt(Math.abs(diff)):''} (${pct!=null?Math.abs(pct).toFixed(2)+'%':'—'})</b></span>
      <span>Confidence ±1σ: <b class="conf-pill">₹${fmt(d.conf_band)}</b></span>
    </div>
    <div class="conf-bar-wrap" style="margin-top:12px">
      <div class="conf-bar-fill" style="width:${Math.min(100,Math.max(5,d.best_r2*100||60))}%;background:${up?'var(--green)':'var(--red)'}"></div>
    </div>`;
}

/* ── Metric cards ────────────────────────────────────────────── */
function renderMetrics(d){
  const cur=d.current_price, ens=d.ensemble;
  const diff=ens&&cur?ens-cur:null, pct=diff&&cur?diff/cur*100:null, up=diff>=0;
  document.getElementById('metric-row').innerHTML=`
    <div class="mcard saffron">
      <div class="mc-label">Stock</div>
      <div class="mc-val" style="font-size:1rem;font-family:var(--font)">${selName}</div>
      <div class="mc-sub">${selSym}</div>
    </div>
    <div class="mcard gold">
      <div class="mc-label">Current Price</div>
      <div class="mc-val">₹${fmt(cur)}</div>
      <div class="mc-sub">Latest close · ${d.last_date||''}</div>
    </div>
    <div class="mcard ${up?'green':'red'}">
      <div class="mc-label">Ensemble Forecast</div>
      <div class="mc-val ${up?'mc-up':'mc-dn'}">₹${fmt(ens)}</div>
      <div class="mc-sub ${up?'mc-up':'mc-dn'}">${diff!=null?(up?'▲':'▼')+' ₹'+fmt(Math.abs(diff))+' ('+Math.abs(pct).toFixed(2)+'%)':''}</div>
    </div>
    <div class="mcard violet">
      <div class="mc-label">Training Rows</div>
      <div class="mc-val">${d.train_size}</div>
      <div class="mc-sub">data points</div>
    </div>
    <div class="mcard cyan">
      <div class="mc-label">Test Rows</div>
      <div class="mc-val">${d.test_size}</div>
      <div class="mc-sub">held-out data</div>
    </div>
    <div class="mcard saffron">
      <div class="mc-label">Horizon</div>
      <div class="mc-val" style="font-size:1.2rem">${d.days_ahead||1}</div>
      <div class="mc-sub">trading day(s) ahead</div>
    </div>`;
}

/* ── Performance table ───────────────────────────────────────── */
function renderPerfTable(rows){
  if(!rows?.length){document.getElementById('perf-tbl').innerHTML='<p style="padding:12px;color:var(--muted)">No data</p>';return}
  const cols=Object.keys(rows[0]);
  const tbody=rows.map(r=>'<tr>'+cols.map((c,i)=>
    `<td class="${i===0?'td-model':''}">${typeof r[c]==='number'?r[c].toFixed(4):r[c]}</td>`
  ).join('')+'</tr>').join('');
  document.getElementById('perf-tbl').innerHTML=
    `<table><thead><tr>${cols.map(c=>`<th>${c}</th>`).join('')}</tr></thead><tbody>${tbody}</tbody></table>`;
}

/* ── Prediction table ────────────────────────────────────────── */
function renderPredTable(preds,cur,resStd,confBand){
  if(!preds){document.getElementById('pred-tbl').innerHTML='<p style="padding:12px;color:var(--muted)">No data</p>';return}
  const rows=Object.entries(preds).map(([m,v])=>{
    const d=v&&cur?v-cur:null, p=d&&cur?d/cur*100:null, up=d>=0;
    const sigma=resStd?resStd[m]:null;
=======
  </div><!-- #results -->

</main>
</div>

<script>
/* ── Stock list state ──────────────────────────────────────── */
let ALL_STOCKS = {};   // { name: symbol }
let selectedSym  = null;
let selectedName = null;

/* ── Load stock list from API ──────────────────────────────── */
fetch("/api/stocks").then(r=>r.json()).then(d=>{
  ALL_STOCKS = d.stocks;
  renderList(ALL_STOCKS);
});

function renderList(stocks) {
  const el = document.getElementById("stock-list");
  el.innerHTML = Object.entries(stocks).map(([n,s])=>
    `<div class="stock-item${s===selectedSym?' selected':''}"
          onclick="selectStock('${n}','${s}')"
          data-name="${n}" data-sym="${s}">
       <span class="stock-item-name">${n}</span>
       <span class="stock-item-sym">${s.replace('.NS','')}</span>
     </div>`
  ).join("");
}

function filterStocks() {
  const q = document.getElementById("stock-search").value.toLowerCase();
  const filtered = Object.fromEntries(
    Object.entries(ALL_STOCKS).filter(([n,s])=>
      n.toLowerCase().includes(q) || s.toLowerCase().includes(q)
    )
  );
  renderList(filtered);
}

function selectStock(name, sym) {
  selectedSym  = sym;
  selectedName = name;
  document.getElementById("sel-display").classList.add("show");
  document.getElementById("sel-name").textContent = name;
  document.getElementById("sel-sym").textContent  = sym;
  document.getElementById("run-btn").disabled = false;
  renderList(
    document.getElementById("stock-search").value
      ? Object.fromEntries(Object.entries(ALL_STOCKS).filter(([n])=>
          n.toLowerCase().includes(document.getElementById("stock-search").value.toLowerCase())))
      : ALL_STOCKS
  );
}

/* ── Default date = tomorrow ───────────────────────────────── */
const tmr = new Date(); tmr.setDate(tmr.getDate()+1);
document.getElementById("pred-date").value = tmr.toISOString().split("T")[0];

/* ── Tab switcher ──────────────────────────────────────────── */
function switchTab(name, btn){
  document.querySelectorAll(".tab-btn").forEach(b=>b.classList.remove("active"));
  document.querySelectorAll(".tab-panel").forEach(p=>p.classList.remove("active"));
  document.getElementById("tab-"+name).classList.add("active");
  btn.classList.add("active");
}

/* ── Status helper ─────────────────────────────────────────── */
function setStatus(msg, type, spinner=false){
  const el = document.getElementById("status");
  el.innerHTML = (spinner?'<div class="spinner"></div>':'')+`<span>${msg}</span>`;
  el.className = "show "+type;
}
function hideStatus(){ document.getElementById("status").className=""; }

/* ── Main: run analysis ────────────────────────────────────── */
async function runAnalysis(){
  if(!selectedSym){ setStatus("Pick a stock first.","error"); return; }
  const btn = document.getElementById("run-btn");
  btn.disabled = true;
  btn.innerHTML = "⏳ &nbsp;Analysing…";

  setStatus(`Fetching ${selectedName} data and training models…`, "info", true);
  document.getElementById("welcome").style.display  = "none";
  document.getElementById("results").style.display  = "none";

  const payload = {
    ticker:          selectedSym,
    prediction_date: document.getElementById("pred-date").value,
    lookback_days:   +document.getElementById("lookback").value,
    test_frac:       +document.getElementById("test-frac").value,
    prediction_days: +document.getElementById("pred-days").value,
  };

  try {
    const res  = await fetch("/api/analyze", {method:"POST",
      headers:{"Content-Type":"application/json"}, body:JSON.stringify(payload)});
    const data = await res.json();
    if(!res.ok){ setStatus("❌ "+( data.error||"Unknown error"), "error"); return; }

    renderMetrics(data);
    renderChart("ch-price",   data.chart_price);
    renderChart("ch-perf",    data.chart_perf);
    renderChart("ch-overlay", data.chart_overlay);
    renderChart("ch-next",    data.chart_next);
    renderPerfTable(data.performance);
    renderPredTable(data.next_pred, data.current_price);

    document.getElementById("results").style.display = "block";
    setStatus(
      `✅ Done! Ensemble: ₹${fmt(data.ensemble)} · Current: ₹${fmt(data.current_price)}`,
      "success"
    );
  } catch(e){
    setStatus("❌ Network error: "+e.message, "error");
  } finally {
    btn.disabled = false;
    btn.innerHTML = "🚀 &nbsp;Run Analysis";
  }
}

const fmt = v => v!=null ? Number(v).toLocaleString('en-IN',{maximumFractionDigits:2}) : "—";

function renderChart(id, json){
  const fig = JSON.parse(json);
  Plotly.react(id, fig.data, fig.layout, {responsive:true, displayModeBar:false});
}

function renderMetrics(d){
  const cur = d.current_price;
  const ens = d.ensemble;
  const diff = ens&&cur ? ens-cur : null;
  const diffP= diff&&cur ? diff/cur*100 : null;
  const up   = diff > 0;

  document.getElementById("metric-row").innerHTML = `
    <div class="metric-card blue">
      <div class="m-label">Stock</div>
      <div class="m-value" style="font-size:1.1rem;font-family:var(--font)">${selectedName}</div>
      <div class="m-sub">${selectedSym}</div>
    </div>
    <div class="metric-card gold">
      <div class="m-label">Current Price</div>
      <div class="m-value">₹${fmt(cur)}</div>
      <div class="m-sub">Latest closing</div>
    </div>
    <div class="metric-card ${up?'green':'red'}">
      <div class="m-label">Ensemble Prediction</div>
      <div class="m-value ${up?'m-up':'m-dn'}">₹${fmt(ens)}</div>
      <div class="m-sub ${up?'m-up':'m-dn'}">${diff!=null?(up?'▲':'▼')+' ₹'+fmt(Math.abs(diff))+' ('+Math.abs(diffP).toFixed(2)+'%)':''}</div>
    </div>
    <div class="metric-card purple">
      <div class="m-label">Training Rows</div>
      <div class="m-value">${d.train_size}</div>
      <div class="m-sub">data points</div>
    </div>
    <div class="metric-card blue">
      <div class="m-label">Test Rows</div>
      <div class="m-value">${d.test_size}</div>
      <div class="m-sub">data points</div>
    </div>`;
}

function renderPerfTable(rows){
  if(!rows||!rows.length){document.getElementById("perf-tbl").innerHTML="<p style='color:var(--muted);padding:12px'>No data</p>";return;}
  const cols = Object.keys(rows[0]);
  const tbody = rows.map(r=>"<tr>"+cols.map((c,i)=>
    `<td class="${i===0?'td-model':''}">${typeof r[c]==='number'?r[c].toFixed(4):r[c]}</td>`
  ).join("")+"</tr>").join("");
  document.getElementById("perf-tbl").innerHTML=
    `<table><thead><tr>${cols.map(c=>`<th>${c}</th>`).join("")}</tr></thead><tbody>${tbody}</tbody></table>`;
}

function renderPredTable(preds, cur){
  if(!preds){document.getElementById("pred-tbl").innerHTML="<p style='color:var(--muted);padding:12px'>No data</p>";return;}
  const rows = Object.entries(preds).map(([m,v])=>{
    const d=v&&cur?v-cur:null, p=d&&cur?d/cur*100:null, up=d>0;
>>>>>>> 236a2c92b346f989d77d458d7e9deda2ee9cb5d1
    return `<tr>
      <td class="td-model">${m}</td>
      <td>₹${fmt(v)}</td>
      <td>${d!=null?`<span class="badge ${up?'badge-up':'badge-dn'}">${up?'+':''}₹${fmt(Math.abs(d))}</span>`:'—'}</td>
      <td>${p!=null?`<span class="badge ${up?'badge-up':'badge-dn'}">${up?'+':''}${Math.abs(p).toFixed(2)}%</span>`:'—'}</td>
<<<<<<< HEAD
      <td style="color:var(--violet2);font-size:.75rem">${sigma?'±₹'+fmt(sigma):'—'}</td>
    </tr>`;
  }).join('');
  document.getElementById('pred-tbl').innerHTML=
    `<table><thead><tr><th>Model</th><th>Predicted</th><th>Δ Price</th><th>Δ %</th><th>±1σ Error</th></tr></thead><tbody>${rows}</tbody></table>`;
}

/* ── Feature table ───────────────────────────────────────────── */
const FEAT_INFO=[
  ['sma_20','SMA 20','20-day simple moving average — short-term trend'],
  ['sma_50','SMA 50','50-day simple moving average — medium-term trend'],
  ['ema_20','EMA 20','20-day exponential MA — reacts faster to price changes'],
  ['price_vs_sma20','Price vs SMA20','Normalised distance of price from SMA 20 — mean reversion signal'],
  ['macd','MACD','12/26 EMA difference — trend momentum signal'],
  ['macd_signal','MACD Signal','9-day EMA of MACD — crossover signal line'],
  ['macd_hist','MACD Histogram','MACD − Signal — confirms divergence/convergence'],
  ['rsi','RSI 14','Relative Strength Index — overbought (>70) / oversold (<30)'],
  ['stoch_k','Stochastic %K','14-day stochastic — momentum / reversal signal'],
  ['stoch_d','Stochastic %D','3-day SMA of %K — signal line for stochastic'],
  ['bb_pct','Bollinger %B','Price position within Bollinger Band (0=lower, 1=upper)'],
  ['bb_width','BB Width','Normalised bandwidth — measures volatility squeeze'],
  ['atr_pct','ATR %','Average True Range normalised by price — volatility magnitude'],
  ['volatility_20','Volatility 20','20-day rolling std of daily returns — risk measure'],
  ['volume_ratio','Volume Ratio','Today\'s volume ÷ 10-day average — unusual activity detector'],
  ['obv_norm','OBV Norm','On-Balance Volume normalised — volume-price trend confirmation'],
  ['roc_5','ROC 5','5-day Rate of Change — 1-week momentum'],
  ['roc_20','ROC 20','20-day Rate of Change — 1-month momentum'],
  ['daily_return','Daily Return','Today\'s percentage price change'],
  ['lag_1','Lag 1','Yesterday\'s closing price — direct price memory'],
  ['lag_5','Lag 5','Price 5 days ago — weekly price memory'],
  ['lag_10','Lag 10','Price 10 days ago — bi-weekly price memory'],
];
function renderFeatTable(){
  document.getElementById('feat-tbl').innerHTML=
    `<table><thead><tr><th>Feature</th><th>Full Name</th><th>Purpose</th></tr></thead><tbody>`+
    FEAT_INFO.map(([k,n,d])=>`<tr><td style="font-family:var(--mono);color:var(--cyan);font-size:.75rem">${k}</td><td class="td-model">${n}</td><td style="color:var(--muted);font-size:.78rem">${d}</td></tr>`).join('')+
    `</tbody></table>`;
=======
    </tr>`;
  }).join("");
  document.getElementById("pred-tbl").innerHTML=
    `<table><thead><tr><th>Model</th><th>Predicted</th><th>Δ Price</th><th>Δ %</th></tr></thead><tbody>${rows}</tbody></table>`;
>>>>>>> 236a2c92b346f989d77d458d7e9deda2ee9cb5d1
}
</script>
</body>
</html>"""


# ── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return Response(HTML, mimetype="text/html")


@app.route("/api/stocks")
def list_stocks():
    return jsonify({"stocks": NIFTY50_STOCKS})


@app.route("/api/analyze", methods=["POST"])
def analyze():
    body = request.get_json(force=True)
    try:
        result = run(
<<<<<<< HEAD
            ticker          = body.get("ticker", "TCS.NS"),
            prediction_date = body.get("prediction_date"),
            lookback_days   = int(body.get("lookback_days", 730)),
            test_frac       = float(body.get("test_frac", 0.2)),
=======
            ticker=          body.get("ticker", "TCS.NS"),
            prediction_date= body.get("prediction_date"),
            lookback_days=   int(body.get("lookback_days", 365)),
            test_frac=       float(body.get("test_frac", 0.2)),
            prediction_days= int(body.get("prediction_days", 1)),
>>>>>>> 236a2c92b346f989d77d458d7e9deda2ee9cb5d1
        )
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

<<<<<<< HEAD
    df      = result["df"]
    perf    = result["performance"]
    name    = body.get("ticker", "Stock")

    perf_rows = [
        {"Model": idx, **{k: round(v, 4) for k, v in row.items()}}
        for idx, row in perf.iterrows()
    ]

    # Best R² for the confidence bar width
    best_r2 = float(perf["R²"].max()) if "R²" in perf.columns else 0.6
=======
    df   = result["df"]
    perf = result["performance"]
    name = body.get("ticker", "Stock")

    perf_rows = [{"Model": idx, **{k: round(v, 4) for k, v in row.items()}}
                 for idx, row in perf.iterrows()]
>>>>>>> 236a2c92b346f989d77d458d7e9deda2ee9cb5d1

    return jsonify({
        "chart_price":   chart_price(df, name),
        "chart_perf":    chart_performance(perf),
<<<<<<< HEAD
        "chart_overlay": chart_overlay(df, result["test_preds"],
                                       result["test_start_idx"], name),
        "chart_target":  chart_target(
                            result["target_pred"],
                            result["current_price"],
                            result["res_std"],
                            result["prediction_date"],
                            result["days_ahead"],
                         ),
        "chart_feat_imp": chart_feature_importance(result["feat_imp"]),

        "performance":   perf_rows,
        "target_pred":   result["target_pred"],
        "ensemble":      result["ensemble"],
        "conf_band":     result["conf_band"],
        "days_ahead":    result["days_ahead"],
        "prediction_date": result["prediction_date"],
        "current_price": result["current_price"],
        "last_date":     result["last_date"],
        "train_size":    result["train_size"],
        "test_size":     result["test_size"],
        "res_std":       result["res_std"],
        "best_r2":       best_r2,
=======
        "chart_overlay": chart_overlay(df, result["test_preds"], result["test_start_idx"], name),
        "chart_next":    chart_next(result["next_pred"], result["current_price"]),
        "performance":   perf_rows,
        "next_pred":     result["next_pred"],
        "ensemble":      result["ensemble"],
        "current_price": result["current_price"],
        "train_size":    result["train_size"],
        "test_size":     result["test_size"],
>>>>>>> 236a2c92b346f989d77d458d7e9deda2ee9cb5d1
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
