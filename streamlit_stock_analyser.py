import streamlit as st
from data_downloader import get_stock_data
from kpis import compute_kpis, format_kpis_for_prompt
from stock_analyser import ask_gpt_to_analyze

def main():
    # App configuration
    st.set_page_config(page_title="Stock Analyser", layout="wide")

    # Custom CSS for styling
    st.markdown(
        """
        <style>
        .main-title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #2E86C1;
        }
        .description {
            font-size: 1.2rem;
            color: #555555;
        }
        .card {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .positive {
            color: #28a745;
            font-weight: bold;
        }
        .negative {
            color: #dc3545;
            font-weight: bold;
        }
        .neutral {
            color: #6c757d;
            font-weight: bold;
        }
        ul {
            padding-left: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # App title and description
    st.markdown('<div class="main-title">📈 Stock Analyser</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="description">Analyze stock performance and get actionable insights powered by GPT. Enter a stock ticker and select a time period to get started.</div>',
        unsafe_allow_html=True,
    )

    # Sidebar for inputs
    st.sidebar.header("Input Parameters")
    ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL):", value="AAPL")
    period = st.sidebar.selectbox("Select Data Period:", ["1y", "2y", "5y"], index=1)
    analyze_button = st.sidebar.button("Analyze")

    # Main content
    if analyze_button:
        try:
            # Fetch stock data
            with st.spinner("Fetching stock data..."):
                df = get_stock_data(ticker, period=period)

            # Compute KPIs
            with st.spinner("Computing KPIs..."):
                kpis = compute_kpis(df)
                metrics_text = format_kpis_for_prompt(ticker, kpis)

            # Layout: Two columns
            col1, col2 = st.columns(2)

            # KPI Summary in a card
            with col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("📊 KPI Summary")
                for line in metrics_text.split("\n"):
                    if "positive" in line.lower():
                        st.markdown(f'<span class="positive">{line}</span>', unsafe_allow_html=True)
                    elif "negative" in line.lower():
                        st.markdown(f'<span class="negative">{line}</span>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<span class="neutral">{line}</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # GPT Analysis in a card
            with col2:
                with st.spinner("Generating GPT Analysis..."):
                    analysis = ask_gpt_to_analyze(metrics_text)

                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("🤖 GPT Analysis")
                st.markdown(
                    f"""
                    <ul>
                        {"".join([f"<li>{line}</li>" for line in analysis.split("\n")])}
                    </ul>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"⚠️ An error occurred: {e}")

if __name__ == "__main__":
    main()