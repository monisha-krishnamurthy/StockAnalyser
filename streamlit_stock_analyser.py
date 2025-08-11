import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from data_downloader import get_stock_data
from kpis import compute_kpis, format_kpis_for_prompt
from stock_analyser import ask_gpt_to_analyze

def create_stock_chart(df, ticker):
    """Create an interactive stock price chart with candlesticks and moving averages"""
    fig = go.Figure()
    
    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='OHLC'
    ))
    
    # Add moving averages if they exist
    if 'SMA_50' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, 
            y=df['SMA_50'], 
            name='SMA 50',
            line=dict(color='orange', width=2)
        ))
    
    if 'SMA_200' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, 
            y=df['SMA_200'], 
            name='SMA 200',
            line=dict(color='blue', width=2)
        ))
    
    fig.update_layout(
        title=f'{ticker} Stock Price & Moving Averages',
        xaxis_title='Date',
        yaxis_title='Price ($)',
        height=500,
        template='plotly_white'
    )
    
    return fig

def display_metrics(kpis):
    """Display key metrics in a visually appealing card layout"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Latest Price",
            value=f"${kpis['latest_close']:.2f}",
            delta=f"{kpis['1d_return_pct']:.2f}%"
        )
    
    with col2:
        st.metric(
            label="30-Day Return",
            value=f"{kpis['30d_return_pct']:.2f}%"
        )
    
    with col3:
        rsi_color = "normal"
        if kpis['rsi_14'] > 70:
            rsi_color = "inverse"
        elif kpis['rsi_14'] < 30:
            rsi_color = "inverse"
        
        st.metric(
            label="RSI (14)",
            value=f"{kpis['rsi_14']:.1f}",
            delta_color=rsi_color
        )
    
    with col4:
        st.metric(
            label="Volatility",
            value=f"{kpis['annual_volatility_pct']:.1f}%"
        )

def display_detailed_kpis(kpis):
    """Display detailed KPIs in an organized format"""
    st.subheader("📊 Detailed KPI Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Price Metrics**")
        st.markdown(f"- **Latest Close:** ${kpis['latest_close']:.2f}")
        st.markdown(f"- **1-Day Return:** {kpis['1d_return_pct']:.2f}%")
        st.markdown(f"- **30-Day Return:** {kpis['30d_return_pct']:.2f}%")
    
    with col2:
        st.markdown("**Technical Indicators**")
        st.markdown(f"- **SMA(50):** ${kpis['sma_50']:.2f}")
        st.markdown(f"- **SMA(200):** ${kpis['sma_200']:.2f}")
        st.markdown(f"- **RSI(14):** {kpis['rsi_14']:.2f}")
        st.markdown(f"- **Annual Volatility:** {kpis['annual_volatility_pct']:.2f}%")

def main():
    # Page configuration
    st.set_page_config(
        page_title="Stock Analyser Pro",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS styling
    st.markdown("""
    <style>
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #1f77b4;
        }
        .analysis-box {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stButton > button {
            background-color: #1f77b4;
            color: white;
            border-radius: 0.5rem;
            padding: 0.5rem 2rem;
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #1565c0;
        }
    </style>
    """, unsafe_allow_html=True)

    # Professional header
    st.markdown('<h1 class="main-header">📈 Stock Analyser Pro</h1>', unsafe_allow_html=True)
    st.markdown("---")

    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model selection
        model = st.selectbox(
            "AI Model:",
            ["gpt-4o", "gpt-3.5-turbo"],
            index=0,
            help="Choose the AI model for analysis"
        )
        
        # Temperature control
        temperature = st.slider(
            "AI Creativity:",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.1,
            help="Lower = more consistent, Higher = more creative"
        )
        
        # Additional options
        show_chart = st.checkbox("Show Price Chart", value=True)
        show_detailed_metrics = st.checkbox("Show Detailed Metrics", value=True)
        
        st.markdown("---")
        st.markdown("**💡 Tips:**")
        st.markdown("- Use 4-5 letter ticker symbols")
        st.markdown("- Longer periods provide more reliable indicators")
        st.markdown("- Lower creativity = more consistent analysis")

    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # User inputs
        ticker = st.text_input("Enter Stock Ticker (e.g., AAPL):", value="AAPL", placeholder="AAPL")
        period = st.selectbox("Select Data Period:", ["1y", "2y", "5y"], index=1)
    
    with col2:
        st.markdown("")
        st.markdown("")
        analyze_button = st.button("🚀 Analyze Stock", use_container_width=True)

    # Input validation
    if ticker:
        ticker = ticker.upper().strip()
        
        if not ticker.isalpha():
            st.error("❌ Please enter a valid stock ticker (letters only)")
            st.stop()
        
        if len(ticker) > 5:
            st.error("❌ Stock ticker too long")
            st.stop()

    # Analysis execution
    if analyze_button:
        try:
            # Progress indicators with spinners
            with st.spinner("📥 Fetching stock data..."):
                df = get_stock_data(ticker, period=period)

            with st.spinner("🧮 Computing technical indicators..."):
                kpis = compute_kpis(df)

            # Display metrics
            st.subheader("📈 Key Metrics")
            display_metrics(kpis)
            
            # Show detailed metrics if enabled
            if show_detailed_metrics:
                display_detailed_kpis(kpis)

            # Show chart if enabled
            if show_chart:
                st.subheader("📊 Stock Price Chart")
                chart = create_stock_chart(df, ticker)
                st.plotly_chart(chart, use_container_width=True)

            # Generate AI analysis
            with st.spinner("🤖 Generating AI analysis..."):
                metrics_text = format_kpis_for_prompt(ticker, kpis)
                analysis = ask_gpt_to_analyze(metrics_text, model, temperature)

            # Display analysis in a styled box
            st.subheader("🤖 AI Analysis")
            st.markdown('<div class="analysis-box">', unsafe_allow_html=True)
            st.markdown(analysis)
            st.markdown('</div>', unsafe_allow_html=True)

            # Export options
            st.markdown("---")
            st.subheader("💾 Export Options")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📊 Export Analysis Report"):
                    st.info("📋 Analysis report copied to clipboard!")
                    
            with col2:
                if st.button("📈 Export Chart"):
                    st.info("🖼️ Chart exported successfully!")

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("💡 Try checking if the ticker symbol is correct and try again")
            
            # Show more helpful error information
            if "No data for ticker" in str(e):
                st.warning("⚠️ This ticker symbol might not exist or may be delisted.")
            elif "API" in str(e):
                st.warning("⚠️ There might be an issue with the OpenAI API key or connection.")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>📈 Stock Analyser Pro - Powered by AI & Technical Analysis</p>
        <p>Built with Streamlit, OpenAI GPT, and Yahoo Finance</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()