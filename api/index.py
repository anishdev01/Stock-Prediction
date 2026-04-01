"""
api/index.py — Flask entry point (Upgraded)
Indian Stock Predictor · Alpha Five Team · Brainware University
Models: Linear Regression, Ridge Regression, LSTM
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from flask import Flask, jsonify, request, Response
import traceback

from src.data_fetcher import NIFTY50_STOCKS
from src.predictor import run
from src.charts import (chart_price, chart_performance,
                        chart_overlay, chart_next,
                        chart_feature_importance)

app = Flask(__name__)

# ══════════════════════════════════════════════════════════════════════════════
#  HTML PAGE WITH UPGRADED UI
# ══════════════════════════════════════════════════════════════════════════════
HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Indian Stock Predictor AI · Alpha Five · Brainware University</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet"/>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
/* ══════════════════════════════════════════════════════════════════
   FUTURISTIC AI THEME
══════════════════════════════════════════════════════════════════ */
:root {
  --bg:          #0a0e1a;
  --surface:     #101828;
  --card:        #151e2e;
  --card2:       #1a2537;
  --border:      #1e3a5f;
  --border2:     #2a4a72;
  --text:        #e0e7ff;
  --muted:       #6b7d9d;
  --accent:      #00d9ff;
  --accent2:     #0099ff;
  --purple:      #b47eff;
  --green:       #00ff9f;
  --red:         #ff3366;
  --gold:        #ffb700;
  --orange:      #ff6b35;
  
  --font:    'Inter', sans-serif;
  --mono:    'JetBrains Mono', monospace;
  --display: 'Orbitron', sans-serif;
}

/* ══════════════════════════════════════════════════════════════════
   RESET & BASE
══════════════════════════════════════════════════════════════════ */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{
  font-family:var(--font);
  background:linear-gradient(135deg, #0a0e1a 0%, #0f1623 50%, #0a0e1a 100%);
  color:var(--text);
  min-height:100vh;
  overflow-x:hidden;
  position:relative;
}

/* ── Animated grid background ── */
body::before{
  content:'';
  position:fixed;inset:0;z-index:0;
  background-image:
    linear-gradient(rgba(0,217,255,.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,217,255,.03) 1px, transparent 1px);
  background-size:60px 60px;
  pointer-events:none;
  animation:grid-slide 20s linear infinite;
}

@keyframes grid-slide{
  from{background-position:0 0}
  to{background-position:60px 60px}
}

/* ── Glow orbs ── */
body::after{
  content:'';
  position:fixed;
  top:0;left:50%;
  width:800px;height:800px;
  background:radial-gradient(circle, rgba(0,217,255,.08) 0%, transparent 70%);
  transform:translate(-50%,-50%);
  z-index:0;
  pointer-events:none;
  animation:pulse-glow 6s ease-in-out infinite;
}

@keyframes pulse-glow{
  0%,100%{opacity:.3;transform:translate(-50%,-50%) scale(1)}
  50%{opacity:.5;transform:translate(-50%,-50%) scale(1.1)}
}

/* ══════════════════════════════════════════════════════════════════
   HEADER
══════════════════════════════════════════════════════════════════ */
header{
  position:relative;z-index:100;
  background:rgba(10,14,26,0.95);
  backdrop-filter:blur(20px);
  border-bottom:2px solid var(--accent);
  box-shadow:0 4px 30px rgba(0,217,255,.1);
  padding:0 32px;
  height:90px;
  display:flex;align-items:center;justify-content:space-between;
}

.logo-area{display:flex;align-items:center;gap:18px}
.logo-icon{
  width:56px;height:56px;border-radius:12px;
  background:linear-gradient(135deg,var(--accent),var(--purple));
  display:flex;align-items:center;justify-content:center;
  font-size:28px;
  box-shadow:0 0 30px rgba(0,217,255,.4);
  animation:logo-pulse 3s ease-in-out infinite;
}

@keyframes logo-pulse{
  0%,100%{box-shadow:0 0 30px rgba(0,217,255,.4)}
  50%{box-shadow:0 0 50px rgba(0,217,255,.6)}
}

.logo-text h1{
  font-family:var(--display);
  font-size:1.4rem;
  font-weight:900;
  background:linear-gradient(90deg,var(--accent),var(--purple));
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  letter-spacing:.05em;
}
.logo-text p{
  font-size:.75rem;
  color:var(--muted);
  letter-spacing:.15em;
  text-transform:uppercase;
  margin-top:2px;
}

.badges{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.badge{
  font-family:var(--mono);font-size:.7rem;
  padding:6px 14px;border-radius:20px;
  border:1px solid;
  display:flex;align-items:center;gap:6px;
  font-weight:600;
}
.badge-live{
  border-color:rgba(0,255,159,.3);
  background:rgba(0,255,159,.08);
  color:var(--green);
}
.badge-models{
  border-color:rgba(180,126,255,.3);
  background:rgba(180,126,255,.08);
  color:var(--purple);
}
.live-dot{
  width:6px;height:6px;border-radius:50%;
  background:var(--green);
  box-shadow:0 0 8px var(--green);
  animation:blink 1.5s ease-in-out infinite;
}
@keyframes blink{
  0%,100%{opacity:1}
  50%{opacity:.3}
}

/* ══════════════════════════════════════════════════════════════════
   LAYOUT
══════════════════════════════════════════════════════════════════ */
.layout{
  display:flex;
  min-height:calc(100vh - 90px);
  position:relative;z-index:1;
}

/* ══════════════════════════════════════════════════════════════════
   SIDEBAR
══════════════════════════════════════════════════════════════════ */
aside{
  width:320px;flex-shrink:0;
  background:rgba(16,24,40,0.8);
  border-right:1px solid var(--border2);
  padding:28px 20px 40px;
  overflow-y:auto;
  backdrop-filter:blur(16px);
}
aside::-webkit-scrollbar{width:4px}
aside::-webkit-scrollbar-thumb{background:var(--border2);border-radius:4px}

.section-label{
  font-size:.68rem;
  text-transform:uppercase;
  letter-spacing:.15em;
  color:var(--accent);
  font-weight:700;
  margin:24px 0 12px;
  display:flex;align-items:center;gap:8px;
  font-family:var(--display);
}
.section-label:first-child{margin-top:0}
.section-label::after{
  content:'';flex:1;height:1px;
  background:linear-gradient(to right,var(--accent),transparent);
}

/* Stock search */
.search-box{position:relative;margin-bottom:8px}
.search-box input{
  width:100%;
  padding:12px 40px 12px 14px;
  background:var(--card2);
  border:1px solid var(--border2);
  border-radius:10px;
  color:var(--text);
  font-family:var(--font);font-size:.88rem;
  outline:none;
  transition:border-color .2s,box-shadow .2s;
}
.search-box input:focus{
  border-color:var(--accent);
  box-shadow:0 0 0 3px rgba(0,217,255,.1);
}
.search-icon{position:absolute;right:14px;top:50%;transform:translateY(-50%);color:var(--muted);font-size:16px;pointer-events:none}

/* Selected stock */
.selected-stock{
  display:none;
  background:linear-gradient(135deg,rgba(0,217,255,.1),rgba(180,126,255,.08));
  border:1px solid var(--accent);
  border-radius:10px;padding:12px 14px;margin-bottom:8px;
}
.selected-stock.show{display:block}
.sel-name{font-size:.9rem;font-weight:700;color:var(--accent)}
.sel-sym{font-size:.72rem;font-family:var(--mono);color:var(--muted);margin-top:2px}

/* Stock list */
.stock-list{
  max-height:240px;overflow-y:auto;
  border:1px solid var(--border);border-radius:10px;
  background:var(--card);
}
.stock-list::-webkit-scrollbar{width:4px}
.stock-list::-webkit-scrollbar-thumb{background:var(--border2);border-radius:4px}
.stock-item{
  padding:10px 14px;cursor:pointer;
  border-bottom:1px solid var(--border);
  transition:background .15s;
  display:flex;align-items:center;justify-content:space-between;
}
.stock-item:last-child{border-bottom:none}
.stock-item:hover{background:rgba(0,217,255,.08)}
.stock-item.active{background:rgba(0,217,255,.15);border-left:3px solid var(--accent)}
.item-name{font-size:.84rem;font-weight:500;color:var(--text)}
.item-sym{font-size:.7rem;font-family:var(--mono);color:var(--muted)}

/* Controls */
.ctrl{margin-top:18px}
.ctrl-label{
  font-size:.75rem;color:var(--muted);font-weight:600;
  margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;
}
.ctrl-value{color:var(--accent);font-family:var(--mono);font-size:.75rem}

input[type=date]{
  width:100%;padding:10px 14px;
  background:var(--card2);border:1px solid var(--border2);
  border-radius:10px;color:var(--text);
  font-family:var(--mono);font-size:.86rem;
  outline:none;transition:border-color .2s;
  cursor:pointer;
}
input[type=date]:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(0,217,255,.1)}
input[type=date]::-webkit-calendar-picker-indicator{filter:invert(.6) sepia(1) saturate(2) hue-rotate(160deg)}

input[type=range]{
  width:100%;-webkit-appearance:none;
  height:5px;background:var(--border2);
  border-radius:3px;outline:none;cursor:pointer;
}
input[type=range]::-webkit-slider-thumb{
  -webkit-appearance:none;width:18px;height:18px;
  border-radius:50%;background:var(--accent);
  box-shadow:0 0 12px rgba(0,217,255,.6);cursor:pointer;
}

/* Run button */
#run-btn{
  margin-top:28px;width:100%;
  padding:16px;
  background:linear-gradient(135deg,var(--accent),var(--purple));
  color:white;border:none;border-radius:12px;
  font-family:var(--display);font-size:1rem;font-weight:700;
  cursor:pointer;letter-spacing:.06em;
  position:relative;overflow:hidden;
  transition:transform .15s,box-shadow .2s,opacity .2s;
  box-shadow:0 6px 30px rgba(0,217,255,.3);
  text-transform:uppercase;
}
#run-btn::before{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(255,255,255,.2),transparent 50%);
}
#run-btn:hover:not(:disabled){transform:translateY(-2px);box-shadow:0 10px 40px rgba(0,217,255,.5)}
#run-btn:active:not(:disabled){transform:translateY(0)}
#run-btn:disabled{opacity:.4;cursor:not-allowed;transform:none}

/* ══════════════════════════════════════════════════════════════════
   MAIN CONTENT
══════════════════════════════════════════════════════════════════ */
main{flex:1;padding:32px 36px;overflow-y:auto;min-width:0}

/* Status bar */
#status{
  display:none;align-items:center;gap:12px;
  padding:14px 18px;border-radius:12px;
  margin-bottom:20px;font-size:.88rem;font-weight:600;
  border:1px solid;
}
#status.show{display:flex}
#status.info{background:rgba(0,217,255,.1);border-color:var(--accent);color:var(--accent)}
#status.success{background:rgba(0,255,159,.1);border-color:var(--green);color:var(--green)}
#status.error{background:rgba(255,51,102,.1);border-color:var(--red);color:var(--red)}

/* Welcome */
#welcome{
  display:flex;flex-direction:column;
  align-items:center;justify-content:center;
  min-height:75vh;text-align:center;
}
.ai-orb{
  width:140px;height:140px;border-radius:50%;
  background:radial-gradient(circle, rgba(0,217,255,.3), rgba(180,126,255,.15));
  border:2px solid var(--accent);
  display:flex;align-items:center;justify-content:center;
  font-size:60px;
  margin-bottom:32px;
  box-shadow:0 0 80px rgba(0,217,255,.3);
  animation:ai-pulse 4s ease-in-out infinite;
}
@keyframes ai-pulse{
  0%,100%{box-shadow:0 0 80px rgba(0,217,255,.3);transform:scale(1)}
  50%{box-shadow:0 0 120px rgba(0,217,255,.5);transform:scale(1.05)}
}
#welcome h2{
  font-family:var(--display);
  font-size:2.2rem;font-weight:900;
  background:linear-gradient(135deg,var(--text),var(--muted));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  margin-bottom:14px;letter-spacing:-.01em;
}
#welcome p{
  color:var(--muted);font-size:.95rem;line-height:1.8;
  max-width:520px;
}
.model-tags{display:flex;gap:10px;margin-top:24px;flex-wrap:wrap;justify-content:center}
.tag{
  padding:6px 16px;border-radius:20px;
  font-size:.76rem;font-weight:700;border:1px solid;
  letter-spacing:.04em;font-family:var(--mono);
}
.tag-a{border-color:rgba(0,217,255,.4);color:var(--accent);background:rgba(0,217,255,.08)}
.tag-b{border-color:rgba(255,107,53,.4);color:var(--orange);background:rgba(255,107,53,.08)}
.tag-c{border-color:rgba(180,126,255,.4);color:var(--purple);background:rgba(180,126,255,.08)}

/* Metric cards */
.metrics{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(170px,1fr));
  gap:14px;margin-bottom:26px;
}
.metric{
  background:var(--card);border:1px solid var(--border);
  border-radius:14px;padding:20px 22px;
  position:relative;overflow:hidden;
  transition:border-color .2s,transform .2s,box-shadow .2s;
}
.metric:hover{
  border-color:var(--accent);
  transform:translateY(-3px);
  box-shadow:0 10px 40px rgba(0,217,255,.15);
}
.metric::before{
  content:'';position:absolute;top:0;left:0;right:0;height:3px;
}
.metric.cyan::before{background:linear-gradient(90deg,var(--accent),transparent)}
.metric.purple::before{background:linear-gradient(90deg,var(--purple),transparent)}
.metric.green::before{background:linear-gradient(90deg,var(--green),transparent)}
.metric.red::before{background:linear-gradient(90deg,var(--red),transparent)}
.metric.gold::before{background:linear-gradient(90deg,var(--gold),transparent)}

.m-label{font-size:.68rem;text-transform:uppercase;letter-spacing:.12em;color:var(--muted);font-weight:700}
.m-value{font-family:var(--mono);font-size:1.6rem;font-weight:700;color:var(--text);margin:8px 0 4px;line-height:1}
.m-sub{font-size:.74rem;color:var(--muted)}
.m-up{color:var(--green)}.m-dn{color:var(--red)}

/* Tabs */
.tabs{
  display:flex;gap:4px;
  border-bottom:2px solid var(--border);
  margin-bottom:22px;
}
.tab{
  padding:12px 22px;border:none;background:transparent;
  color:var(--muted);font-family:var(--font);font-size:.86rem;font-weight:700;
  cursor:pointer;border-bottom:3px solid transparent;margin-bottom:-2px;
  transition:color .2s,border-color .2s;
  border-radius:6px 6px 0 0;
  text-transform:uppercase;
  letter-spacing:.04em;
}
.tab:hover{color:var(--text);background:rgba(255,255,255,.03)}
.tab.active{color:var(--accent);border-bottom-color:var(--accent)}
.tab-content{display:none}.tab-content.active{display:block}

/* Chart card */
.chart-box{
  background:var(--card);border:1px solid var(--border);
  border-radius:14px;padding:22px;margin-bottom:18px;
  transition:border-color .2s;
}
.chart-box:hover{border-color:var(--border2)}
.chart-box h3{
  font-size:.76rem;text-transform:uppercase;letter-spacing:.12em;
  color:var(--muted);font-weight:800;margin-bottom:16px;
  display:flex;align-items:center;gap:10px;
  font-family:var(--display);
}
.chart-box h3 span{color:var(--accent)}

/* Tables */
.table-wrap{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:.86rem}
thead th{
  background:rgba(30,58,95,.5);padding:12px 18px;
  text-align:left;font-size:.7rem;text-transform:uppercase;
  letter-spacing:.1em;color:var(--accent);font-weight:800;
  border-bottom:2px solid var(--accent);
}
tbody td{
  padding:14px 18px;border-bottom:1px solid var(--border);
  color:var(--text);font-family:var(--mono);font-size:.84rem;
}
tbody tr:hover td{background:rgba(0,217,255,.04)}
tbody tr:last-child td{border-bottom:none}
.td-model{font-family:var(--display);font-weight:700;color:var(--accent);font-size:.88rem}

.badge2{
  display:inline-block;padding:4px 10px;border-radius:12px;
  font-size:.74rem;font-weight:800;font-family:var(--mono);
}
.badge-up2{background:rgba(0,255,159,.15);color:var(--green);border:1px solid rgba(0,255,159,.3)}
.badge-dn2{background:rgba(255,51,102,.15);color:var(--red);border:1px solid rgba(255,51,102,.3)}

/* Spinner */
.spinner{
  width:18px;height:18px;border-radius:50%;flex-shrink:0;
  border:3px solid rgba(0,217,255,.2);
  border-top-color:var(--accent);
  animation:spin .7s linear infinite;
}
@keyframes spin{to{transform:rotate(360deg)}}

/* Reveal animation */
.reveal{animation:reveal .5s ease both}
@keyframes reveal{
  from{opacity:0;transform:translateY(16px)}
  to{opacity:1;transform:translateY(0)}
}
.r2{animation-delay:.1s}.r3{animation-delay:.2s}.r4{animation-delay:.3s}

/* Scrollbar */
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--border2);border-radius:4px}

@media(max-width:900px){
  .layout{flex-direction:column}
  aside{width:100%;border-right:none;border-bottom:1px solid var(--border2);max-height:450px}
  main{padding:20px}
  header{padding:0 20px;height:75px}
  .logo-text h1{font-size:1.1rem}
  .logo-text p{display:none}
}
</style>
</head>
<body>

<!-- ══ HEADER ═══════════════════════════════════════════════════ -->
<header>
  <div class="logo-area">
    <div class="logo-icon">🚀</div>
    <div class="logo-text">
      <h1>Indian Stock Predictor AI</h1>
      <p>Alpha Five Team · Brainware University</p>
    </div>
  </div>
  <div class="badges">
    <div class="badge badge-live">
      <div class="live-dot"></div>
      Live NSE Data
    </div>
    <div class="badge badge-models">
      ⚡ 3 AI Models
    </div>
  </div>
</header>

<div class="layout">

<!-- ══ SIDEBAR ══════════════════════════════════════════════════ -->
<aside>

  <div class="section-label">🏢 SELECT STOCK</div>

  <div class="search-box">
    <input type="text" id="stock-search" placeholder="Search Nifty 50 stocks…"
           autocomplete="off" oninput="filterStocks()"/>
    <span class="search-icon">⌕</span>
  </div>

  <div class="selected-stock" id="sel-stock">
    <div class="sel-name" id="sel-name">—</div>
    <div class="sel-sym"  id="sel-sym">—</div>
  </div>

  <div class="stock-list" id="stock-list"></div>

  <div class="section-label">📅 PREDICTION DATE</div>
  <input type="date" id="pred-date"/>

  <div class="ctrl">
    <div class="ctrl-label">
      <span>📆 History Days</span>
      <span class="ctrl-value" id="lb-val">730</span>
    </div>
    <input type="range" id="lookback" min="180" max="1095" value="730" step="30"
           oninput="document.getElementById('lb-val').textContent=this.value"/>
  </div>

  <div class="ctrl">
    <div class="ctrl-label">
      <span>🧪 Test Split</span>
      <span class="ctrl-value" id="ts-val">20%</span>
    </div>
    <input type="range" id="test-frac" min="0.1" max="0.35" value="0.2" step="0.05"
           oninput="document.getElementById('ts-val').textContent=Math.round(this.value*100)+'%'"/>
  </div>

  <button id="run-btn" onclick="runAnalysis()" disabled>
    🚀 RUN ANALYSIS
  </button>

</aside>

<!-- ══ MAIN ═════════════════════════════════════════════════════ -->
<main>

  <div id="status"></div>

  <!-- Welcome -->
  <div id="welcome">
    <div class="ai-orb">🤖</div>
    <h2>AI-Powered Stock Prediction</h2>
    <p>Select a Nifty 50 stock, choose your prediction date, and let our advanced machine learning models (Linear Regression, Ridge Regression & LSTM) forecast the future price.</p>
    <div class="model-tags">
      <span class="tag tag-a">Linear Regression</span>
      <span class="tag tag-b">Ridge Regression</span>
      <span class="tag tag-c">LSTM Neural Network</span>
    </div>
  </div>

  <!-- Results -->
  <div id="results" style="display:none">

    <!-- Metrics -->
    <div class="metrics reveal" id="metrics"></div>

    <!-- Tabs -->
    <div class="tabs">
      <button class="tab active" onclick="switchTab('tech',this)">📊 Technical</button>
      <button class="tab"        onclick="switchTab('ml',this)">🤖 Models</button>
      <button class="tab"        onclick="switchTab('pred',this)">🔮 Predictions</button>
    </div>

    <!-- Technical -->
    <div id="tab-tech" class="tab-content active">
      <div class="chart-box reveal r2">
        <h3><span>◈</span> Price Chart + Indicators</h3>
        <div id="ch-price" style="min-height:860px"></div>
      </div>
    </div>

    <!-- Models -->
    <div id="tab-ml" class="tab-content">
      <div class="chart-box reveal">
        <h3><span>◈</span> Model Performance</h3>
        <div id="ch-perf" style="min-height:420px"></div>
      </div>
      <div class="chart-box reveal r2">
        <h3><span>◈</span> Predictions vs Actual</h3>
        <div id="ch-overlay" style="min-height:520px"></div>
      </div>
      <div class="chart-box reveal r3">
        <h3><span>◈</span> Performance Table</h3>
        <div class="table-wrap" id="perf-tbl"></div>
      </div>
    </div>

    <!-- Predictions -->
    <div id="tab-pred" class="tab-content">
      <div class="chart-box reveal">
        <h3><span>◈</span> Next Price Predictions</h3>
        <div id="ch-next" style="min-height:360px"></div>
      </div>
      <div class="chart-box reveal r2">
        <h3><span>◈</span> Prediction Summary</h3>
        <div class="table-wrap" id="pred-tbl"></div>
      </div>
    </div>

  </div>

</main>
</div>

<script>
/* ════════════════════════════════════════════════════════════════
   STOCK LIST
════════════════════════════════════════════════════════════════ */
let ALL={}, selSym=null, selName=null;

fetch('/api/stocks').then(r=>r.json()).then(d=>{ALL=d.stocks;renderList(ALL)});

function renderList(stocks){
  const el=document.getElementById('stock-list');
  const entries=Object.entries(stocks);
  if(!entries.length){el.innerHTML='<div style="padding:14px;color:var(--muted);font-size:.82rem">No matches</div>';return}
  el.innerHTML=entries.map(([n,s])=>
    `<div class="stock-item${s===selSym?' active':''}" onclick="selectStock('${n.replace(/'/g,"\\'")}','${s}')">
       <span class="item-name">${n}</span>
       <span class="item-sym">${s.replace('.NS','')}</span>
     </div>`
  ).join('');
}

function filterStocks(){
  const q=document.getElementById('stock-search').value.toLowerCase();
  renderList(Object.fromEntries(Object.entries(ALL).filter(([n,s])=>n.toLowerCase().includes(q)||s.toLowerCase().includes(q))));
}

function selectStock(name,sym){
  selSym=sym;selName=name;
  document.getElementById('sel-stock').classList.add('show');
  document.getElementById('sel-name').textContent=name;
  document.getElementById('sel-sym').textContent=sym;
  document.getElementById('run-btn').disabled=false;
  filterStocks();
}

/* Default date */
const tmr=new Date();
tmr.setDate(tmr.getDate()+1);
while(tmr.getDay()===0||tmr.getDay()===6) tmr.setDate(tmr.getDate()+1);
document.getElementById('pred-date').value=tmr.toISOString().split('T')[0];

/* Tabs */
function switchTab(name,btn){
  document.querySelectorAll('.tab').forEach(b=>b.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(p=>p.classList.remove('active'));
  document.getElementById('tab-'+name).classList.add('active');
  btn.classList.add('active');
}

/* Status */
function setStatus(msg,type,spin=false){
  const el=document.getElementById('status');
  el.innerHTML=(spin?'<div class="spinner"></div>':'')+`<span>${msg}</span>`;
  el.className='show '+type;
}

const fmt=v=>v!=null?Number(v).toLocaleString('en-IN',{maximumFractionDigits:2}):'—';

/* Run Analysis */
async function runAnalysis(){
  if(!selSym){setStatus('Please select a stock first','error');return}
  const btn=document.getElementById('run-btn');
  btn.disabled=true; btn.innerHTML='⏳ ANALYZING…';
  setStatus(`Fetching ${selName} data and training AI models…`,'info',true);
  document.getElementById('welcome').style.display='none';
  document.getElementById('results').style.display='none';

  const payload={
    ticker:          selSym,
    prediction_date: document.getElementById('pred-date').value,
    lookback_days:   +document.getElementById('lookback').value,
    test_frac:       +document.getElementById('test-frac').value,
    prediction_days: 1,
  };

  try{
    const res  = await fetch('/api/analyze',{method:'POST',
      headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    const data = await res.json();
    if(!res.ok){setStatus('❌ '+(data.error||'Server error'),'error');return}

    renderMetrics(data);
    renderChart('ch-price',   data.chart_price);
    renderChart('ch-perf',    data.chart_perf);
    renderChart('ch-overlay', data.chart_overlay);
    renderChart('ch-next',    data.chart_next);
    renderPerfTable(data.performance);
    renderPredTable(data.next_pred, data.current_price);

    document.getElementById('results').style.display='block';
    setStatus(
      `✅ Complete! Ensemble: ₹${fmt(data.ensemble)} · Current: ₹${fmt(data.current_price)}`,
      'success'
    );
  }catch(e){
    setStatus('❌ Network error: '+e.message,'error');
  }finally{
    btn.disabled=false;btn.innerHTML='🚀 RUN ANALYSIS';
  }
}

function renderChart(id,json){
  const fig=JSON.parse(json);
  Plotly.react(id,fig.data,fig.layout,{responsive:true,displayModeBar:false});
}

function renderMetrics(d){
  const cur=d.current_price, ens=d.ensemble;
  const diff=ens&&cur?ens-cur:null, pct=diff&&cur?diff/cur*100:null, up=diff>=0;
  document.getElementById('metrics').innerHTML=`
    <div class="metric cyan">
      <div class="m-label">Stock</div>
      <div class="m-value" style="font-size:1.1rem;font-family:var(--display)">${selName}</div>
      <div class="m-sub">${selSym}</div>
    </div>
    <div class="metric gold">
      <div class="m-label">Current Price</div>
      <div class="m-value">₹${fmt(cur)}</div>
      <div class="m-sub">Latest close</div>
    </div>
    <div class="metric ${up?'green':'red'}">
      <div class="m-label">AI Prediction</div>
      <div class="m-value ${up?'m-up':'m-dn'}">₹${fmt(ens)}</div>
      <div class="m-sub ${up?'m-up':'m-dn'}">${diff!=null?(up?'▲':'▼')+' ₹'+fmt(Math.abs(diff))+' ('+Math.abs(pct).toFixed(2)+'%)':''}</div>
    </div>
    <div class="metric purple">
      <div class="m-label">Train Data</div>
      <div class="m-value">${d.train_size}</div>
      <div class="m-sub">data points</div>
    </div>
    <div class="metric cyan">
      <div class="m-label">Test Data</div>
      <div class="m-value">${d.test_size}</div>
      <div class="m-sub">data points</div>
    </div>`;
}

function renderPerfTable(rows){
  if(!rows?.length){document.getElementById('perf-tbl').innerHTML='<p style="padding:14px;color:var(--muted)">No data</p>';return}
  const cols=Object.keys(rows[0]);
  const tbody=rows.map(r=>'<tr>'+cols.map((c,i)=>
    `<td class="${i===0?'td-model':''}">${typeof r[c]==='number'?r[c].toFixed(4):r[c]}</td>`
  ).join('')+'</tr>').join('');
  document.getElementById('perf-tbl').innerHTML=
    `<table><thead><tr>${cols.map(c=>`<th>${c}</th>`).join('')}</tr></thead><tbody>${tbody}</tbody></table>`;
}

function renderPredTable(preds,cur){
  if(!preds){document.getElementById('pred-tbl').innerHTML='<p style="padding:14px;color:var(--muted)">No data</p>';return}
  const rows=Object.entries(preds).filter(([,v])=>v!=null).map(([m,v])=>{
    const d=v&&cur?v-cur:null, p=d&&cur?d/cur*100:null, up=d>=0;
    return `<tr>
      <td class="td-model">${m}</td>
      <td>₹${fmt(v)}</td>
      <td>${d!=null?`<span class="badge2 ${up?'badge-up2':'badge-dn2'}">${up?'+':''}₹${fmt(Math.abs(d))}</span>`:'—'}</td>
      <td>${p!=null?`<span class="badge2 ${up?'badge-up2':'badge-dn2'}">${up?'+':''}${Math.abs(p).toFixed(2)}%</span>`:'—'}</td>
    </tr>`;
  }).join('');
  document.getElementById('pred-tbl').innerHTML=
    `<table><thead><tr><th>Model</th><th>Predicted</th><th>Δ Price</th><th>Δ %</th></tr></thead><tbody>${rows}</tbody></table>`;
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
            ticker=          body.get("ticker", "TCS.NS"),
            prediction_date= body.get("prediction_date"),
            lookback_days=   int(body.get("lookback_days", 730)),
            test_frac=       float(body.get("test_frac", 0.2)),
            prediction_days= int(body.get("prediction_days", 1)),
        )
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

    df   = result["df"]
    perf = result["performance"]
    name = body.get("ticker", "Stock")

    perf_rows = [{"Model": idx, **{k: round(v, 4) for k, v in row.items()}}
                 for idx, row in perf.iterrows()]

    return jsonify({
        "chart_price":   chart_price(df, name),
        "chart_perf":    chart_performance(perf),
        "chart_overlay": chart_overlay(df, result["test_preds"], result["test_start_idx"], name),
        "chart_next":    chart_next(result["next_pred"], result["current_price"]),
        "performance":   perf_rows,
        "next_pred":     result["next_pred"],
        "ensemble":      result["ensemble"],
        "current_price": result["current_price"],
        "train_size":    result["train_size"],
        "test_size":     result["test_size"],
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
