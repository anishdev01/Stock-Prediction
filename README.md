# 🇮🇳 Indian Stock Predictor

<div align="center">

```
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║        🇮🇳  I N D I A N   S T O C K   P R E D I C T O R           ║
║                                                                      ║
║            Powered by 3 Machine Learning Models                      ║
║              Live Nifty 50 · NSE Data · Plotly Charts               ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Vercel](https://img.shields.io/badge/Deploy-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com)
[![NSE](https://img.shields.io/badge/Data-Yahoo_Finance_NSE-0078D4?style=for-the-badge)](https://finance.yahoo.com)

**by Alpha Five Team** · *Brainware University Project*

</div>

---

## 📖 What Is This?

This is a **web application** that predicts the future closing price of any **Nifty 50** stock using three carefully tuned Machine Learning models trained on historical NSE (National Stock Exchange of India) data.

You pick a stock and a date → the app downloads real price history, engineers 18+ technical indicators, trains 3 ML models, and shows you the predicted closing price for your chosen date — with confidence intervals.

> ⚠️ **Disclaimer:** This is an academic project. Predictions are for educational purposes only and should not be used for actual trading decisions.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER (Browser)                              │
│                    selects stock + date → clicks Run                │
└───────────────────────────┬─────────────────────────────────────────┘
                            │  HTTP POST /api/analyze
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     FLASK WEB SERVER                                │
│                     api/index.py                                    │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  Route: POST /api/analyze → calls run() → returns JSON      │    │
│  └─────────────────────────────────────────────────────────────┘    │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    PIPELINE (src/predictor.py)                      │
│                                                                     │
│   Step 1         Step 2         Step 3         Step 4              │
│  ┌────────┐    ┌─────────┐    ┌────────┐    ┌─────────┐           │
│  │  FETCH │───▶│ENGINEER │───▶│ SPLIT  │───▶│  SCALE  │           │
│  │  DATA  │    │FEATURES │    │Train/  │    │Impute + │           │
│  └────────┘    └─────────┘    │ Test   │    │Standard │           │
│                               └────────┘    │  ize    │           │
│                                             └────┬────┘           │
│   Step 5                           Step 6        │                 │
│  ┌───────────────────────────┐   ┌───────────┐  │                 │
│  │        TRAIN MODELS       │◀──┤  SCALED   │◀─┘                 │
│  │  ┌─────────────────────┐  │   │   DATA    │                    │
│  │  │  Ridge Regression   │  │   └───────────┘                    │
│  │  │  Gradient Boosting  │  │                                     │
│  │  │  Random Forest      │  │                                     │
│  │  └─────────────────────┘  │                                     │
│  └──────────────┬────────────┘                                     │
│                 │   Step 7                                          │
│                 ▼                                                   │
│  ┌──────────────────────────────────────────────────────────┐      │
│  │              PREDICT for Target Date                      │      │
│  │  days_ahead = trading days until prediction date         │      │
│  │  if days=1  → direct 1-step prediction                   │      │
│  │  if days>1  → recursive multi-step forecasting           │      │
│  │  ensemble   = mean of all model predictions              │      │
│  │  confidence = ±1σ residuals × horizon_factor             │      │
│  └──────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         CHARTS (Plotly)                             │
│  ┌────────────┐  ┌────────────┐  ┌───────────┐  ┌──────────────┐  │
│  │  Technical │  │  Model     │  │ Prediction│  │  Feature     │  │
│  │  Chart     │  │  Perf Bar  │  │ Bar Chart │  │  Importance  │  │
│  │ Candlestick│  │ RMSE/MAE   │  │ ±1σ bands │  │  Top 10     │  │
│  │ SMA/EMA/BB │  │ R²/CV-RMSE │  │ per model │  │  per model  │  │
│  └────────────┘  └────────────┘  └───────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                            │  JSON response
                            ▼
                    Browser renders charts
```

---

## 🤖 The Three ML Models

### 1️⃣ Ridge Regression
```
Linear model with L2 regularisation (α = 50)

  ŷ = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ
  
  Loss = MSE + α × Σ(βᵢ²)
  
  → Penalises large coefficients
  → Prevents overfitting to noisy market data
  → Fast, interpretable, strong baseline
```

### 2️⃣ Gradient Boosting Regressor
```
Ensemble of 300 weak learners trained sequentially

  F₀(x) = mean(y)
  Fₘ(x) = Fₘ₋₁(x) + η × hₘ(x)    ← small steps
  
  Settings:
  • learning_rate = 0.03  (tiny steps → stable)
  • max_depth     = 3     (shallow trees → less overfit)
  • subsample     = 0.8   (80% of data per round → diversity)
  • n_iter_no_change = 25 (early stopping)
  
  → Usually most accurate on tabular data
  → Built-in regularisation via subsampling
```

### 3️⃣ Random Forest Regressor
```
Ensemble of 300 decision trees trained on random subsets

  Output = average(Tree₁(x), Tree₂(x), ..., Tree₃₀₀(x))
  
  Settings:
  • max_depth       = 8    (controlled depth)
  • min_samples_leaf = 10  (smooth leaf nodes)
  • max_features    = sqrt (each split sees √n features)
  • oob_score       = True (free out-of-bag validation)
  
  → Naturally resistant to overfitting (bagging diversity)
  → Gives feature importances
  → OOB score = extra free validation metric
```

---

## 📐 Feature Engineering (18 Technical Indicators)

| # | Feature | Category | What It Tells Us |
|---|---------|----------|------------------|
| 1 | `sma_20` | Trend | 20-day simple moving average — short-term direction |
| 2 | `sma_50` | Trend | 50-day simple moving average — medium-term direction |
| 3 | `ema_20` | Trend | Exponential MA — reacts faster to recent price |
| 4 | `price_vs_sma20` | Trend | How far price is from SMA 20 — mean reversion |
| 5 | `macd` | Momentum | 12-EMA minus 26-EMA — trend change signal |
| 6 | `macd_signal` | Momentum | 9-day EMA of MACD — crossover line |
| 7 | `macd_hist` | Momentum | MACD minus Signal — divergence indicator |
| 8 | `rsi` | Momentum | Overbought (>70) / Oversold (<30) signal |
| 9 | `stoch_k` | Momentum | Stochastic %K — reversal signal |
| 10 | `stoch_d` | Momentum | Stochastic %D — signal line |
| 11 | `bb_pct` | Volatility | Price position in Bollinger Band (0–1) |
| 12 | `bb_width` | Volatility | Band width — detects volatility squeezes |
| 13 | `atr_pct` | Volatility | Average True Range normalised — swing size |
| 14 | `volatility_20` | Volatility | 20-day rolling std of returns — risk |
| 15 | `volume_ratio` | Volume | Today's volume vs 10-day average |
| 16 | `obv_norm` | Volume | On-Balance Volume — confirms price moves |
| 17 | `roc_5` | Returns | 5-day rate of change — 1-week momentum |
| 18 | `roc_20` | Returns | 20-day rate of change — 1-month momentum |

**Price lags** (also used as features):
`lag_1` (yesterday) · `lag_5` (last week) · `lag_10` (2 weeks ago)

---

## 🛡️ Anti-Overfitting Strategy

Stock market data is notoriously noisy. Here's how each layer of the system prevents overfitting:

```
Layer               Technique                   Why It Helps
─────────────────── ─────────────────────────── ─────────────────────────────
Data split          Chronological (no shuffle)  Prevents look-ahead bias
                    Never random split!

Feature design      Normalised indicators        Removes absolute scale leakage
                    No raw OHLCV as features     Avoids trivial memorisation

Ridge Regression    L2 penalty (α=50)            Shrinks noisy coefficients

Gradient Boosting   Low learning rate (0.03)     Slow, stable convergence
                    Subsample = 0.8              Trains on random 80% each round
                    Early stopping (25 rounds)   Stops when validation stops improving

Random Forest       max_features = sqrt          Each split sees random subset
                    min_samples_leaf = 10        Prevents tiny, noisy leaves
                    OOB validation               Free out-of-bag error estimate

Validation          TimeSeriesSplit (5 folds)    Walk-forward cross-validation
                    CV-RMSE reported             Honest future-unseen performance
```

---

## 🔮 Prediction Logic: How Dates Work

```
Timeline Example:
─────────────────────────────────────────────────────────────────────
  Last Data  → April 1, 2026 (Wednesday)
  Pred Date  → April 8, 2026 (Wednesday)
  Days Ahead → 5 trading days (Mon, Tue, Wed, Thu, Fri skip weekends)

Step 1: Predict April 2 using last known features
Step 2: Use April 2 prediction → update lag_1 → predict April 3
Step 3: Use April 3 prediction → update lag_1 → predict April 4
Step 4: Use April 4 prediction → update lag_1 → predict April 5
Step 5: Use April 5 prediction → update lag_1 → predict April 8 ✓

Confidence band widens with each step:
  σ₁ = residual_std × 1.0
  σ₂ = residual_std × 1.15
  σₙ = residual_std × (1 + 0.15 × (n-1))
```

---

## 📁 Project File Structure

```
alpha-five-stock-predictor/
│
├── api/
│   └── index.py          ← Flask server + full HTML/CSS/JS page
│
├── src/
│   ├── __init__.py
│   ├── data_fetcher.py   ← Downloads NSE data via Yahoo Finance
│   ├── features.py       ← Computes 18+ technical indicators
│   ├── trainer.py        ← Trains 3 ML models with CV validation
│   ├── predictor.py      ← Orchestrates the full pipeline
│   └── charts.py         ← Generates 5 Plotly charts as JSON
│
├── requirements.txt      ← Python dependencies
├── vercel.json           ← Vercel deployment config
├── .vercelignore         ← Files to skip in deployment
└── README.md             ← This file
```

---

## 🚀 How to Run Locally (Step by Step)

### Step 1 — Make sure Python is installed
Open your terminal (Command Prompt / PowerShell on Windows, Terminal on Mac/Linux):
```bash
python --version
# Should show Python 3.10 or higher
```
Download Python from https://python.org if needed.

### Step 2 — Download the project
```bash
# If you have git:
git clone <your-repo-url>
cd alpha-five-stock-predictor

# Or just unzip the downloaded ZIP and open the folder in terminal
```

### Step 3 — Create a virtual environment (recommended)
```bash
# Windows:
python -m venv venv
venv\Scripts\activate

# Mac / Linux:
python -m venv venv
source venv/bin/activate
```
You should see `(venv)` appear in your terminal prompt.

### Step 4 — Install dependencies
```bash
pip install -r requirements.txt
```
This installs Flask, scikit-learn, pandas, plotly, yfinance, and numpy.
It takes about 1–2 minutes.

### Step 5 — Start the server
```bash
python api/index.py
```
You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 6 — Open the app
Open your browser and go to: **http://localhost:5000**

That's it! 🎉

---

## 🌐 How to Deploy on Vercel (Free Hosting)

### Step 1 — Create a free account
Go to https://vercel.com and sign up (use your GitHub account).

### Step 2 — Install Vercel CLI
```bash
npm install -g vercel
```

### Step 3 — Deploy
```bash
cd alpha-five-stock-predictor
vercel
```
Follow the prompts. Vercel will give you a live URL like `https://your-project.vercel.app`

---

## 📊 How to Use the App

```
1. Open the app in your browser
   └── You'll see the sidebar on the left and a welcome screen

2. Search for a stock
   └── Type "Reliance", "HDFC", "TCS", etc. in the search box
   └── Click the stock name to select it

3. Pick a prediction date
   └── Click the calendar icon
   └── Choose any future trading day (Monday–Friday)
   └── The further in the future, the wider the confidence band

4. Adjust settings (optional)
   └── History Days: more history = more training data (default 730 = 2 years)
   └── Test Split: fraction of data held for evaluation (default 20%)

5. Click "Run Analysis"
   └── Wait ~15 seconds while models train
   └── Results appear with 4 interactive chart tabs

6. Read the results
   └── Ensemble Prediction = average of all 3 models
   └── ±1σ Confidence = expected error range
   └── R² closer to 1.0 = better model fit
   └── CV-RMSE = honest walk-forward validation error
```

---

## 📈 Reading the Charts

| Tab | Chart | What to Look For |
|-----|-------|-----------------|
| Technical Chart | Candlestick + SMA/EMA + Bollinger Bands + Volume + RSI | Overall price trend, support/resistance levels |
| Model Results | RMSE / MAE / R² / CV-RMSE bars | Which model performs best; R² > 0.8 is good |
| Model Results | Predictions vs Actual (test window) | How closely dashed lines follow the white actual price |
| Predictions | Target-date prediction with ±1σ error bars | The actual price forecast for your chosen date |
| Features | Feature importance bars | Which indicators drive each model's predictions |

---

## 🧠 Understanding the Metrics

```
RMSE (Root Mean Squared Error)
  → Average prediction error in rupees (₹)
  → Lower = better  e.g. RMSE=45 means predictions are ~₹45 off on average

MAE (Mean Absolute Error)
  → Similar to RMSE but not sensitive to large errors
  → Lower = better

R² (R-Squared / Coefficient of Determination)
  → How much variance in prices the model explains
  → 1.0 = perfect, 0.0 = useless, negative = worse than just guessing the mean
  → Higher = better  (aim for > 0.85)

CV-RMSE (Cross-Validated RMSE using TimeSeriesSplit)
  → Most honest metric — tests on unseen FUTURE data 5 times
  → Walk-forward validation: always train on past, test on future
  → The best way to know if the model will work in the real world
  → Lower = better
```

---

## 👥 Team Alpha Five

| Role | Name |
|------|------|
| Team Lead & ML Engineer | [Team Member 1] |
| Frontend Developer | [Team Member 2] |
| Data Engineer | [Team Member 3] |
| Backend Developer | [Team Member 4] |
| Analyst & Documentation | [Team Member 5] |

**Institution:** Brainware University
**Department:** Computer Science & Engineering
**Project Type:** Major Academic Project

---

## 📚 Technologies Used

| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.10+ | Core programming language |
| Flask | 3.0.3 | Web server and REST API |
| scikit-learn | 1.5.1 | Ridge, Gradient Boosting, Random Forest |
| pandas | 2.2.2 | Data manipulation and analysis |
| numpy | 1.26.4 | Numerical computation |
| yfinance | 0.2.65 | Yahoo Finance stock data downloader |
| Plotly | 5.22.0 | Interactive charts |
| Vercel | — | Cloud deployment platform |
| Google Fonts | — | Playfair Display, DM Sans, JetBrains Mono |

---

## 🔬 How the ML Pipeline Works (For Non-Coders)

Think of it like this:

```
STEP 1: Collect history  📥
  Like looking at a stock's past 2 years of price data.
  "On Jan 5, the price was ₹2,340. On Jan 6, it was ₹2,380..."

STEP 2: Create clues  🔍
  Calculate 18 technical signals from the price history.
  Like a detective finding patterns:
  "When RSI is high and price is above SMA, it tends to go up."

STEP 3: Split into training and test  ✂️
  80% of data: the model studies this (like studying for an exam).
  20% of data: we quiz the model on this (the exam it hasn't seen).

STEP 4: Scale the numbers  ⚖️
  Make all features the same size so no one feature dominates.
  Like converting rupees, percentages, and volumes to the same scale.

STEP 5: Train the models  🏋️
  Each model finds patterns between the 18 clues and tomorrow's price.
  All three learn slightly different things — that's the power of ensemble.

STEP 6: Evaluate honestly  📊
  Test on the 20% held-out data to see real accuracy.
  Also run 5-fold walk-forward validation for extra honesty.

STEP 7: Make the prediction  🔮
  Give the trained models today's technical indicators.
  Each model says: "Based on the patterns I learned, tomorrow's price is X."
  Ensemble = average of all three predictions.
```

---

## ⚠️ Important Limitations

- **Stock markets are inherently unpredictable.** No ML model can predict with certainty.
- **Accuracy drops with distance.** 1-day predictions are more reliable than 10-day ones.
- **External events are not modelled.** News, policy changes, and global events can override technical signals.
- **Indian market holidays are not accounted for.** The app counts all weekday business days.
- **Data quality depends on Yahoo Finance.** Occasionally data may be delayed or missing.

---

## 📄 License

This project was created for academic purposes at Brainware University.
For educational and research use only.

---

<div align="center">

Made with ❤️ by **Alpha Five Team** · Brainware University

*"Combining the power of machine learning with India's stock market."*

</div>
