from data_downloader import get_stock_data
from kpis import compute_kpis, format_kpis_for_prompt
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

import os
from usage_limits import reserve_request

load_dotenv()

def ask_gpt_to_analyze(metrics_text: str, model_name: str = "gpt-4o", temperature: float = 0.0, api_key=None) -> str:
    # Use an explicitly supplied key or the local environment.
    chat = ChatOpenAI(model=model_name, temperature=temperature,
                      api_key=api_key or os.getenv("OPENAI_API_KEY"),
                      max_tokens=500, max_retries=0, timeout=30)
    prompt = f"""
You are a professional investment analyst. Given the stock KPIs below, provide:
1) A concise summary (2-4 sentences).
2) Top 3 risks.
3) Short-term (next 1-3 months) outlook and key things to monitor.
4) Suggested next steps / actions for a cautious retail investor.

KPIs:
{metrics_text}
"""
    # invoke returns a message; the interface expects its text content.
    reserve_request()
    response = chat.invoke(prompt)
    return response.content

# -------------------------
# Main runner
# -------------------------
def analyze_ticker(ticker: str, period: str = "2y", model_name: str = "gpt-4o", temperature: float = 0.0):
    df = get_stock_data(ticker, period=period)

    # compute indicators used in KPIs (we already compute inside compute_kpis)
    kpis = compute_kpis(df)
    metrics_text = format_kpis_for_prompt(ticker, kpis)

    print("----- KPI SUMMARY -----")
    print(metrics_text)
    print("\n----- GPT ANALYSIS -----")
    analysis = ask_gpt_to_analyze(metrics_text, model_name, temperature)
    print(analysis)

if __name__ == "__main__":
    # Example usage: set ticker below or accept from env / CLI
    ticker = os.getenv("TICKER", "AAPL")
    try:
        analyze_ticker(ticker)
    except Exception as exc:
        print("Error:", exc)