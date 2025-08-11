# 📈 Stock Analyser Pro

A professional-grade stock analysis application that combines traditional technical indicators with AI-powered insights using OpenAI's GPT models.

## ✨ Features

- **📊 Interactive Stock Charts**: Candlestick charts with moving averages
- **📈 Technical Indicators**: RSI, SMA, volatility, and return metrics
- **🤖 AI Analysis**: Professional investment insights powered by GPT
- **🎨 Modern UI**: Beautiful, responsive interface built with Streamlit
- **⚙️ Configurable**: Adjustable AI models and creativity settings
- **📱 Mobile Friendly**: Responsive design for all devices

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Application
```bash
streamlit run streamlit_stock_analyser.py
```

## 🎯 How to Use

1. **Enter Stock Ticker**: Type a valid stock symbol (e.g., AAPL, MSFT, GOOGL)
2. **Select Time Period**: Choose from 1 year, 2 years, or 5 years of data
3. **Configure AI Settings**: Adjust model and creativity in the sidebar
4. **Analyze**: Click "Analyze Stock" to get comprehensive insights
5. **Review Results**: View metrics, charts, and AI-generated analysis

## 🔧 Configuration Options

### AI Model Selection
- **GPT-4o**: Most advanced analysis (default)
- **GPT-3.5-turbo**: Faster, cost-effective analysis

### Creativity Control
- **Low (0.0)**: Consistent, conservative analysis
- **High (1.0)**: More creative, varied insights

### Display Options
- **Price Chart**: Interactive candlestick chart with moving averages
- **Detailed Metrics**: Comprehensive KPI breakdown

## 📊 Technical Indicators

- **Price Metrics**: Latest close, daily returns, 30-day performance
- **Moving Averages**: 50-day and 200-day SMAs
- **Momentum**: 14-period RSI
- **Risk**: Annualized volatility

## 🏗️ Architecture

- **Data Layer**: Yahoo Finance integration via `yfinance`
- **Analysis Engine**: Technical indicators and KPI calculations
- **AI Integration**: OpenAI GPT via LangChain
- **Frontend**: Streamlit web application
- **Visualization**: Plotly interactive charts

## 📁 Project Structure

```
StockAnalyser/
├── streamlit_stock_analyser.py  # Main web application
├── stock_analyser.py            # AI analysis engine
├── kpis.py                      # Technical indicators
├── data_downloader.py           # Data fetching
├── requirements.txt             # Dependencies
└── README.md                   # This file
```

## 🎨 UI Improvements Made

- ✨ Professional styling with custom CSS
- 📱 Responsive layout with sidebar configuration
- 🎯 Interactive metric cards with color coding
- 📊 Beautiful stock price charts
- 🔄 Progress indicators and loading states
- ⚠️ Enhanced error handling and validation
- 💾 Export functionality (placeholder)
- 🎨 Modern color scheme and typography

## 🔮 Future Enhancements

- [ ] Stock comparison functionality
- [ ] Portfolio analysis tools
- [ ] Advanced charting indicators
- [ ] Export to PDF/Excel
- [ ] Historical analysis tracking
- [ ] Real-time alerts and notifications

## 🛠️ Requirements

- Python 3.7+
- OpenAI API key
- Internet connection for stock data

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests. 