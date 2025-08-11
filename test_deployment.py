"""
Simple test file to verify deployment setup
Run this locally to test before deploying
"""

import streamlit as st
import sys
import importlib

def test_imports():
    """Test if all required packages can be imported"""
    st.write("🧪 Testing package imports...")
    
    packages = [
        'streamlit',
        'plotly',
        'yfinance', 
        'pandas',
        'numpy',
        'openai',
        'langchain'
    ]
    
    for package in packages:
        try:
            importlib.import_module(package)
            st.success(f"✅ {package}")
        except ImportError as e:
            st.error(f"❌ {package}: {e}")
    
    return True

def test_local_files():
    """Test if local modules can be imported"""
    st.write("📁 Testing local module imports...")
    
    try:
        from data_downloader import get_stock_data
        st.success("✅ data_downloader")
    except Exception as e:
        st.error(f"❌ data_downloader: {e}")
    
    try:
        from kpis import compute_kpis
        st.success("✅ kpis")
    except Exception as e:
        st.error(f"❌ kpis: {e}")
    
    try:
        from stock_analyser import ask_gpt_to_analyze
        st.success("✅ stock_analyser")
    except Exception as e:
        st.error(f"❌ stock_analyser: {e}")

def main():
    st.title("🧪 Deployment Test")
    st.write("Testing if your app is ready for Streamlit Cloud deployment")
    
    test_imports()
    test_local_files()
    
    st.success("🎉 If all tests pass, your app is ready for deployment!")
    st.info("Next: Push to GitHub and deploy on Streamlit Cloud")

if __name__ == "__main__":
    main() 