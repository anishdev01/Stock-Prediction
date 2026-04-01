# 🚀 DEPLOYMENT GUIDE - Alpha Five Stock Predictor

## ✅ What We Upgraded

### 🤖 **Models Changed:**
- ❌ Removed: Decision Tree, Random Forest  
- ✅ Kept: Linear Regression
- ✅ Added: **Ridge Regression** (L2 regularization for better generalization)
- ✅ Added: **LSTM Neural Network** (Deep learning for time series)

### 🎨 **UI Improvements:**
- Modern futuristic AI-themed design
- Gradient backgrounds with animated grid
- Glowing effects and smooth animations
- Better color scheme (cyan/purple/orange theme)
- Improved typography with Orbitron display font
- Enhanced responsive layout
- Better metric cards with hover effects

### 📊 **Features:**
- 3 Advanced ML models
- Interactive Plotly charts
- Real-time NSE data from yfinance
- Technical indicators (SMA, EMA, RSI, Bollinger Bands, Volume)
- Model performance comparison
- Ensemble predictions

---

## 🌐 Deploy to Vercel

### **Option 1: Deploy via Vercel CLI (Recommended)**

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Navigate to project directory**
   ```bash
   cd C:\Users\91700\OneDrive\Documents\alpha-five5
   ```

4. **Deploy**
   ```bash
   vercel --prod
   ```

5. **Follow the prompts:**
   - Set up and deploy? **Y**
   - Which scope? Choose your account
   - Link to existing project? **N** (first time) or **Y** (if updating)
   - Project name: `alpha-five-stock-predictor` (or your choice)
   - Directory: `./` (just press Enter)
   - Override settings? **N**

---

### **Option 2: Deploy via GitHub + Vercel Dashboard**

1. **Create a Git Repository**
   ```bash
   cd C:\Users\91700\OneDrive\Documents\alpha-five5
   git init
   git add .
   git commit -m "Initial commit - Stock Predictor with Linear, Ridge & LSTM"
   ```

2. **Push to GitHub**
   ```bash
   # Create a new repository on GitHub first, then:
   git remote add origin https://github.com/YOUR_USERNAME/alpha-five-predictor.git
   git branch -M main
   git push -u origin main
   ```

3. **Connect to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click **"Add New Project"**
   - Import your GitHub repository
   - Vercel will auto-detect settings from `vercel.json`
   - Click **"Deploy"**

---

### **Option 3: Deploy from Local Directory**

1. **Open Terminal in Project Folder**
   ```bash
   cd C:\Users\91700\OneDrive\Documents\alpha-five5
   ```

2. **Run Vercel**
   ```bash
   vercel
   ```

3. **For Production**
   ```bash
   vercel --prod
   ```

---

## ⚙️ Important Notes

### **TensorFlow Warning**
- The `requirements.txt` includes `tensorflow==2.15.0` for LSTM
- **Vercel has a 50MB limit** per serverless function
- TensorFlow is ~450MB, so **LSTM will be skipped on Vercel** if it exceeds limits
- The app will still work with Linear & Ridge Regression
- For full LSTM support, consider deploying to:
  - **Railway.app** (recommended for TensorFlow)
  - **Render.com**
  - **Google Cloud Run**
  - **AWS Lambda** with container support

### **Alternative: Deploy without LSTM (Lighter)**
If you want faster cold starts on Vercel, create a lightweight version:

```bash
# Edit requirements.txt - remove tensorflow line
# The trainer.py will automatically skip LSTM if TensorFlow is not available
```

---

## 🧪 Test Locally First

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python api/index.py

# Open browser
# Go to http://localhost:5000
```

---

## 📦 Project Structure

```
alpha-five5/
├── api/
│   └── index.py          # Flask app + HTML UI
├── src/
│   ├── data_fetcher.py   # yfinance data downloader
│   ├── features.py       # Technical indicators
│   ├── trainer.py        # 3 ML models (Linear, Ridge, LSTM)
│   ├── predictor.py      # Full pipeline
│   └── charts.py         # Plotly visualizations
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel configuration
├── .vercelignore        # Files to ignore
└── README.md            # This file
```

---

## 🎯 After Deployment

Once deployed, Vercel will give you a URL like:
```
https://alpha-five-stock-predictor.vercel.app
```

**Test the app:**
1. Select a Nifty 50 stock (e.g., TCS, Reliance)
2. Choose prediction date
3. Adjust history days and test split
4. Click "RUN ANALYSIS"
5. View results in 3 tabs (Technical, Models, Predictions)

---

## 🐛 Troubleshooting

### **Build Fails**
- Check that all files are committed
- Verify `requirements.txt` is correct
- Remove `tensorflow` if size is an issue

### **Cold Start Timeout**
- First request might take 15-20 seconds
- Subsequent requests will be faster
- Consider upgrading Vercel plan for better performance

### **LSTM Not Working**
- This is expected on Vercel due to size limits
- App will work with Linear & Ridge only
- For LSTM, deploy to Railway/Render

---

## 📧 Support

For issues or questions:
- Check Vercel logs: `vercel logs`
- Review build output
- Verify all imports are in requirements.txt

---

## ✨ Features Summary

✅ **3 ML Models**: Linear Regression, Ridge Regression, LSTM  
✅ **Modern UI**: Futuristic design with animations  
✅ **Live Data**: Real-time NSE stock data  
✅ **Technical Analysis**: 10+ indicators  
✅ **Interactive Charts**: Plotly visualizations  
✅ **Ensemble Prediction**: Average of all models  
✅ **Responsive**: Works on mobile & desktop  

---

**Made with ❤️ by Alpha Five Team**  
**Brainware University Project**
